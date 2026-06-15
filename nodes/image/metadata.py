"""Image metadata nodes (issue #26).

Three nodes that round-trip arbitrary metadata through media files:

- ``SaveImageWithMetadata`` — write an IMAGE to the output folder with
  user-supplied key/value pairs embedded as PNG text chunks (alongside the
  usual ``prompt`` / workflow chunks, unless ComfyUI was started with
  ``--disable-metadata``).
- ``LoadImageWithMetadata`` — load an image and emit IMAGE + MASK plus the
  metadata it carries as a STRING.
- ``ExtractImageMetadata`` — read *every* piece of metadata from a media file
  (PNG text chunks, EXIF, format/size/mode) as a STRING, without decoding the
  pixels into a tensor.

PIL / numpy / torch / folder_paths are ComfyUI-runtime modules, so they are
imported lazily inside the methods — the module stays importable (and the pure
parse/format helpers stay unit-testable) without them installed.
"""

from __future__ import annotations

import json
from typing import Any, ClassVar


def _to_str(value: object) -> str:
    """Coerce an arbitrary metadata value to a display string.

    PNG text chunks are already ``str``; EXIF / ``img.info`` values can be
    ``bytes`` (decode lenient UTF-8), tuples (``dpi``), ints, etc.
    """
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def parse_metadata_text(text: str) -> dict[str, str]:
    """Parse the user's ``metadata`` field into ordered key/value pairs.

    Accepts either a JSON object, or newline-separated ``key=value`` /
    ``key: value`` lines. ``=`` takes precedence over ``:`` so values may
    contain colons (timestamps, URLs). Blank lines and ``#`` comments are
    ignored; lines with no separator are skipped.
    """
    text = (text or "").strip()
    if not text:
        return {}

    if text[0] == "{":
        try:
            obj = json.loads(text)
        except (ValueError, TypeError):
            obj = None
        if isinstance(obj, dict):
            return {str(k): _to_str(v) for k, v in obj.items()}

    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
        elif ":" in line:
            key, _, value = line.partition(":")
        else:
            continue
        key = key.strip()
        if key:
            out[key] = value.strip()
    return out


def stringify_info(info: dict[Any, Any]) -> dict[str, str]:
    """Turn a raw ``img.info`` / EXIF mapping into a ``str -> str`` dict."""
    return {str(k): _to_str(v) for k, v in info.items()}


def format_metadata(metadata: dict[str, str]) -> str:
    """Render ordered key/value pairs as ``key: value`` lines (one per line)."""
    return "\n".join(f"{k}: {v}" for k, v in metadata.items())


def _collect_image_metadata(img: Any) -> dict[str, str]:
    """Gather PNG text chunks, ``img.info`` and decoded EXIF from a PIL image.

    PNG text lives in ``img.text``; ``img.info`` also holds it (plus things like
    ``dpi``). EXIF tag ids are mapped to human names via ``PIL.ExifTags``.
    """
    from PIL import ExifTags

    collected: dict[str, str] = {}
    # img.text (PNG) is the richest source; fall back to img.info for the rest.
    text = getattr(img, "text", None)
    if isinstance(text, dict):
        collected.update(stringify_info(text))
    info = {k: v for k, v in (getattr(img, "info", {}) or {}).items() if k not in collected and k != "exif"}
    collected.update(stringify_info(info))

    try:
        exif = img.getexif()
    except Exception:
        exif = None
    if exif:
        for tag_id, value in exif.items():
            name = ExifTags.TAGS.get(tag_id, f"Exif_{tag_id}")
            collected.setdefault(str(name), _to_str(value))
    return collected


class SaveImageWithMetadata:
    """Save an IMAGE to the output folder with custom metadata embedded.

    Mirrors the built-in ``SaveImage`` (same filename counter / output preview)
    but adds every ``key=value`` from the ``metadata`` field as a PNG text
    chunk, so the data round-trips through the file and can later be read back
    with ``LoadImageWithMetadata`` / ``ExtractImageMetadata``.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ()
    FUNCTION: ClassVar[str] = "save"
    OUTPUT_NODE: ClassVar[bool] = True
    CATEGORY: ClassVar[str] = "UtilityNodes/Image"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI_meta"}),
                "metadata": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                        "tooltip": "JSON object, or key=value / key: value lines. Each becomes a PNG text chunk.",
                    },
                ),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    def save(
        self,
        images: Any,
        filename_prefix: str,
        metadata: str,
        prompt: Any = None,
        extra_pnginfo: Any = None,
    ) -> dict[str, Any]:
        import os

        import folder_paths
        import numpy as np
        from PIL import Image
        from PIL.PngImagePlugin import PngInfo

        disable_metadata = False
        try:
            from comfy.cli_args import args as _cli_args

            disable_metadata = bool(_cli_args.disable_metadata)
        except Exception:
            pass

        pairs = parse_metadata_text(metadata)
        output_dir = folder_paths.get_output_directory()
        height, width = int(images[0].shape[0]), int(images[0].shape[1])
        full_output_folder, filename, counter, subfolder, _ = folder_paths.get_save_image_path(
            filename_prefix, output_dir, width, height
        )

        results: list[dict[str, str]] = []
        for image in images:
            array = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(array, 0, 255).astype(np.uint8))

            png_info = PngInfo()
            if not disable_metadata:
                if prompt is not None:
                    png_info.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for key, value in extra_pnginfo.items():
                        png_info.add_text(key, json.dumps(value))
            for key, value in pairs.items():
                png_info.add_text(key, value)

            file = f"{filename}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file), pnginfo=png_info, compress_level=4)
            results.append({"filename": file, "subfolder": subfolder, "type": "output"})
            counter += 1

        return {"ui": {"images": results}}


class LoadImageWithMetadata:
    """Load an image and emit IMAGE + MASK plus its embedded metadata STRING.

    The image-decode path matches the built-in ``LoadImage`` (EXIF transpose,
    RGB tensor, alpha → mask); the third output is the file's metadata rendered
    as ``key: value`` lines.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("image", "mask", "metadata")
    FUNCTION: ClassVar[str] = "load"
    CATEGORY: ClassVar[str] = "UtilityNodes/Image"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        import os

        import folder_paths

        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required": {"image": (sorted(files), {"image_upload": True})}}

    def load(self, image: str) -> tuple[Any, Any, str]:
        import folder_paths
        import numpy as np
        import torch
        from PIL import Image, ImageOps

        path = folder_paths.get_annotated_filepath(image)
        img = Image.open(path)
        metadata = format_metadata(_collect_image_metadata(img))

        img = ImageOps.exif_transpose(img)
        rgb = img.convert("RGB")
        array = np.array(rgb).astype(np.float32) / 255.0
        tensor = torch.from_numpy(array)[None,]

        if "A" in img.getbands():
            alpha = np.array(img.getchannel("A")).astype(np.float32) / 255.0
            mask = 1.0 - torch.from_numpy(alpha)
        else:
            mask = torch.zeros((img.height, img.width), dtype=torch.float32)

        return (tensor, mask.unsqueeze(0), metadata)

    @classmethod
    def IS_CHANGED(cls, image: str) -> str:
        import hashlib

        import folder_paths

        path = folder_paths.get_annotated_filepath(image)
        digest = hashlib.sha256()
        with open(path, "rb") as f:
            digest.update(f.read())
        return digest.hexdigest()

    @classmethod
    def VALIDATE_INPUTS(cls, image: str) -> bool | str:
        import folder_paths

        if not folder_paths.exists_annotated_filepath(image):
            return f"Invalid image file: {image}"
        return True


class ExtractImageMetadata:
    """Extract *all* metadata from a media file as a STRING.

    Unlike ``LoadImageWithMetadata`` this never decodes the pixels — it just
    opens the file and dumps PNG text chunks, EXIF, and the format/size/mode
    header. Useful for inspecting what a generator wrote into an image, or
    recovering a prompt from a saved PNG.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("metadata",)
    FUNCTION: ClassVar[str] = "extract"
    CATEGORY: ClassVar[str] = "UtilityNodes/Image"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        import os

        import folder_paths

        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required": {"image": (sorted(files), {"image_upload": True})}}

    def extract(self, image: str) -> tuple[str]:
        import folder_paths
        from PIL import Image

        path = folder_paths.get_annotated_filepath(image)
        with Image.open(path) as img:
            header = {
                "format": str(img.format),
                "size": f"{img.width}x{img.height}",
                "mode": str(img.mode),
            }
            collected = {**header, **_collect_image_metadata(img)}
        return (format_metadata(collected),)

    @classmethod
    def IS_CHANGED(cls, image: str) -> str:
        import hashlib

        import folder_paths

        path = folder_paths.get_annotated_filepath(image)
        digest = hashlib.sha256()
        with open(path, "rb") as f:
            digest.update(f.read())
        return digest.hexdigest()

    @classmethod
    def VALIDATE_INPUTS(cls, image: str) -> bool | str:
        import folder_paths

        if not folder_paths.exists_annotated_filepath(image):
            return f"Invalid image file: {image}"
        return True


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "UtilityNodesSaveImageWithMetadata": SaveImageWithMetadata,
    "UtilityNodesLoadImageWithMetadata": LoadImageWithMetadata,
    "UtilityNodesExtractImageMetadata": ExtractImageMetadata,
}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "UtilityNodesSaveImageWithMetadata": "Save Image with Metadata",
    "UtilityNodesLoadImageWithMetadata": "Load Image with Metadata",
    "UtilityNodesExtractImageMetadata": "Extract Image Metadata",
}

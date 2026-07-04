"""Image metadata nodes (issue #26, #29).

Four nodes that round-trip arbitrary metadata through media files:

- ``MetadataSet`` — build a ``CUUN_METADATA`` bundle one key/value pair at a
  time, optionally extending an upstream bundle (last-write-wins on
  duplicate keys). This is what feeds ``SaveImageWithMetadata.metadata``.
- ``SaveImageWithMetadata`` — write an IMAGE to the output folder with a
  ``CUUN_METADATA`` bundle embedded as PNG text chunks (alongside the usual
  ``prompt`` / workflow chunks, unless ``embed_workflow`` is off or ComfyUI
  was started with ``--disable-metadata``). It also emits the saved file
  path(s) as a STRING so they can be wired straight into the load/extract
  nodes below.
- ``LoadImageWithMetadata`` — load an image and emit IMAGE + MASK plus the
  metadata it carries as a STRING.
- ``ExtractImageMetadata`` — read *every* piece of metadata from a media file
  (PNG text chunks, EXIF, format/size/mode) as a STRING, without decoding the
  pixels into a tensor.

Both loaders accept either an ``image`` picked from the input folder or an
explicit ``path`` (an annotated filepath such as ``"foo.png [output]"``), so a
just-saved file can be read back in the same graph.

PIL / numpy / torch / folder_paths are ComfyUI-runtime modules, so they are
imported lazily inside the methods — the module stays importable (and the pure
parse/format helpers stay unit-testable) without them installed.
"""

from __future__ import annotations

import json
from typing import Any, ClassVar

METADATA_TYPE = "CUUN_METADATA"


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


def stringify_info(info: dict[Any, Any]) -> dict[str, str]:
    """Turn a raw ``img.info`` / EXIF mapping into a ``str -> str`` dict."""
    return {str(k): _to_str(v) for k, v in info.items()}


def format_metadata(metadata: dict[str, str]) -> str:
    """Render ordered key/value pairs as ``key: value`` lines (one per line)."""
    return "\n".join(f"{k}: {v}" for k, v in metadata.items())


def parse_formatted_metadata(text: str) -> dict[str, str]:
    """Inverse of :func:`format_metadata` — split ``key: value`` lines back into
    a dict.

    Splits each line on the first ``": "`` (the exact separator
    ``format_metadata`` writes), so values may freely contain ``:``, ``=`` and
    further ``": "`` pairs. Lines without the separator are skipped.
    """
    out: dict[str, str] = {}
    for raw in (text or "").splitlines():
        if ": " in raw:
            key, _, value = raw.partition(": ")
            out[key] = value
    return out


def metadata_pairs_to_dict(metadata: tuple[tuple[str, str], ...] | None) -> dict[str, str]:
    """Flatten a ``CUUN_METADATA`` bundle (ordered key/value pairs) into a dict.

    Later entries win on duplicate keys, matching ``MetadataSet``'s
    last-write-wins semantics.
    """
    return dict(metadata or ())


def get_metadata_value(metadata: str, key: str, default: str = "") -> tuple[str, bool]:
    """Look up one ``key`` in a formatted metadata dump.

    Returns ``(value, found)``; ``value`` is ``default`` when the key is absent.
    """
    parsed = parse_formatted_metadata(metadata)
    key = (key or "").strip()
    if key in parsed:
        return parsed[key], True
    return default, False


def annotated_output_path(filename: str, subfolder: str) -> str:
    """Build the ``"name [output]"`` annotated path a save result maps to.

    ``folder_paths.get_annotated_filepath`` understands a trailing
    ``[output]`` / ``[input]`` / ``[temp]`` tag and a ``subfolder/`` prefix —
    this is the exact form the load/extract nodes can resolve straight back.
    """
    name = f"{subfolder}/{filename}" if subfolder else filename
    return f"{name} [output]"


def first_path_line(path: str) -> str:
    """First non-blank line of a (possibly multi-file) path string."""
    for raw in (path or "").splitlines():
        line = raw.strip()
        if line:
            return line
    return ""


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


def _resolve_filepath(image: str | None, path: str) -> str:
    """Resolve the load source: an explicit ``path`` wins over the ``image`` pick."""
    import folder_paths

    chosen = first_path_line(path) or (image or "")
    if not chosen:
        raise ValueError("provide an `image` (input folder) or a `path`")
    return folder_paths.get_annotated_filepath(chosen)  # type: ignore[no-any-return]


def _file_digest(image: str | None, path: str) -> str:
    """Content hash for IS_CHANGED; falls back to the raw value if unresolvable
    (e.g. a linked `path` not visible at validation time — ComfyUI re-runs on
    upstream change anyway)."""
    import hashlib

    target = first_path_line(path) or (image or "")
    if not target:
        return ""
    try:
        import folder_paths

        resolved = folder_paths.get_annotated_filepath(target)
        digest = hashlib.sha256()
        with open(resolved, "rb") as f:
            digest.update(f.read())
        return digest.hexdigest()
    except Exception:
        return target


def _validate_source(image: str | None, path: str) -> bool | str:
    """VALIDATE_INPUTS body shared by both loaders. Lenient when neither value
    is a literal (a linked `path` isn't passed at validation time)."""
    if first_path_line(path):
        return True
    if image:
        import folder_paths

        if not folder_paths.exists_annotated_filepath(image):
            return f"Invalid image file: {image}"
    return True


class SaveImageWithMetadata:
    """Save an IMAGE to the output folder with custom metadata embedded.

    Mirrors the built-in ``SaveImage`` (same filename counter / output preview)
    but adds every pair from an incoming ``CUUN_METADATA`` bundle (built with
    one or more ``MetadataSet`` nodes) as a PNG text chunk, so the data
    round-trips through the file and can later be read back with
    ``LoadImageWithMetadata`` / ``ExtractImageMetadata``. The ``filenames``
    output carries the saved path(s) so they can be wired straight into those
    nodes.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("filenames",)
    FUNCTION: ClassVar[str] = "save"
    OUTPUT_NODE: ClassVar[bool] = True
    CATEGORY: ClassVar[str] = "UtilityNodes/Image"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI_meta"}),
            },
            "optional": {
                "metadata": (
                    METADATA_TYPE,
                    {"tooltip": "A CUUN_METADATA bundle built with MetadataSet. Each pair becomes a PNG text chunk."},
                ),
                "embed_workflow": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "Also embed the prompt/workflow chunks (like Save Image). Off = only your metadata.",
                    },
                ),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    def save(
        self,
        images: Any,
        filename_prefix: str,
        metadata: tuple[tuple[str, str], ...] | None = None,
        embed_workflow: bool = True,
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

        pairs = metadata_pairs_to_dict(metadata)
        output_dir = folder_paths.get_output_directory()
        height, width = int(images[0].shape[0]), int(images[0].shape[1])
        full_output_folder, filename, counter, subfolder, _ = folder_paths.get_save_image_path(
            filename_prefix, output_dir, width, height
        )

        results: list[dict[str, str]] = []
        saved_paths: list[str] = []
        for image in images:
            array = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(array, 0, 255).astype(np.uint8))

            png_info = PngInfo()
            if embed_workflow and not disable_metadata:
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
            saved_paths.append(annotated_output_path(file, subfolder))
            counter += 1

        return {"ui": {"images": results}, "result": ("\n".join(saved_paths),)}


class LoadImageWithMetadata:
    """Load an image and emit IMAGE + MASK plus its embedded metadata STRING.

    The image-decode path matches the built-in ``LoadImage`` (EXIF transpose,
    RGB tensor, alpha → mask); the third output is the file's metadata rendered
    as ``key: value`` lines. Source is an ``image`` from the input folder, or an
    explicit ``path`` (which wins) — e.g. wired from ``SaveImageWithMetadata``.
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
        return {
            "required": {},
            "optional": {
                "image": (sorted(files), {"image_upload": True}),
                "path": (
                    "STRING",
                    {"default": "", "tooltip": "Annotated filepath, e.g. 'foo.png [output]'. Overrides image."},
                ),
            },
        }

    def load(self, image: str | None = None, path: str = "") -> tuple[Any, Any, str]:
        import numpy as np
        import torch
        from PIL import Image, ImageOps

        resolved = _resolve_filepath(image, path)
        img = Image.open(resolved)
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
    def IS_CHANGED(cls, image: str | None = None, path: str = "") -> str:
        return _file_digest(image, path)

    @classmethod
    def VALIDATE_INPUTS(cls, image: str | None = None, path: str = "") -> bool | str:
        return _validate_source(image, path)


class ExtractImageMetadata:
    """Extract *all* metadata from a media file as a STRING.

    Unlike ``LoadImageWithMetadata`` this never decodes the pixels — it just
    opens the file and dumps PNG text chunks, EXIF, and the format/size/mode
    header. Useful for inspecting what a generator wrote into an image, or
    recovering a prompt from a saved PNG. Source is an ``image`` from the input
    folder, or an explicit ``path`` (which wins).
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
        return {
            "required": {},
            "optional": {
                "image": (sorted(files), {"image_upload": True}),
                "path": (
                    "STRING",
                    {"default": "", "tooltip": "Annotated filepath, e.g. 'foo.png [output]'. Overrides image."},
                ),
            },
        }

    def extract(self, image: str | None = None, path: str = "") -> tuple[str]:
        from PIL import Image

        resolved = _resolve_filepath(image, path)
        with Image.open(resolved) as img:
            header = {
                "format": str(img.format),
                "size": f"{img.width}x{img.height}",
                "mode": str(img.mode),
            }
            collected = {**header, **_collect_image_metadata(img)}
        return (format_metadata(collected),)

    @classmethod
    def IS_CHANGED(cls, image: str | None = None, path: str = "") -> str:
        return _file_digest(image, path)

    @classmethod
    def VALIDATE_INPUTS(cls, image: str | None = None, path: str = "") -> bool | str:
        return _validate_source(image, path)


class MetadataGetValue:
    """Pull a single value out of a formatted metadata dump by key.

    Wire the ``metadata`` STRING from ``LoadImageWithMetadata`` /
    ``ExtractImageMetadata`` (or paste a dump) and a ``key`` — e.g. ``seed``,
    ``author``, ``prompt`` — to get just that value, instead of the whole block.
    ``found`` is ``False`` (and ``value`` falls back to ``default``) when the
    key is absent.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", "BOOLEAN")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("value", "found")
    FUNCTION: ClassVar[str] = "get"
    CATEGORY: ClassVar[str] = "UtilityNodes/Image"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "metadata": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "A 'key: value' dump from Load/Extract Metadata"},
                ),
                "key": ("STRING", {"default": "", "tooltip": "The metadata key to read (exact match)."}),
            },
            "optional": {
                "default": ("STRING", {"default": "", "tooltip": "Returned when the key is absent."}),
            },
        }

    def get(self, metadata: str, key: str, default: str = "") -> tuple[str, bool]:
        return get_metadata_value(metadata, key, default)


class MetadataSet:
    """Build a ``CUUN_METADATA`` bundle one key/value pair at a time (issue #29).

    Chain several of these — each takes an optional upstream ``metadata``
    bundle and appends its own ``key``/``value`` pair — to build up the set
    that ``SaveImageWithMetadata`` embeds. Duplicate keys resolve last-write-
    wins (the pair closest to ``SaveImageWithMetadata`` in the chain wins).
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (METADATA_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("metadata",)
    FUNCTION: ClassVar[str] = "set"
    CATEGORY: ClassVar[str] = "UtilityNodes/Image"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "key": ("STRING", {"default": ""}),
                "value": ("STRING", {"default": ""}),
            },
            "optional": {
                "metadata": (METADATA_TYPE, {"tooltip": "An upstream CUUN_METADATA bundle to extend."}),
            },
        }

    def set(
        self, key: str, value: str, metadata: tuple[tuple[str, str], ...] | None = None
    ) -> tuple[tuple[tuple[str, str], ...]]:
        return ((*(metadata or ()), (key, value)),)


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "UtilityNodesSaveImageWithMetadata": SaveImageWithMetadata,
    "UtilityNodesLoadImageWithMetadata": LoadImageWithMetadata,
    "UtilityNodesExtractImageMetadata": ExtractImageMetadata,
    "UtilityNodesMetadataGetValue": MetadataGetValue,
    "UtilityNodesMetadataSet": MetadataSet,
}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "UtilityNodesSaveImageWithMetadata": "Save Image with Metadata",
    "UtilityNodesLoadImageWithMetadata": "Load Image with Metadata",
    "UtilityNodesExtractImageMetadata": "Extract Image Metadata",
    "UtilityNodesMetadataGetValue": "Get Metadata Value",
    "UtilityNodesMetadataSet": "Set Metadata",
}

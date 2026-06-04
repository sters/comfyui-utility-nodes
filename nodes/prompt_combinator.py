import re
from itertools import product
from typing import Any, ClassVar

_PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")


def _parse_axes(text: str, delimiter: str) -> list[tuple[str, list[str]]]:
    axes: list[tuple[str, list[str]]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"axis line must contain ':' — got {raw_line!r}")
        name, values = line.split(":", 1)
        name = name.strip()
        if not name:
            raise ValueError(f"axis name is empty in {raw_line!r}")
        items = [v.strip() for v in values.split(delimiter)]
        items = [v for v in items if v]
        if not items:
            raise ValueError(f"axis {name!r} has no values")
        axes.append((name, items))
    return axes


class PromptCombinator:
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", "STRING", "INT")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("prompt", "label", "index")
    OUTPUT_IS_LIST: ClassVar[tuple[bool, ...]] = (True, True, True)
    FUNCTION: ClassVar[str] = "expand"
    CATEGORY: ClassVar[str] = "utility/text"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "template": ("STRING", {"multiline": True, "default": ""}),
                "axes": ("STRING", {"multiline": True, "default": ""}),
                "delimiter": ("STRING", {"multiline": False, "default": ","}),
            },
        }

    def expand(
        self,
        template: str,
        axes: str,
        delimiter: str,
    ) -> tuple[list[str], list[str], list[int]]:
        sep = delimiter.encode("utf-8").decode("unicode_escape") if delimiter else ","
        parsed = _parse_axes(axes, sep)

        if not parsed:
            return ([], [], [])

        names = [n for n, _ in parsed]
        value_lists = [v for _, v in parsed]

        referenced = set(_PLACEHOLDER_RE.findall(template))
        unknown = referenced - set(names)
        if unknown:
            raise ValueError(f"template references unknown axes: {sorted(unknown)}")

        prompts: list[str] = []
        labels: list[str] = []
        indices: list[int] = []

        for i, combo in enumerate(product(*value_lists)):
            mapping = dict(zip(names, combo, strict=True))

            def _sub(m: re.Match[str], mp: dict[str, str] = mapping) -> str:
                return mp[m.group(1)]

            prompt = _PLACEHOLDER_RE.sub(_sub, template)
            label = "__".join(f"{n}={mapping[n]}" for n in names)
            prompts.append(prompt)
            labels.append(label)
            indices.append(i)

        return (prompts, labels, indices)


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "PromptCombinator": PromptCombinator,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "PromptCombinator": "Prompt Combinator",
}

from typing import ClassVar

from .._base import TagNodeBase

_FLUIDS: tuple[str, ...] = (
    "cum",
    "cum_in_pussy",
    "cum_in_ass",
    "cum_in_mouth",
    "cum_in_nose",
    "cum_on_body",
    "cum_on_face",
    "cum_on_breasts",
    "cum_on_stomach",
    "cum_on_hair",
    "cum_on_ass",
    "cum_on_self",
    "cum_string",
    "facial",
    "ejaculation",
    "ejaculating_while_penetrated",
    "excessive_cum",
    "overflow",
    "female_ejaculation",
    "squirting",
    "pussy_juice",
    "pussy_juice_trail",
    "saliva",
    "saliva_trail",
    "tears",
    "sweat",
)

_AFTERMATH_EXPRESSION: tuple[str, ...] = (
    "after_sex",
    "after_vaginal",
    "after_anal",
    "after_oral",
    "after_fellatio",
    "orgasm",
    "female_orgasm",
    "male_orgasm",
    "simultaneous_orgasm",
    "convulsing",
    "moaning",
    "x-ray",
    "internal_cumshot",
    "cross-section",
)


class NsfwStateFluids(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "nsfw.state.fluids"
    LAYER: ClassVar[str] = "nsfw_state"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _FLUIDS


class NsfwStateAftermathExpression(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "nsfw.state.aftermath"
    LAYER: ClassVar[str] = "nsfw_state"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _AFTERMATH_EXPRESSION


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "NsfwStateFluids": NsfwStateFluids,
    "NsfwStateAftermathExpression": NsfwStateAftermathExpression,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "NsfwStateFluids": "NSFW State: Fluids",
    "NsfwStateAftermathExpression": "NSFW State: Aftermath & Expression",
}

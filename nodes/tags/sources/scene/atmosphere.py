from typing import ClassVar

from ..._base import TagNodeBase

_TIME_OF_DAY: tuple[str, ...] = (
    "morning",
    "noon",
    "afternoon",
    "evening",
    "sunset",
    "sunrise",
    "dusk",
    "dawn",
    "day",
    "night",
    "midnight",
    "golden_hour",
    "blue_hour",
)

_WEATHER: tuple[str, ...] = (
    "sunny",
    "cloudy",
    "overcast",
    "foggy",
    "misty",
    "rain",
    "raining",
    "snow",
    "snowing",
    "storm",
    "thunderstorm",
    "blizzard",
    "windy",
    "calm",
    "clear_sky",
)

_PARTICLES: tuple[str, ...] = (
    "petals",
    "falling_petals",
    "cherry_blossoms",
    "falling_leaves",
    "autumn_leaves",
    "snowflakes",
    "fireflies",
    "sparkles",
    "glitter",
    "light_particles",
    "dust",
    "embers",
    "bubbles",
    "feathers",
    "confetti",
    "smoke",
    "steam",
    "mist",
    "fog",
    "water_drops",
    "splashing",
    "splashing_water",
)


class SceneTimeOfDay(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "scene.time_of_day"
    LAYER: ClassVar[str] = "scene"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _TIME_OF_DAY


class SceneWeather(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "scene.weather"
    LAYER: ClassVar[str] = "scene"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _WEATHER


class SceneParticles(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "scene.particles"
    LAYER: ClassVar[str] = "scene"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _PARTICLES


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "SceneTimeOfDay": SceneTimeOfDay,
    "SceneWeather": SceneWeather,
    "SceneParticles": SceneParticles,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "SceneTimeOfDay": "Scene: Time of Day",
    "SceneWeather": "Scene: Weather",
    "SceneParticles": "Scene: Particles & Atmosphere",
}

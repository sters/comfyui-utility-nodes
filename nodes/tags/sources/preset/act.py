from ._base import PresetNodeBase

# SFW act presets — curated multi-tag combinations describing what a character
# is *doing*, independent of where they are. Designed to layer on top of
# SituationPreset (setting) and CharacterPreset (visuals) via TagsBuild.
#
# Unlike the single-toggle BodyAction / BodyPosture / HandsGesture nodes,
# each preset here packages several related tags (action + posture + hand pose
# + expression) that belong together for a coherent activity. Choose one of
# these when you want the activity to be the focus, then add a situation for
# the backdrop if needed.
ACT_PRESETS: dict[str, tuple[str, ...]] = {
    # ── Reading / Writing ──────────────────────────────────────────────────
    "reading_absorbed": (
        "reading",
        "holding_book",
        "sitting",
        "from_side",
    ),
    "studying_focused": (
        "studying",
        "holding_pencil",
        "sitting",
        "serious",
        "looking_down",
    ),
    "writing_letter": (
        "writing",
        "holding_pen",
        "sitting",
        "smile",
    ),
    # ── Phone / Camera ─────────────────────────────────────────────────────
    "selfie_peace": (
        "selfie",
        "holding_phone",
        "peace_sign",
        "smile",
        "looking_at_viewer",
    ),
    "selfie_wink": (
        "selfie",
        "holding_phone",
        "v",
        "one_eye_closed",
        "smile",
        "looking_at_viewer",
    ),
    "phone_call_serious": (
        "phone_call",
        "holding_phone",
        "from_side",
        "looking_away",
        "serious",
    ),
    "texting_casual": (
        "texting",
        "holding_phone",
        "sitting",
        "smile",
        "looking_down",
    ),
    "taking_photo": (
        "holding_camera",
        "looking_at_viewer",
        "smile",
    ),
    # ── Rest / Relaxation ─────────────────────────────────────────────────
    "sleeping_peaceful": (
        "sleeping",
        "lying",
        "on_side",
        "closed_eyes",
    ),
    "napping_lazy": (
        "napping",
        "lying",
        "on_back",
        "closed_eyes",
        "sleepy",
    ),
    "stretching_morning": (
        "stretching",
        "arms_up",
        "sleepy",
        "closed_eyes",
    ),
    "daydreaming": (
        "dreaming",
        "sitting",
        "hand_on_own_face",
        "looking_away",
    ),
    # ── Emotional ──────────────────────────────────────────────────────────
    "laughing_joyful": (
        "laughing",
        "happy",
        "open_mouth",
        "closed_eyes",
    ),
    "crying_sad": (
        "crying",
        "tearful",
        "sad",
        "looking_away",
    ),
    # ── Active ─────────────────────────────────────────────────────────────
    "running_sprint": (
        "running",
        "dynamic_pose",
        "determined",
    ),
    "jumping_joyful": (
        "jumping",
        "arms_up",
        "smile",
        "happy",
        "open_mouth",
    ),
    "dancing_energetic": (
        "dancing",
        "dynamic_pose",
        "smile",
        "open_mouth",
    ),
    # ── Music / Performance ────────────────────────────────────────────────
    "playing_guitar_intense": (
        "playing_guitar",
        "playing_instrument",
        "dynamic_pose",
        "determined",
    ),
    "playing_piano_focused": (
        "playing_piano",
        "playing_instrument",
        "serious",
        "from_side",
    ),
    "singing_stage": (
        "singing",
        "holding_microphone",
        "smile",
        "open_mouth",
        "looking_at_viewer",
    ),
    # ── Domestic / Daily ──────────────────────────────────────────────────
    "cooking_happy": (
        "cooking",
        "smile",
        "from_side",
    ),
    "eating_delighted": (
        "eating",
        "holding_chopsticks",
        "smile",
        "happy",
    ),
    "drinking_tea": (
        "drinking",
        "holding_cup",
        "smile",
    ),
    # ── Pose / Attitude ────────────────────────────────────────────────────
    "confident_standing": (
        "standing",
        "hand_on_own_hip",
        "smirk",
        "looking_at_viewer",
    ),
    "victory_thumbs": (
        "thumbs_up",
        "smile",
        "looking_at_viewer",
        "happy",
    ),
    "shy_pose": (
        "embarrassed",
        "arm_behind_back",
        "looking_away",
    ),
    "thinking_chin": (
        "hand_on_own_face",
        "sitting",
        "looking_away",
        "serious",
    ),
    "waving_greeting": (
        "waving",
        "smile",
        "looking_at_viewer",
        "happy",
    ),
    "arms_crossed_stern": (
        "crossed_arms",
        "standing",
        "serious",
        "looking_at_viewer",
    ),
    # ── Social / Activity ──────────────────────────────────────────────────
    "gaming_focused": (
        "gaming",
        "sitting",
        "leaning_forward",
        "determined",
    ),
    "hugging_warmly": (
        "hugging",
        "smile",
        "happy",
        "closed_eyes",
    ),
    "pointing_excited": (
        "pointing_at_viewer",
        "smile",
        "happy",
        "looking_at_viewer",
    ),
    "praying_serene": (
        "praying",
        "own_hands_together",
        "closed_eyes",
        "serious",
    ),
}


class ActPreset(PresetNodeBase):
    PRESETS = ACT_PRESETS
    PARAM = "act"
    LAYER = "situation"


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesActPreset": ActPreset}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesActPreset": "Act"}

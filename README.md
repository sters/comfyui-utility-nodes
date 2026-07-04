# comfyui-utility-nodes

A pack of utility custom nodes for [ComfyUI](https://github.com/comfyanonymous/ComfyUI), focused on **prompt construction for tag-based models**. It gives you checkbox-driven tag-group nodes, cross-node conflict resolution, one-click character/scene presets, and a handful of general text/image helpers.

## Installation

```sh
cd ComfyUI/custom_nodes
git clone https://github.com/sters/comfyui-utility-nodes.git
```

Restart ComfyUI. The nodes appear in the Add-Node menu under the `UtilityNodes` category (with `TagMaster`, `Text`, `Image`, and `Util` sub-menus).

## Per-node help

Every node ships an in-app help page. Click the **help (?) button on the node** to read its full spec — inputs/outputs, the exact tags it emits, and any mutex/conflict behavior — without leaving ComfyUI ([Help Page feature](https://docs.comfy.org/custom-nodes/help_page)). The pages are the English docs under `web/docs/<ClassName>.md`.

## Workflow templates

Ready-made example graphs are bundled as ComfyUI [Workflow Templates](https://docs.comfy.org/custom-nodes/workflow_templates). Open them from **Workflow → Browse Templates → `comfyui-utility-nodes`**.

## How the tag pipeline works

The core idea: instead of hand-typing tags, you toggle them on dedicated nodes, then merge everything through a single node that resolves conflicts and emits the final prompt string.

```
Tag-source nodes  ──►  bundle (CUUN_TAGS)  ──►  Tags: Merge & Validate  ──►  prompt (STRING)
  (checkbox UIs)        structured tags          conflict resolution        + warnings + bundle
```

- **Tag-source nodes** (`Hair: ...`, `Body: ...`, `Clothing: ...`, `Scene: ...`, `NSFW ...`, etc.) are boolean-checkbox UIs. Their single output is `bundle`, a structured `CUUN_TAGS` value that carries each selection's category, layer, and mutex metadata. The flattened tag text is shown as a preview on the node, but it is **not** a separate output socket — wire `bundle` onward to get a STRING.
- Each source also has an `invert` toggle (flips every checkbox at once — handy for "everything except a few" on large nodes) and an optional free-form `extra` text field that is appended verbatim.
- **`Tags: Merge & Validate`** (`TagsMerge`) accepts up to 10 `CUUN_TAGS` bundles and applies the conflict rules defined in `nodes/tags/_conflicts.py` (`MUTEX_GROUPS` and `TAG_CONFLICTS`). It resolves things like `nude` vs. clothing, `topless` vs. bras, `barefoot` vs. legwear, or `long_hair` vs. `short_hair` automatically. It returns three outputs: `prompt` (the joined STRING), `warnings` (what was dropped and why), and `bundle` (the merged structured result for further chaining).

For quick-and-dirty graphs you can also feed a bundle through `Tags: Combinator` / `Tags: Decorate` / `Tags: Filter` and friends without a full merge — but `Merge & Validate` is the node that guarantees a coherent, conflict-free prompt.

## Node catalog

> The **Class** column below is the Python class / menu name. The actual registered `class_type` is that name prefixed with `UtilityNodes` (e.g. `TagsMerge` → `UtilityNodesTagsMerge`) so it can't be shadowed by another pack's same-named node. Workflows saved before the prefix auto-upgrade on load — the pack registers a ComfyUI node-replacement (`<bare>` → `UtilityNodes<bare>`) for every node.

### Tag operations — `UtilityNodes/TagMaster`

These consume/transform `CUUN_TAGS` bundles (or, where noted, a prompt STRING).

| Node | Class | Purpose |
| --- | --- | --- |
| `Tags: Merge & Validate` | `TagsMerge` | The pipeline's terminal build step — merge up to 10 bundles and resolve up to 10 random specs, resolve all cross-node conflicts, emit the final prompt + warnings. |
| `Tags: Combinator` | `TagsCombinator` | Cartesian product over tag axes — emits a list of `bundle`/`label`/`index` (feed `bundle` into `Merge & Validate`) for batch/variation runs. |
| `Tags: Decorate` | `TagsDecorate` | Prefix the tags of a chosen category with a decoration phrase (built from another bundle); broadcasts as a cross product for multi-variant runs. |
| `Tags: Explode` | `TagsExplode` | Split a bundle into one single-tag bundle per tag — feed it into `Combinator` to turn N checked tags into N axis values. |
| `Tags: Collect` | `TagsCollect` | Gather several whole bundles into one list — feed it into `Combinator` to vary over whole bundles (e.g. multiple characters), one combination per bundle. |
| `Tags: Select` | `TagsSelect` | Pick one combination out of a `Combinator` list by index (wraps) — drive `index` from `Seed` and queue N runs for memory-safe large sweeps instead of one N-wide Run. |
| `Tags: Filter` | `TagsFilter` | Drop every tag whose registered category matches a target category. |
| `Tags: Random Pick` | `TagsRandomPick` | Describe a random subset-of-tags pick from a bundle (resolved by `Merge & Validate`). |
| `Tags: Random Bundle` | `TagsRandomBundle` | Describe a random whole-bundle choice among several alternatives (resolved by `Merge & Validate`). |
| `Tags: Shuffle` | `TagsShuffle` | Shuffle tag order within a bundle. |
| `Tags: Extract Subject Count` | `TagsExtractSubjectCount` | Parse a prompt STRING and extract a person/subject count as an INT. |
| `Tags: Bundle Inspector` | `TagsBundleInspector` | Debug helper — surface the structured contents of a `CUUN_TAGS` bundle. |

### Presets — `UtilityNodes/TagMaster/Preset`

One-click, pre-composed tag sets that still flow through the same merge pipeline.

| Node | Class |
| --- | --- |
| `Character` | `CharacterPreset` |
| `Personality` | `PersonalityPreset` |
| `Situation` | `SituationPreset` |
| `NSFW Scene` | `NsfwScenePreset` |

### Tag sources

Checkbox tag-group nodes, organized by what they describe:

| Group | Examples |
| --- | --- |
| **Body** | `Figure`, `Posture`, `Action`, `Seating Style`, `Skin`, `Exposure`, `Scars`, `Tattoos`, `Moles & Freckles`, `Lower Anatomy`, `Breasts: Size`, `Breasts: Shape & State` |
| **Face** | `Expression`, `Blush & Flush`, `Eyes: Color / State & Gaze / Pupils & Details`, `Mouth: State / Details` |
| **Hair** | `Hair: Color`, `Hair: Length & Style`, `Hair: Details` |
| **Hands & Feet** | `Hands: Pose / Gesture / Detail`, `Feet: Anatomy`, `Feet: Legs & Pose` |
| **Holding** | `Holding: Object`, `Holding: Weapon` |
| **Animal features** | `Animal Ears`, `Animal Horns`, `Animal Tail`, `Animal Wings` |
| **Clothing** | `Tops`, `Bottoms`, `Dress & One-piece`, `Underwear`, `Swimwear`, `Legwear`, `Footwear`, `Headwear`, `Eyewear`, `Neck`, `Hand & Arm`, `Accessory`, `Uniform & Costume`, `Material`, `Pattern`, `Fit`, `State`, `Position`, `Lift & Pull`, `Aside & Partial Expose`, `Naked X` |
| **Scene** | `Background Type`, `Indoor Location`, `Outdoor Location`, `Lighting`, `Time of Day`, `Weather`, `Particles & Atmosphere` |
| **Composition** | `Angle`, `Framing`, `Crop`, `Focus`, `Multi-View` |
| **Color** | `Color Palette` |
| **Meta** | `Quality` (`MetaQuality`), `Pony` (`MetaPony`, Pony Diffusion template), `Subject Count: Total / Girls / Boys / Other` |
| **Bad / negative** | `Bad: General`, `Bad: Head & Face`, `Bad: Body`, `Bad: Limbs`, `Bad: Quality`, `Bad: NSFW` — `bad_*` / `extra_*` families split by body part for negative prompts |
| **NSFW** | `Solo`, `Position`, `Act: Oral & Contact`, `Act: Penetrative`, `State: Fluids`, `State: Aftermath & Expression`, `BDSM`, `Toy` |

### Text — `UtilityNodes/Text`

General prompt utilities, independent of the tag bundle system: `Text Concat` (`TextConcat`), `List Shuffle` (`ListShuffle`), `Random Text Picker` (`RandomTextPicker`).

### Image & Util

`Aspect Ratio Preset` (`AspectRatioPreset`, under `UtilityNodes/Image`) and `Seed` (`Seed`, under `UtilityNodes/Util`).

## Development

```sh
make sync     # install dependencies (uv)
make check    # lint + fmt-check + typecheck + pytest
make fix      # ruff --fix + format
make integration  # end-to-end check against a CPU-only ComfyUI Docker image
```

Target Python is 3.10+, mypy runs in `strict` mode, and ruff enforces a 120-char line length. See `CLAUDE.md` for the architecture, naming conventions, and how to add a new tag node.

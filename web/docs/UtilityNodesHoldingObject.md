# Body: Holding (object)

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `anatomy` / `body.holding.object`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `holding`
- `holding_book`
- `holding_phone`
- `holding_food`
- `holding_cup`
- `holding_bottle`
- `holding_drink`
- `holding_pen`
- `holding_pencil`
- `holding_paper`
- `holding_letter`
- `holding_envelope`
- `holding_flower`
- `holding_bouquet`
- `holding_umbrella`
- `holding_microphone`
- `holding_camera`
- `holding_stuffed_toy`
- `holding_bag`
- `holding_basket`
- `holding_chopsticks`
- `holding_fork`
- `holding_spoon`
- `holding_cigarette`
- `holding_fan`
- `holding_mask`
- `holding_clothes`
- `holding_underwear`
- `holding_leash`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).

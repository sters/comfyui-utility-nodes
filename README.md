# comfyui-utility-nodes

ComfyUI 向けのユーティリティ系カスタムノード集。

## インストール

ComfyUI の `custom_nodes/` 配下にこのリポジトリを clone する。

```sh
cd ComfyUI/custom_nodes
git clone https://github.com/sters/comfyui-utility-nodes.git
```

ComfyUI を再起動するとノードが読み込まれる。

## ノード一覧

### Prompt Combinator

`utility/text` カテゴリ。テンプレートと軸定義から全組み合わせのプロンプトを展開する。出力は STRING リスト (`OUTPUT_IS_LIST=True`) なので、下流の CLIPTextEncode / KSampler / SaveImage が要素ごとに自動で繰り返し実行される。

- 入力
  - `template` (STRING, multiline): プレースホルダ `{name}` 入りテンプレ
  - `axes` (STRING, multiline): `name: v1, v2, v3` 形式を1行1軸で。`#` で始まる行と空行は無視
  - `delimiter` (STRING): 軸内の区切り文字。`\n` などのエスケープも可
- 出力 (すべてリスト)
  - `prompt` (STRING): 展開されたプロンプト
  - `label` (STRING): `name=value__...` 形式の識別子。SaveImage の filename_prefix 用
  - `index` (INT): 0始まり連番

例:
```
template: {hair} hair, {eye} eyes
axes:
  hair: short, long
  eye: red, blue
```
→ 4件の prompt が下流に流れる。

### List Shuffle

`utility/text` カテゴリ。STRING リストをシード付きでシャッフルし、必要なら先頭 N 件だけ返す。`PromptCombinator` の後段に挟むと「全組み合わせからランダム N 件だけ生成」が実現できる。

- 入力
  - `items` (STRING list): 上流ノードから接続する想定
  - `seed` (INT): 乱数シード
  - `limit` (INT): 0なら全件、>0なら先頭N件にキャップ
- 出力
  - `items` (STRING list)

### Text Concat

`utility/text` カテゴリ。最大10個までの STRING 入力を `separator` で連結する。`None` および空文字の入力はスキップ。

- 入力
  - `separator` (STRING): 区切り文字。`\n` などのエスケープ可
  - `text_1` ~ `text_10` (STRING, optional): 接続された分だけ使われる
- 出力
  - `text` (STRING)

### Pony Prompt Builder

`utility/text` カテゴリ。Pony Diffusion V6 XL 用の専用タグを GUI でポチポチ選んで合成する。

- 入力
  - `separator` (STRING)
  - `score_9` ~ `score_4_up` (BOOLEAN, 個別 on/off): negative 用に弱いスコアだけ ON、強いスコアだけ ON など微調整可
  - `rating` (combo): `none` / `safe` / `questionable` / `explicit`
  - `source` (combo): `none` / `pony` / `furry` / `cartoon` / `anime`
  - `extra` (STRING, multiline, optional): 後ろに連結する本文
- 出力
  - `prompt` (STRING)

出力順は score → rating → source → extra（README の推奨テンプレ準拠）。

`OUTPUT_NODE = True` を設定しているので、Queue Prompt 実行後にノード下に組み立て結果のプレビューが表示される。

### Danbooru Bad Tags (5ノード)

Negative prompt 用に、Danbooru の [bad_anatomy](https://danbooru.donmai.us/wiki_pages/bad_anatomy) / [artistic_error](https://danbooru.donmai.us/wiki_pages/artistic_error) 系タグをパーツ別に分けた5ノード。各ノードは個別 BOOLEAN（デフォルト全 True）。合計52タグ。`TextConcat` で繋いで最終 negative prompt を組み立てる想定。

すべて `utility/text` カテゴリ、`OUTPUT_NODE = True`（実行後にプレビュー表示）、共通入力 `separator` (STRING) と `extra` (STRING, multiline, optional)、出力 `prompt` (STRING)。

| ノード | 対象タグ |
| --- | --- |
| Danbooru Bad: General | `artistic_error`, `bad_anatomy`, `anatomical_nonsense`, `bad_proportions`, `bad_perspective`, `bad_reflection`, `bad_multiple_views`, `bad_shadow`, `bad_gun_anatomy`, `bad_vehicle_anatomy`, `bad_internal_anatomy` |
| Danbooru Bad: Head & Face | `bad_face`, `bad_neck`, `bad_ears`, `bad_teeth`, `extra_ears`, `extra_eyes`, `extra_eyelids`, `extra_eyebrows`, `extra_pupils`, `extra_mouth`, `extra_tongue`, `extra_teeth`, `extra_noses`, `extra_faces`, `extra_horns`, `extra_tusks` |
| Danbooru Bad: Body | `bad_torso`, `bad_ass`, `extra_pectorals`, `extra_nipples`, `extra_breasts`, `extra_tails` |
| Danbooru Bad: Limbs | `bad_arm`, `bad_hands`, `bad_leg`, `bad_knees`, `bad_feet`, `wrong_hand`, `wrong_foot`, `extra_digits`, `extra_arms`, `extra_hands`, `extra_legs`, `extra_toes`, `fewer_digits` |
| Danbooru Bad: NSFW | `bad_vulva`, `extra_penises`, `extra_testicles`, `extra_pussies`, `extra_clitorises`, `extra_anus` |

「今は NSFW 生成じゃない」「猫耳/獣耳キャラなので Head & Face は外す」のようにノード単位で一括 on/off できる（不要なノードはワークフローから外すか出力を繋がない）。意図的なキャラ設計（`extra_ears`, `extra_tails`, `extra_horns` 等）と当たるタグは個別に off にする。

### Composition Tags (5ノード)

Danbooru の [tag_group:image_composition](https://danbooru.donmai.us/wiki_pages/tag_group%3Aimage_composition) 由来のアングル/構図/フォーカス系タグ。デフォルト全 False で、欲しいタグだけ ON にする。全部 ON にして `RandomTextPicker` でランダム選択する運用も可。

すべて `utility/text` カテゴリ、`OUTPUT_NODE = True`、共通入力 `separator` と `extra`、出力 `prompt`。

| ノード | 対象タグ |
| --- | --- |
| Composition: Angle | `dutch_angle`, `from_above`, `from_behind`, `from_below`, `from_side`, `sideways`, `three-quarter_view`, `straight-on`, `upside-down`, `pov`, `from_outside`, `from_inside`, `partially_underwater_shot`, `atmospheric_perspective`, `fisheye`, `perspective`, `vanishing_point`, `foreshortening` |
| Composition: Framing | `portrait`, `upper_body`, `cowboy_shot`, `full_body`, `wide_shot`, `very_wide_shot`, `lower_body`, `close-up`, `profile`, `group_profile`, `cut-in`, `split_crop` |
| Composition: Crop | `cropped_legs`, `cropped_torso`, `cropped_arms`, `cropped_shoulders`, `cropped_head`, `head_out_of_frame`, `feet_out_of_frame`, `eyes_out_of_frame`, `foot_out_of_frame`, `knees_out_of_frame` |
| Composition: Focus | `armpit_focus`, `ass_focus`, `back_focus`, `breast_focus`, `eye_focus`, `foot_focus`, `hand_focus`, `hip_focus`, `leg_focus`, `navel_focus`, `pectoral_focus`, `penis_focus`, `thigh_focus` |
| Composition: Multi-View | `multiple_views`, `reference_sheet`, `character_chart`, `turnaround`, `sprite_sheet`, `multiple_expressions`, `variations`, `projected_inset`, `zoom_layer`, `age_comparison`, `clothes_on_and_off` |

Crop 系（`cropped_*`, `*_out_of_frame`）は「見切れ」なので negative prompt 用途で使うことが多い。

### Random Text Picker

`utility/text` カテゴリ。入力テキストを区切り文字で分割し、指定数だけランダムに抽出する。プロンプトのランダム選択用途。

- 入力
  - `text` (STRING, multiline): 対象テキスト
  - `delimiter` (STRING): 区切り文字。`\n` や `\t` などのエスケープシーケンスも使える
  - `count` (INT): 抽出数。要素数より大きければ全件返す
  - `seed` (INT): 乱数シード
- 出力
  - `text` (STRING): 抽出結果を同じ区切り文字で連結したテキスト

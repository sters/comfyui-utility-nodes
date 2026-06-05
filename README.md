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

### Bad Tags (5ノード)

Negative prompt 用に、Danbooru の [bad_anatomy](https://danbooru.donmai.us/wiki_pages/bad_anatomy) / [artistic_error](https://danbooru.donmai.us/wiki_pages/artistic_error) 系タグをパーツ別に分けた5ノード。各ノードは個別 BOOLEAN（デフォルト全 True）。合計52タグ。`TextConcat` で繋いで最終 negative prompt を組み立てる想定。

すべて `utility/text` カテゴリ、`OUTPUT_NODE = True`（実行後にプレビュー表示）、共通入力 `separator` (STRING) と `extra` (STRING, multiline, optional)、出力 `prompt` (STRING)。

| ノード | 対象タグ |
| --- | --- |
| Bad: General | `artistic_error`, `bad_anatomy`, `anatomical_nonsense`, `bad_proportions`, `bad_perspective`, `bad_reflection`, `bad_multiple_views`, `bad_shadow`, `bad_gun_anatomy`, `bad_vehicle_anatomy`, `bad_internal_anatomy` |
| Bad: Head & Face | `bad_face`, `bad_neck`, `bad_ears`, `bad_teeth`, `extra_ears`, `extra_eyes`, `extra_eyelids`, `extra_eyebrows`, `extra_pupils`, `extra_mouth`, `extra_tongue`, `extra_teeth`, `extra_noses`, `extra_faces`, `extra_horns`, `extra_tusks` |
| Bad: Body | `bad_torso`, `bad_ass`, `extra_pectorals`, `extra_nipples`, `extra_breasts`, `extra_tails` |
| Bad: Limbs | `bad_arm`, `bad_hands`, `bad_leg`, `bad_knees`, `bad_feet`, `wrong_hand`, `wrong_foot`, `extra_digits`, `extra_arms`, `extra_hands`, `extra_legs`, `extra_toes`, `fewer_digits` |
| Bad: NSFW | `bad_vulva`, `extra_penises`, `extra_testicles`, `extra_pussies`, `extra_clitorises`, `extra_anus` |

「今は NSFW 生成じゃない」「猫耳/獣耳キャラなので Head & Face は外す」のようにノード単位で一括 on/off できる（不要なノードはワークフローから外すか出力を繋がない）。意図的なキャラ設計（`extra_ears`, `extra_tails`, `extra_horns` 等）と当たるタグは個別に off にする。

### タグ系ノード共通: `preset` combo

Bad / Composition / Hair / Hands / Feet / Breasts / Body / Clothing 系の全タグノードは共通で `preset` combo を持つ。

| 値 | 挙動 |
| --- | --- |
| `custom` (デフォルト) | 各チェックボックスの値どおり |
| `all_on` | チェックボックスを無視して全タグ ON |
| `all_off` | チェックボックスを無視して全タグ OFF |
| `invert` | チェックボックスの値を反転 |

50タグ以上ある node で「全部入れたい」「とりあえず全部消して数個だけ入れる」をワンクリックで切り替えられる。`invert` は「ほぼ全部入れたいが2,3個だけ外したい」時に便利。

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

### Hair Tags (3ノード)

髪型・髪色・髪まわりのディテール系タグ。Danbooru の count 上位タグから定番を抽出。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Hair: Length & Style | `very_long_hair`, `long_hair`, `medium_hair`, `short_hair`, `short_hair_with_long_locks`, `low-tied_long_hair`, `ponytail`, `high_ponytail`, `low_ponytail`, `side_ponytail`, `twintails`, `low_twintails`, `short_twintails`, `twin_braids`, `side_braid`, `single_braid`, `braid`, `bob_cut`, `hair_bun`, `double_bun`, `single_hair_bun`, `drill_hair`, `twin_drills`, `one_side_up`, `two_side_up`, `half_updo`, `wavy_hair`, `straight_hair`, `curly_hair`, `messy_hair`, `spiked_hair`, `floating_hair` |
| Hair: Color | `blonde_hair`, `black_hair`, `brown_hair`, `blue_hair`, `light_blue_hair`, `pink_hair`, `white_hair`, `grey_hair`, `silver_hair`, `purple_hair`, `red_hair`, `green_hair`, `orange_hair`, `aqua_hair`, `multicolored_hair`, `two-tone_hair`, `streaked_hair`, `gradient_hair`, `colored_inner_hair` |
| Hair: Details | `bangs`, `blunt_bangs`, `parted_bangs`, `swept_bangs`, `crossed_bangs`, `double-parted_bangs`, `hair_between_eyes`, `hair_over_one_eye`, `hair_over_eyes`, `hair_over_shoulder`, `hair_behind_ear`, `hair_flaps`, `sidelocks`, `ahoge`, `antenna_hair`, `hair_intakes`, `hair_tubes`, `blunt_ends`, `hair_ornament`, `x_hair_ornament`, `star_hair_ornament`, `hair_bow`, `hair_ribbon`, `hair_flower`, `hairband`, `hairclip`, `hair_bobbles`, `hair_rings`, `hair_scrunchie` |

### Hands Tags (3ノード)

手・腕・指まわりのポーズ/ジェスチャー/ディテール。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Hands: Pose | `hand_up`, `hands_up`, `arm_up`, `arms_up`, `arm_behind_back`, `arms_behind_back`, `arm_behind_head`, `arms_behind_head`, `arm_at_side`, `arm_support`, `outstretched_arm`, `outstretched_arms`, `crossed_arms`, `hand_on_own_hip`, `hand_on_own_chest`, `hand_on_own_face`, `hand_to_own_mouth`, `hand_on_another's_head`, `hand_in_pocket`, `own_hands_together`, `holding_hands`, `interlocked_fingers`, `finger_to_mouth` |
| Hands: Gesture | `v`, `peace_sign`, `double_peace`, `thumbs_up`, `pointing`, `pointing_at_viewer`, `index_finger_raised`, `clenched_hand`, `clenched_hands`, `open_hand`, `fist`, `waving` |
| Hands: Detail | `fingernails`, `long_fingernails`, `sharp_fingernails`, `nail_polish`, `black_nails`, `red_nails`, `pink_nails`, `blue_nails`, `claws` |

### Feet Tags (2ノード)

足・脚まわり。`foot_focus` / `feet_out_of_frame` は Composition: Focus / Crop と重複するのでそちらを使う。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Feet: Anatomy | `barefoot`, `no_shoes`, `feet`, `toes`, `toenails`, `soles`, `feet_together`, `feet_up`, `crossed_ankles`, `tiptoes` |
| Feet: Legs & Pose | `legs`, `thighs`, `bare_legs`, `thigh_gap`, `spread_legs`, `crossed_legs`, `leg_up`, `leg_lift`, `knee_up`, `knees_up`, `knees_together_feet_apart`, `standing_on_one_leg`, `on_one_leg`, `kneeling`, `squatting`, `wariza`, `seiza`, `indian_style` |

### Breasts Tags (2ノード)

胸まわり。サイズと形状/状態の2分割。サイズはどれか1つだけ ON にする運用が想定。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Breasts: Size | `flat_chest`, `small_breasts`, `medium_breasts`, `large_breasts`, `huge_breasts`, `gigantic_breasts` |
| Breasts: Shape & State | `cleavage`, `sideboob`, `underboob`, `backboob`, `breasts_apart`, `breast_press`, `between_breasts`, `covered_nipples`, `cleavage_cutout`, `asymmetrical_docking`, `sagging_breasts`, `downblouse`, `nipples`, `puffy_nipples`, `inverted_nipples`, `pointy_breasts`, `areolae`, `areola_slip`, `nipple_slip`, `breasts_out`, `no_bra`, `pasties`, `nipple_piercing` |

### Body Type Tags (2ノード)

体型と肌色。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Body: Figure | `petite`, `slim`, `curvy`, `toned`, `muscular`, `muscular_female`, `muscular_male`, `abs`, `toned_female`, `toned_male`, `thick_thighs`, `wide_hips`, `thigh_gap`, `skindentation`, `pectorals`, `large_pectorals`, `narrow_waist`, `plump`, `chubby` |
| Body: Skin | `pale_skin`, `white_skin`, `fair_skin`, `tan`, `tanlines`, `dark_skin`, `dark-skinned_female`, `dark-skinned_male`, `very_dark_skin`, `shiny_skin`, `colored_skin` |

### Body Exposure Tags (2ノード)

純粋なヌード状態と下半身解剖。服装系は別の Clothing ノード群に分離。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Body: Exposure | `nude`, `completely_nude`, `partially_nude` |
| Body: Lower Anatomy | `ass`, `ass_visible_through_thighs`, `cameltoe`, `pussy`, `anus`, `clitoris`, `pubic_hair`, `female_pubic_hair`, `presenting` |

### Body Marks Tags (3ノード)

キャラ判別用の体表マーク。NSFW 関係なくキャラの一貫性に効く。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Body: Moles & Freckles | `mole`, `mole_under_eye`, `mole_under_mouth`, `mole_on_cheek`, `mole_on_neck`, `mole_on_breast`, `mole_on_stomach`, `mole_on_thigh`, `mole_on_ass`, `mole_on_armpit`, `freckles`, `beauty_mark`, `birthmark` |
| Body: Scars | `scar`, `scar_on_face`, `scar_on_cheek`, `scar_across_eye`, `scar_on_nose`, `scar_on_forehead`, `scar_on_arm`, `scar_on_chest`, `scar_on_stomach`, `scar_on_back`, `scar_on_neck`, `scar_on_leg`, `bandages`, `bandaged_arm`, `bandaged_leg`, `bandage_over_one_eye` |
| Body: Tattoos | `tattoo`, `facial_tattoo`, `neck_tattoo`, `shoulder_tattoo`, `arm_tattoo`, `hand_tattoo`, `chest_tattoo`, `breast_tattoo`, `back_tattoo`, `lower_back_tattoo`, `stomach_tattoo`, `thigh_tattoo`, `leg_tattoo` |

### Clothing State Tags (3ノード)

服の着方/状態。露出ヌードではなく「ボタン開いてる」「めくれてる」「これしか着てない」系。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Clothing: State | `topless`, `bottomless`, `no_panties`, `undressing`, `dressing`, `half-undressed`, `open_clothes`, `open_shirt`, `open_jacket`, `open_coat`, `open_robe`, `open_kimono`, `open_dress`, `open_vest`, `open_cardigan`, `partially_unbuttoned`, `unbuttoned`, `untied`, `loose_clothes`, `loose_shirt`, `loose_necktie`, `wardrobe_malfunction` |
| Clothing: Lift & Pull | `clothes_lift`, `shirt_lift`, `skirt_lift`, `dress_lift`, `kimono_lift`, `clothes_pull`, `panty_pull`, `bra_pull`, `shirt_pull`, `skirt_pull`, `clothes_down`, `panties_down`, `shirt_tug`, `clothes_tug`, `clothes_removed`, `shirt_removed`, `panties_removed`, `bra_removed`, `clothes_around_waist`, `clothes_in_mouth` |
| Clothing: Naked X (wearing only) | `naked_shirt`, `naked_apron`, `naked_towel`, `naked_ribbon`, `naked_sheet`, `naked_jacket`, `naked_scarf`, `naked_overalls`, `naked_cape`, `naked_coat`, `naked_hoodie`, `naked_sweater` |

### Clothing Outfit Tags (4ノード)

服のベース名のみ (色は持たない — `extra` 欄や `TextConcat` で補う)。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Clothing: Tops | `shirt`, `t-shirt`, `dress_shirt`, `blouse`, `collared_shirt`, `polo_shirt`, `tank_top`, `camisole`, `crop_top`, `tube_top`, `off-shoulder_shirt`, `sleeveless_shirt`, `frilled_shirt`, `sweater`, `turtleneck`, `ribbed_sweater`, `sweater_vest`, `hoodie`, `cardigan`, `vest`, `waistcoat`, `jacket`, `blazer`, `coat`, `trench_coat`, `long_coat`, `winter_coat`, `raincoat`, `windbreaker` |
| Clothing: Bottoms | `skirt`, `miniskirt`, `long_skirt`, `pleated_skirt`, `high-waist_skirt`, `frilled_skirt`, `pencil_skirt`, `tutu`, `hakama_skirt`, `pants`, `jeans`, `denim_pants`, `leggings`, `harem_pants`, `wide-leg_pants`, `cargo_pants`, `track_pants`, `shorts`, `short_shorts`, `hot_pants`, `denim_shorts`, `bike_shorts`, `bloomers`, `overalls`, `suspenders` |
| Clothing: Dress & One-piece | `dress`, `sundress`, `long_dress`, `short_dress`, `evening_gown`, `ball_gown`, `wedding_dress`, `off-shoulder_dress`, `halter_dress`, `pinafore_dress`, `frilled_dress`, `kimono`, `yukata`, `furisode`, `hakama`, `qipao`, `china_dress`, `hanfu`, `ao_dai`, `sari`, `robe`, `jumpsuit`, `romper`, `leotard` |
| Clothing: Uniform & Costume | `school_uniform`, `serafuku`, `sailor_collar`, `sailor_dress`, `blazer_uniform`, `gym_uniform`, `business_suit`, `suit`, `pant_suit`, `skirt_suit`, `military_uniform`, `uniform`, `maid`, `waitress`, `nurse`, `police_uniform`, `cheerleader`, `miko`, `nun`, `kunoichi`, `witch`, `santa_costume`, `bunny_girl`, `playboy_bunny`, `ninja`, `armor`, `dougi`, `track_suit` |

### Clothing Underwear & Swimwear Tags (2ノード)

下着・水着系。キャラ設定で頻繁に使う。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Clothing: Underwear | `underwear`, `underwear_only`, `bra`, `sports_bra`, `strapless_bra`, `frilled_bra`, `lace_bra`, `panties`, `thong`, `side-tie_panties`, `string_panties`, `frilled_panties`, `lace_panties`, `boyshorts`, `boxers`, `briefs`, `boxer_briefs`, `lingerie`, `babydoll`, `chemise`, `teddy`, `bodystocking`, `garter_belt`, `garter_straps`, `corset`, `bustier`, `camisole_(underwear)`, `slip_(clothing)`, `fundoshi` |
| Clothing: Swimwear | `swimsuit`, `one-piece_swimsuit`, `school_swimsuit`, `competition_swimsuit`, `bikini`, `string_bikini`, `side-tie_bikini`, `front-tie_bikini`, `micro_bikini`, `sling_bikini`, `halterneck_bikini`, `frilled_bikini`, `polka_dot_bikini`, `striped_bikini`, `o-ring_bikini`, `bikini_top`, `bikini_bottom`, `swim_briefs`, `swim_trunks`, `rash_guard`, `wetsuit`, `highleg_swimsuit`, `thong_bikini` |

### Clothing Material & Pattern Tags (2ノード)

服の素材感とパターン。`see-through` 半透明系、`lace`/`frilled`/`leather`/`latex`、`striped`/`polka_dot`/`plaid` などキャラ衣装の質感指定。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Clothing: Material | `see-through`, `see-through_silhouette`, `transparent`, `wet_clothes`, `torn_clothes`, `lace`, `lace_trim`, `frilled`, `frills`, `ribbed`, `knit`, `mesh`, `fishnets`, `denim`, `leather`, `latex`, `rubber`, `vinyl`, `silk`, `satin`, `velvet`, `fur`, `fur_trim`, `wool`, `metallic`, `shiny_clothes` |
| Clothing: Pattern | `striped`, `vertical_stripes`, `horizontal_stripes`, `diagonal_stripes`, `striped_clothes`, `polka_dot`, `plaid`, `checkered`, `checkered_clothes`, `argyle`, `houndstooth`, `floral_print`, `leaf_print`, `star_print`, `heart_print`, `animal_print`, `leopard_print`, `zebra_print`, `camouflage`, `tie-dye`, `gradient_clothes`, `two-tone_clothes`, `multicolored_clothes`, `print_shirt`, `print_dress`, `print_skirt` |

### Clothing Legwear & Footwear Tags (2ノード)

靴下・タイツ系と靴系。色付き変種(`black_thighhighs` 等)はベース名 + 色合成で対応する想定で含めず。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Clothing: Legwear | `thighhighs`, `over-the-knee_socks`, `kneehighs`, `socks`, `ankle_socks`, `loose_socks`, `bobby_socks`, `tabi`, `stockings`, `pantyhose`, `leg_warmers`, `single_thighhigh`, `single_kneehigh`, `single_sock`, `zettai_ryouiki`, `no_socks`, `no_legwear` |
| Clothing: Footwear | `shoes`, `sneakers`, `loafers`, `mary_janes`, `high_heels`, `stiletto_heels`, `platform_heels`, `platform_footwear`, `wedge_heels`, `pumps`, `boots`, `ankle_boots`, `knee_boots`, `thigh_boots`, `cross-laced_footwear`, `combat_boots`, `rain_boots`, `sandals`, `flip-flops`, `geta`, `okobo`, `zouri`, `slippers`, `uwabaki`, `ballet_slippers`, `cleats` |

### Clothing Headwear & Eyewear Tags (2ノード)

頭にかぶる物 / メガネ系。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Clothing: Headwear | `hat`, `baseball_cap`, `beret`, `cap`, `peaked_cap`, `newsboy_cap`, `flat_cap`, `fedora`, `top_hat`, `bowler_hat`, `mob_cap`, `sun_hat`, `straw_hat`, `witch_hat`, `wizard_hat`, `santa_hat`, `party_hat`, `nurse_cap`, `police_hat`, `military_hat`, `helmet`, `bicycle_helmet`, `motorcycle_helmet`, `hood`, `hood_up`, `hood_down`, `hooded_jacket`, `hooded_cape`, `headphones`, `headset`, `earmuffs`, `headband`, `head_wreath`, `head_scarf`, `veil`, `crown`, `mini_crown`, `tiara`, `hat_ribbon`, `hat_bow`, `hat_flower`, `hat_feather` |
| Clothing: Eyewear | `glasses`, `sunglasses`, `round_eyewear`, `semi-rimless_eyewear`, `rimless_eyewear`, `over-rim_eyewear`, `under-rim_eyewear`, `goggles`, `goggles_on_head`, `swim_goggles`, `eyepatch`, `medical_eyepatch`, `monocle`, `pince-nez`, `blindfold` |

### Clothing Accessory Tags (3ノード)

手・首・その他小物。デフォルト全 False。

| ノード | 対象タグ |
| --- | --- |
| Clothing: Hand & Arm | `gloves`, `fingerless_gloves`, `half_gloves`, `elbow_gloves`, `mittens`, `single_glove`, `mismatched_gloves`, `arm_warmers`, `wrist_cuffs`, `wristband`, `sweatband`, `bracelet`, `bangle`, `watch`, `wristwatch`, `ring`, `armlet`, `armband`, `shoulder_armor`, `pauldron`, `vambraces`, `gauntlets` |
| Clothing: Neck | `necklace`, `pendant`, `choker`, `frilled_choker`, `collar`, `neck_ribbon`, `neck_bow`, `necktie`, `bowtie`, `neckerchief`, `ascot`, `scarf`, `muffler`, `shawl`, `cape`, `capelet` |
| Clothing: Accessory (other) | `earrings`, `single_earring`, `ear_piercing`, `stud_earrings`, `hoop_earrings`, `drop_earrings`, `belt`, `waist_cape`, `obi`, `sash`, `belt_pouch`, `apron`, `frilled_apron`, `waist_apron`, `bag`, `handbag`, `shoulder_bag`, `backpack`, `satchel`, `school_bag`, `umbrella`, `parasol`, `fan`, `folding_fan`, `lip_piercing`, `nose_piercing`, `navel_piercing`, `tongue_piercing` |

### Random Text Picker

`utility/text` カテゴリ。入力テキストを区切り文字で分割し、指定数だけランダムに抽出する。プロンプトのランダム選択用途。

- 入力
  - `text` (STRING, multiline): 対象テキスト
  - `delimiter` (STRING): 区切り文字。`\n` や `\t` などのエスケープシーケンスも使える
  - `count` (INT): 抽出数。要素数より大きければ全件返す
  - `seed` (INT): 乱数シード
- 出力
  - `text` (STRING): 抽出結果を同じ区切り文字で連結したテキスト

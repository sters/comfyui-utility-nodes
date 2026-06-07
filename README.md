# comfyui-utility-nodes

ComfyUI 向けのユーティリティ系カスタムノード集。プロンプト組み立て・タグ整合性チェック・キャラ/シーンプリセットなどを提供する。

## インストール

```sh
cd ComfyUI/custom_nodes
git clone https://github.com/sters/comfyui-utility-nodes.git
```

ComfyUI を再起動すると `utility/text` カテゴリにノードが追加される。

## ヘルプ

各ノードの詳細仕様 (入出力 / 対応タグ / mutex 挙動など) は **ノード上の help (?) ボタン** から ComfyUI 内でそのまま読める ([Help Page Feature](https://docs.comfy.org/custom-nodes/help_page))。`web/docs/<ClassName>.md` の英語ドキュメントが表示される。

## ノード分類

| カテゴリ | 用途 | 代表ノード |
| --- | --- | --- |
| 汎用テキスト | プロンプト合成・連結・ランダム抽出 | `Prompt Combinator`, `List Shuffle`, `Text Concat`, `Random Text Picker` |
| モデル固有 | Pony Diffusion 用テンプレ | `Meta: Pony` |
| Bad / Negative | Danbooru の `bad_*` / `extra_*` 系をパーツ別に分割 | `Bad: General` / `Bad: Head & Face` / `Bad: Body` / `Bad: Limbs` / `Bad: NSFW` |
| 構図 | アングル / フレーミング / クロップ / フォーカス | `Composition: Angle` ほか |
| 髪 / 顔 / 体 | キャラ造形タグをパーツ別に | `Hair: ...`, `Face: ...`, `Body: ...`, `Breasts: ...` ほか |
| 服飾 | 種類 / 素材 / フィット / 状態 / 着崩し | `Clothing: ...` ほか |
| Meta / Scene | 人数指定・品質・背景・照明・天気 | `Meta: ...`, `Scene: ...` |
| NSFW | 行為 / 体位 / 状態 / ソロ / 玩具 / 拘束 | `NSFW Act: ...`, `NSFW: Position`, `NSFW State: ...` ほか |
| プリセット | 1クリックでキャラ / 性格 / シーン一式 | `Character Preset`, `Personality Preset`, `NSFW Scene Preset` |
| 統合 | 全タグノードの矛盾解決と最終 prompt 生成 | `Tags: Merge & Validate` |

## 推奨ワークフロー

タグ系ノードはすべて 2 出力:

- `prompt` (STRING): 選択タグを `separator` で連結した文字列。手軽に `Text Concat` などへ
- `bundle` (`CUUN_TAGS`): 構造化データ。category / layer / mutex 情報を保持

整合性をきっちり取りたい場合は **全タグノードの `bundle` を `Tags: Merge & Validate` に集約** する。`nodes/tags/_conflicts.py` のルール (`MUTEX_GROUPS` と `TAG_CONFLICTS`) に従って、`nude` と clothing、`topless` と bras、`barefoot` と legwear などが自動で解決される。`warnings` 出力で drop 内容を確認できる。

タグノード共通の `preset` combo (`custom` / `all_on` / `all_off` / `invert`) で、50タグ超のノードでも一括 on/off やスポット除外がワンクリックで切り替えられる。

## 開発

```sh
make sync     # 依存導入
make check    # lint + fmt-check + typecheck + pytest
make fix      # ruff --fix + format
```

Python 3.10+ / mypy strict / ruff。詳細は `CLAUDE.md` を参照。

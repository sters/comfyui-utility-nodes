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

### Random Text Picker

`utility/text` カテゴリ。入力テキストを区切り文字で分割し、指定数だけランダムに抽出する。プロンプトのランダム選択用途。

- 入力
  - `text` (STRING, multiline): 対象テキスト
  - `delimiter` (STRING): 区切り文字。`\n` や `\t` などのエスケープシーケンスも使える
  - `count` (INT): 抽出数。要素数より大きければ全件返す
  - `seed` (INT): 乱数シード
- 出力
  - `text` (STRING): 抽出結果を同じ区切り文字で連結したテキスト

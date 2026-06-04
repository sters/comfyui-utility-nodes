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

### Random Text Picker

`utility/text` カテゴリ。入力テキストを区切り文字で分割し、指定数だけランダムに抽出する。プロンプトのランダム選択用途。

- 入力
  - `text` (STRING, multiline): 対象テキスト
  - `delimiter` (STRING): 区切り文字。`\n` や `\t` などのエスケープシーケンスも使える
  - `count` (INT): 抽出数。要素数より大きければ全件返す
  - `seed` (INT): 乱数シード
- 出力
  - `text` (STRING): 抽出結果を同じ区切り文字で連結したテキスト

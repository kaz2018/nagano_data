# CLAUDE.md — 開発規約

このプロジェクトでの作業時に守るべき規約をまとめています。

## Python の実行

Python スクリプトは必ず `uv` 経由で実行すること。

```bash
# 正しい
uv run python3 script.py
uv run python3 -c "..."

# 禁止
.venv/bin/python3 script.py
python3 script.py
```

## データ確認・正解導出

レッスンの正解をコードで確認するときも `uv run` を使う。
CSVファイルは `utf-8-sig` エンコーディングで読み込む（BOM付き）。

```python
import csv
with open('kids/data/lesson02_cities_2025.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))
```

## データカード UIパターン

各レッスンの説明セクション（ポイントボックスの直後）に、そのレッスンで使うデータを紹介するカードを置く。

### ルール

- **答えになる数字は書かない**（例：「35の村」「9年分」はNG）
- データの**種類**（村か市かなど）と**特徴**を文章で説明する
- 「前のレッスンとはちがうよ！」という一言を添える（レッスン2以降）
- カードの色・スプレッドシートを開くボタンの色をレッスンごとに統一する

### レッスンごとの色とカード内容

| レッスン | 色 | カード説明文（方針） |
|---------|----|--------------------|
| L1 | 緑（green-600） | 村のデータ。何年分・何村かはスプレッドシートで確かめてもらう |
| L2 | 青（blue-600） | 市のデータ。L1の村との違いを強調 |
| L3 | 紫（purple-600） | 6つの村の複数年データ。L2との違いを強調 |
| L4 | オレンジ（orange-500） | 全市町村のデータ。L3との違いを強調 |

### HTMLパターン例（L1・緑）

```html
<div class="bg-green-600 text-white rounded-xl p-4 text-sm">
  <p class="font-bold mb-1">📂 レッスン1のデータ</p>
  <p class="text-green-100 leading-relaxed">長野県の<strong class="text-white">村</strong>の人口データを集めたよ。何年ぶんあるかな？村はいくつあるかな？スプレッドシートをひらいて確かめてみよう！</p>
</div>
```

スプレッドシートを開くボタンも同じ色系統にすること（例：`bg-green-500 hover:bg-green-600`）。

## やってみよう（答え合わせ）UIパターン

子ども向けレッスンの「やってみよう」セクションのルール：

- **1問ごとに「答え合わせ」ボタンを設ける**（全問まとめて確認するボタンは不要）
- ボタンを押すと、その問の直下に結果（⭕ せいかい！ / ❌ もう一かい！）を表示する
- 自由記述・理由を問う問題は正誤判定せず、「こたえのれいを見る」ボタンで模範解答を表示する
- 結果は `hidden` クラスの `<span>` または `<div>` に書き込み、ボタン押下で表示する

### 正解一覧（各レッスン）

| レッスン | Q1 | Q2 | Q3 | Q4 |
|---------|----|----|----|----|
| L1 | 35村 | 9年分 | 南箕輪村・松川村・白馬村（順不同） | — |
| L2 | 長野市 | 松本市 | 343099人 | — |
| L3 | 白馬村 | 445人 | 自由記述（コロナ影響）→ 模範解答表示 | — |
| L4 | 長野市・361045人 | 平谷村・368人 | 麻績村65番め・筑北村55番め | 360677人 |
| L5 | 長野市・14865人へった | 6市町村 | 御代田町・1288人ふえた | — |
| L6 | 天龍村 | 8.5%ふえた（±0.2許容） | 5.9%ふえた（±0.2許容） | — |
| L7 | 女・42244人多い | 62市町村 | 川上村は男が多い | — |
| L8 | 1984926人 | 18.2%（±0.2許容） | 10市 | — |
| L9 | 346180人（長野市2033年予測） | 668人（天龍村2033年予測） | 自由記述 → 模範解答表示 | — |
| L10 | 自由探究（正誤なし） | — | — | — |

---

## 大人コース

### 基本方針

- ディレクトリ: `adults/`
- **文章レベル**: 中学2〜3年生が読めること。短文・改行多め・平易な日本語
- **テーマカラー**: インディゴ（`indigo-600` / `indigo-900`）
- **技術スタック**: Tailwind CSS + Alpine.js（子どもコースとは異なるモダンデザイン）

### ディレクトリ構成

```
adults/
  index.html          # コーストップ（レッスン一覧）
  lesson01/index.html
  lesson02/index.html  # 以降同様
  data/
    lesson01_dirty.csv  # 神Excel風サンプル
    lesson01_clean.csv  # きれいなデータサンプル
```

### デザイン規約

- **ヘッダー**: sticky + `backdrop-blur-sm` + `bg-white/90`
- **ヒーロー**: `bg-gradient-to-r from-indigo-600 to-violet-600`（レッスンページ）/ `from-indigo-900 to-slate-900`（indexページ）
- **カード**: `bg-white rounded-2xl border border-slate-200`（shadowより borderを基本に）
- **成功色**: `emerald-600`
- **エラー色**: `red-500`

### Alpine.js 実装パターン

コンポーネント関数を `<head>` 内の `<script>` に定義し、Alpine は `defer` で読み込む。

```html
<head>
  <script>
    function lesson1() {
      return { /* state & methods */ };
    }
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
  <style>
    [x-cloak] { display: none !important; }
  </style>
</head>
<body x-data="lesson1()">
```

`x-cloak` は `x-show` で初期状態が非表示になる要素にのみ付ける（body全体には付けない）。

### やってみよう（大人コース）UIパターン

子どもコースと異なり Alpine.js で状態管理する：

- `x-model` でラジオ・テキスト入力をバインド
- 未入力時はボタンを `disabled` + グレーアウト（`:disabled` + `:class`）
- 結果は `x-show` + `x-transition` でスライドイン表示
- 正解: `bg-emerald-50 border-emerald-200 text-emerald-800`
- 不正解: `bg-red-50 border-red-200 text-red-700`

```html
<div x-show="result !== null" x-cloak
  x-transition:enter="transition ease-out duration-200"
  x-transition:enter-start="opacity-0 translate-y-1"
  x-transition:enter-end="opacity-100 translate-y-0"
  :class="result === 'ok' ? 'bg-emerald-50 border-emerald-200 text-emerald-800' : 'bg-red-50 border-red-200 text-red-700'"
  class="border rounded-xl p-3 text-sm font-bold">
```

### スプレッドシートの権限・コピー案内

- すべてのスプレッドシートは**閲覧権限のみ**（編集不可）
- スプレッドシートを開くボタンの**直下**に、以下の文言を必ず記載する

```html
<p class="text-xs text-indigo-600 font-bold">元のデータは閲覧のみです。「ファイル → コピーを作成」で自分のドライブにコピーしてから使ってください。</p>
```

### スプレッドシート URL（大人コース）

| レッスン | 種別 | URL |
|---------|------|-----|
| L1 | 神Excel版（dirty） | https://docs.google.com/spreadsheets/d/1vlR7DHRlOCR2LGxL0JLTmF_1WNvq6ZVPwRLtkTZMY7g/edit?gid=2032434459#gid=2032434459 |
| L1 | きれいなデータ（clean） | https://docs.google.com/spreadsheets/d/1Lfe_jTcJ_Od_R5XO3Yzba0annsaHAHFwpHESYYzvHmY/edit?gid=1772913169#gid=1772913169 |
| L2 | 人口データ（2023〜2025年・77市町村） | https://docs.google.com/spreadsheets/d/1FWIY49b3a9GZJrW6p003DpAvHyZjLGOZDzP5aS7DEPg/edit?gid=294120410#gid=294120410 |

### 正解一覧（大人コース）

| レッスン | Q1 | Q2 | Q3 |
|---------|----|----|-----|
| L1 | ②できない（全角数字・メモが混入しているから） | 4個 | 1件 |
| L2 | ②大量のデータをすばやく集計できる | ②別々の行として集計される | ③名前の代わりにIDで管理する |

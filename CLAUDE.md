# CLAUDE.md — 開発規約

このプロジェクトでの作業時に守るべき規約をまとめています。

## アナリティクス

HTML を新規作成するときは、必ず `</head>` の直前に以下の2つのスクリプトを記載すること。

```html
  <script defer src="https://cloud.umami.is/script.js" data-website-id="a0c03729-de7a-4bde-af6e-9919a23b24e7"></script>
</head>
```

- **Umami**: ユーザー行動（PV・レッスン別アクセス・リファラー）の把握
- **Cloudflare Analytics**: 実際のリクエスト数の把握（広告ブロッカーに左右されない。Workers 経由で自動収集のため HTML への追記は不要）

---

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

## 子どもコース ストーリー設計

### キャラクター設定

| キャラクター | 画像ファイル | 説明 |
|---|---|---|
| **でい太** | `kids/images/main_character.png` | 主人公。元気な男の子、スキー好き |
| **ポン太** | `kids/images/assistant.png` | ホンドタヌキ。でい太のアシスタント。関係ないことをよく呟く |
| **ものしり仙人** | `kids/images/harmit.png` | データに詳しい物知り老人。自然を大切にしたい |

### 会話形式UIパターン

各レッスンのタイトル直後（「このレッスンでわかること」の直前）に、でい太・ポン太の会話吹き出しを置く。

**でい太（左）:**
```html
<div class="flex items-start gap-3">
  <img src="../images/main_character.png" alt="でい太" class="shrink-0 w-10 h-10 rounded-full object-cover shadow" />
  <div>
    <p class="text-xs font-bold text-amber-600 mb-1">でい太</p>
    <div class="bg-amber-50 border border-amber-200 rounded-2xl rounded-tl-none px-4 py-3 text-sm text-gray-700 leading-relaxed">
      「セリフ」
    </div>
  </div>
</div>
```

**ポン太（左・でい太の次に置く）:**
```html
<div class="flex items-start gap-3">
  <img src="../images/assistant.png" alt="ポン太" class="shrink-0 w-10 h-10 rounded-full object-cover shadow" />
  <div>
    <p class="text-xs font-bold text-stone-500 mb-1">ポン太</p>
    <div class="bg-stone-50 border border-stone-200 rounded-2xl rounded-tl-none px-4 py-3 text-sm text-gray-700 leading-relaxed">
      「関係ないひとこと」
    </div>
  </div>
</div>
```

**ものしり仙人（右・必要なときのみ）:**
```html
<div class="flex items-start gap-3 flex-row-reverse">
  <img src="../images/harmit.png" alt="ものしり仙人" class="shrink-0 w-10 h-10 rounded-full object-cover shadow" />
  <div class="text-right">
    <p class="text-xs font-bold text-blue-600 mb-1">ものしり仙人</p>
    <div class="bg-blue-50 border border-blue-200 rounded-2xl rounded-tr-none px-4 py-3 text-sm text-gray-700 leading-relaxed text-left">
      「セリフ」
    </div>
  </div>
</div>
```

**まとめてセクションに入れる:**
```html
<section class="space-y-3">
  <!-- でい太 → ポン太 → (必要なら でい太 or ものしり仙人) -->
</section>
```

L10（最終章）のみ でい太→ポン太→でい太→ものしり仙人 の4者構成。背景は `bg-amber-50 border-2 border-amber-300 rounded-2xl` のボックスで囲む。

### ミッション

麻績村（おみむら）の人口が2017〜2025年で **−16.1%（2756→2311人、−445人）** 減っている謎を解く。
周辺の筑北村（−17.5%）も同様の傾向。

でい太のおじさんが麻績村在住という設定で、「なぜ村が縮んでいるのか」をデータで調べるのが全体の動機。

### チャプター構成（kids/index.html）

| 章 | レッスン | サブタイトル |
|---|---|---|
| 第1章：はじめの一歩 | L1〜L2 | データを読んで、長野県を知ろう |
| 第2章：変化を追え | L3〜L4 | 人口はどう動いた？ |
| 第3章：数字で深掘り | L5〜L7 | 計算で本当のことがわかる |
| 第4章：全体と未来 | L8〜L9 | 長野全体と、この先を見通す |
| 最終章：謎を解け！ | L10 | 自分だけの発見を発表しよう |

### 各レッスンのでい太のセリフ方針とポン太のひとこと

| L | でい太のセリフの焦点 | ポン太のひとこと |
|---|---|---|
| L1 | 麻績村を初めて紹介し、データを見ようと誘う | 「お腹すいたな。」 |
| L2 | 大きな市と小さな村の人口差を実感させる | 「スイカって野菜なんだよ。これマメな。」 |
| L3 | 「村から人がいなくなった」を折れ線グラフで確かめる | 「山の紅葉ってきれいだよね。今の季節は何色かな。」 |
| L4 | 麻績村が77市町村のランキングで何番目か調べる | 「77って中途半端な数だね。80とかじゃないんだ。」 |
| L5 | 麻績村は8年で445人減ったと数字で実感させる | 「ひき算か。オレ算数苦手なんだよね。」 |
| L6 | %で比べることで−16%の深刻さを伝える | 「パーセントって、セールで30%オフとかに使うやつ？」 |
| L7 | 男女どちらが多く減っているか調べる | 「オレ、オスのタヌキだよ。ちなみに。」 |
| L8 | 長野県全体でも同じ傾向かを確認する | 「そばは何もつけずに食うのが通。」 |
| L9 | このまま続くと2033年は何人になるか予測する | 「ハドリーは神。」 |
| L10 | 最終局面として自分なりの答えを出すよう促す | 「おやつまだかな。」 |

---

## やってみよう（答え合わせ）UIパターン

子ども向けレッスンの「やってみよう」セクションのルール：

- **入力形式ではなく選択形式（ラジオボタン4択）を使う**
- **1問ごとに「答え合わせ」ボタンを設ける**（全問まとめて確認するボタンは不要）
- ボタンを押すと、その問の直下に結果（⭕ せいかい！ / ❌ もう一かい！）を表示する
- 自由記述・理由を問う問題は選択肢なし・テキストエリアなし。「こたえのれいを見る」ボタンのみ設置し模範解答を表示する
- 結果は `hidden` クラスの `<span>` に書き込み、ボタン押下で表示する

### ラジオボタン HTMLパターン

```html
<div class="space-y-1 mt-2">
  <label class="flex items-center gap-2 cursor-pointer">
    <input type="radio" name="q1" value="A" class="accent-amber-500" />
    <span class="text-sm text-gray-700">選択肢A</span>
  </label>
  <label class="flex items-center gap-2 cursor-pointer">
    <input type="radio" name="q1" value="B" class="accent-amber-500" />
    <span class="text-sm text-gray-700">選択肢B（正解）</span>
  </label>
</div>
<button onclick="checkQ1()" class="mt-2 bg-amber-400 hover:bg-amber-500 text-white font-bold px-4 py-2 rounded-lg text-sm transition-colors">
  答え合わせ
</button>
<span id="result1" class="text-sm font-bold hidden"></span>
```

### JS パターン

```js
function showResult(id, ok) {
  const r = document.getElementById(id);
  r.textContent = ok ? '⭕ せいかい！' : '❌ もう一かい！';
  r.className = 'text-sm font-bold ' + (ok ? 'text-green-600' : 'text-red-500');
  r.classList.remove('hidden');
}
function checkQ1() {
  const el = document.querySelector('input[name="q1"]:checked');
  if (!el) return;
  showResult('result1', el.value === '正解の値');
}
```

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
| L1 | 生データ（長野県公式・2025年1月） | https://docs.google.com/spreadsheets/d/16-pJmYMado9aECy-5I9PQQLbAVVjp-xF/edit?gid=1621259894#gid=1621259894 |
| L1 | 神Excel版（dirty） | https://docs.google.com/spreadsheets/d/1vlR7DHRlOCR2LGxL0JLTmF_1WNvq6ZVPwRLtkTZMY7g/edit?gid=2032434459#gid=2032434459 |
| L1 | きれいなデータ（clean） | https://docs.google.com/spreadsheets/d/1Lfe_jTcJ_Od_R5XO3Yzba0annsaHAHFwpHESYYzvHmY/edit?gid=1772913169#gid=1772913169 |
| L2 | 人口データ（2023〜2025年・77市町村） | https://docs.google.com/spreadsheets/d/1FWIY49b3a9GZJrW6p003DpAvHyZjLGOZDzP5aS7DEPg/edit?gid=294120410#gid=294120410 |

### 正解一覧（大人コース）

| レッスン | Q1 | Q2 | Q3 |
|---------|----|----|-----|
| L1 | ②できない（全角数字・メモが混入しているから） | 4個 | 1件 |
| L2 | ②大量のデータをすばやく集計できる | ②別々の行として集計される | ③名前の代わりにIDで管理する |

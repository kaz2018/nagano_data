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

## サイト構成とフォルダ規約

**本番**: https://nagano-data.willbefree-k-m.workers.dev/ （Cloudflare Workers の静的アセット配信）

サイトは**テーマ**で分かれている。年齢では分けない（トップページの入り口もテーマ単位）。

```
nagano_data/
├── index.html              # トップ（テーマの入り口）
├── 404.html                # 見つからないページの案内
├── _redirects              # 旧URLの301転送（Cloudflare）
├── assets/images/          # トップページなど、サイト共通の画像
├── kids/                   # こどもコース（小学生〜）
│   ├── index.html          #   3テーマのハブ
│   ├── images/             #   3テーマ共通の画像（でい太・ポン太・仙人ほか）
│   ├── js/                 #   3テーマ共通の JS
│   ├── nagano/             #   🏔 長野県編
│   │   ├── index.html
│   │   ├── data/           #     このコース専用データ
│   │   └── lesson01〜10/
│   ├── penguins/           #   🐧 ペンギン研究所
│   │   ├── index.html
│   │   ├── data/
│   │   └── lesson01〜08/
│   └── extra/              #   💡 番外編
│       ├── index.html
│       └── trash / youtube / instagram / games / freedom/
├── adults/                 # しごととデータ（中学生〜大人）
└── contact/
```

### コース追加の型

新しいコースは `kids/<コース名>/` に作り、必ずこの形にする。

- `index.html` — コースの入り口（必須）
- `data/` — そのコース専用のデータ。共通ディレクトリには置かない
- `lessonNN/` — **順序が内容に固有な**連続レッスンだけ連番にする
- `<slug>/` — **順序が編集判断で変わる**単発コンテンツはスラッグ名（連番は禁止）

番外編が `extra01` ではなくスラッグ（`trash` / `youtube` …）なのはこのため。
表示順は `kids/extra/index.html` の中だけに存在し、並べ替えてもフォルダ名は変わらない。

共通アセットは `kids/images/` と `kids/js/` の2つだけ。コース固有の画像・データをここに置かない。

### 番外編の並び順

| # | スラッグ | タイトル | 色 |
|---|---------|---------|----|
| 1 | `trash` | 信州ごみ減らし大作戦！ | teal |
| 2 | `youtube` | YouTubeのわな | red |
| 3 | `instagram` | インスタのわな | pink |
| 4 | `games` | ゲームのわな | indigo |
| 5 | `freedom` | ほんとうの自由ってなに？ | sky |

**データを読む話 → 3つの「わな」 → 自由とは何かを考える**、という流れ。
追加するときは、この流れのどこに入るかを考えて並べる。

### 共通ヘッダー

こどもコースの全レッスンページのヘッダーに、3テーマへのナビを入れる。現在地だけ色つきのピルにする。

```html
<header class="bg-white shadow-sm">
  <div class="max-w-3xl mx-auto px-6 pt-3 pb-2">
    <div class="flex items-center gap-3">
      <!-- 既存の「← レッスン一らんへ」＋レッスン番号 -->
    </div>
    <nav class="flex gap-1.5 mt-2 text-xs font-bold">
      <a href="../../nagano/index.html" class="px-2.5 py-1 rounded-full bg-green-100 text-green-700">🏔 長野県編</a>
      <a href="../../penguins/index.html" class="px-2.5 py-1 rounded-full text-gray-400 hover:bg-gray-100">🐧 ペンギン研究所</a>
      <a href="../../extra/index.html" class="px-2.5 py-1 rounded-full text-gray-400 hover:bg-gray-100">💡 番外編</a>
    </nav>
  </div>
</header>
```

現在地の色：長野県編 `bg-green-100 text-green-700` ／ ペンギン研究所 `bg-sky-100 text-sky-700` ／ 番外編 `bg-red-100 text-red-600`

### URL を変えるとき

本番は **Cloudflare Workers の静的アセット配信**。サーバ側リダイレクトが使えるので、
公開済みのページを移動したら **ルートの `_redirects` に301を追記する**。HTMLのスタブは作らない。

```
# [旧パス] [新パス] [ステータス]
/kids/lesson01   /kids/nagano/lesson01/   301
/kids/lesson01/* /kids/nagano/lesson01/   301
```

- 末尾スラッシュなしと配下（`*`）の2行を書く。片方だけだと取りこぼす
- パスは**ルートからの絶対パス**（`/kids/...`）で書く
- 上限は静的2,000件・動的（`*` を含む）100件
- 仕様: https://developers.cloudflare.com/workers/static-assets/redirects/

**注意**: `_redirects` が効くのは静的アセットとして返るリクエストだけ。
Worker のコードが処理したレスポンスには適用されない。

存在しないパスは `404.html` が受ける。ただし Workers Static Assets では
**wrangler 設定の `not_found_handling: "404-page"` が必要**（この設定ファイルは本リポジトリ外）。
未設定だと素っ気ない404が返るだけで、`_redirects` による転送自体には影響しない。

---

## ページの動作確認

子どもコースのページは `fetch()` でCSVを読むため、**HTMLファイルを直接ひらく（`file://`）と動かない**。
ブラウザのCORS制限で読み込みがブロックされ、数値が `—` のまま・表が空になる。

必ずローカルサーバ経由で確認すること。

```bash
uv run python3 -m http.server 8000
```

`http://localhost:8000/kids/penguins/lesson01/index.html` のように開く。

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

### 外部データの取得とサンドボックス環境
- CLI の実行環境（サンドボックス）は外部ネットワークが遮断されているため、Python スクリプト内でのダウンロード処理は `URLError` / `socket.gaierror` で失敗する。
- 外部データが必要な場合は、スクリプト実行前に `curl` 等で生ファイル（`*_raw.csv`）をローカルに落としておき、スクリプトはローカルファイルを読み込む設計にすること。


## データ確認・正解導出

レッスンの正解をコードで確認するときも `uv run` を使う。
CSVファイルは `utf-8-sig` エンコーディングで読み込む（BOM付き）。

```python
import csv
with open('kids/nagano/data/lesson02_cities_2025.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))
```

## データカード UIパターン

各レッスンの説明セクション（ポイントボックスの直後）に、そのレッスンで使うデータを紹介するカードを置く。

データカードの直後には、**ページ内のインタラクティブなデータ可視化**を置く。
子どもコースでは、この可視化を見れば「やってみよう」に答えられるようにする。
スプレッドシートは必須導線ではなく、**やってみたい人向けの発展セクション**としてページ下部（やってみようの後、ナビゲーションの前）に置く。

### ルール

- **答えになる数字は書かない**（例：「35の村」「9年分」はNG）
- データの**種類**（村か市かなど）と**特徴**を文章で説明する
- 「前のレッスンとはちがうよ！」という一言を添える（レッスン2以降）
- カードの色・可視化の強調色・発展用スプレッドシートボタンの色をレッスンごとに統一する
- 学習目的に合った形を選ぶ（例：比較＝棒グラフ、推移＝折れ線、順位や一覧＝表）
- 表を使う場合は `<table>` を使い、列見出しタップで並び替えできるようにする
- 最大値や注目点は、そのレッスンの色系統でハイライトする

### レッスンごとの色とカード内容

| レッスン | 色 | カード説明文（方針） |
|---------|----|--------------------|
| L1 | 緑（green-600） | 村のデータ。何年分・何村かはページ内の表を見て確かめてもらう |
| L2 | 青（blue-600） | 市のデータ。L1の村との違いを強調 |
| L3 | 紫（purple-600） | 6つの村の複数年データ。L2との違いを強調 |
| L4 | オレンジ（orange-500） | 全市町村のデータ。L3との違いを強調 |

### HTMLパターン例（L1・緑）

```html
<div class="bg-green-600 text-white rounded-xl p-4 text-sm">
  <p class="font-bold mb-1">📂 レッスン1のデータ</p>
  <p class="text-green-100 leading-relaxed">長野県の<strong class="text-white">村</strong>の人口データを集めたよ。何年ぶんあるかな？村はいくつあるかな？この下の表を見て確かめてみよう！</p>
</div>
```

この直後に、そのレッスンの色でそろえたデータ可視化セクションを置くこと。
発展用のスプレッドシートボタンも同じ色系統にすること（例：`bg-green-500 hover:bg-green-600`）。

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

### チャプター構成（kids/nagano/index.html）

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

## 子どもコース・ペンギン研究所

### 基本方針
- **配置**: `kids/penguins/` 配下（こどもコースの一部）
- **body背景**: `bg-sky-50`（全ページ共通）
- **登場人物**: でい太・ポン太・ものしり仙人（既存キャラ3名のみ。新キャラは作らない）
- **使用データと出典**: [palmerpenguins](https://allisonhorst.github.io/palmerpenguins/)（Horst, Hill & Gorman, 2020／CC0）。南極パーマー基地のKristen Gorman博士らが2007〜2009年に収集。全ページのナビゲーション直前に出典セクションを設ける。
- **欠損値ルール**: 欠損値は `0` や「不明」で埋めず、空欄のまま保持する（後のレッスンの教材となるため）。

### レッスンごとのテーマ色

| レッスン | テーマ色 | 主な用途 |
|---|---|---|
| P1 | cyan (`cyan-600` / `cyan-500` / `cyan-100`) | バッジ・データカード・表のハイライト・発展ボタン |
| P2 | blue (`blue-600` / `blue-500` / `blue-100`) | 同上（棒グラフのバー色も） |
| P3 | indigo (`indigo-600` / `indigo-500` / `indigo-100`) | 同上（ヒストグラムの基調色） |
| P4 | violet (`violet-600` / `violet-500` / `violet-100`) | 同上（散布図の向きの線も） |
| P5 | emerald (`emerald-600` / `emerald-500` / `emerald-100`) | 同上（クロス集計表・棒グラフも） |
| P6 | rose (`rose-600` / `rose-500` / `rose-100`) | 同上 |
| P7 | slate (`slate-600` / `slate-200` / `slate-100`) | 欠損値のレッスン。ひかえめな色で「データが欠けている」を表す |
| P8 | orange (`orange-600` / `orange-500` / `orange-100`) | グラフのわな（シンプソンのパラドックス）。注意をうながす色 |

※答え合わせボタンは全レッスン共通で amber（`bg-amber-400 hover:bg-amber-500`）。

### しゅるいの色（P4以降・チャート内で固定）

テーマ色はページの「外わく」の色。**チャートの中でしゅるいを塗り分ける色は、レッスンをまたいで固定**する。
`kids/js/kids-visuals.js` の `KIDS_SPECIES_COLORS` が唯一の定義。

| しゅるい | 色 |
|---|---|
| アデリーペンギン | `#4f46e5`（indigo-600） |
| ヒゲペンギン | `#db2777`（pink-600） |
| ジェンツーペンギン | `#0891b2`（cyan-600） |

P6 のオス／メスだけは別系統：オス `#0d9488`（teal-600）／メス `#e11d48`（rose-600）。

**Tailwind の色クラスは JS で生成した要素には効かない**（CDN版はHTMLを読んだ時点でしかクラスを作らない）。
JS で描く SVG や棒グラフの色は、必ず `style="background-color: #..."` / `fill="#..."` のように16進で指定すること。

### 散布図（ちらばりグラフ）

`kids-visuals.js` の `renderKidsScatter()` を使う。SVG で描画し、点のタップで読み取り欄を更新できる。
`trend: 'all' | 'each'` で最小二乗法の「だいたいの向きの線」を重ねられる。

### 正解一覧（P1〜P3）

| レッスン | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P1 | 344ひき | 3しゅるい | 1ぴきのペンギン | アデリーペンギン |
| P2 | ジェンツーペンギン | 約5,076g | 約30g（ほとんど同じ） | 約1,375g |
| P3 | 6,300g | 2,700g | アデリーの中でいちばん重い子 | 自由記述 → 模範解答表示 |
| P4 | 重くなっている（右上がり） | 231mm | ジェンツーペンギン | 自由記述 → 模範解答表示 |
| P5 | ドリーム島 | どの島にもそろっていない | ジェンツーがビスコー島にしかいないから | 自由記述 → 模範解答表示 |
| P6 | どのしゅるいもオス | ジェンツーペンギン（差805g） | ジェンツーのメス | 自由記述 → 模範解答表示 |
| P7 | 11ぴき | 2ひき | 4,177g | 自由記述 → 模範解答表示 |
| P8 | 薄くなっている（右下がり） | 3しゅるいとも右上がり | ジェンツーが右下にかたまっているから | 自由記述 → 模範解答表示 |

### P4〜P6 で使う主な数

| 内容 | 値 |
|---|---|
| ひれの長さ（P4） | 最小172mm（アデリー）／最大231mm（ジェンツー・体重5,650g） |
| いちばん重い子（P4） | 6,300g（ジェンツー・ひれ221mm） |
| 島×しゅるい（P5） | ビスコー：アデリー44・ジェンツー124／ドリーム：アデリー56・ヒゲ68／トーゲルセン：アデリー52 |
| 島別へいきん体重・全種（P5） | ビスコー4,716g／ドリーム3,713g／トーゲルセン3,706g（差1,010g） |
| 島別へいきん体重・アデリーのみ（P5） | ビスコー3,710g／ドリーム3,688g／トーゲルセン3,706g（差22g） |
| オス／メスのへいきん体重（P6） | アデリー4,043／3,369（差674）・ヒゲ3,939／3,527（差412）・ジェンツー5,485／4,680（差805） |

### P7・P8 で使う主な数

**P7（欠損値）**: `penguins_ja.csv` を新規ファイルなしでそのまま読む（空らん自体が教材）。

| 内容 | 値 |
|---|---|
| 列ごとの空らん | せいべつ11／くちばしの長さ・厚さ・ひれ・体重 各2／しゅるい・島・年 0 |
| 空らんがある行 | 11行（うち2行は測定値がぜんぶ空、9行はせいべつのみ空） |
| 正しいへいきん体重 | 1,437,000g ÷ 342ひき = 4,202g |
| 0でうめた場合 | 1,437,000g ÷ 344ひき = 4,177g（25g 軽くずれる） |

**P8（シンプソンのパラドックス）**: `lesson08_bill.csv`（342行）。このレッスンの核心は相関の符号。

| 範囲 | 相関 | グラフの向き |
|---|---|---|
| 342ひき全体 | −0.24 | 右下がり |
| アデリーの中 | +0.39 | 右上がり |
| ヒゲの中 | +0.65 | 右上がり |
| ジェンツーの中 | +0.64 | 右上がり |

この符号の逆転は `penguins.py` の assert で常時検証している（崩れたらデータ生成時にエラーで落ちる）。
ページ側は `renderKidsScatter()` を `trend: 'all'`（1色・全体）と `trend: 'each'`（しゅるい別）で切りかえ、
向きが逆転するのを目で見せるのがクライマックス。P8 は最終回なので、会話は
でい太→ポン太→でい太→ものしり仙人の4者構成。

---

## しごととデータ（旧・大人コース）

### 基本方針

- ディレクトリ: `adults/`（表示名は「しごととデータ」。ディレクトリ名は旧URL維持のため変更しない）
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

### やってみよう（しごととデータ）UIパターン

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

### スプレッドシート URL（しごととデータ）

| レッスン | 種別 | URL |
|---------|------|-----|
| L1 | 生データ（長野県公式・2025年1月） | https://docs.google.com/spreadsheets/d/16-pJmYMado9aECy-5I9PQQLbAVVjp-xF/edit?gid=1621259894#gid=1621259894 |
| L1 | 神Excel版（dirty） | https://docs.google.com/spreadsheets/d/1vlR7DHRlOCR2LGxL0JLTmF_1WNvq6ZVPwRLtkTZMY7g/edit?gid=2032434459#gid=2032434459 |
| L1 | きれいなデータ（clean） | https://docs.google.com/spreadsheets/d/1Lfe_jTcJ_Od_R5XO3Yzba0annsaHAHFwpHESYYzvHmY/edit?gid=1772913169#gid=1772913169 |
| L2 | 人口データ（2023〜2025年・77市町村） | https://docs.google.com/spreadsheets/d/1FWIY49b3a9GZJrW6p003DpAvHyZjLGOZDzP5aS7DEPg/edit?gid=294120410#gid=294120410 |

### 正解一覧（しごととデータ）

| レッスン | Q1 | Q2 | Q3 |
|---------|----|----|-----|
| L1 | ②できない（全角数字・メモが混入しているから） | 4個 | 1件 |
| L2 | ②6,000円（3,000円×2時間） | ③216,000円（72,000円×3人） | ②入力する人と、あとで困る人が違うから |

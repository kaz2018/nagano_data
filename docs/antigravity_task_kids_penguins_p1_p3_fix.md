# 修正依頼：ペンギン研究所 第1章（kids/penguins/ P1〜P3）レビュー指摘の反映

## 概要

`docs/antigravity_task_kids_penguins_p1_p3.md` で実装した P1〜P3 のレビュー結果にもとづく修正依頼。
データ生成（`penguins.py` と4つのCSV）は**原典と全セル照合済みで問題なし**。修正対象は **HTML/CSS/JS のみ**。

### 検証結果の前提（再確認不要）

以下は実機確認済みで正常。**いじらないこと**。

- `penguins.py` / `kids/penguins/data/*.csv`（344行・欠損保持・平均 3701/3733/5076・342行 2700〜6300）
- スプレッドシートのリンク（`.../19b6QYQtof7msFCeKfJete7267sNi5PveTyhAOCQ_G1w/copy`）は**オーナー所有の正規シートで、そのままでよい**。「じゅんび中」表示に戻す必要はない
- P1 の表の中身（344行・空欄「—」表示・sticky thead・体重ソート）
- P2 の横棒グラフ（3,701 / 3,733 / 5,076、最重種のみ濃色）
- P3 のサマリーカード3枚（期待値と完全一致）
- 全クイズの選択肢・正解・○×文言
- Umami設置、CFビーコン不使用、相対パス、導線、`kids/index.html` の追加分、CLAUDE.md・README.md の追記

---

## 修正一覧

| # | 優先度 | 対象 | 内容 |
|---|---|---|---|
| 1 | 🔴 必須 | `kids/penguins/lesson03/index.html` | ヒストグラムのバーが高さ0で表示されない |
| 2 | 🟡 推奨 | `kids/penguins/lesson01/index.html` | スマホで表が崩れて実用にならない |
| 3 | 🟡 推奨 | `kids/penguins/lesson01/index.html` | No列のソートが文字列順（1, 10, 100…） |
| 4 | 🔵 軽微 | `lesson01` / `lesson03` | 見出しに件数をハードコードしている |
| 5 | 🔵 軽微 | `kids/penguins/lesson03/index.html` | ヒストグラムの縦軸が固定値50 |
| 6 | 🔵 軽微 | `kids/penguins/lesson03/index.html` | 度数がホバーでしか読めずスマホで確認できない |
| 7 | ⚪ 任意 | `kids/js/kids-visuals.js` ほか | P1 が同じCSVを2回fetchしている |
| 8 | ⚪ 判断 | `pyproject.toml` / `uv.lock` | 指示外で追加された playwright の扱い |

---

## 1. 🔴 P3のヒストグラムが完全に表示されない

### 症状

グラフ枠（`#peng3-chart-bars`）の中身が白紙。**16本×3色すべてのバーが高さ0px**。JSエラーは出ないため気づきにくい。

ブラウザで実測した値：

```json
{"barsH":224,"cols":[{"colH":219,"stackH":0,"segs":[0,0,0]}, ...16本すべて同じ]}
```

### 原因

`lesson03/index.html` の `renderPeng3Histogram()` が生成する積み上げコンテナに高さ指定がない。

```
#peng3-chart-bars        h-56 → 224px（definite）
 └ 列 div                h-full → 219px（definite）
    └ 積み上げ div       ★高さ指定なし → auto（indefinite）
       └ 各セグメント     style="height: X%" → 親がindefiniteなので解決できず 0 になる
```

CSSの仕様上、`height: %` は「親の高さが確定している」ときしか解決されない。

### 修正

`kids/penguins/lesson03/index.html` の **432行目付近**、テンプレートリテラル内のこの行：

```html
<!-- 現在 -->
<div class="w-full flex flex-col-reverse items-center justify-start rounded-t overflow-hidden">
  <div class="w-full bg-indigo-400 transition-all duration-300" style="height: ${hAdelie}%"></div>
  <div class="w-full bg-violet-400 transition-all duration-300" style="height: ${hChinstrap}%"></div>
  <div class="w-full bg-sky-400 transition-all duration-300" style="height: ${hGentoo}%"></div>
</div>
```

を、以下に変更する。

```html
<!-- 修正後：積み上げコンテナに h-full、各セグメントに shrink-0 -->
<div class="w-full h-full flex flex-col-reverse items-center justify-start overflow-hidden">
  <div class="w-full shrink-0 bg-indigo-400 transition-all duration-300" style="height: ${hAdelie}%"></div>
  <div class="w-full shrink-0 bg-violet-400 transition-all duration-300" style="height: ${hChinstrap}%"></div>
  <div class="w-full shrink-0 bg-sky-400 transition-all duration-300" style="height: ${hGentoo}%"></div>
</div>
```

- `h-full` を足すことで親が確定高さになり、`height: X%` が解決する
- `shrink-0` は、積み上げ合計が100%に近いときにflexの縮小が働いてしまうのを防ぐ
- `rounded-t` は、コンテナが常に全高になるため見た目に効かなくなるので**外す**（バーの角を丸めたい場合は、その階級でいちばん上に積まれるセグメントにだけ `rounded-t` を付ける。必須ではない）

`flex-col-reverse` + `justify-start` はそのままでよい（主軸の始点が下になるので、バーは下端から積み上がる）。

### 確認方法

ブラウザのコンソールで以下を実行し、**すべての `segs` が0以外の値を含み、`stackH` が219になること**。

```js
[...document.getElementById('peng3-chart-bars').children].map(c => {
  const stack = c.querySelector('div:last-child');
  return {
    stackH: Math.round(stack.getBoundingClientRect().height),
    segs: [...stack.children].map(s => Math.round(s.getBoundingClientRect().height))
  };
});
```

さらに、目視で以下の形になっていること。

- 「ぜんぶ」表示のとき、3,250〜3,999g あたりに高い山（アデリー＋ヒゲ）、4,500〜5,749g あたりにもう一つの山（ジェンツー）という**ふたこぶ**になる
- 「アデリーペンギン」だけにすると、3,250〜3,999g の3本が同じ高さ（各29ひき）で並ぶ

---

## 2. 🟡 P1の表がスマホで崩れる

### 症状

375px幅で実測：

| 項目 | 実測値 |
|---|---|
| 1行の高さ | **177px**（デスクトップは37px） |
| 「しゅるい」列の幅 | 39px |
| スクロール枠内に見える行数 | **2.5行** |

「アデリーペンギン」「トーゲルセン島」が39px幅に押し込まれ、**1文字ずつ縦に折り返されている**。344行をスクロールして読む体験が成立しない。

### 修正

`kids/penguins/lesson01/index.html`。**横スクロールを許可し、セルの折り返しを止める**方針にする。

**(a) `<head>` の `<style>` に追記**

```css
#peng1-table-head th,
#peng1-table-body td {
  white-space: nowrap;
}
```

**(b) 表のラッパー（107行目付近のセクション内）を変更**

```html
<!-- 現在 -->
<div class="max-h-[28rem] overflow-y-auto rounded-xl border border-cyan-100">
  <table class="w-full text-sm text-left border-collapse">

<!-- 修正後：縦横どちらもスクロール可にし、表に最小幅を与える -->
<div class="max-h-[28rem] overflow-auto rounded-xl border border-cyan-100">
  <table class="w-full min-w-[600px] text-sm text-left border-collapse">
```

**(c) 表の上の案内文を差し替え**

```html
<!-- 現在 -->
<p class="text-xs text-gray-500 mb-2">💡 列の名前をタップすると、ならびかえられるよ（スクロールして344ぴき全部見られます）。</p>

<!-- 修正後（件数のハードコードも外す。修正#4と共通） -->
<p class="text-xs text-gray-500 mb-2">💡 列の名前をタップすると、ならびかえられるよ。たてにも、よこにもスクロールできます。</p>
```

### 確認方法

375px幅（Chrome DevToolsのiPhone SE相当）で以下を実行し、**`rowH` が50px以下**、**`visibleRows` が8以上**になること。`thead` が縦スクロール時に残ることも目視確認する。

```js
const tr = document.getElementById('peng1-table-body').children[0];
const box = document.querySelector('table').parentElement;
({
  rowH: Math.round(tr.getBoundingClientRect().height),
  visibleRows: +(box.getBoundingClientRect().height / tr.getBoundingClientRect().height).toFixed(1)
});
```

また、**ページ自体（body）に横スクロールが出ていないこと**も確認する（横スクロールするのは表の枠の中だけ）。

```js
document.documentElement.scrollWidth <= window.innerWidth  // → true
```

---

## 3. 🟡 P1のNo列のソートが文字列順になる

### 症状

No列の見出しをタップすると `1, 10, 100, 101, 102, 103, …` と辞書順に並ぶ。

### 原因

`lesson01/index.html` の 383行目付近で `key: 'no'` を `type: 'text'` にしている。
これは `initKidsSortableTable` が数値列の最大値セルをハイライトする仕様を回避するための指定だが、その副作用でソートが `localeCompare` になっている。

### 修正

**(a) 列定義を数値に戻す**

```js
{
  key: 'no',
  label: 'No',
  type: 'number',        // ← 'text' から変更
  align: 'right',
  render: (val) => `<span class="text-gray-400 font-mono text-xs">${val}</span>`
},
```

**(b) `transformRow` の `no` を数値にする**

```js
no: index + 1,           // ← String(index + 1) から変更
```

**(c) 最大値ハイライトを1列目だけ打ち消すCSSを `<style>` に追記**

`initKidsSortableTable` は最大値のセルに `theme.maxCellClass` を付けるため、そのままだと No=344 のセルが強調されてしまう。No は常に1列目なので、first-child で打ち消す。

```css
#peng1-table-body td:first-child {
  background-color: transparent !important;
  color: #9ca3af !important;
  font-weight: 400 !important;
}
```

`kids/js/kids-visuals.js` は**変更しない**（他のレッスンに影響するため）。

### 確認方法

No列の見出しを1回タップして降順、もう1回で昇順になり、先頭6行が `344, 343, 342, …` / `1, 2, 3, …` となること。344行目のセルに背景色が付いていないこと。

```js
const head = document.getElementById('peng1-table-head');
head.querySelector('button[data-col-key="no"]').click();
[...document.getElementById('peng1-table-body').children].slice(0,6).map(r => r.children[0].innerText.trim());
// → ["344","343","342","341","340","339"]
```

---

## 4. 🔵 見出しに件数をハードコードしている

### 症状・理由

- `lesson01/index.html:107` → `📊 ペンギンのデータ（344ぴき）`
  **もんだい1の答え（344ひき）を、子どもが数える前に見出しで教えてしまっている。**
  CLAUDE.md の「答えになる数字は書かない」に抵触する。サマリーカードがJSで `344ひき` を出すので、そちらで確認させればよい。
- `lesson03/index.html:107` → `📊 体重のちらばり（342ひき）`
  クイズの答えではないが、CSVの行数を手書きしているのでデータ更新時にズレる。

### 修正

```html
<!-- lesson01 -->
<h2 class="font-black text-gray-800">📊 ペンギンのデータ</h2>

<!-- lesson03 -->
<h2 class="font-black text-gray-800">📊 体重のちらばり</h2>
```

`lesson03` は、必要なら見出しの下に「体重がはかれた子だけを集めているよ。」という説明文（`text-xs text-gray-500`）を足してよい（数値は書かない）。

あわせて、修正#2(c) の案内文からも「344ぴき」を外すこと。

---

## 5. 🔵 P3のヒストグラムの縦軸が固定値

### 症状

`lesson03/index.html:413` で `const maxCount = 50;` と決め打ちしている。
「ぜんぶ」表示では最大49ひきなのでちょうどよいが、**1しゅるいだけに絞ると最大29ひき＝58%** までしか伸びず、グラフが低く潰れて見える。

### 修正

表示中のデータの最大度数を基準にする。

```js
// 現在
// 見やすさのため基準の最大度数を 50 とする
const maxCount = 50;

// 修正後：いま表示している中でいちばん多い階級を基準にする
const maxCount = Math.max(1, ...bins.map(b => b.adelie + b.chinstrap + b.gentoo));
```

縦軸の基準がフィルタによって変わるので、**基準値を画面に出す**こと。グラフ枠の上（凡例の下あたり）に次の要素を足し、`renderPeng3Histogram()` の中で毎回更新する。

```html
<p class="text-[10px] text-gray-400" id="peng3-scale-note"></p>
```

```js
document.getElementById('peng3-scale-note').textContent =
  `たて（バーの高さ）のいちばん上 ＝ ${maxCount}ひき`;
```

### 確認方法

「ぜんぶ」で最も高いバー（3,500〜3,749g、49ひき）が枠の上端近くまで届くこと。
「アデリーペンギン」に絞ったとき、29ひきの3本が上端近くまで届き、注記が `29ひき` に変わること。

---

## 6. 🔵 P3の度数がスマホで読めない

### 症状

各階級のひき数は `title` 属性と `group-hover` のツールチップでしか出ない。**タッチ端末ではホバーできない**ため、スマホの子どもは数を確認できない。
（クイズはサマリーカードで解けるので学習上の支障はないが、グラフの情報量が落ちている）

### 修正

バーをタップしたら、グラフの下の読み取り欄にその階級の内訳を表示する。ホバーのツールチップは**そのまま残してよい**。

**(a) グラフ枠の下（横軸ラベルの下）に読み取り欄を足す**

```html
<p id="peng3-readout" class="text-xs text-center text-gray-500 pt-2 min-h-[1.5rem]">
  バーをタップすると、その体重のペンギンが何びきいるかわかるよ。
</p>
```

**(b) 各列に `onclick` を付け、内訳を書き込む**

`renderPeng3Histogram()` のテンプレート内、列の `<div class="flex-1 ...">` に `onclick="showPeng3Bin(${idx})"` を付ける。
階級ごとの集計結果は、描画時にモジュールスコープの配列（例 `p3Bins`）へ保持しておき、次の関数から参照する。

```js
function showPeng3Bin(idx) {
  const b = p3Bins[idx];
  const start = 2500 + idx * 250;
  const end = start + 249;
  const total = b.adelie + b.chinstrap + b.gentoo;
  const parts = [];
  if (b.adelie) parts.push(`アデリー ${b.adelie}`);
  if (b.chinstrap) parts.push(`ヒゲ ${b.chinstrap}`);
  if (b.gentoo) parts.push(`ジェンツー ${b.gentoo}`);
  const readout = document.getElementById('peng3-readout');
  readout.textContent = total === 0
    ? `${formatKidsNumber(start)}〜${formatKidsNumber(end)}g：この体重の子はいないよ`
    : `${formatKidsNumber(start)}〜${formatKidsNumber(end)}g：ぜんぶで ${total}ひき（${parts.join(' / ')}）`;
}
```

フィルタを切り替えたときは読み取り欄を初期文言に戻すこと。

### 確認方法

375px幅で 3,500〜3,749g のバーをタップし、`3,500〜3,749g：ぜんぶで 49ひき（アデリー 29 / ヒゲ 20）` のように表示されること。

---

## 7. ⚪ P1が同じCSVを2回fetchしている

`initP1()` が `loadKidsCsv('../data/penguins_ja.csv')` でサマリー用に1回、`initKidsSortableTable({ csvUrl: ... })` が内部でもう1回、同じ30KBのファイルを取得している。
ブラウザキャッシュが効くので実害は小さい。**対応は任意**。

対応する場合は、`kids/js/kids-visuals.js` に**後方互換のオプション**を足す（既存の呼び出しは引数が増えないので影響を受けない）。

```js
async function initKidsSortableTable({
  csvUrl,
  rows: providedRows = null,   // 追加：すでに読み込み済みの行を渡せる
  headId,
  ...
}) {
  const sourceRows = providedRows || await loadKidsCsv(csvUrl);
  ...
```

P1 側は `csvUrl` の代わりに `rows` を渡す。**既存レッスン（`kids/lesson01`〜`lesson10`）の呼び出しは一切変更しないこと。**

---

## 8. ⚪ playwright の扱い（オーナー判断）

指示書になかった変更として、`pyproject.toml` に `[dependency-groups] dev = ["playwright>=1.63.0"]` が追加され、`uv.lock` に115行増えている。実装時の画面検証用と思われる。

- **検証にだけ使ったのであれば、`uv remove --dev playwright` で元に戻す**（このリポジトリは静的サイトで、CIでの利用もない）
- 今後もブラウザ検証に使い続ける方針なら、そのまま残したうえで **README の「セットアップ」に用途を1行書く**

どちらにするかはオーナーに確認すること。**自己判断で残す／消すのどちらもしないこと。**

---

## 変更してはいけないもの（再掲）

- `penguins.py` と `kids/penguins/data/*.csv`（照合済み。再生成も不要）
- スプレッドシートのリンクと「コピーのしかた」の説明
- クイズの問題文・選択肢・正解・○×メッセージ
- 会話吹き出しのセリフ
- `kids/lesson01`〜`lesson10`、`kids/extra01`〜`extra05`、`adults/`
- `kids/js/kids-visuals.js`（修正#7を採用する場合の後方互換な追記のみ可。既存関数の挙動は変えない）
- `kids/index.html` / `CLAUDE.md` / `README.md` の既存の追記内容（修正#8で README に1行足す場合を除く）

---

## 動作確認のしかた

`fetch()` を使うため `file://` では動かない。必ずローカルサーバで確認する。

```bash
uv run python3 -m http.server 8000
```

確認するURL：

- `http://localhost:8000/kids/penguins/lesson01/index.html`（修正 #2 #3 #4 #7）
- `http://localhost:8000/kids/penguins/lesson03/index.html`（修正 #1 #4 #5 #6）

**デスクトップ幅と375px幅の両方**で確認すること。コンソールにエラーが出ないこと。

### 最終チェックリスト

- [ ] P3：16本すべてのバーが表示され、ふたこぶの形になる
- [ ] P3：フィルタを切り替えてもバーが上端近くまで伸びる／基準値の注記が変わる
- [ ] P3：バーをタップすると階級ごとのひき数が読み取り欄に出る
- [ ] P1：375px幅で1行50px以下、8行以上見える、横スクロールは表の枠内だけ
- [ ] P1：No列のソートが 1,2,3… / 344,343,342… になる
- [ ] P1：No列の最大値セルに背景色が付かない
- [ ] P1・P3：見出しから件数のハードコードが消えている
- [ ] P1のサマリー・バッジ、P2のバー、P3のサマリーカードの数値が修正前と変わっていない
- [ ] 4ページともコンソールエラーなし・body に横スクロールなし

## 報告に含めてほしいこと

1. 修正した項目と、見送った項目（#7 #8 を含む）
2. 最終チェックリストのうち確認できなかった項目とその理由
3. #8（playwright）についてのオーナーへの確認結果、または未確認である旨

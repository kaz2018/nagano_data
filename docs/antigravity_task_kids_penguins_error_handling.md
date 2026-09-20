# 修正依頼：ペンギン研究所 P1〜P3 のデータ読み込み失敗を画面に出す

## 背景

P1 のページを開いたとき、サマリーが `—` のまま・バッジが空・表が0行という状態になることがある。

原因は **CSVの読み込みに失敗している**こと（多くは `file://` で直接HTMLを開いたケース。`fetch()` がCORSでブロックされる）。
ところが現在のコードは `async` の即時関数に `try/catch` がないため、**失敗しても画面には何も出ない**。
ユーザーからは「こわれている」「まだ読み込み中なのか失敗したのか分からない」状態に見える。

この依頼では、**読み込みに失敗したことが画面で分かるようにする**。

### スコープ

- 対象は **`kids/penguins/lesson01` 〜 `lesson03` の3ページのみ**
- 長野編（`kids/lesson01`〜`lesson10`）と `kids/js/kids-visuals.js` は **今回は変更しない**（同じ弱点があるが、影響範囲が広いため別タスクとする）
- データ生成（`penguins.py` / CSV）、クイズ、会話、グラフのロジックは**変更しない**

---

## 1. 共通仕様

### エラーボックスのHTML

各ページの可視化セクションの中、**見出し `<h2>` の直後**に置く。初期状態は `hidden`。

```html
<div id="pengX-error" class="hidden bg-amber-50 border border-amber-200 rounded-xl p-4 text-sm text-amber-800">
  <p class="font-bold mb-1">⚠️ データをよみこめなかったよ</p>
  <p class="leading-relaxed">インターネットにつながっているか確かめて、ページをもういちどひらいてみてね。なおらないときは、おうちの人か先生に教えてね。</p>
</div>
```

`pengX` はページごとに `peng1` / `peng2` / `peng3` とする。
文言は3ページとも同じ。子ども向けなので、技術的な原因（CORS・404など）は**画面に出さない**。

### 共通のエラー処理関数

各ページの `<script>` 内、`showResult()` の近くに置く。

```js
function showPengError(errorId, hideIds, err) {
  console.error('[penguins] データの読み込みに失敗しました:', err);
  const box = document.getElementById(errorId);
  if (box) box.classList.remove('hidden');
  hideIds.forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.classList.add('hidden');
  });
}
```

- `console.error` は**必ず残す**（開発時に原因を追うため）
- `hideIds` には、データがないと空箱になってしまう要素のidを渡して隠す

### 初期化処理の書き換え方（3ページ共通の型）

現在は次の形になっている。

```js
(async function initPX() {
  const rows = await loadKidsCsv('../data/....csv');
  // …描画…
})();
```

これを `try/catch` で包む。

```js
(async function initPX() {
  try {
    const rows = await loadKidsCsv('../data/....csv');
    // …描画…
  } catch (err) {
    showPengError('pengX-error', [/* 隠す要素のid */], err);
  }
})();
```

**注意：`initKidsSortableTable()` は `await` を付けること。** 現在の P1 は `await` なしで呼んでいるため、
そのままでは表の初期化が失敗しても `catch` に入らない（未処理のPromise拒否になる）。

---

## 2. P1：`kids/penguins/lesson01/index.html`

### 隠す要素

データがないと空箱になる、次の2つにidを付けて `hideIds` に渡す。

| 要素 | 付けるid | 場所 |
|---|---|---|
| サマリーカード4枚 + バッジをまとめた親 | `peng1-summary` | サマリーカードの `grid` とバッジの `div` を1つの `<div>` で囲み、そこに付ける |
| 表のラッパー（案内文を含む） | `peng1-table-area` | `💡 列の名前をタップすると…` の `<p>` と、`max-h-[28rem] overflow-auto` の `<div>` を囲む既存の `<div>` |

（表のラッパーを囲んでいる `<div>` はすでに存在するので、そこに `id="peng1-table-area"` を足すだけでよい）

### 修正後の初期化処理

```js
(async function initP1() {
  try {
    const rows = await loadKidsCsv('../data/penguins_ja.csv');

    // …サマリー集計・バッジ生成（現状のまま）…

    await initKidsSortableTable({   // ← await を追加
      csvUrl: '../data/penguins_ja.csv',
      rows,
      // …以下そのまま…
    });
  } catch (err) {
    showPengError('peng1-error', ['peng1-summary', 'peng1-table-area'], err);
  }
})();
```

---

## 3. P2：`kids/penguins/lesson02/index.html`

### 隠す要素

| 要素 | 付けるid |
|---|---|
| 横棒グラフのコンテナ | `peng2-chart-container`（既存のidをそのまま使う） |
| グラフ下の `💡 バーが長いほど重いよ。…` の `<p>` | `peng2-chart-note` |

### 修正後

```js
(async function initP2() {
  try {
    const rows = await loadKidsCsv('../data/lesson02_species_mass.csv');
    // …描画（現状のまま）…
  } catch (err) {
    showPengError('peng2-error', ['peng2-chart-container', 'peng2-chart-note'], err);
  }
})();
```

---

## 4. P3：`kids/penguins/lesson03/index.html`

### 隠す要素

| 要素 | 付けるid |
|---|---|
| しゅるい別サマリーカード | `peng3-summary-cards`（既存） |
| フィルタボタン・凡例・グラフ枠・読み取り欄をまとめた親 | `peng3-chart-area`（既存の `<div class="space-y-3 pt-2">` に付ける） |

### 修正後

```js
(async function initP3() {
  try {
    p3Data = await loadKidsCsv('../data/lesson03_mass.csv');
    // …サマリーカード生成・renderPeng3Histogram()（現状のまま）…
  } catch (err) {
    showPengError('peng3-error', ['peng3-summary-cards', 'peng3-chart-area'], err);
  }
})();
```

`setPeng3Filter()` と `showPeng3Bin()` は、エラー時はボタンごと隠れるので呼ばれない。追加の防御は不要。

---

## 5. 開発者向けメモを CLAUDE.md に追記

同じ混乱を繰り返さないよう、`CLAUDE.md` の「## Python の実行」の直前に次のセクションを追加する。

```markdown
## ページの動作確認

子どもコースのページは `fetch()` でCSVを読むため、**HTMLファイルを直接ひらく（`file://`）と動かない**。
ブラウザのCORS制限で読み込みがブロックされ、数値が `—` のまま・表が空になる。

必ずローカルサーバ経由で確認すること。

```bash
uv run python3 -m http.server 8000
```

`http://localhost:8000/kids/penguins/lesson01/index.html` のように開く。
```

---

## 6. 動作確認

### (a) 正常時：これまでどおり動くこと

```bash
uv run python3 -m http.server 8000
```

- P1：`344ひき / 3 / 3 / 2007〜2009`、バッジ `152 / 124 / 68`、表344行
- P2：バー3本（3,701 / 3,733 / 5,076）
- P3：サマリーカード3枚、ヒストグラム16本、フィルタ、タップ読み取り

**エラーボックスが表示されていないこと**（`hidden` のまま）も確認する。

### (b) 失敗時：エラーボックスが出ること

CSVを一時的に退避して確認する。

```bash
mv kids/penguins/data/penguins_ja.csv kids/penguins/data/penguins_ja.csv.bak
# → P1 を開き、⚠️ のボックスが出て、サマリーと表が消えることを確認
mv kids/penguins/data/penguins_ja.csv.bak kids/penguins/data/penguins_ja.csv
```

P2 は `lesson02_species_mass.csv`、P3 は `lesson03_mass.csv` で同様に確認する。
**確認が終わったら必ずファイルを元に戻すこと。**

あわせて、3ページとも `file://` で直接開いたときにもエラーボックスが出ることを確認する（これが実際に報告されたケース）。

### チェックリスト

- [ ] 正常時、3ページとも従来どおり描画され、エラーボックスは出ない
- [ ] CSVを退避すると、3ページとも ⚠️ のボックスが出る
- [ ] エラー時、空箱になる要素（サマリー・表・グラフ）が隠れている
- [ ] エラー時、コンソールに `[penguins] データの読み込みに失敗しました:` が出る
- [ ] `file://` で開いてもエラーボックスが出る
- [ ] クイズ・会話・出典・発展セクションは正常時・エラー時ともそのまま表示される
- [ ] CSVを元に戻し、`git status` に `.bak` などの残骸がない
- [ ] `kids/js/kids-visuals.js` と長野編のページを変更していない

## 報告に含めてほしいこと

1. 変更したファイルと、追加したid
2. チェックリストのうち確認できなかった項目とその理由

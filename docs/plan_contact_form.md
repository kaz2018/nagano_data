# 実装プラン：質問・要望フォーム（contact ページ）

サイト全体（子どもコース・大人コース共通）の質問・要望を受け付けるフォームを追加する。
このドキュメントは単体で実装できるよう、背景・仕様・コード・手順をすべて含む。
実装時は必ずリポジトリルートの `CLAUDE.md`（開発規約）にも従うこと。

## 背景と全体像

- このサイトは Cloudflare Workers の静的アセット配信のみで、サーバー処理はない
- フォームの受け皿は **Google Apps Script（GAS）のウェブアプリ** を使う
  - ユーザーに Google ログインを求めない（Google フォームは使わない）
  - 送信内容はスプレッドシートに1行ずつ追記
  - 送信があったらサイト管理者の Gmail に通知メールを送る
- スパム対策は「ハニーポット＋経過時間チェック＋サーバー側入力検証」の3つ。
  **Cloudflare Turnstile は今回は実装しない**（スパムが実際に来たら追加する方針）

```
contact/index.html（自作フォーム・静的ページ）
      │ fetch POST（application/x-www-form-urlencoded）
      ▼
GAS ウェブアプリ doPost
      ├─ スパム判定・入力検証
      ├─ スプレッドシートに追記
      └─ MailApp で管理者 Gmail に通知
```

## 作成・変更するファイル

| ファイル | 作業 |
|---|---|
| `contact/index.html` | 新規作成（フォームページ） |
| `docs/gas_contact_form.gs` | 新規作成（GAS に貼り付けるコード。リポジトリには手順書として保存） |
| `docs/setup_contact_form.md` | 新規作成（管理者向けデプロイ手順書） |
| `index.html` | フッター手前に contact へのリンクセクションを追加 |
| `kids/index.html` | 同上 |
| `adults/index.html` | 同上 |

---

## 1. フォーム項目

ユーザーに入力させるのは4項目のみ。必須は「内容」だけ。

| 項目 | name属性 | 形式 | 必須 | 備考 |
|---|---|---|---|---|
| 種別 | `type` | ラジオ（質問 / 要望 / 不具合の報告 / その他） | 任意 | 未選択なら「その他」扱い |
| お名前・ニックネーム | `name` | テキスト1行 | 任意 | 「ニックネームでOK・本名でなくてよい」と明記。最大100文字 |
| 返信用メールアドレス | `email` | テキスト1行（type=email） | 任意 | 「返信がほしい場合だけ書いてね」と明記。最大254文字 |
| 内容 | `message` | テキストエリア | **必須** | 最大1000文字。プレースホルダーで記入例を示す |

### 内部項目（ユーザーには見えない）

| 項目 | name属性 | 内容 |
|---|---|---|
| どのページから来たか | `page` | URLパラメータ `?from=...` の値を JS で hidden フィールドに入れる。英数字・`/`・`-`・`_` のみ許可、最大50文字にサニタイズ。無ければ空 |
| ハニーポット | `website` | CSSで不可視にした入力欄（`display:none` ではなく画面外配置＋`tabindex="-1"`＋`autocomplete="off"`）。値が入っていたら bot と判定 |
| 経過秒数 | `elapsed` | ページ読み込みからの秒数を JS でセット。4秒未満の送信は bot と判定 |

- 送信日時は GAS 側で記録する（フォームからは送らない）
- ハニーポット・経過秒数はスプレッドシートには記録しない（判定にのみ使う）

## 2. contact/index.html の仕様

### デザイン

トップページ（`index.html`）と同じ雰囲気にそろえる：

- `<html lang="ja">`、Tailwind CDN（`https://cdn.tailwindcss.com`）
- Noto Sans JP（トップページと同じ `<link>` と `<style>`）
- `body class="bg-amber-50 min-h-screen"`
- ヘッダーはトップページと同一構成（📊 ながのデータ探検隊）。ただしヘッダー全体をトップ（`../index.html`）へのリンクにする
- フォームは `bg-white rounded-3xl shadow-sm p-8` のカードに入れる
- 送信ボタン：`bg-amber-500 hover:bg-amber-600 text-white font-bold rounded-xl px-8 py-3`。送信中は `disabled` ＋グレーアウト
- 文章は子どもも読める平易な日本語（ひらがな多め、短文）。ページタイトルは「📮 質問・要望フォーム」
- フッターはトップページと同一
- **CLAUDE.md の規約どおり、`</head>` 直前に Umami スクリプトを入れること**

### 動作（Vanilla JS。Alpine.js は使わない）

1. ページ読み込み時：
   - `location.search` から `from` を取得しサニタイズして hidden `page` にセット
   - 読み込み時刻を記録
2. 送信時（submit イベントを preventDefault）：
   - `message` が空なら送信せずエラー表示「内容を書いてね」
   - `elapsed` を計算して hidden にセット
   - `fetch(GAS_ENDPOINT_URL, { method: 'POST', body: new URLSearchParams(formData) })` で送信
     - **重要**: ヘッダーは付けない（カスタムヘッダーを付けるとプリフライトが発生し GAS で CORS エラーになる。URLSearchParams ボディの簡易リクエストならリダイレクト先で `Access-Control-Allow-Origin: *` が返り、レスポンス JSON を読める）
   - レスポンス JSON の `status` が `"ok"` なら：フォームを隠して「✅ 送信しました！ありがとう！」メッセージを表示
   - 失敗（ネットワークエラー・status が ok 以外）なら：フォームは残したまま「送信できませんでした。時間をおいてもう一度ためしてね」を赤字で表示
3. GAS の URL はファイル冒頭の定数に置く：

```js
// デプロイ後に GAS ウェブアプリの URL に差し替える
const GAS_ENDPOINT_URL = 'PASTE_GAS_WEBAPP_URL_HERE';
```

`PASTE_GAS_WEBAPP_URL_HERE` のままの場合は送信ボタン押下時にエラーメッセージを出す（デプロイ忘れ検知）。

## 3. GAS コード（docs/gas_contact_form.gs として保存）

以下をそのまま保存する。`SHEET_ID` と `NOTIFY_EMAIL` は手順書でユーザーが書き換える。

```javascript
// ===== 設定（デプロイ時に書き換える） =====
const SHEET_ID = 'PASTE_SPREADSHEET_ID_HERE'; // 記録先スプレッドシートのID
const NOTIFY_EMAIL = 'PASTE_YOUR_EMAIL_HERE'; // 通知先メールアドレス
// ==========================================

const VALID_TYPES = ['質問', '要望', '不具合の報告', 'その他'];

function doPost(e) {
  try {
    const p = (e && e.parameter) || {};

    // --- スパム判定（該当したら記録せず ok を返して bot に悟らせない） ---
    if (p.website) return jsonResponse({ status: 'ok' });
    const elapsed = Number(p.elapsed || 0);
    if (!elapsed || elapsed < 4) return jsonResponse({ status: 'ok' });

    // --- 入力検証 ---
    const message = String(p.message || '').trim();
    if (!message) return jsonResponse({ status: 'error', reason: 'empty' });
    if (message.length > 1000) return jsonResponse({ status: 'error', reason: 'too_long' });

    const type = VALID_TYPES.includes(p.type) ? p.type : 'その他';
    const name = String(p.name || '').slice(0, 100);
    const email = String(p.email || '').slice(0, 254);
    const page = String(p.page || '').replace(/[^a-zA-Z0-9\/_-]/g, '').slice(0, 50);

    // --- スプレッドシートに追記 ---
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheets()[0];
    sheet.appendRow([new Date(), type, name, email, message, page]);

    // --- 通知メール ---
    MailApp.sendEmail({
      to: NOTIFY_EMAIL,
      subject: '【ながのデータ探検隊】' + type + 'が届きました',
      body: [
        '種別: ' + type,
        '名前: ' + (name || '（未記入）'),
        'メール: ' + (email || '（未記入）'),
        'ページ: ' + (page || '（不明）'),
        '',
        '--- 内容 ---',
        message,
      ].join('\n'),
    });

    return jsonResponse({ status: 'ok' });
  } catch (err) {
    return jsonResponse({ status: 'error', reason: 'server' });
  }
}

function jsonResponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
```

## 4. デプロイ手順書（docs/setup_contact_form.md として保存）

管理者（サイトオーナー）が自分の Google アカウントで行う手順を、以下の流れで書く：

1. Google スプレッドシートを新規作成（名前：「ながのデータ探検隊 質問・要望」）
   - 1行目にヘッダー：`受信日時 | 種別 | 名前 | メール | 内容 | ページ`
   - URL 中のスプレッドシートIDを控える
2. スプレッドシートのメニュー「拡張機能 → Apps Script」を開き、`docs/gas_contact_form.gs` の内容を貼り付け
   - `SHEET_ID` と `NOTIFY_EMAIL` を書き換え
3. 「デプロイ → 新しいデプロイ → ウェブアプリ」
   - 実行ユーザー：**自分**
   - アクセスできるユーザー：**全員**
   - デプロイして表示されるウェブアプリ URL（`https://script.google.com/macros/s/.../exec`）を控える
4. `contact/index.html` の `GAS_ENDPOINT_URL` にその URL を貼り付ける
5. 動作テスト（後述の確認項目）

コードを修正して再デプロイする場合は「デプロイを管理 → 編集 → 新バージョン」で更新しないと URL に反映されない、という注意も手順書に書くこと。

## 5. 各 index ページへのリンク追加

3ページとも **最後のセクションの後・フッターの前** に、質問・要望への誘導セクションを追加する。ヘッダーにナビメニューは作らない。

| ページ | リンク先 | デザイン |
|---|---|---|
| `index.html`（トップ） | `contact/index.html?from=top` | 白カード（`bg-white rounded-3xl shadow-sm`）＋アンバー系のリンク色。既存セクションと同じトーン |
| `kids/index.html` | `../contact/index.html?from=kids` | kids/index.html の既存セクションのスタイルに合わせる（アンバー系） |
| `adults/index.html` | `../contact/index.html?from=adults` | 大人コース規約に合わせる：`bg-white rounded-2xl border border-slate-200`、リンク色はインディゴ |

文言の例（各ページのトーンに合わせて調整してよい）：

> 📮 **質問・要望をおくる**
> わからないこと、「こんなレッスンがほしい」などがあったら、気軽におくってね。

## 6. 確認項目（実装後のチェックリスト)

静的ページ部分（GAS デプロイ前でも確認可能）：

- [ ] `contact/index.html` が Umami スクリプトを含む（CLAUDE.md 規約）
- [ ] `?from=kids/lesson03` 付きで開くと hidden `page` に `kids/lesson03` が入る。`?from=<script>` のような不正値は除去される
- [ ] 内容が空のまま送信するとエラーメッセージが出て送信されない
- [ ] `GAS_ENDPOINT_URL` が未設定のときは送信時にエラーメッセージが出る
- [ ] スマホ幅（375px）でレイアウトが崩れない
- [ ] 3つの index ページのリンクから contact ページに正しく遷移し、`from` が付いている

GAS デプロイ後（管理者がブラウザで手動確認）：

- [ ] 送信するとスプレッドシートに1行追加され、通知メールが届く
- [ ] 送信成功後にフォームが隠れて完了メッセージが表示される
- [ ] ページ表示直後（4秒未満）の送信は記録されない（スパム判定の確認）

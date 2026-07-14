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

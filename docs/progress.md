# 進捗管理 - 長野県データ分析教育サイト

最終更新: 2026-03-19（会話セッション5終了時点）

---

## フェーズ1：子ども向けサイト

### 完了

- [x] プロジェクト要件定義
- [x] フォルダ構成の作成
- [x] .gitignore 作成（macOS・uv・Python対応）
- [x] README.md 作成
- [x] リモートリポジトリ設定・GitHub push（https://github.com/kaz2018/nagano_data.git）
- [x] GitHub Pages URL確認（https://kaz2018.github.io/nagano_data/）
- [x] トップページ（`index.html`）— 架空データ表記の削除・子ども向け説明文の平易化済み
- [x] 子どもコース一覧ページ（`kids/index.html`）— 小学生向けにひらがな多用・平易な日本語に改訂済み。レッスンごとの個別色に統一。トップ画像追加。
- [x] レッスン1ページ（`kids/lesson01/index.html`）— 村データのみに絞り込み・「総人口」→「人口」に統一
- [x] レッスン2ページ（`kids/lesson02/index.html`）— 棒グラフ・19市＋麻績村・筑北村
- [x] レッスン3ページ（`kids/lesson03/index.html`）— 折れ線グラフ・6村（麻績村・筑北村・青木村・生坂村・白馬村・野沢温泉村）
- [x] レッスン4ページ（`kids/lesson04/index.html`）— 並べ替え・77市町村全件
- [x] レッスン5ページ（`kids/lesson05/index.html`）— 引き算でへんかを調べる・77市町村・2017年vs2025年
- [x] レッスン6ページ（`kids/lesson06/index.html`）— 変化率（パーセント）・ROUND関数
- [x] レッスン7ページ（`kids/lesson07/index.html`）— 男女比・SUM関数・2025年全市町村
- [x] レッスン8ページ（`kids/lesson08/index.html`）— 合計・COUNTIF関数・全体と部分
- [x] レッスン9ページ（`kids/lesson09/index.html`）— 2033年人口予測・外挿
- [x] レッスン10ページ（`kids/lesson10/index.html`）— 自由探究・まとめ
- [x] データ収集：長野県毎月人口異動調査 2017〜2025年（9年分）手動ダウンロード
- [x] データ整形：77市町村 × 9年分のCSV作成（ワイド形式・ロング形式）
- [x] データ検証：9項目チェック（行数・重複・nullなし・男女計＝総人口・年次整合性など）にてゼロエラー確認
- [x] データソース・要件定義ドキュメントの整備
- [x] 全ページで「市」のみの表記を「市町村」または「村」に統一
- [x] Google Sheetsの作成・共有リンク取得
  - レッスン1（村のみ・2017〜2025年）: `1x0g6VegtsCjnHUoNphpto4m80bA90mWVNEsXlFyQan8`（35行×10列）
  - レッスン2（19市＋麻績村・筑北村・2025年）: `1GAt8JexG_lT5njSKnFgZaVUeL-ma5vsAwJvGPzaT3Kc`（21行×2列）
  - レッスン3（6村・2017〜2025年）: `1PFRrECxXxLXZ5dNS3_6cvvcsgUTt5m0wJMUT8UzmNCc`（9行×7列）
  - レッスン4・8（77市町村・2025年）: `1-d4jhAnABO_l2VATw4a39DMvmSpmEJbwewvQ4nDxdkM`（77行×2列）
  - レッスン5・6・9（77市町村・2017年＆2025年）: `1HjTbRqW85qg22EHLtht3GaLi-SZp9woBu0hmIykIaxk`（77行×3列）
  - レッスン7（77市町村・2025年・男女別）: `1n9RCKCRSk2pl90Wzdj7QroETMkYYFN3mgvUtHynndyQ`（77行×3列）
- [x] 全レッスンに「やってみよう」答え合わせ機能を追加（1問ごとに「答え合わせ」ボタン）
  - L1: 35村・9年分・上位3村（部分一致対応）
  - L2: 長野市・松本市・343099人
  - L3: 白馬村・445人・自由記述（模範解答表示）
  - L4: 長野市361045人・平谷村368人・順位2問・差360677人
  - L5: 長野市14865人減・6市町村増・御代田町1288人増
  - L6: 天龍村・御代田町8.5%・南箕輪村5.9%（±0.2許容）
  - L7: 女42244人多・62市町村で女多・川上村は男多
  - L8: 1984926人・18.2%・10市（±0.2許容）
  - L9: 長野市346180人・天龍村668人・自由記述（模範解答表示）
  - L10: 自由探究（正誤なし）
- [x] CLAUDE.md 作成（uv実行規約・答え合わせUIパターン・正解一覧）
- [x] トップ画像（`kids/images/kids_top_image.png`）追加

### 未着手

- [ ] GitHub Pagesの設定・デプロイ確認
- [ ] 動作確認・リンクチェック（全レッスン）

---

## フェーズ2：大人向けサイト（未着手）

- [ ] 要件詳細定義
- [ ] 大人向けトップページ（`adults/index.html`）
- [ ] Google Sheetsコース設計
- [ ] Pythonコース設計
- [ ] コンテンツ作成

---

## データ管理メモ

| 項目 | 内容 |
|------|------|
| 元データ格納先 | `kids/data/raw/` |
| 教材用CSV（全件） | `kids/data/nagano_population_raw.csv`（ワイド・77市町村×9年） |
| 分析用CSV（全件） | `kids/data/nagano_population_long.csv`（ロング・693行） |
| 2025年のみCSV | `kids/data/nagano_population_long_2025only.csv`（77行・総人口・男・女） |
| レッスン2用CSV | `kids/data/lesson02_cities_2025.csv`（19市＋麻績村・筑北村） |
| レッスン3用CSV | `kids/data/lesson03_population_trend.csv`（6村×9年） |
| レッスン4用CSV | `kids/data/lesson04_all_2025.csv`（77市町村・2025年） |
| レッスン5・6・9用CSV | `kids/data/lesson05_change.csv`（77市町村・2017年＆2025年） |
| レッスン7用CSV | `kids/data/lesson07_gender_2025.csv`（77市町村・男・女・2025年） |

---

## 課題・メモ

- `pj_data_science/data/raw/` に不正ファイル（curlで取得失敗したHTMLファイル）が残存中 → 削除してよければ整理する
- 2024年データのファイル名が `1882-R6_1-2.xlsx`（末尾に`-2`）← 修正版の可能性あり、要確認

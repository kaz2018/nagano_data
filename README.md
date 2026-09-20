# 長野県データ分析教育サイト

長野県の人口データを使って、地元の子どもから大人までがデータ分析を学べる教育サイトです。
実際の長野県オープンデータを教材に使用しています。

**本番サイト**: https://nagano-data.willbefree-k-m.workers.dev/

**ホスティング**: Cloudflare Workers の静的アセット配信
（`https://kaz2018.github.io/nagano_data/` は旧・GitHub Pages のURL）

## サイト構成

サイトは**テーマ**で分かれています（年齢では分けていません）。

| テーマ | パス | 対象 | 内容 | 状態 |
|--------|------|------|------|------|
| 🏔 長野県編 | `kids/nagano/` | 小学生〜 | 長野県の人口データで読む・くらべる・変化を追う | 全10レッスン完成 |
| 🐧 ペンギン研究所 | `kids/penguins/` | 小学生〜 | 南極のペンギン344ひきの測定データで統計の考え方 | 全8レッスン完成 |
| 💡 番外編 | `kids/extra/` | 小学生〜 | 身のまわりのしくみを見ぬく単発の話 | 全5話完成 |
| 👩‍💻 しごととデータ | `adults/` | 中学生〜大人 | 神Excelの直し方・表の設計・ピボット集計 | 3レッスン完成（続編準備中） |

## 長野県編のレッスン

| レッスン | タイトル | 章 |
|---------|---------|-----|
| 1 | 長野県ってどんなところ？ | 第1章：はじめの一歩 |
| 2 | 市の人口をくらべよう | 第1章：はじめの一歩 |
| 3 | 人口はどうかわってきた？ | 第2章：変化を追え |
| 4 | いちばん人口が多い市はどこ？ | 第2章：変化を追え |
| 5 | ふえた？へった？ | 第3章：数字で深掘り |
| 6 | 何パーセントへった？ | 第3章：数字で深掘り |
| 7 | おとことおんな | 第3章：数字で深掘り |
| 8 | ぜんぶ合わせたら？ | 第4章：全体と未来 |
| 9 | このままだとどうなる？ | 第4章：全体と未来 |
| 10 | じぶんで調べてみよう | 最終章：謎を解け！ |

## 番外編

表示順は「データを読む話 → 3つの『わな』 → 自由とは何かを考える」。
フォルダ名は連番ではなくスラッグなので、並べ替えてもパスは変わりません。

| # | パス | タイトル |
|---|------|---------|
| 1 | `kids/extra/trash/` | 信州ごみ減らし大作戦！ |
| 2 | `kids/extra/youtube/` | YouTubeのわな |
| 3 | `kids/extra/instagram/` | インスタのわな |
| 4 | `kids/extra/games/` | ゲームのわな |
| 5 | `kids/extra/freedom/` | ほんとうの自由ってなに？ |

## データ

### 長野県人口データ
- **出典**: 長野県毎月人口異動調査（住民基本台帳ベース、各年1月1日現在）
- **収録年**: 2017〜2025年（9年分）
- **対象**: 77市町村（19市・23町・35村）
- **項目**: 市町村名・総人口・男・女

| ファイル | 形式 | 用途 |
|----------|------|------|
| `kids/nagano/data/nagano_population_raw.csv` | ワイド（77行×28列） | 教材・Google Sheets |
| `kids/nagano/data/nagano_population_long.csv` | ロング（693行×5列） | データ分析 |
| `kids/nagano/data/raw/` | 公式Excelファイル原本 | ソースデータ |

### ペンギンデータ
- **出典**: [palmerpenguins](https://allisonhorst.github.io/palmerpenguins/)（Horst, Hill & Gorman, 2020／CC0）
- **観測**: 南極パーマー基地（Palmer Station LTER）で 2007〜2009年に観測された3種344羽の記録
- **項目**: しゅるい、島、くちばしの長さ・厚さ、ひれの長さ、体重、せいべつ、年

| ファイル | 行数 | 用途 |
|----------|------|------|
| `kids/penguins/data/penguins_raw.csv` | 344行 | 原典データ（英語・ヘッダー込み345行） |
| `kids/penguins/data/penguins_ja.csv` | 344行 | 日本語化データ（P1教材・スプレッドシート原稿） |
| `kids/penguins/data/lesson02_species_mass.csv` | 3行 | しゅるい別集計（P2平均体重教材） |
| `kids/penguins/data/lesson03_mass.csv` | 342行 | 体重測定データ（P3ヒストグラム教材） |
| `kids/penguins/data/lesson04_flipper_mass.csv` | 342行 | ひれの長さ×体重（P4散布図教材） |
| `kids/penguins/data/lesson05_island_mass.csv` | 344行 | 島×しゅるい×体重（P5クロス集計教材・空らん保持） |
| `kids/penguins/data/lesson06_sex.csv` | 6行 | しゅるい×せいべつ集計（P6比較教材） |
| `kids/penguins/data/lesson08_bill.csv` | 342行 | くちばしの長さ×厚さ（P8シンプソンのパラドックス教材） |

※ P7（欠損値）は専用ファイルを作らず `penguins_ja.csv` をそのまま読む（空らん自体が教材のため）。

## フォルダ構成

```
nagano_data/
├── index.html              # トップページ（テーマの入り口）
├── 404.html                # 見つからないページの案内
├── _redirects              # 旧URLの301転送（Cloudflare）
├── assets/images/          # サイト共通の画像
├── kids/                   # こどもコース（小学生〜）
│   ├── index.html          #   3テーマのハブ
│   ├── images/             #   3テーマ共通の画像
│   ├── js/                 #   3テーマ共通の JS（kids-visuals.js）
│   ├── nagano/             #   🏔 長野県編
│   │   ├── index.html
│   │   ├── data/           #     長野編の教材データ
│   │   └── lesson01〜10/
│   ├── penguins/           #   🐧 ペンギン研究所
│   │   ├── index.html
│   │   ├── data/           #     ペンギンデータ
│   │   └── lesson01〜08/
│   └── extra/              #   💡 番外編
│       ├── index.html
│       └── trash / youtube / instagram / games / freedom/
├── adults/                 # しごととデータ（中学生〜大人）
├── contact/                # 質問・要望フォーム
├── docs/                   # ドキュメント
├── penguins.py             # ペンギンデータ取得・加工スクリプト
└── main.py                 # 長野データ処理スクリプト
```

### 旧URLについて

2026年9月にフォルダ構成を整理し、レッスンをテーマごとのフォルダへ移しました。
`kids/lesson01/` `kids/extra01/` などの旧パスは、ルートの `_redirects` により
**301で新しいURLへ転送**されます（Cloudflare の静的アセット配信の機能）。

どのURLにも該当しないリクエストは `404.html` が受け、各テーマへ案内します。

## セットアップ

```bash
# 依存関係のインストール（uv使用）
uv sync

# データ処理スクリプトの実行
uv run python main.py
```

### 依存パッケージ

- Python 3.12+
- pandas
- openpyxl

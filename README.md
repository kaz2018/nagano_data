# 長野県データ分析教育サイト
https://kaz2018.github.io/nagano_data/
長野県の人口データを使って、地元の子どもから大人までがデータ分析を学べる教育サイトです。
GitHub Pages でホスティングし、実際の長野県オープンデータを教材に使用します。

## サイト構成

| コース | 対象 | ツール | 状態 |
|--------|------|--------|------|
| 子ども向け（長野県編） | 小学生〜 | Google Sheets / Web | 進行中 |
| 子ども向け・ペンギン研究所 | 小学生〜 | Web / Google Sheets | 第1章（P1〜P3）完成 |
| 大人向け | 高校生〜社会人 | Google Sheets → Python | 進行中 |

## 子ども向けレッスン

| レッスン | タイトル | 状態 |
|---------|---------|------|
| 1 | 長野県ってどんなところ？ | 完成 |
| 2 | 市の人口をくらべよう | 未作成 |
| 3 | 人口はどうかわってきた？ | 未作成 |
| 4 | いちばん人口が多い市はどこ？ | 未作成 |

## データ

### 長野県人口データ
- **出典**: 長野県毎月人口異動調査（住民基本台帳ベース、各年1月1日現在）
- **収録年**: 2017〜2025年（9年分）
- **対象**: 77市町村（19市・23町・35村）
- **項目**: 市町村名・総人口・男・女

| ファイル | 形式 | 用途 |
|----------|------|------|
| `kids/data/nagano_population_raw.csv` | ワイド（77行×28列） | 教材・Google Sheets |
| `kids/data/nagano_population_long.csv` | ロング（693行×5列） | データ分析 |
| `kids/data/raw/` | 公式Excelファイル原本 | ソースデータ |

### ペンギンデータ
- **出典**: [palmerpenguins](https://allisonhorst.github.io/palmerpenguins/)（Horst, Hill & Gorman, 2020／CC0）
- **観測**: 南極パーマー基地（Palmer Station LTER）で 2007〜2009年に観測された3種344羽の記録
- **項目**: しゅるい、島、くちばしの長さ・深さ、ひれの長さ、体重、せいべつ、年

| ファイル | 行数 | 用途 |
|----------|------|------|
| `kids/penguins/data/penguins_raw.csv` | 344行 | 原典データ（英語・ヘッダー込み345行） |
| `kids/penguins/data/penguins_ja.csv` | 344行 | 日本語化データ（P1教材・スプレッドシート原稿） |
| `kids/penguins/data/lesson02_species_mass.csv` | 3行 | しゅるい別集計（P2平均体重教材） |
| `kids/penguins/data/lesson03_mass.csv` | 342行 | 体重測定データ（P3ヒストグラム教材） |

## フォルダ構成

```
nagano_data/
├── index.html              # トップページ
├── kids/
│   ├── index.html          # 子ども向けコース一覧
│   ├── lesson01/index.html # 長野編レッスン
│   ├── data/               # 長野編教材データ
│   └── penguins/           # ペンギン研究所コース
│       ├── index.html      # ペンギン研究所一覧
│       ├── lesson01/       # P1: 表の読み方
│       ├── lesson02/       # P2: 平均体重
│       ├── lesson03/       # P3: ちらばり（ヒストグラム）
│       └── data/           # ペンギンデータ
├── adults/                 # 大人向け
├── assets/                 # CSS・画像
├── docs/                   # ドキュメント
├── penguins.py             # ペンギンデータ取得・加工スクリプト
└── main.py                 # 長野データ処理スクリプト
```

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

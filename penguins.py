"""
Palmer Penguins データ取得・加工スクリプト
"""
import csv
import io
import os
import sys
import urllib.request

RAW_URL = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv"
DATA_DIR = os.path.join(os.path.dirname(__file__), "kids", "penguins", "data")
RAW_PATH = os.path.join(DATA_DIR, "penguins_raw.csv")
JA_PATH = os.path.join(DATA_DIR, "penguins_ja.csv")
L2_PATH = os.path.join(DATA_DIR, "lesson02_species_mass.csv")
L3_PATH = os.path.join(DATA_DIR, "lesson03_mass.csv")

SPECIES_MAP = {
    "Adelie": "アデリーペンギン",
    "Chinstrap": "ヒゲペンギン",
    "Gentoo": "ジェンツーペンギン",
}

ISLAND_MAP = {
    "Biscoe": "ビスコー島",
    "Dream": "ドリーム島",
    "Torgersen": "トーゲルセン島",
}

SEX_MAP = {
    "male": "オス",
    "female": "メス",
}


def fetch_raw_csv() -> str:
    if os.path.exists(RAW_PATH):
        print(f"Using existing raw file: {RAW_PATH}")
        with open(RAW_PATH, "r", encoding="utf-8") as f:
            return f.read()
    else:
        print(f"Downloading raw data from {RAW_URL}...")
        os.makedirs(DATA_DIR, exist_ok=True)
        req = urllib.request.Request(RAW_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode("utf-8")
        with open(RAW_PATH, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        print(f"Saved raw file to: {RAW_PATH}")
        return content


def format_val(val: str, is_float: bool = False, is_int: bool = False) -> str:
    val = val.strip()
    if not val or val == "NA":
        return ""
    try:
        f = float(val)
        if is_int:
            return str(int(round(f)))
        if is_float:
            return f"{f:.1f}"
        return str(f)
    except ValueError:
        return val


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    raw_content = fetch_raw_csv()

    reader = csv.DictReader(io.StringIO(raw_content))
    raw_rows = list(reader)

    # 1. penguins_ja.csv 生成
    # 列: しゅるい,島,くちばしの長さ(mm),くちばしの深さ(mm),ひれの長さ(mm),体重(g),せいべつ,年
    ja_headers = [
        "しゅるい",
        "島",
        "くちばしの長さ(mm)",
        "くちばしの深さ(mm)",
        "ひれの長さ(mm)",
        "体重(g)",
        "せいべつ",
        "年",
    ]

    ja_rows = []
    for r in raw_rows:
        species_en = r["species"].strip()
        island_en = r["island"].strip()
        sex_en = r["sex"].strip()

        species_ja = SPECIES_MAP.get(species_en, species_en)
        island_ja = ISLAND_MAP.get(island_en, island_en)
        sex_ja = SEX_MAP.get(sex_en, "" if sex_en in ("NA", "") else sex_en)

        bill_length = format_val(r["bill_length_mm"], is_float=True)
        bill_depth = format_val(r["bill_depth_mm"], is_float=True)
        flipper_length = format_val(r["flipper_length_mm"], is_int=True)
        body_mass = format_val(r["body_mass_g"], is_int=True)
        year = r["year"].strip()

        ja_rows.append({
            "しゅるい": species_ja,
            "島": island_ja,
            "くちばしの長さ(mm)": bill_length,
            "くちばしの深さ(mm)": bill_depth,
            "ひれの長さ(mm)": flipper_length,
            "体重(g)": body_mass,
            "せいべつ": sex_ja,
            "年": year,
        })

    with open(JA_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ja_headers)
        writer.writeheader()
        writer.writerows(ja_rows)
    print(f"Generated: {JA_PATH} ({len(ja_rows)} rows)")

    # 2. lesson02_species_mass.csv 生成
    # 行順固定: アデリーペンギン -> ヒゲペンギン -> ジェンツーペンギン
    target_species = ["アデリーペンギン", "ヒゲペンギン", "ジェンツーペンギン"]
    l2_rows = []
    for sp in target_species:
        sp_rows = [r for r in ja_rows if r["しゅるい"] == sp]
        count = len(sp_rows)

        valid_mass = [float(r["体重(g)"]) for r in sp_rows if r["体重(g)"]]
        avg_mass = round(sum(valid_mass) / len(valid_mass))

        valid_flipper = [float(r["ひれの長さ(mm)"]) for r in sp_rows if r["ひれの長さ(mm)"]]
        avg_flipper = round(sum(valid_flipper) / len(valid_flipper), 1)

        l2_rows.append({
            "しゅるい": sp,
            "ひき数": count,
            "へいきん体重(g)": avg_mass,
            "へいきんひれの長さ(mm)": f"{avg_flipper:.1f}",
        })

    l2_headers = ["しゅるい", "ひき数", "へいきん体重(g)", "へいきんひれの長さ(mm)"]
    with open(L2_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=l2_headers)
        writer.writeheader()
        writer.writerows(l2_rows)
    print(f"Generated: {L2_PATH} ({len(l2_rows)} rows)")

    # 3. lesson03_mass.csv 生成
    # 体重が欠損している2行を除外した342行
    l3_rows = [
        {"しゅるい": r["しゅるい"], "体重(g)": r["体重(g)"]}
        for r in ja_rows
        if r["体重(g)"] != ""
    ]
    l3_headers = ["しゅるい", "体重(g)"]
    with open(L3_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=l3_headers)
        writer.writeheader()
        writer.writerows(l3_rows)
    print(f"Generated: {L3_PATH} ({len(l3_rows)} rows)")

    # --- 検証 (assert) ---
    print("\n--- Running validations ---")

    # penguins_ja.csv
    assert len(ja_rows) == 344, f"Expected 344 rows, got {len(ja_rows)}"

    species_counts = {}
    for r in ja_rows:
        species_counts[r["しゅるい"]] = species_counts.get(r["しゅるい"], 0) + 1
    assert species_counts == {
        "アデリーペンギン": 152,
        "ジェンツーペンギン": 124,
        "ヒゲペンギン": 68,
    }, f"Unexpected species breakdown: {species_counts}"

    island_counts = {}
    for r in ja_rows:
        island_counts[r["島"]] = island_counts.get(r["島"], 0) + 1
    assert island_counts == {
        "ビスコー島": 168,
        "ドリーム島": 124,
        "トーゲルセン島": 52,
    }, f"Unexpected island breakdown: {island_counts}"

    year_counts = {}
    for r in ja_rows:
        year_counts[r["年"]] = year_counts.get(r["年"], 0) + 1
    assert year_counts == {
        "2007": 110,
        "2008": 114,
        "2009": 120,
    }, f"Unexpected year breakdown: {year_counts}"

    empty_mass = sum(1 for r in ja_rows if not r["体重(g)"])
    assert empty_mass == 2, f"Expected 2 empty mass, got {empty_mass}"

    empty_sex = sum(1 for r in ja_rows if not r["せいべつ"])
    assert empty_sex == 11, f"Expected 11 empty sex, got {empty_sex}"

    # lesson02_species_mass.csv
    assert len(l2_rows) == 3, f"Expected 3 rows in L2, got {len(l2_rows)}"
    l2_avg_mass = [r["へいきん体重(g)"] for r in l2_rows]
    assert l2_avg_mass == [3701, 3733, 5076], f"Unexpected avg mass in L2: {l2_avg_mass}"

    # lesson03_mass.csv
    assert len(l3_rows) == 342, f"Expected 342 rows in L3, got {len(l3_rows)}"
    all_mass_l3 = [int(r["体重(g)"]) for r in l3_rows]
    min_mass = min(all_mass_l3)
    max_mass = max(all_mass_l3)
    assert min_mass == 2700, f"Expected min mass 2700, got {min_mass}"
    assert max_mass == 6300, f"Expected max mass 6300, got {max_mass}"

    print("✅ All validations passed successfully!")
    print(f"Summary:")
    print(f"  - penguins_ja.csv: {len(ja_rows)} rows (Adelie: 152, Gentoo: 124, Chinstrap: 68)")
    print(f"  - Islands: Biscoe: 168, Dream: 124, Torgersen: 52")
    print(f"  - Years: 2007: 110, 2008: 114, 2009: 120")
    print(f"  - Empty mass: {empty_mass}, Empty sex: {empty_sex}")
    print(f"  - lesson02_species_mass.csv: {len(l2_rows)} rows, avg mass: {l2_avg_mass}")
    print(f"  - lesson03_mass.csv: {len(l3_rows)} rows, min: {min_mass}, max: {max_mass}")


if __name__ == "__main__":
    main()

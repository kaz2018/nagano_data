"""
Palmer Penguins データ取得・加工スクリプト
"""
import csv
import io
import os
import statistics
import sys
import urllib.request

RAW_URL = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv"
DATA_DIR = os.path.join(os.path.dirname(__file__), "kids", "penguins", "data")
RAW_PATH = os.path.join(DATA_DIR, "penguins_raw.csv")
JA_PATH = os.path.join(DATA_DIR, "penguins_ja.csv")
L2_PATH = os.path.join(DATA_DIR, "lesson02_species_mass.csv")
L3_PATH = os.path.join(DATA_DIR, "lesson03_mass.csv")
L4_PATH = os.path.join(DATA_DIR, "lesson04_flipper_mass.csv")
L5_PATH = os.path.join(DATA_DIR, "lesson05_island_mass.csv")
L6_PATH = os.path.join(DATA_DIR, "lesson06_sex.csv")
L8_PATH = os.path.join(DATA_DIR, "lesson08_bill.csv")

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
    # 列: しゅるい,島,くちばしの長さ(mm),くちばしの厚さ(mm),ひれの長さ(mm),体重(g),せいべつ,年
    ja_headers = [
        "しゅるい",
        "島",
        "くちばしの長さ(mm)",
        "くちばしの厚さ(mm)",
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
            "くちばしの厚さ(mm)": bill_depth,
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

    # 4. lesson04_flipper_mass.csv 生成
    # ひれの長さ・体重の両方がそろっている342行
    l4_headers = ["しゅるい", "ひれの長さ(mm)", "体重(g)"]
    l4_rows = [
        {
            "しゅるい": r["しゅるい"],
            "ひれの長さ(mm)": r["ひれの長さ(mm)"],
            "体重(g)": r["体重(g)"],
        }
        for r in ja_rows
        if r["ひれの長さ(mm)"] != "" and r["体重(g)"] != ""
    ]
    with open(L4_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=l4_headers)
        writer.writeheader()
        writer.writerows(l4_rows)
    print(f"Generated: {L4_PATH} ({len(l4_rows)} rows)")

    # 5. lesson05_island_mass.csv 生成
    # 344行すべて。体重の欠損は空欄のまま残す（0で埋めない）
    l5_headers = ["島", "しゅるい", "体重(g)"]
    l5_rows = [
        {"島": r["島"], "しゅるい": r["しゅるい"], "体重(g)": r["体重(g)"]}
        for r in ja_rows
    ]
    with open(L5_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=l5_headers)
        writer.writeheader()
        writer.writerows(l5_rows)
    print(f"Generated: {L5_PATH} ({len(l5_rows)} rows)")

    # 6. lesson06_sex.csv 生成
    # しゅるい×せいべつの集計6行。せいべつが空欄の11行は集計から除く
    l6_headers = ["しゅるい", "せいべつ", "ひき数", "へいきん体重(g)", "へいきんひれの長さ(mm)"]
    l6_rows = []
    for sp in target_species:
        for sex in ["オス", "メス"]:
            sub = [r for r in ja_rows if r["しゅるい"] == sp and r["せいべつ"] == sex]
            masses = [float(r["体重(g)"]) for r in sub if r["体重(g)"]]
            flippers = [float(r["ひれの長さ(mm)"]) for r in sub if r["ひれの長さ(mm)"]]
            l6_rows.append({
                "しゅるい": sp,
                "せいべつ": sex,
                "ひき数": len(sub),
                "へいきん体重(g)": round(sum(masses) / len(masses)),
                "へいきんひれの長さ(mm)": f"{round(sum(flippers) / len(flippers), 1):.1f}",
            })
    with open(L6_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=l6_headers)
        writer.writeheader()
        writer.writerows(l6_rows)
    print(f"Generated: {L6_PATH} ({len(l6_rows)} rows)")

    # 7. lesson08_bill.csv 生成
    # くちばしの長さ・厚さの両方がそろっている342行
    l8_headers = ["しゅるい", "くちばしの長さ(mm)", "くちばしの厚さ(mm)"]
    l8_rows = [
        {
            "しゅるい": r["しゅるい"],
            "くちばしの長さ(mm)": r["くちばしの長さ(mm)"],
            "くちばしの厚さ(mm)": r["くちばしの厚さ(mm)"],
        }
        for r in ja_rows
        if r["くちばしの長さ(mm)"] != "" and r["くちばしの厚さ(mm)"] != ""
    ]
    with open(L8_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=l8_headers)
        writer.writeheader()
        writer.writerows(l8_rows)
    print(f"Generated: {L8_PATH} ({len(l8_rows)} rows)")

    # レッスン7は penguins_ja.csv をそのまま読む（空欄を教材にするため新規ファイルなし）

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

    # lesson04_flipper_mass.csv
    assert len(l4_rows) == 342, f"Expected 342 rows in L4, got {len(l4_rows)}"
    l4_flippers = [float(r["ひれの長さ(mm)"]) for r in l4_rows]
    assert (min(l4_flippers), max(l4_flippers)) == (172.0, 231.0), \
        f"Unexpected flipper range in L4: {min(l4_flippers)}-{max(l4_flippers)}"

    # lesson05_island_mass.csv
    assert len(l5_rows) == 344, f"Expected 344 rows in L5, got {len(l5_rows)}"
    l5_cross = {}
    for r in l5_rows:
        key = (r["島"], r["しゅるい"])
        l5_cross[key] = l5_cross.get(key, 0) + 1
    assert l5_cross == {
        ("ビスコー島", "アデリーペンギン"): 44,
        ("ビスコー島", "ジェンツーペンギン"): 124,
        ("ドリーム島", "アデリーペンギン"): 56,
        ("ドリーム島", "ヒゲペンギン"): 68,
        ("トーゲルセン島", "アデリーペンギン"): 52,
    }, f"Unexpected island x species cross tab: {l5_cross}"

    # lesson06_sex.csv
    assert len(l6_rows) == 6, f"Expected 6 rows in L6, got {len(l6_rows)}"
    assert sum(r["ひき数"] for r in l6_rows) == 333, \
        "L6 should cover 333 penguins (344 - 11 with unknown sex)"
    l6_avg_mass = [r["へいきん体重(g)"] for r in l6_rows]
    assert l6_avg_mass == [4043, 3369, 3939, 3527, 5485, 4680], \
        f"Unexpected avg mass in L6: {l6_avg_mass}"

    # lesson08_bill.csv
    assert len(l8_rows) == 342, f"Expected 342 rows in L8, got {len(l8_rows)}"
    bill_len = [float(r["くちばしの長さ(mm)"]) for r in l8_rows]
    bill_depth = [float(r["くちばしの厚さ(mm)"]) for r in l8_rows]
    assert (min(bill_len), max(bill_len)) == (32.1, 59.6), "Unexpected bill length range"
    assert (min(bill_depth), max(bill_depth)) == (13.1, 21.5), "Unexpected bill depth range"

    # シンプソンのパラドックス（レッスン8の核心）が成立していること
    overall_corr = statistics.correlation(bill_len, bill_depth)
    assert overall_corr < 0, f"Expected negative overall bill correlation, got {overall_corr:.3f}"
    for sp in target_species:
        sub = [r for r in l8_rows if r["しゅるい"] == sp]
        corr = statistics.correlation(
            [float(r["くちばしの長さ(mm)"]) for r in sub],
            [float(r["くちばしの厚さ(mm)"]) for r in sub],
        )
        assert corr > 0, f"Expected positive bill correlation for {sp}, got {corr:.3f}"

    print("✅ All validations passed successfully!")
    print(f"Summary:")
    print(f"  - penguins_ja.csv: {len(ja_rows)} rows (Adelie: 152, Gentoo: 124, Chinstrap: 68)")
    print(f"  - Islands: Biscoe: 168, Dream: 124, Torgersen: 52")
    print(f"  - Years: 2007: 110, 2008: 114, 2009: 120")
    print(f"  - Empty mass: {empty_mass}, Empty sex: {empty_sex}")
    print(f"  - lesson02_species_mass.csv: {len(l2_rows)} rows, avg mass: {l2_avg_mass}")
    print(f"  - lesson03_mass.csv: {len(l3_rows)} rows, min: {min_mass}, max: {max_mass}")
    print(f"  - lesson04_flipper_mass.csv: {len(l4_rows)} rows")
    print(f"  - lesson05_island_mass.csv: {len(l5_rows)} rows")
    print(f"  - lesson06_sex.csv: {len(l6_rows)} rows, avg mass: {l6_avg_mass}")
    print(f"  - lesson08_bill.csv: {len(l8_rows)} rows, overall corr: {overall_corr:.3f}")


if __name__ == "__main__":
    main()

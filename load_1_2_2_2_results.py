#!/usr/bin/env python3
"""Parse 1-2 and 2-2 result Excel files into sem_results (same format as 1-1 loader)."""
import openpyxl
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "eee.db"
EXCEL_DIR = Path("/data/data/com.termux/files/home/storage/downloads/college website")

EXAM_MAP = {
    "1-2 REG (1) .xlsx": ("1-2", 1, "MAY 2025"),
    "1-2 SUPPLY [2] .xlsx": ("1-2", 2, "NOV 2025"),
    "1-2 SUPPLY [3] .xlsx": ("1-2", 3, "JUN 2026"),
    "2-1  REGULAR .xlsx": ("2-1", 1, "DEC 2025"),
    "2-1 SUPPLY .xlsx": ("2-1", 2, "JUN 2026"),
    "2-2 REG .xlsx": ("2-2", 1, "MAY 2026"),
}

def gv(row, i):
    return row[i] if i < len(row) else None

def parse_excel(filepath, year_sem, exam_cycle, exam_label):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    records = []

    main = next(ws for ws in wb.worksheets if ws.title.lower() == "main")
    sgpa_map = {}
    for row in main.iter_rows(min_row=2, values_only=True):
        if not gv(row, 2):
            continue
        ht = str(gv(row, 2)).strip()
        sgpa_map[ht] = {
            "sgpa": float(gv(row, 5)) if gv(row, 5) else 0,
            "total_credit": int(gv(row, 6)) if gv(row, 6) else 0,
            "total_appeared": int(gv(row, 7)) if gv(row, 7) else 0,
            "total_passed": int(gv(row, 8)) if gv(row, 8) else 0,
        }

    for sheet_name in wb.sheetnames:
        if sheet_name.lower() in ("main", "readme"):
            continue
        ws = wb[sheet_name]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not gv(row, 2):
                continue
            ht = str(gv(row, 2)).strip()
            s = sgpa_map.get(ht, {})
            records.append({
                "username": ht,
                "year_sem": year_sem,
                "subject": str(gv(row, 3)).strip() if gv(row, 3) else "",
                "code": str(gv(row, 4)).strip() if gv(row, 4) else "",
                "grade": str(gv(row, 5)).strip() if gv(row, 5) else "",
                "grade_point": int(gv(row, 6)) if gv(row, 6) else 0,
                "credit": int(gv(row, 7)) if gv(row, 7) else 0,
                "credit_status": str(gv(row, 8)).strip() if gv(row, 8) else "",
                "exam_cycle": exam_cycle,
                "exam_label": exam_label,
                "sgpa": s.get("sgpa", 0),
                "total_credits": s.get("total_credit", 0),
                "total_appeared": s.get("total_appeared", 0),
                "total_passed": s.get("total_passed", 0),
            })
    wb.close()
    return records

def load_to_db(records):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    inserted = updated = 0
    for r in records:
        if not r["subject"]:
            continue
        cur.execute("""INSERT INTO sem_results
            (username, year_sem, subject, code, grade, grade_point, credit,
             credit_status, exam_cycle, exam_label, sgpa, total_credits,
             total_appeared, total_passed)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(username, year_sem, subject, exam_cycle) DO UPDATE SET
              code=excluded.code, grade=excluded.grade, grade_point=excluded.grade_point,
              credit=excluded.credit, credit_status=excluded.credit_status,
              exam_label=excluded.exam_label, sgpa=excluded.sgpa,
              total_credits=excluded.total_credits, total_appeared=excluded.total_appeared,
              total_passed=excluded.total_passed,
              updated_at=datetime('now','localtime')""",
            (r["username"], r["year_sem"], r["subject"], r["code"], r["grade"],
             r["grade_point"], r["credit"], r["credit_status"], r["exam_cycle"],
             r["exam_label"], r["sgpa"], r["total_credits"], r["total_appeared"],
             r["total_passed"]))
        inserted += 1
        updated += cur.rowcount == 1
    conn.commit()
    conn.close()
    return inserted

if __name__ == "__main__":
    for filename, (year_sem, cycle, label) in EXAM_MAP.items():
        filepath = EXCEL_DIR / filename
        if not filepath.exists():
            print(f"SKIP: {filename} not found")
            continue
        recs = parse_excel(filepath, year_sem, cycle, label)
        insert = load_to_db(recs)
        stus = sorted({r["username"] for r in recs})
        print(f"{filename}: {len(recs):4d} rows | {len(stus):3d} students | {len(recs)//max(1,len(stus))} subjects avg")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    for sem, cyc in (("1-2", 1), ("1-2", 2), ("1-2", 3), ("2-1", 1), ("2-1", 2), ("2-2", 1)):
        n = conn.execute("SELECT COUNT(*) c FROM sem_results WHERE year_sem=? AND exam_cycle=?",
                         (sem, cyc)).fetchone()["c"]
        print(f"sem_results total {sem} cycle {cyc}: {n}")
    conn.close()
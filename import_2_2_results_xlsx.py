"""Import real 2-2 sem results (JNTUGV R23 Apr 2026) into eee.db marks table.

Source: ~/storage/downloads/college website/2-2sem.xlsx  ->  'All Subject Details' (long format)
Maps to app schema: marks(username, subject, exam, marks, max_marks, updated_at)

Design:
  - per-subject grade row:  subject='2-2 | <CODE>', exam='RESULT', marks=<grade_point>, max_marks=1000
  - overall row:            subject='2-2 | RESULT (PASS|FAIL)', exam='RESULT', marks=<sgpa*100>, max_marks=1000
  (template renders RESULT rows via exams.get('MID1') fallback: shows marks/10 when max_marks==1000)

Keeps existing MID1 internal rows intact (different exam key).
Idempotent: deletes prior RESULT rows for 2-2 before inserting.
"""
import sqlite3
from openpyxl import load_workbook

DB = "eee.db"
XLSX = "/data/data/com.termux/files/home/storage/downloads/college website/2-2sem.xlsx"

wb = load_workbook(XLSX, data_only=True)
ws = wb["All Subject Details"]
rows = list(ws.iter_rows(min_row=2, values_only=True))  # skip header
rows = [r for r in rows if r[1]]  # PIN / Hallticket No present

# collect: pin -> {subject_code: (grade_point, grade, status), ...}, sgpa, overall
students = {}
for r in rows:
    pin = str(r[1]).strip()
    name = r[2]
    sgpa = r[5]
    overall = r[6]
    code = str(r[10]).strip() if r[10] else ""
    grade = r[11]
    gp = r[12]
    status = r[14]
    d = students.setdefault(pin, {"name": name, "sgpa": sgpa, "overall": overall, "subs": {}})
    if code:
        d["subs"][code] = (gp, grade, status)

conn = sqlite3.connect(DB)
cur = conn.cursor()

# --- widen marks.exam CHECK to allow RESULT (keeps all existing rows) ---
# SQLite can't ALTER a CHECK, so recreate the table preserving data.
cur.execute("SELECT sql FROM sqlite_master WHERE name='marks'")
ddl = cur.fetchone()[0]
new_ddl = ddl.replace("CHECK(exam IN ('MID1','MID2'))", "CHECK(exam IN ('MID1','MID2','RESULT'))")
cur.execute("ALTER TABLE marks RENAME TO marks_old")
cur.execute(new_ddl)
cur.execute("INSERT INTO marks SELECT * FROM marks_old")
cur.execute("DROP TABLE marks_old")
conn.commit()
print("[migrate] marks CHECK widened to include RESULT; existing rows preserved")

# clear old RESULT rows for 2-2 (keep MID1/MID2 internal)
cur.execute("DELETE FROM marks WHERE subject LIKE '2-2 |%' AND exam='RESULT'")

inserted = 0
for pin, d in students.items():
    for code, (gp, grade, status) in d["subs"].items():
        cur.execute(
            "INSERT INTO marks(username, subject, exam, marks, max_marks) VALUES (?,?,?,?,?)",
            (pin, f"2-2 | {code}", "RESULT", gp or 0, 1000))
        inserted += 1
    # summary row: SGPA * 100 (so marks/10 => SGPA), overall pass/fail in subject
    overall = (d["overall"] or "").upper()
    passfail = "PASS" if "PASS" in overall else ("FAIL" if "FAIL" in overall else "RESULT")
    sgpa = d["sgpa"] or 0
    cur.execute(
        "INSERT INTO marks(username, subject, exam, marks, max_marks) VALUES (?,?,?,?,?)",
        (pin, f"2-2 | RESULT ({passfail})", "RESULT", int(round(sgpa * 100)), 1000))
    inserted += 1

conn.commit()

# report
print(f"students: {len(students)}")
print(f"rows inserted: {inserted} ({len(students)*9} subject + {len(students)} summary)")
conn.close()

# spot-check
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
for pin in ["24W61A0201", "25W65A0201"]:
    print(f"\n--- {pin} ---")
    for r in conn.execute("SELECT subject, exam, marks, max_marks FROM marks WHERE username=? AND exam='RESULT' ORDER BY subject", (pin,)).fetchall():
        print(f"  {r['subject']:22s} {r['exam']:7s} {r['marks']:>5} /{r['max_marks']}")
conn.close()
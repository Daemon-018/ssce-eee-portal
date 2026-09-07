#!/usr/bin/env python3
"""Import 2-2 (II B.Tech II Sem, R23 April 2026) results from the Excel workbook
into the marks table as labeled rows: '2-2 | <code>' + a per-student SGPA row."""
import pandas as pd
import sqlite3
from datetime import datetime

XL = '/sdcard/Download/college website/EEE_All_Students_All_Subjects_Results.xlsx'
DB = '/data/data/com.termux/files/home/eee_site/eee.db'
EXAM_TAG = 'MID1'      # schema CHECK allows only MID1/MID2; 2-2 externals stored under MID1
PREFIX = '2-2 | '

df = pd.read_excel(XL, sheet_name='All Subject Details')
df = df.dropna(subset=['PIN / Hallticket No'])

conn = sqlite3.connect(DB)
pins_in_db = {u for (u,) in conn.execute("SELECT username FROM users WHERE role='student'")}
df = df[df['PIN / Hallticket No'].isin(pins_in_db)]
print(f"Excel rows for known students: {len(df)} ({df['PIN / Hallticket No'].nunique()} students)")

grade_to_marks = {'S': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 6, 'E': 5, 'F': 0, 'AB': 0}
now = datetime.now().strftime('%Y-%m-%d %H:%M')

inserted = skipped = 0
for _, r in df.iterrows():
    pin = str(r['PIN / Hallticket No'])
    code = str(r['Course Code'])
    grade = str(r['Grade']).strip()
    pts = grade_to_marks.get(grade, 0)

    if conn.execute("SELECT id FROM marks WHERE username=? AND subject=? AND exam=?",
                    (pin, PREFIX + code, EXAM_TAG)).fetchone():
        skipped += 1
        continue
    conn.execute(
        "INSERT INTO marks (username, subject, exam, marks, max_marks, updated_at) VALUES (?,?,?,?,?,?)",
        (pin, PREFIX + code, EXAM_TAG, pts, 10, now))
    inserted += 1

# Per-student SGPA row: marks column is INTEGER NOT NULL -> store SGPA*100 (7.58 -> 758)
sgpa_rows = 0
g = df.groupby('PIN / Hallticket No').agg(SGPA=('SGPA', 'first'), RES=('Overall Result', 'first'))
for pin, row in g.iterrows():
    subj = PREFIX + 'SGPA & RESULT'
    if conn.execute("SELECT id FROM marks WHERE username=? AND subject=? AND exam=?",
                    (pin, subj, EXAM_TAG)).fetchone():
        continue
    sgpa100 = int(round(float(row['SGPA']) * 100)) if pd.notna(row['SGPA']) else 0
    res = str(row['RES']).strip() if pd.notna(row['RES']) else '-'
    conn.execute(
        "INSERT INTO marks (username, subject, exam, marks, max_marks, updated_at) VALUES (?,?,?,?,?,?)",
        (pin, subj, EXAM_TAG, sgpa100, 1000, now))
    sgpa_rows += 1

# Also update users.cgpa with the latest SGPA so profile page reflects it
for pin, row in g.iterrows():
    if pd.notna(row['SGPA']):
        conn.execute("UPDATE users SET cgpa=? WHERE username=?", (float(row['SGPA']), pin))

conn.commit()
c = conn.cursor()
c.execute("SELECT COUNT(*), COUNT(DISTINCT username) FROM marks WHERE subject LIKE '2-2%'")
total22, studs = c.fetchone()
conn.close()

print(f"subject rows inserted: {inserted} (dupes skipped: {skipped})")
print(f"SGPA rows inserted: {sgpa_rows}")
print(f"total '2-2 |' rows in DB: {total22} across {studs} students")

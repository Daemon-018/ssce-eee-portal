#!/usr/bin/env python3
"""v4.2: Add demo students for 1st, 2nd, 4th years + their attendance/marks.

Safe to run repeatedly. Does NOT touch syllabus/timetable/notices.
Only inserts missing students and their attendance/marks (upsert for marks).
"""
import os, sys
import sqlite3
from werkzeug.security import generate_password_hash

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eee.db")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seed_data import NEW_STUDENTS, STUDENT_ATTENDANCE, STUDENT_MARKS

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def year_label(username):
    if username.startswith("25W"): return "1st Year (2025 batch)"
    if username.startswith("24A"): return "2nd Year (2024 batch)"
    if username.startswith("21A"): return "3rd Year (2021 batch)"
    if username.startswith("20A"): return "4th Year (2020 batch)"
    return "1st Year (2025 batch)"

def entry_type(username):
    return "lateral" if username.startswith("25W") else "regular"

# 1. Insert missing students
added = 0
for username, name, password, email, section, batch, cgpa in NEW_STUDENTS:
    exists = cur.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
    if not exists:
        cur.execute(
            """INSERT INTO users (username,password_hash,role,name,email,section,year,batch,cgpa,designation,extra,entry)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (username, generate_password_hash(password), "student", name, email,
             section, year_label(username), batch, cgpa, "", f"Roll {username}", entry_type(username)))
        added += 1
print(f"[v4.2] students added: {added}")

# 2. Attendance (insert only if row missing; do not overwrite existing)
att_added = 0
for username, att_map in STUDENT_ATTENDANCE.items():
    for subj, (att, tot) in att_map.items():
        exists = cur.execute(
            "SELECT id FROM attendance WHERE username=? AND subject=?",
            (username, subj)).fetchone()
        if not exists:
            cur.execute(
                "INSERT INTO attendance (username,subject,attended,total) VALUES (?,?,?,?)",
                (username, subj, att, tot))
            att_added += 1
print(f"[v4.2] attendance rows added: {att_added}")

# 3. Marks (upsert - never reset existing)
marks_added = 0
for username, subj_map in STUDENT_MARKS.items():
    for subj, exams in subj_map.items():
        for exam, marks in exams.items():
            exists = cur.execute(
                "SELECT id FROM marks WHERE username=? AND subject=? AND exam=?",
                (username, subj, exam)).fetchone()
            if not exists:
                cur.execute(
                    "INSERT INTO marks (username,subject,exam,marks,max_marks) VALUES (?,?,?,?,30)",
                    (username, subj, exam, marks))
                marks_added += 1
print(f"[v4.2] marks rows added: {marks_added}")

conn.commit()

# Summary
print("\n=== STUDENTS BY YEAR ===")
for r in cur.execute("SELECT username, name, year, entry FROM users WHERE role='student' ORDER BY username"):
    print(f"  {r['username']} | {r['name']} | {r['year']} | {r['entry']}")
print(f"\nTOTAL students: {cur.execute('SELECT COUNT(*) FROM users WHERE role=?', ('student',)).fetchone()[0]}")

conn.close()
print("\n[v4.2] DONE")

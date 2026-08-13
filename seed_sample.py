"""Seed sample portal data (idempotent - safe to re-run)."""
import json
import sqlite3
from werkzeug.security import generate_password_hash
from db import get_db, init_db, seed_users
from seed_data import (NOTICES, TIMETABLE, SYLLABUS, STUDENTS,
                       STUDENT_ATTENDANCE, STUDENT_MARKS,
                       STUDY_MATERIALS, PYQ, SOLVED_PAPERS, ACADEMIC_CALENDAR,
                       BACKLOGS, EXAM_NOTIFICATIONS, MENTORSHIP,
                       JOB_RESOURCES, EXTRA_CLASSES, SYLLABUS_TRACKER,
                       NEW_STUDENTS, NEW_FACULTY)

init_db()
seed_users()
conn = get_db()

def clear(table):
    conn.execute(f"DELETE FROM {table}")

# --- students (insert if missing, refresh profile) ---
for username, name, email, section, batch, cgpa in STUDENTS:
    exists = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
    if exists:
        conn.execute(
            """UPDATE users SET name=?, email=?, section=?, batch=?, cgpa=? WHERE username=?""",
            (name, email, section, batch, cgpa, username),
        )
    else:
        conn.execute(
            """INSERT INTO users (username,password_hash,role,name,email,section,year,batch,cgpa,designation,extra)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (username, generate_password_hash("student123"), "student", name, email,
             section, "III-I (3rd Year, 1st Sem)", batch, cgpa, "", f"Roll {username}"),
        )
print(f"[seed] students: {len(STUDENTS)}")

# --- demo students across all years (custom passwords, insert if missing, never reset pw) ---
def year_label(username):
    """Map roll-number prefix -> year label."""
    if username.startswith("25W"):
        return "1st Year (2025 batch)"
    if username.startswith("24A"):
        return "2nd Year (2024 batch)"
    if username.startswith("21A"):
        return "3rd Year (2021 batch)"
    if username.startswith("20A"):
        return "4th Year (2020 batch)"
    return "1st Year (2025 batch)"

def entry_type(username):
    return "lateral" if username.startswith("25W") else "regular"

added_new = 0
for username, name, password, email, section, batch, cgpa in NEW_STUDENTS:
    exists = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
    if not exists:
        conn.execute(
            """INSERT INTO users (username,password_hash,role,name,email,section,year,batch,cgpa,designation,extra,entry)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (username, generate_password_hash(password), "student", name, email,
             section, year_label(username), batch, cgpa, "", f"Roll {username}", entry_type(username)),
        )
        added_new += 1
print(f"[seed] new students added: {added_new}")

# --- new faculty (custom passwords, insert if missing, never reset pw) ---
added_fac = 0
for username, password, name, email, designation, extra in NEW_FACULTY:
    exists = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
    if not exists:
        conn.execute(
            """INSERT INTO users (username,password_hash,role,name,email,section,year,batch,cgpa,designation,extra)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (username, generate_password_hash(password), "faculty", name, email,
             "", "", "", None, designation, extra),
        )
        added_fac += 1
print(f"[seed] new faculty added: {added_fac}")

# --- notices ---
clear("notices")
for title, body, cat, date in NOTICES:
    conn.execute(
        "INSERT INTO notices (title,body,category,posted_on,author) VALUES (?,?,?,?,?)",
        (title, body, cat, date, "EEE Office"),
    )
print(f"[seed] notices: {len(NOTICES)}")

# --- timetable ---
clear("timetable")
for day, period, subj, fac, room in TIMETABLE:
    conn.execute(
        """INSERT INTO timetable (program,year_sem,day,period,subject,faculty,room)
           VALUES ('B.Tech','3-1',?,?,?,?,?)""",
        (day, period, subj, fac, room),
    )
print(f"[seed] timetable: {len(TIMETABLE)} slots")

# --- syllabus ---
clear("syllabus")
for subj, code, creds, units in SYLLABUS:
    conn.execute(
        """INSERT INTO syllabus (program,year_sem,subject,code,credits,units)
           VALUES ('B.Tech','3-1',?,?,?,?)""",
        (subj, code, creds, json.dumps(units)),
    )
print(f"[seed] syllabus: {len(SYLLABUS)} subjects")

# --- attendance (all students) ---
clear("attendance")
count = 0
for username, att_map in STUDENT_ATTENDANCE.items():
    for subj, (att, tot) in att_map.items():
        conn.execute(
            "INSERT INTO attendance (username,subject,attended,total) VALUES (?,?,?,?)",
            (username, subj, att, tot),
        )
        count += 1
print(f"[seed] attendance: {count} rows")

# --- marks (all students, MID1 + MID2) ---
clear("marks")
count = 0
for username, subj_map in STUDENT_MARKS.items():
    for subj, exams in subj_map.items():
        for exam, marks in exams.items():
            conn.execute(
                """INSERT INTO marks (username,subject,exam,marks,max_marks)
                   VALUES (?,?,?,?,30)""",
                (username, subj, exam, marks),
            )
            count += 1
print(f"[seed] marks: {count} rows")

conn.commit()
conn.close()
print("[seed] DONE")

# ============ v3: new module seeding ============
conn = get_db()

def clear(table):
    conn.execute(f"DELETE FROM {table}")

# --- study materials ---
clear("study_materials")
for subj, title, kind, link in STUDY_MATERIALS:
    conn.execute(
        "INSERT INTO study_materials (subject,title,kind,link,uploaded_by) VALUES (?,?,?,?,?)",
        (subj, title, kind, link, "EEE Dept"),
    )
print(f"[seed] study_materials: {len(STUDY_MATERIALS)}")

# --- previous year question papers ---
clear("pyq")
for subj, year, exam, dl in PYQ:
    conn.execute(
        "INSERT INTO pyq (subject,year,exam,download) VALUES (?,?,?,?)",
        (subj, year, exam, dl),
    )
print(f"[seed] pyq: {len(PYQ)}")

# --- solved papers ---
clear("solved_papers")
for subj, year, exam, link in SOLVED_PAPERS:
    conn.execute(
        "INSERT INTO solved_papers (subject,year,exam,link) VALUES (?,?,?,?)",
        (subj, year, exam, link),
    )
print(f"[seed] solved_papers: {len(SOLVED_PAPERS)}")

# --- academic calendar ---
clear("academic_calendar")
for title, date, cat, note in ACADEMIC_CALENDAR:
    conn.execute(
        "INSERT INTO academic_calendar (title,event_date,category,note) VALUES (?,?,?,?)",
        (title, date, cat, note),
    )
print(f"[seed] academic_calendar: {len(ACADEMIC_CALENDAR)}")

# --- backlog tracker ---
clear("backlog")
count = 0
for username, rows in BACKLOGS.items():
    for subj, sem, attempts, cleared, cleared_date, note in rows:
        conn.execute(
            """INSERT INTO backlog (username,subject,sem,attempts,cleared,cleared_date,note)
               VALUES (?,?,?,?,?,?,?)""",
            (username, subj, sem, attempts, cleared, cleared_date, note),
        )
        count += 1
print(f"[seed] backlog: {count} rows")

# --- exam notifications ---
clear("exam_notifications")
for title, body, exam_type, link in EXAM_NOTIFICATIONS:
    conn.execute(
        "INSERT INTO exam_notifications (title,body,exam_type,link) VALUES (?,?,?,?)",
        (title, body, exam_type, link),
    )
print(f"[seed] exam_notifications: {len(EXAM_NOTIFICATIONS)}")

# --- mentorship ---
clear("mentorship")
for username, (mentor, last_m, next_m, notes) in MENTORSHIP.items():
    conn.execute(
        """INSERT INTO mentorship (username,mentor,last_meeting,next_meeting,notes)
           VALUES (?,?,?,?,?)""",
        (username, mentor, last_m, next_m, notes),
    )
print(f"[seed] mentorship: {len(MENTORSHIP)}")

# --- job resources ---
clear("job_resources")
for cat, title, desc, link in JOB_RESOURCES:
    conn.execute(
        "INSERT INTO job_resources (category,title,description,link) VALUES (?,?,?,?)",
        (cat, title, desc, link),
    )
print(f"[seed] job_resources: {len(JOB_RESOURCES)}")

# --- extra classes ---
clear("extra_classes")
for subj, topic, date, time, room, targeted, notes in EXTRA_CLASSES:
    conn.execute(
        """INSERT INTO extra_classes (subject,topic,date,time,room,targeted_to,notes,posted_by)
           VALUES (?,?,?,?,?,?,?,?)""",
        (subj, topic, date, time, room, targeted, notes, "EEE Office"),
    )
print(f"[seed] extra_classes: {len(EXTRA_CLASSES)}")

# --- syllabus tracker ---
clear("syllabus_tracker")
for subj, unit, status, covered in SYLLABUS_TRACKER:
    conn.execute(
        """INSERT INTO syllabus_tracker (subject,unit,status,covered_on,updated_by)
           VALUES (?,?,?,?,?)""",
        (subj, unit, status, covered, "EEE Office"),
    )
print(f"[seed] syllabus_tracker: {len(SYLLABUS_TRACKER)}")

conn.commit()
conn.close()
print("[seed] v3 DONE")
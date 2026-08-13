"""EEE Dept app - database layer v2 (portal modules)."""
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

DB_PATH = Path(__file__).parent / "eee.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student','faculty')),
    name TEXT NOT NULL,
    email TEXT DEFAULT '',
    section TEXT DEFAULT '',
    year TEXT DEFAULT '',
    batch TEXT DEFAULT '',
    cgpa REAL,
    designation TEXT DEFAULT '',
    extra TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS notices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    category TEXT DEFAULT 'General',
    posted_on TEXT DEFAULT (date('now','localtime')),
    author TEXT DEFAULT 'EEE Office'
);

CREATE TABLE IF NOT EXISTS timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program TEXT DEFAULT 'B.Tech',
    year_sem TEXT NOT NULL,
    day INTEGER NOT NULL,            -- 1=Mon .. 6=Sat
    period INTEGER NOT NULL,         -- 1..7
    subject TEXT NOT NULL,
    faculty TEXT DEFAULT '',
    room TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS syllabus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program TEXT DEFAULT 'B.Tech',
    year_sem TEXT NOT NULL,
    subject TEXT NOT NULL,
    code TEXT DEFAULT '',
    credits INTEGER DEFAULT 3,
    units TEXT DEFAULT '[]'          -- JSON list of {"unit":"I","topics":[...]}
);

CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    subject TEXT NOT NULL,
    attended INTEGER NOT NULL DEFAULT 0,
    total INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    subject TEXT NOT NULL,
    exam TEXT NOT NULL CHECK(exam IN ('MID1','MID2')),
    marks INTEGER NOT NULL,
    max_marks INTEGER DEFAULT 30,
    updated_at TEXT DEFAULT (datetime('now','localtime')),
    UNIQUE(username, subject, exam)
);

-- ============ v3: study support ============

CREATE TABLE IF NOT EXISTS study_materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    title TEXT NOT NULL,
    kind TEXT NOT NULL DEFAULT 'notes',   -- notes | pdf | link | ppt | video
    link TEXT DEFAULT '',
    uploaded_by TEXT DEFAULT 'EEE Dept',
    posted_on TEXT DEFAULT (date('now','localtime'))
);

CREATE TABLE IF NOT EXISTS pyq (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    year TEXT NOT NULL,
    exam TEXT NOT NULL DEFAULT 'Regular',  -- Regular | Supply
    download TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS solved_papers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    year TEXT NOT NULL,
    exam TEXT NOT NULL DEFAULT 'Regular',
    link TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS academic_calendar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    event_date TEXT NOT NULL,
    category TEXT DEFAULT 'Academic',
    note TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS backlog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    subject TEXT NOT NULL,
    sem TEXT NOT NULL,
    attempts INTEGER DEFAULT 0,
    cleared INTEGER DEFAULT 0,       -- 0=pending, 1=cleared
    cleared_date TEXT DEFAULT '',
    note TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS exam_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    exam_type TEXT NOT NULL,          -- Regular | Supply
    link TEXT DEFAULT '',
    posted_on TEXT DEFAULT (date('now','localtime'))
);

CREATE TABLE IF NOT EXISTS mentorship (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,           -- student roll
    mentor TEXT NOT NULL,
    last_meeting TEXT DEFAULT '',
    next_meeting TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    updated_at TEXT DEFAULT (datetime('now','localtime'))
);

-- ============ v3: career / jobs ============

CREATE TABLE IF NOT EXISTS job_resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,           -- core-govt | core-private | noncore-govt | noncore-private | reasoning | aptitude | arithmetic | resume
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    link TEXT DEFAULT '',
    posted_on TEXT DEFAULT (date('now','localtime'))
);

CREATE TABLE IF NOT EXISTS resume_builder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    data TEXT DEFAULT '{}',           -- JSON: {fullname,email,phone,objective,education:[],skills:[],projects:[],certifications:[],achievements:[]}
    updated_at TEXT DEFAULT (datetime('now','localtime'))
);

-- ============ v3: faculty tools ============

CREATE TABLE IF NOT EXISTS extra_classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT DEFAULT '',
    room TEXT DEFAULT '',
    targeted_to TEXT DEFAULT 'All',   -- All | backlog | specific usernames
    notes TEXT DEFAULT '',
    posted_by TEXT DEFAULT 'EEE Office'
);

CREATE TABLE IF NOT EXISTS syllabus_tracker (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    unit TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',    -- Pending | In Progress | Completed
    covered_on TEXT DEFAULT '',
    updated_by TEXT DEFAULT ''
);
"""

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    for stmt in SCHEMA.split(";"):
        stmt = stmt.strip()
        if stmt:
            conn.execute(stmt)
    # migration: add profile columns to users if missing (v1 -> v2)
    existing = {r["name"] for r in conn.execute("PRAGMA table_info(users)").fetchall()}
    for col, decl in [
        ("email", "TEXT DEFAULT ''"),
        ("section", "TEXT DEFAULT ''"),
        ("year", "TEXT DEFAULT ''"),
        ("batch", "TEXT DEFAULT ''"),
        ("cgpa", "REAL"),
        ("designation", "TEXT DEFAULT ''"),
    ]:
        if col not in existing:
            conn.execute(f"ALTER TABLE users ADD COLUMN {col} {decl}")
            print(f"[db] migrated: added users.{col}")
    conn.commit()
    conn.close()

def seed_users():
    conn = get_db()
    users = [
        ("21A31A0201", "student123", "student", "K. Venkata Surya",
         "surya.21a31a0201@srisivani.edu.in", "A", "III-I (3rd Year, 1st Sem)",
         "2021-25", 8.24, "", "Roll 21A31A0201"),
        ("faculty", "faculty123", "faculty", "Dr. G.T. Chandra Sekhar",
         "hod.eee@srisivani.edu.in", "", "", "", None,
         "Professor & HoD", "M.Tech, Ph.D. - 18 years experience"),
    ]
    for u in users:
        exists = conn.execute("SELECT id FROM users WHERE username=?", (u[0],)).fetchone()
        if not exists:
            conn.execute(
                """INSERT INTO users
                   (username,password_hash,role,name,email,section,year,batch,cgpa,designation,extra)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (u[0], generate_password_hash(u[1]), u[2], u[3], u[4],
                 u[5], u[6], u[7], u[8], u[9], u[10]),
            )
        else:
            # refresh profile data if the row already exists (idempotent)
            conn.execute(
                """UPDATE users SET name=?,email=?,section=?,year=?,batch=?,cgpa=?,designation=?,extra=?
                   WHERE username=?""",
                (u[3], u[4], u[5], u[6], u[7], u[8], u[9], u[10], u[0]),
            )
    conn.commit()
    conn.close()
    print("[db] seeded/refreshed demo users")

if __name__ == "__main__":
    init_db()
    seed_users()
    print(f"[db] OK -> {DB_PATH}")
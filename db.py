"""EEE Dept app - database layer v2 (portal modules)."""
import json
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

-- ============ v4: faculty profiles ============

CREATE TABLE IF NOT EXISTS faculty_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    photo TEXT DEFAULT '',            -- static/images/faculty/xxx.jpg
    designation TEXT DEFAULT '',
    qualification TEXT DEFAULT '',
    experience TEXT DEFAULT '',
    bio TEXT DEFAULT '',
    research TEXT DEFAULT '[]',       -- JSON array
    subjects TEXT DEFAULT '[]',       -- JSON array
    achievements TEXT DEFAULT '[]',   -- JSON array
    email TEXT DEFAULT '',
    cabin TEXT DEFAULT '',
    joined_year TEXT DEFAULT '',
    sort_order INTEGER DEFAULT 0,
    active INTEGER DEFAULT 1
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



def _ensure_leaves_gallery(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS leaves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        name TEXT NOT NULL,
        reason TEXT NOT NULL,
        from_date TEXT NOT NULL,
        to_date TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS gallery (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        filename TEXT,
        caption TEXT,
        added_at TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.commit()

def seed_users():
    conn = get_db()
    _ensure_leaves_gallery(conn)
    users = [
        ("faculty", "faculty123", "faculty", "Dr. G.T. Chandra Sekhar",
         "hod.eee@srisivani.edu.in", "", "", "", None,
         "Vice Principal", "M.Tech, Ph.D. - 18 years experience"),
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

def seed_faculty():
    conn = get_db()
    profiles = [
        # slug, name, photo, designation, qualification, experience, bio, research, subjects, achievements, email, cabin, joined, sort
        ("dr-g-t-chandra-sekhar", "Dr. G.T. Chandra Sekhar", "01_hod.jpg",
         "Vice Principal & Professor", "M.Tech, Ph.D.",
         "18+ years", "Experienced academic leader guiding the EEE department with a strong research background.",
         ["Power Systems", "Renewable Energy", "FACTS Devices"],
         ["Power System Protection", "Electrical Machines", "Renewable Energy Sources", "Power System Analysis"],
         ["Ph.D. in Power Systems", "18+ years of teaching", "Multiple research papers"],
         "hod.eee@srisivani.edu.in", "Block A - Office", "2008", 1),
        ("dr-kanthi-andhavarapu", "Dr. Kanthi Andhavarapu", "03_kanthi.jpg",
         "HoD of EEE", "M.Tech, Ph.D.",
         "15+ years", "Head of the EEE department, focused on curriculum excellence and student mentorship.",
         ["Power Electronics", "Drives", "Control Systems"],
         ["Power Electronics", "Electrical Drives", "Control Systems Engineering"],
         ["Ph.D., 15+ years experience", "Led department accreditation"],
         "kanthi.eee@srisivani.edu.in", "Block A - HoD Room", "2010", 2),
        ("ms-majji-sai-sudha", "Ms. Majji Sai Sudha", "04_saisudha.jpg",
         "Assistant Professor", "M.Tech",
         "8 years", "Dedicated educator passionate about making core EEE concepts accessible.",
         ["Power Electronics", "Digital Electronics"],
         ["Power Electronics", "Digital Electronics", "Basic Electrical Engineering"],
         ["M.Tech, 8 years experience"],
         "saisudha.eee@srisivani.edu.in", "Block A - Room 204", "2018", 3),
        ("ms-padmini-anakapalli", "Ms. Padmini Anakapalli", "07_padmini.jpg",
         "Diploma HoD of EEE", "M.Tech",
         "10 years", "Leads diploma-level EEE education, bridging theory with hands-on lab work.",
         ["Electrical Circuits", "Measurements", "Instrumentation"],
         ["Electrical Circuits", "Electrical Measurements", "Basic Electrical Engineering"],
         ["M.Tech, 10 years experience"],
         "padmini.eee@srisivani.edu.in", "Block B - Diploma Office", "2015", 4),
        ("mr-praveen-kumar-jammu", "Mr. Praveen Kumar Jammu", "08_praveen.jpg",
         "Assistant Professor", "M.Tech",
         "6 years", "Young faculty focused on modern teaching methods and student engagement.",
         ["Power Systems", "Machine Learning Applications"],
         ["Electrical Machines", "Power System Operation & Control", "Network Theory"],
         ["M.Tech, 6 years experience"],
         "praveen.eee@srisivani.edu.in", "Block A - Room 210", "2020", 5),
        ("mr-rajselvan", "Mr. Raj Selvan", "02_rajselvan.jpg",
         "Assistant Professor", "M.Tech",
         "7 years", "Specializes in control systems and automation with hands-on lab expertise.",
         ["Control Systems", "Automation", "PLC"],
         ["Control Systems", "Industrial Automation", "Signals & Systems"],
         ["M.Tech, 7 years experience", "PLC/SCADA certified"],
         "rajselvan.eee@srisivani.edu.in", "Block A - Room 212", "2019", 6),
        ("mr-gopi", "Mr. Gopi", "05_gopi.jpg",
         "Assistant Professor", "M.Tech",
         "5 years", "Passionate about electrical machines and power engineering fundamentals.",
         ["Electrical Machines", "Power Systems", "EMI/EMC"],
         ["Electrical Machines - I & II", "Electromagnetic Fields", "Power System Analysis"],
         ["M.Tech, 5 years experience"],
         "gopi.eee@srisivani.edu.in", "Block A - Room 214", "2021", 7),
        ("mr-sairajesh", "Mr. Sai Rajesh", "06_sairajesh.jpg",
         "Assistant Professor", "M.Tech",
         "4 years", "Focuses on network analysis and circuit theory with strong student rapport.",
         ["Network Theory", "Circuit Analysis", "Basic Electronics"],
         ["Network Theory", "Circuit Analysis", "Basic Electronics"],
         ["M.Tech, 4 years experience"],
         "sairajesh.eee@srisivani.edu.in", "Block A - Room 216", "2022", 8),
        ("mr-bhargav", "Mr. Bhargav", "09_bhargav.jpg",
         "Assistant Professor", "M.Tech",
         "3 years", "New-generation educator focusing on embedded systems and IoT for EEE.",
         ["Embedded Systems", "IoT", "Renewables"],
         ["Embedded Systems", "IoT Applications", "Renewable Energy"],
         ["M.Tech, 3 years experience", "IoT certified"],
         "bhargav.eee@srisivani.edu.in", "Block A - Room 218", "2023", 9),
    ]
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM faculty_profiles")
    if cur.fetchone()[0] == 0:
        for p in profiles:
            cur.execute(
                """INSERT INTO faculty_profiles
                   (slug,name,photo,designation,qualification,experience,bio,research,subjects,achievements,email,cabin,joined_year,sort_order,active)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)""",
                (p[0], p[1], p[2], p[3], p[4], p[5], p[6],
                 json.dumps(p[7]), json.dumps(p[8]), json.dumps(p[9]),
                 p[10], p[11], p[12], p[13]),
            )
        conn.commit()
        print("[db] seeded faculty profiles")
    conn.close()


if __name__ == "__main__":
    init_db()
    seed_users()
    print(f"[db] OK -> {DB_PATH}")
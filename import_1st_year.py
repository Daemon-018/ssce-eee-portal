#!/usr/bin/env python3
"""
Parse R23 EEE syllabus and populate database with 1st year data.
"""
import sqlite3
import re
import json
from pathlib import Path
from werkzeug.security import generate_password_hash

DB_PATH = Path(__file__).parent / "eee.db"

def parse_syllabus():
    """Extract all 1st year subjects from syllabus text."""
    with open("syllabus_raw.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    subjects = []
    
    # Find I Year I Semester section (line 32+)
    # Pattern: "1.  R23BS01 Linear Algebra & Calculus" or "2.  R23BS04T Chemistry"
    pattern = r'^\d+\.\s+(R\d{4}[A-Z]\d+[A-Z]?)\s+([^\n]+?)(?:\s*\n\s*\n|\s+\d+\s+\d+\s+\d+\s+\d+)'
    
    # Search in first year section only (lines 32-77)
    lines = text.split('\n')
    first_year_section = '\n'.join(lines[31:77])  # 0-indexed, so 31-76
    
    matches = re.findall(pattern, first_year_section, re.MULTILINE)
    print(f"Found {len(matches)} matches in I-I semester")
    
    for code, name in matches:
        name = name.strip()
        name = re.sub(r'\s+', ' ', name)
        
        subjects.append({
            'code': code.strip(),
            'name': name,
            'type': 'core' if 'ES' in code or 'PC' in code else 'basic'
        })
    
    return subjects

def parse_units(subject_name):
    """Extract units for a subject."""
    with open("syllabus_raw.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    # Find the subject section
    idx = text.find(subject_name)
    if idx == -1:
        return []
    
    # Look for UNIT patterns after the subject
    units = []
    unit_pattern = r'UNIT\s*([IVX]+)\s+(.+?)(?=\nUNIT\s*[IVX]+|\nTextbooks:|\nReference Books:|$)'
    
    matches = re.findall(unit_pattern, text[idx:idx+15000], re.DOTALL)
    
    for unit_num, unit_text in matches:
        unit_text = unit_text.strip()
        if unit_text and len(unit_text) > 10:
            units.append({
                'unit': unit_num.upper(),
                'topics': unit_text
            })
    
    return units

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
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
    
    CREATE TABLE IF NOT EXISTS syllabus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program TEXT DEFAULT 'B.Tech',
        year_sem TEXT NOT NULL,
        subject TEXT NOT NULL,
        code TEXT DEFAULT '',
        credits INTEGER DEFAULT 3,
        units TEXT DEFAULT '[]'
    );
    """
    
    conn = get_db()
    for stmt in SCHEMA.split(";"):
        stmt = stmt.strip()
        if stmt:
            try:
                conn.execute(stmt)
            except:
                pass
    conn.commit()
    conn.close()

def seed_1st_year_students():
    """Add 1st year students."""
    conn = get_db()
    
    students = [
        ("21A31A0101", "student123", "student", "K. Venkata Surya", "surya.21a31a0101@srisivani.edu.in", "A", "I-I", "2021-25", 7.5, "", "Roll 21A31A0101"),
        ("21A31A0102", "student123", "student", "R. Kishore Kumar", "kishore.21a31a0102@srisivani.edu.in", "B", "I-I", "2021-25", 7.8, "", "Roll 21A31A0102"),
        ("21A31A0103", "student123", "student", "M. Lakshmi", "lakshmi.21a31a0103@srisivani.edu.in", "A", "I-I", "2021-25", 8.0, "", "Roll 21A31A0103"),
        ("21A31A0104", "student123", "student", "C. Srinivas", "srinivas.21a31a0104@srisivani.edu.in", "B", "I-I", "2021-25", 7.2, "", "Roll 21A31A0104"),
        ("21A31A0105", "student123", "student", "P. Anusha", "anusha.21a31a0105@srisivani.edu.in", "A", "I-I", "2021-25", 8.5, "", "Roll 21A31A0105"),
        ("21A31A0106", "student123", "student", "V. Harish", "harish.21a31a0106@srisivani.edu.in", "B", "I-I", "2021-25", 7.6, "", "Roll 21A31A0106"),
    ]
    
    for u in students:
        exists = conn.execute("SELECT id FROM users WHERE username=?", (u[0],)).fetchone()
        if not exists:
            conn.execute("""
                INSERT INTO users (username,password_hash,role,name,email,section,year,batch,cgpa,designation,extra)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (u[0], generate_password_hash(u[1]), u[2], u[3], u[4], u[5], u[6], u[7], u[8], u[9], u[10]))
    
    conn.commit()
    conn.close()
    print(f"[db] seeded 6 1st year students")

def populate_syllabus():
    """Populate syllabus table with 1st year data."""
    subjects = parse_syllabus()
    print(f"Found {len(subjects)} subjects")
    
    conn = get_db()
    
    for subj in subjects:
        units = parse_units(subj['name'])
        units_json = json.dumps(units) if units else "[]"
        
        conn.execute("""
            INSERT OR REPLACE INTO syllabus (program, year_sem, subject, code, credits, units)
            VALUES ('B.Tech', 'I-I', ?, ?, 3, ?)
        """, (subj['name'], subj['code'], units_json))
    
    conn.commit()
    conn.close()
    print(f"[db] populated syllabus for {len(subjects)} subjects")

def main():
    print("=== EEE 1st Year Data Import ===")
    
    # Initialize DB
    init_db()
    
    # Seed 1st year students
    seed_1st_year_students()
    
    # Populate syllabus
    populate_syllabus()
    
    print("=== Done ===")

if __name__ == "__main__":
    main()

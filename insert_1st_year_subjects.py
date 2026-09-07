#!/usr/bin/env python3
"""Insert first-year (I-I) subjects into syllabus table."""
import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "eee.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def insert_subjects():
    subjects = [
        ("R23BS01", "Linear Algebra & Calculus"),
        ("R23BS04T", "Chemistry"),
        ("R23ES07T", "Introduction to Programming"),
        ("R23ES03", "Engineering Graphics"),
        ("R23ES04", "Basic Electrical & Electronics Engineering"),
        ("R23BS04P", "Chemistry Lab"),
        ("R23ES07P", "Computer Programming Lab"),
        ("R23ES05", "Electrical & Electronics Engineering Workshop"),
        ("R23MC02", "NSS/NCC/Scouts & Guides/Community Service"),
    ]
    conn = get_db()
    for code, name in subjects:
        conn.execute("""
            INSERT OR REPLACE INTO syllabus (program, year_sem, subject, code, credits, units)
            VALUES ('B.Tech', 'I-I', ?, ?, 3, '[]')
        """, (name, code))
    conn.commit()
    conn.close()
    print(f"Inserted {len(subjects)} first-year subjects")

if __name__ == "__main__":
    insert_subjects()

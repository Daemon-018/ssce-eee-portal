"""Export current eee.db into seed_data.py (regenerate seed after data changes).

Usage:
    .venv/bin/python export_seed.py

Then commit + push to deploy the new data to Render.
"""
import sqlite3

DB = "eee.db"
OUT = "seed_data.py"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
tables = [r[0] for r in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]

lines = []
lines.append('"""Auto-generated seed data for EEE dept portal (from live eee.db).')
lines.append('Rebuilds the full database on a fresh deploy (Render) - idempotent:')
lines.append('drops and recreates all tables, then inserts current data, preserving password hashes.')
lines.append('Regenerate with: .venv/bin/python export_seed.py')
lines.append('"""')
lines.append('')
lines.append('import sqlite3')
lines.append('')
lines.append('SCHEMA = {}')
lines.append('ROWS = {}')
lines.append('')

for t in tables:
    create_sql = conn.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{t}'").fetchone()[0]
    create_sql = create_sql.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
    lines.append('SCHEMA["%s"] = """%s"""' % (t, create_sql))
    lines.append('')

lines.append('')
lines.append('def build_db(db_path="eee.db"):')
lines.append('    conn = sqlite3.connect(db_path)')
lines.append('    conn.row_factory = sqlite3.Row')
lines.append('    for t in SCHEMA:')
lines.append('        conn.execute("DROP TABLE IF EXISTS %s" % t)')
lines.append('        conn.execute(SCHEMA[t])')
lines.append('')
lines.append('    for t, rows in ROWS.items():')
lines.append('        if not rows:')
lines.append('            continue')
lines.append('        cols = list(rows[0].keys())')
lines.append('        placeholders = ",".join("?" for _ in cols)')
lines.append('        collist = ",".join(cols)')
lines.append('        for r in rows:')
lines.append('            vals = [r.get(c) for c in cols]')
lines.append('            q = "INSERT INTO %s (%s) VALUES (%s)" % (t, collist, placeholders)')
lines.append('            conn.execute(q, vals)')
lines.append('    conn.commit()')
lines.append('    conn.close()')
lines.append('')
lines.append('if __name__ == "__main__":')
lines.append('    build_db()')
lines.append('    print("[seed] built DB with %d tables" % len(ROWS))')
lines.append('')

for t in tables:
    rows = conn.execute('SELECT * FROM "%s"' % t).fetchall()
    if not rows:
        lines.append('ROWS["%s"] = []' % t)
        continue
    rows_repr = [repr(dict(r)) for r in rows]
    lines.append('ROWS["%s"] = [%s]' % (t, ", ".join(rows_repr)))
    lines.append('')

with open(OUT, "w") as f:
    f.write("\n".join(lines))

print(f"[export] wrote {OUT} with {len(tables)} tables")
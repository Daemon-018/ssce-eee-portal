"""EEE Dept website - Sri Sivani College of Engineering.
Flask app: home, student login, faculty login, role dashboards.
"""
import functools
import json
import sqlite3
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, g)

from db import get_db, init_db, seed_users, seed_faculty
from seed_data import build_db

app = Flask(__name__)
app.secret_key = "ssce-eee-dev-key-change-me"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

init_db()
seed_users()
seed_faculty()

# Fresh-deploy bootstrap: if the DB has no real data, rebuild it fully from seed_data.py
_conn = get_db()
try:
    _n = _conn.execute("SELECT COUNT(*) FROM marks").fetchone()[0]
except Exception:
    _n = 0
_conn.close()
if _n == 0:
    print("[db] empty DB detected - rebuilding full dataset from seed_data.py")
    build_db()
    init_db()
    seed_users()


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def get_db_conn():
    if "db" not in g:
        g.db = get_db()
    return g.db


def login_required(role=None):
    def deco(view):
        @functools.wraps(view)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                flash("Please login first.", "error")
                return redirect(url_for("login", role=role or "student"))
            if role and session.get("role") != role:
                flash("You do not have access to that page.", "error")
                return redirect(url_for("dashboard"))
            return view(*args, **kwargs)
        return wrapped
    return deco


# ---------------- routes ----------------


@app.route("/")
def home():
    return render_template("home.html", faculty=_faculty_rows())


@app.route("/login/<role>")
def login(role="student"):
    if role not in ("student", "faculty"):
        return render_template("404.html"), 404
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html", role=role)


@app.route("/auth/login", methods=["POST"])
def do_login():
    role = request.form.get("role", "student")
    if role not in ("student", "faculty"):
        return "Bad role", 400
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    db = get_db_conn()
    user = db.execute(
        "SELECT * FROM users WHERE username=? COLLATE NOCASE AND role=?",
        (username, role)).fetchone()
    if user is None:
        flash("Invalid username or password.", "error")
        return redirect(url_for("login", role=role))

    from werkzeug.security import check_password_hash
    if not check_password_hash(user["password_hash"], password):
        flash("Invalid username or password.", "error")
        return redirect(url_for("login", role=role))

    session.clear()
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["name"] = user["name"]
    session["role"] = user["role"]
    session["is_admin"] = user["is_admin"] if "is_admin" in user else 0
    session["year"] = user["year"] or ""
    session.permanent = True
    flash(f"Welcome back, {user['name']}!", "success")
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
@login_required()
def dashboard():
    role = session["role"]
    return render_template("dashboard.html", role=role)


# ---------------- portal pages (student + faculty) ----------------


@app.route("/timetable")
@login_required()
def timetable():
    db = get_db_conn()
    rows = db.execute(
        """SELECT * FROM timetable WHERE program='B.Tech' AND year_sem='3-1'
           ORDER BY day, period""",
    ).fetchall()
    days = {1: "Monday", 2: "Tuesday", 3: "Wednesday",
            4: "Thursday", 5: "Friday", 6: "Saturday"}
    grid = {d: {p: None for p in range(1, 8)} for d in range(1, 7)}
    for r in rows:
        grid[r["day"]][r["period"]] = r
    theory, labs = set(), set()
    for r in rows:
        subj = r["subject"]
        if not subj or subj == "Lunch":
            continue
        if "Lab" in subj or "Lab" in (r["room"] or "") or subj == "Mentor Session / Sports":
            labs.add(subj)
        else:
            theory.add(subj)
    return render_template("timetable.html", grid=grid, days=days,
                           subjects={"theory": sorted(theory), "labs": sorted(labs)})


@app.route("/syllabus")
@login_required()
def syllabus():
    db = get_db_conn()
    sem = request.args.get("sem", "3-1")
    entry = "lateral"
    if session.get("role") == "student":
        me = db.execute("SELECT entry, year FROM users WHERE id=?", (session.get("user_id"),)).fetchone()
        entry = (me["entry"] if me and me["entry"] else "regular")
        is_first_year = bool(me and me["year"] and "1st Year" in me["year"])
        if entry == "lateral" and is_first_year:
            entry = "lateral1y"
    all_sems = ["1-1", "1-2", "2-1", "2-2", "3-1", "3-2", "4-1", "4-2"]
    allowed = all_sems if entry in ("regular", "lateral1y") else all_sems[2:]
    sems = [s for s in all_sems if s in allowed and db.execute(
        "SELECT COUNT(*) c FROM syllabus WHERE year_sem=?", (s,)).fetchone()["c"] > 0]
    if sem not in sems:
        sem = sems[0] if sems else "3-1"
    if session.get("role") == "student":
        me2 = db.execute("SELECT year FROM users WHERE id=?", (session.get("user_id"),)).fetchone()
        y = (me2["year"] if me2 and me2["year"] else "")
        default_sem = {"1st Year": "1-1", "2nd Year": "2-2", "3rd Year": "3-1", "4th Year": "4-1"}.get(
            next((k for k in ["1st Year", "2nd Year", "3rd Year", "4th Year"] if k in y), ""), sem)
        if default_sem in sems:
            sem = request.args.get("sem", default_sem)
    rows = db.execute(
        """SELECT * FROM syllabus WHERE program='B.Tech' AND year_sem=?
           ORDER BY code""", (sem,)).fetchall()
    import json as _json
    subjects = []
    for r in rows:
        d = dict(r)
        d["units"] = _json.loads(d["units"] or "[]")
        subjects.append(d)
    return render_template("syllabus.html", subjects=subjects, sems=sems, sem=sem, entry=entry)


@app.route("/attendance")
@login_required()
def attendance():
    if session["role"] != "student":
        return render_template("404.html"), 404
    db = get_db_conn()
    rows = db.execute(
        "SELECT * FROM attendance WHERE username=?", (session["username"],)
    ).fetchall()
    return render_template("attendance.html", rows=rows)


@app.route("/notices")
@login_required()
def notices():
    db = get_db_conn()
    rows = db.execute(
        "SELECT * FROM notices ORDER BY posted_on DESC, id DESC"
    ).fetchall()
    return render_template("notices.html", rows=rows)


@app.route("/profile")
@login_required()
def profile():
    db = get_db_conn()
    me = db.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()
    return render_template("profile.html", me=me)


# ---------------- faculty: attendance management ----------------


@app.route("/faculty/attendance")
@login_required(role="faculty")
def fac_attendance():
    db = get_db_conn()
    students = db.execute(
        "SELECT username,name,section FROM users WHERE role='student' ORDER BY username"
    ).fetchall()
    rows = db.execute(
        """SELECT a.*, u.name FROM attendance a
           JOIN users u ON u.username=a.username
           ORDER BY a.username, a.subject""",
    ).fetchall()
    data = {}
    for r in rows:
        data.setdefault(r["subject"], {})[r["username"]] = (r["attended"], r["total"])
    return render_template("fac_attendance.html", students=students,
                           subjects=sorted(data.keys()), data=data)


@app.route("/faculty/attendance/update", methods=["POST"])
@login_required(role="faculty")
def fac_attendance_update():
    db = get_db_conn()
    subject = request.form.get("subject", "").strip()
    username = request.form.get("username", "").strip()
    try:
        attended = int(request.form.get("attended", 0))
        total = int(request.form.get("total", 0))
    except ValueError:
        flash("Numbers only for attendance.", "error")
        return redirect(url_for("fac_attendance"))
    if attended < 0 or total < 0 or attended > total:
        flash("Invalid values: attended must be <= total.", "error")
        return redirect(url_for("fac_attendance"))
    exists = db.execute(
        "SELECT id FROM attendance WHERE username=? AND subject=?",
        (username, subject)).fetchone()
    if exists:
        db.execute(
            "UPDATE attendance SET attended=?, total=? WHERE username=? AND subject=?",
            (attended, total, username, subject))
    else:
        db.execute(
            "INSERT INTO attendance (username,subject,attended,total) VALUES (?,?,?,?)",
            (username, subject, attended, total))
    db.commit()
    flash(f"Attendance updated for {username} - {subject}.", "success")
    return redirect(url_for("fac_attendance"))


# ---------------- faculty: timetable editor ----------------


@app.route("/faculty/timetable")
@login_required(role="faculty")
def fac_timetable():
    db = get_db_conn()
    rows = db.execute(
        "SELECT * FROM timetable WHERE program='B.Tech' AND year_sem='3-1' ORDER BY day, period"
    ).fetchall()
    days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
    grid = {d: {p: None for p in range(1, 8)} for d in range(1, 7)}
    for r in rows:
        grid[r["day"]][r["period"]] = r
    return render_template("fac_timetable.html", grid=grid, days=days)


@app.route("/faculty/timetable/update", methods=["POST"])
@login_required(role="faculty")
def fac_timetable_update():
    db = get_db_conn()
    try:
        day = int(request.form.get("day"))
        period = int(request.form.get("period"))
    except (TypeError, ValueError):
        flash("Invalid slot.", "error")
        return redirect(url_for("fac_timetable"))
    subject = request.form.get("subject", "").strip()
    faculty = request.form.get("faculty", "").strip()
    room = request.form.get("room", "").strip()
    if not subject:
        flash("Subject cannot be empty.", "error")
        return redirect(url_for("fac_timetable"))
    exists = db.execute(
        "SELECT id FROM timetable WHERE program='B.Tech' AND year_sem='3-1' AND day=? AND period=?",
        (day, period)).fetchone()
    if exists:
        db.execute(
            """UPDATE timetable SET subject=?,faculty=?,room=?
               WHERE program='B.Tech' AND year_sem='3-1' AND day=? AND period=?""",
            (subject, faculty, room, day, period))
    else:
        db.execute(
            """INSERT INTO timetable (program,year_sem,day,period,subject,faculty,room)
               VALUES ('B.Tech','3-1',?,?,?,?,?)""",
            (day, period, subject, faculty, room))
    db.commit()
    flash(f"Slot updated: Day {day} Period {period}.", "success")
    return redirect(url_for("fac_timetable"))

# ---------------- marks (student view + faculty manage) ----------------


@app.route("/marks")
@login_required(role="student")
def marks():
    db = get_db_conn()
    rows = db.execute(
        "SELECT * FROM marks WHERE username=? ORDER BY subject, exam",
        (session["username"],)).fetchall()
    subj_map = {}
    for r in rows:
        subj_map.setdefault(r["subject"], {})[r["exam"]] = r
    return render_template("marks.html", subj_map=subj_map)


@app.route("/faculty/marks")
@login_required(role="faculty")
def fac_marks():
    db = get_db_conn()
    students = db.execute(
        "SELECT username,name,section FROM users WHERE role='student' ORDER BY username"
    ).fetchall()
    rows = db.execute(
        """SELECT m.*, u.name FROM marks m
           JOIN users u ON u.username=m.username
           ORDER BY m.subject, m.username, m.exam""",
    ).fetchall()
    data = {}
    for r in rows:
        data.setdefault(r["subject"], {}).setdefault(r["username"], {})[r["exam"]] = r
    return render_template("fac_marks.html", students=students, data=data)


@app.route("/faculty/marks/update", methods=["POST"])
@login_required(role="faculty")
def fac_marks_update():
    db = get_db_conn()
    subject = request.form.get("subject", "").strip()
    username = request.form.get("username", "").strip()
    exam = request.form.get("exam", "")
    if exam not in ("MID1", "MID2"):
        flash("Invalid exam.", "error")
        return redirect(url_for("fac_marks"))
    try:
        marks_val = int(request.form.get("marks", 0))
        max_marks = int(request.form.get("max_marks", 30))
    except ValueError:
        flash("Numbers only for marks.", "error")
        return redirect(url_for("fac_marks"))
    if marks_val < 0 or max_marks <= 0 or marks_val > max_marks:
        flash("Invalid marks range.", "error")
        return redirect(url_for("fac_marks"))
    exists = db.execute(
        "SELECT id FROM marks WHERE username=? AND subject=? AND exam=?",
        (username, subject, exam)).fetchone()
    if exists:
        db.execute(
            """UPDATE marks SET marks=?,max_marks=?,updated_at=datetime('now','localtime')
                           WHERE username=? AND subject=? AND exam=?""",
            (marks_val, max_marks, username, subject, exam))
    else:
        db.execute(
            """INSERT INTO marks (username,subject,exam,marks,max_marks)
               VALUES (?,?,?,?,?)""",
            (username, subject, exam, marks_val, max_marks))
    db.commit()
    flash(f"Marks saved: {username} - {subject} - {exam}.", "success")
    return redirect(url_for("fac_marks"))


@app.route("/admin/edit/<path:filepath>", methods=["GET", "POST"])
@login_required(role="faculty")
def admin_edit_file(filepath):
    if not session.get("is_admin"):
        flash("Super Admin access required.", "error")
        return redirect(url_for("dashboard"))
    
    root = "/data/data/com.termux/files/home/eee_site"
    full_path = f"{root}/{filepath}"
    
    if not full_path.startswith(root):
        return "Access Denied", 403

    if request.method == "POST":
        new_content = request.form.get("content", "")
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        flash(f"File {filepath} updated successfully!", "success")
        return redirect(url_for("admin_edit_file", filepath=filepath))

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return "File not found", 404

    return render_template("admin_edit.html", content=content, filepath=filepath)

# ---------------- study support (student + faculty view) ----------------


def _subject_filter_kw():
    return {"program": "B.Tech", "year_sem": "3-1"}


@app.route("/study-materials")
@login_required()
def study_materials():
    db = get_db_conn()
    rows = db.execute(
        "SELECT * FROM study_materials ORDER BY subject, posted_on DESC, id DESC"
    ).fetchall()
    by_subject = {}
    for r in rows:
        by_subject.setdefault(r["subject"], []).append(r)
    return render_template("study_materials.html", by_subject=by_subject)


@app.route("/pyq")
@login_required()
def pyq():
    db = get_db_conn()
    rows = db.execute("SELECT * FROM pyq ORDER BY subject, year DESC, exam").fetchall()
    by_subject = {}
    for r in rows:
        by_subject.setdefault(r["subject"], []).append(r)
    return render_template("pyq.html", by_subject=by_subject)


@app.route("/solved-papers")
@login_required()
def solved_papers():
    db = get_db_conn()
    rows = db.execute("SELECT * FROM solved_papers ORDER BY subject, year DESC, exam").fetchall()
    by_subject = {}
    for r in rows:
        by_subject.setdefault(r["subject"], []).append(r)
    return render_template("solved_papers.html", by_subject=by_subject)


@app.route("/academic-calendar")
@login_required()
def academic_calendar():
    db = get_db_conn()
    rows = db.execute("SELECT * FROM academic_calendar ORDER BY event_date").fetchall()
    return render_template("academic_calendar.html", rows=rows)


@app.route("/backlog-tracker")
@login_required()
def backlog_tracker():
    db = get_db_conn()
    if session["role"] == "student":
        rows = db.execute(
            "SELECT * FROM backlog WHERE username=? ORDER BY cleared, sem, subject",
            (session["username"],)
        ).fetchall()
    else:
        rows = db.execute(
            """SELECT b.*, u.name FROM backlog b
               JOIN users u ON u.username=b.username
               ORDER BY b.cleared, b.sem, b.subject""",
        ).fetchall()
    pending = [r for r in rows if not r["cleared"]]
    cleared = [r for r in rows if r["cleared"]]
    return render_template("backlog_tracker.html", rows=rows,
                           pending=pending, cleared=cleared)

@app.route("/exam-notifications")
@login_required()
def exam_notifications():
    db = get_db_conn()
    rows = db.execute(
        "SELECT * FROM exam_notifications ORDER BY posted_on DESC, id DESC"
    ).fetchall()
    return render_template("exam_notifications.html", rows=rows)


JOB_CATEGORY_META = [
    ("core", "Core Jobs", "Power, energy and electrical core roles."),
    ("noncore", "Non-Core Jobs", "IT, services and analytics roles."),
    ("reasoning", "Reasoning Practice", "Logical and verbal reasoning resources."),
    ("aptitude", "Aptitude Practice", "Quantitative aptitude for placements and govt exams."),
    ("arithmetic", "Arithmetic Practice", "Speed arithmetic and shortcut techniques."),
]


@app.route("/careers")
@login_required()
def careers():
    db = get_db_conn()
    rows = db.execute(
        "SELECT * FROM job_resources ORDER BY category, title"
    ).fetchall() if db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='job_resources'").fetchone() else []
    groups = {}
    for r in rows:
        groups.setdefault(r["category"], []).append(r)
    return render_template("careers.html", groups=groups, meta=JOB_CATEGORY_META)


# ============ faculty profiles (public) ============

def _faculty_rows():
    db = get_db_conn()
    rows = db.execute(
        "SELECT * FROM faculty_profiles WHERE active=1 ORDER BY sort_order, name"
    ).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        for k in ("research", "subjects", "achievements"):
            try:
                d[k] = json.loads(d[k] or "[]")
            except Exception:
                d[k] = []
        out.append(d)
    return out


@app.route("/faculty")
def faculty_list():
    return render_template("faculty.html", faculty=_faculty_rows())


@app.route("/faculty/<slug>")
def faculty_detail(slug):
    rows = _faculty_rows()
    prof = next((r for r in rows if r["slug"] == slug), None)
    if not prof:
        return render_template("404.html"), 404
    return render_template("faculty_detail.html", prof=prof)


@app.route("/faculty/manage", methods=["GET", "POST"])
@login_required(role="faculty")
def faculty_manage():
    db = get_db_conn()
    if request.method == "POST":
        fid = request.form.get("fid", "")
        name = request.form.get("name", "").strip()
        photo = request.form.get("photo", "").strip() or "01_hod.jpg"
        slug = request.form.get("slug", "").strip() or (
            name.lower().replace(".", "").replace(",", "")
            .replace("&", "and").replace("  ", " ")
            .replace(" ", "-").replace("--", "-")
        )
        designation = request.form.get("designation", "").strip()
        qualification = request.form.get("qualification", "").strip()
        experience = request.form.get("experience", "").strip()
        bio = request.form.get("bio", "").strip()
        research = json.dumps([x.strip() for x in request.form.get("research", "").split(",") if x.strip()])
        subjects = json.dumps([x.strip() for x in request.form.get("subjects", "").split(",") if x.strip()])
        achievements = json.dumps([x.strip() for x in request.form.get("achievements", "").split(",") if x.strip()])
        email = request.form.get("email", "").strip()
        cabin = request.form.get("cabin", "").strip()
        joined = request.form.get("joined_year", "").strip()
        sort_order = int(request.form.get("sort_order", "0") or 0)
        if not name:
            flash("Name is required.", "error")
        elif fid:
            db.execute(
                """UPDATE faculty_profiles SET slug=?,name=?,photo=?,designation=?,qualification=?,
                   experience=?,bio=?,research=?,subjects=?,achievements=?,email=?,cabin=?,joined_year=?,sort_order=?
                   WHERE id=?""",
                (slug, name, photo, designation, qualification, experience, bio,
                 research, subjects, achievements, email, cabin, joined, sort_order, fid),
            )
            db.commit()
            flash("Faculty profile updated.", "success")
        else:
            db.execute(
                """INSERT INTO faculty_profiles
                   (slug,name,photo,designation,qualification,experience,bio,research,subjects,achievements,email,cabin,joined_year,sort_order,active)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)""",
                (slug, name, photo, designation, qualification, experience, bio,
                 research, subjects, achievements, email, cabin, joined, sort_order),
            )
            db.commit()
            flash("Faculty profile added.", "success")
        return redirect(url_for("faculty_manage"))
    rows = db.execute("SELECT * FROM faculty_profiles ORDER BY sort_order, name").fetchall()
    faculty = []
    for r in rows:
        d = dict(r)
        for k in ("research", "subjects", "achievements"):
            try:
                d[k] = json.loads(d[k] or "[]")
            except Exception:
                d[k] = []
        faculty.append(d)
    return render_template("faculty_manage.html", faculty=faculty)


@app.route("/faculty/manage/<int:fid>/delete", methods=["POST"])
@login_required(role="faculty")
def faculty_delete(fid):
    db = get_db_conn()
    db.execute("DELETE FROM faculty_profiles WHERE id=?", (fid,))
    db.commit()
    flash("Faculty profile deleted.", "success")
    return redirect(url_for("faculty_manage"))


@app.route("/resume-builder", methods=["GET", "POST"])
@login_required()
def resume_builder():
    db = get_db_conn()
    me = db.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone() if session.get("user_id") else None
    if request.method == "POST":
        me2 = dict(me) if me else {}
        data = {
            "fullname": request.form.get("fullname", me2.get("name", "")),
            "email": request.form.get("email", me2.get("email", "")),
            "phone": request.form.get("phone", ""),
            "objective": request.form.get("objective", ""),
            "education": request.form.get("education", "").splitlines(),
            "skills": request.form.get("skills", "").splitlines(),
            "projects": request.form.get("projects", "").splitlines(),
            "certifications": request.form.get("certifications", "").splitlines(),
            "achievements": request.form.get("achievements", "").splitlines(),
        }
        session["resume"] = data
        flash("Resume saved.", "success")
        return redirect(url_for("resume_builder"))
    data = session.get("resume")
    if not data:
        data = {
            "fullname": me["name"] if me else "",
            "email": me["email"] if me else "",
            "phone": "",
            "objective": "",
            "education": [], "skills": [], "projects": [],
            "certifications": [], "achievements": [],
        }
    return render_template("resume_builder.html", data=data)


@app.route("/resume-print")
@login_required()
def resume_print():
    db = get_db_conn()
    me = db.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone() if session.get("user_id") else None
    data = session.get("resume")
    if not data:
        data = {
            "fullname": me["name"] if me else "",
            "email": me["email"] if me else "",
            "phone": "", "objective": "",
            "education": [], "skills": [], "projects": [],
            "certifications": [], "achievements": [],
        }
    return render_template("resume_print.html", data=data)


@app.route("/change-password", methods=["GET", "POST"])
@login_required()
def change_password():
    db = get_db_conn()
    if request.method == "POST":
        cur = request.form.get("current", "")
        new = request.form.get("new", "")
        conf = request.form.get("confirm", "")
        if not new or len(new) < 4:
            flash("New password must be at least 4 characters.", "error")
            return redirect(url_for("change_password"))
        if new != conf:
            flash("New passwords do not match.", "error")
            return redirect(url_for("change_password"))
        u = db.execute("SELECT password_hash FROM users WHERE id=?", (session["user_id"],)).fetchone()
        from werkzeug.security import check_password_hash, generate_password_hash
        if not u or not check_password_hash(u["password_hash"], cur):
            flash("Current password is incorrect.", "error")
            return redirect(url_for("change_password"))
        db.execute("UPDATE users SET password_hash=? WHERE id=?", (generate_password_hash(new), session["user_id"]))
        db.commit()
        flash("Password updated.", "success")
        return redirect(url_for("dashboard"))
    return render_template("change_password.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


SUBJECT_ORDER = ["Power System Analysis - II", "Power Electronics - II",
                 "Electrical Machine Design", "Control Systems",
                 "Microprocessors & Microcontrollers", "Digital Signal Processing"]


def _analysis_for_student(db, username):
    """Compute strengths / weaknesses / risk per subject from marks + attendance."""
    marks = db.execute(
        "SELECT * FROM marks WHERE username=? ORDER BY subject, exam", (username,)
    ).fetchall()
    att = db.execute(
        "SELECT * FROM attendance WHERE username=?", (username,)
    ).fetchall()
    att_map = {r["subject"]: (r["attended"], r["total"]) for r in att}
    subj_rows = db.execute(
        "SELECT * FROM syllabus ORDER BY code"
    ).fetchall() if db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='syllabus'").fetchone() else []
    subject_names = [r["subject"] for r in subj_rows] or SUBJECT_ORDER

    per_subject = {}
    for s in subject_names:
        m = [x for x in marks if x["subject"] == s]
        best = max([x["marks"] for x in m], default=0)
        total = max([x["max_marks"] for x in m], default=30)
        pct = round(best / total * 100) if total else 0
        a = att_map.get(s, (0, 0))
        att_pct = round(a[0] / a[1] * 100) if a[1] else 0
        per_subject[s] = {"best": best, "pct": pct, "att": att_pct}

    status = []
    for s, d in per_subject.items():
        if d["pct"] >= 75:
            status.append((s, "strong", f"Strong · best {d['best']}/30"))
        elif d["pct"] >= 50:
            status.append((s, "ok", f"Average · best {d['best']}/30"))
        else:
            status.append((s, "weak", f"Weak · best {d['best']}/30"))

    strengths = [x for x in status if x[1] == "strong"]
    weaknesses = [x for x in status if x[1] in ("ok", "weak")]
    risk = [x for x in status if x[1] == "weak" or per_subject[x[0]]["att"] < 75]
    overall = round(sum(d["pct"] for d in per_subject.values()) / len(per_subject)) if per_subject else 0
    att_overall = round(sum(d["att"] for d in per_subject.values()) / len(per_subject)) if per_subject else 0
    return {"per_subject": per_subject, "strengths": strengths,
            "weaknesses": weaknesses, "risk": risk, "overall": overall,
            "att_overall": att_overall}


@app.route("/faculty/performance")
@login_required(role="faculty")
def fac_performance():
    db = get_db_conn()
    students = db.execute(
        "SELECT username,name,section FROM users WHERE role='student' ORDER BY username"
    ).fetchall()
    sel = request.args.get("student", students[0]["username"] if students else "")
    analysis = _analysis_for_student(db, sel) if sel else None
    return render_template("fac_performance.html", students=students, sel=sel,
                           analysis=analysis)


@app.route("/faculty/extra-classes", methods=["GET", "POST"])
@login_required(role="faculty")
def fac_extra_classes():
    db = get_db_conn()
    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        topic = request.form.get("topic", "").strip()
        date = request.form.get("date", "").strip()
        time = request.form.get("time", "").strip()
        room = request.form.get("room", "").strip()
        targeted = request.form.get("targeted_to", "All").strip()
        notes = request.form.get("notes", "").strip()
        if not subject or not topic or not date:
            flash("Subject, topic and date are required.", "error")
        else:
            db.execute(
                """INSERT INTO extra_classes (subject,topic,date,time,room,targeted_to,notes,posted_by)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (subject, topic, date, time, room, targeted, notes, session.get("name", "EEE Office")),
            )
            db.commit()
            flash(f"Extra class scheduled: {subject} - {topic}.", "success")
        return redirect(url_for("fac_extra_classes"))
    rows = db.execute("SELECT * FROM extra_classes ORDER BY date, time").fetchall()
    students = db.execute(
        "SELECT username,name FROM users WHERE role='student' ORDER BY username"
    ).fetchall()
    return render_template("fac_extra_classes.html", rows=rows, students=students)


@app.route("/faculty/syllabus-tracker", methods=["GET", "POST"])
@login_required(role="faculty")
def fac_syllabus_tracker():
    db = get_db_conn()
    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        unit = request.form.get("unit", "").strip()
        status = request.form.get("status", "Pending").strip()
        if not subject or not unit or status not in ("Pending", "In Progress", "Completed"):
            flash("Invalid values.", "error")
        else:
            covered_on = ""
            if status == "Completed":
                covered_on = request.form.get("covered_on", "").strip() or \
                             __import__("datetime").date.today().isoformat()
            exists = db.execute(
                "SELECT id FROM syllabus_tracker WHERE subject=? AND unit=?",
                (subject, unit)).fetchone()
            if exists:
                db.execute(
                    """UPDATE syllabus_tracker SET status=?, covered_on=?, updated_by=?
                       WHERE subject=? AND unit=?""",
                    (status, covered_on, session.get("name", "EEE Office"), subject, unit),
                )
            else:
                db.execute(
                    """INSERT INTO syllabus_tracker (subject,unit,status,covered_on,updated_by)
                       VALUES (?,?,?,?,?)""",
                    (subject, unit, status, covered_on, session.get("name", "EEE Office")),
                )
            db.commit()
            flash(f"Tracker updated: {subject} Unit {unit} -> {status}.", "success")
        return redirect(url_for("fac_syllabus_tracker"))
    rows = db.execute(
        "SELECT * FROM syllabus_tracker ORDER BY subject, unit"
    ).fetchall() if db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='syllabus_tracker'").fetchone() else []
    subjects = sorted({r["subject"] for r in rows})
    return render_template("fac_syllabus_tracker.html", rows=rows, subjects=subjects)


@app.route("/apply-leave", methods=["GET", "POST"])
@login_required(role="student")
def apply_leave():
    db = get_db_conn()
    if request.method == "POST":
        reason = request.form.get("reason", "").strip()
        from_date = request.form.get("from_date", "").strip()
        to_date = request.form.get("to_date", "").strip()
        if not reason or not from_date or not to_date:
            flash("Fill in reason and dates.", "error")
            return redirect(url_for("apply_leave"))
        if from_date > to_date:
            flash("From date cannot be after to date.", "error")
            return redirect(url_for("apply_leave"))
        db.execute(
            "INSERT INTO leaves (username,name,reason,from_date,to_date) VALUES (?,?,?,?,?)",
            (session["username"], session.get("name", ""), reason, from_date, to_date))
        db.commit()
        flash("Leave request submitted — pending approval.", "success")
        return redirect(url_for("apply_leave"))
    rows = db.execute(
        "SELECT * FROM leaves WHERE username=? ORDER BY id DESC",
        (session["username"],)).fetchall()
    return render_template("apply_leave.html", rows=rows)


@app.route("/gallery")
def gallery():
    db = get_db_conn()
    rows = db.execute("SELECT * FROM gallery ORDER BY id DESC").fetchall()
    return render_template("gallery.html", rows=rows)


@app.route("/mentorship")
@login_required()
def mentorship():
    db = get_db_conn()
    if session["role"] == "student":
        rows = db.execute(
            "SELECT * FROM mentorship WHERE username=? ORDER BY username",
            (session["username"],)).fetchall()
    else:
        rows = db.execute(
            """SELECT m.*, u.name FROM mentorship m
               JOIN users u ON u.username=m.username
               ORDER BY m.username""",
        ).fetchall()
    return render_template("mentorship.html", rows=rows)


@app.route("/extra-classes")
@login_required()
def extra_classes():
    db = get_db_conn()
    rows = db.execute(
        "SELECT * FROM extra_classes ORDER BY date, time"
    ).fetchall()
    return render_template("extra_classes.html", rows=rows)
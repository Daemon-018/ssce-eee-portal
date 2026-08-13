#!/usr/bin/env python3
"""v4.1: Add 1-1 & 1-2 semesters + regular/lateral student entry type.

- Adds REAL 1st year R23 subjects (1-1, 1-2) to syllabus
- Adds `entry` column to users: 'regular' (8 sems) or 'lateral' (6 sems)
- Marks existing 2021-batch students as regular, 2025-batch as lateral
- Syllabus page filters semesters by student entry type
"""
import sqlite3, json, os, shutil

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eee.db")
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

REAL_SYLLABUS_1YR = [
    # ---- 1-1 ----
    ("B.Tech", "1-1", "Linear Algebra and Calculus", "R23BS01", 3, [
        ["I", ["Matrices", "Rank of a matrix by echelon and normal form", "Gauss-Jordan method", "System of linear equations", "Gauss Seidel iteration method"]],
        ["II", ["Linear Transformation and Orthogonal Transformation", "Eigenvalues and eigenvectors", "Cayley-Hamilton theorem", "Diagonalization"]],
        ["III", ["Calculus", "Rolle's theorem", "Lagrange's and Cauchy's mean value theorems", "Taylor's and Maclaurin's series"]],
        ["IV", ["Partial differentiation and Applications", "Multi variable calculus", "Jacobians", "Maxima and minima of functions of two variables"]],
        ["V", ["Multiple Integrals", "Double and triple integrals", "Change of order of integration", "Areas and volumes"]],
    ]),
    ("B.Tech", "1-1", "Chemistry", "R23BS04T", 3, [
        ["I", ["Polymer Chemistry", "Functionality of monomers", "Chain growth and step growth polymerization", "Plastics - thermosetting and thermoplastic"]],
        ["II", ["Electrochemistry and Applications", "Nernst equation", "Electrochemical cells", "Batteries - primary and secondary", "Corrosion and its prevention"]],
        ["III", ["Modern Engineering materials", "Composites", "Ceramics", "Lubricants", "Refractories", "Building materials"]],
        ["IV", ["Instrumental Methods and Applications", "Spectroscopy - UV, IR, NMR", "Chromatography - TLC, HPLC", "Thermal analysis"]],
        ["V", ["Surface Chemistry and Nanomaterials", "Adsorption - physisorption and chemisorption", "Langmuir isotherm", "Catalysis", "Nanoparticles and their applications", "Carbon nanotubes"]],
    ]),
    ("B.Tech", "1-1", "Introduction to Programming", "R23ES07T", 3, [
        ["I", ["Introduction to Computer Problem Solving", "Problem solving techniques", "Flowcharts and algorithms", "Pseudocode"]],
        ["II", ["Introduction to C Programming", "Structure of C program", "Data types, operators", "Control statements", "Loops"]],
        ["III", ["Arrays", "One and two dimensional arrays", "String handling", "Matrix operations"]],
        ["IV", ["Functions", "Function declaration and definition", "Parameter passing", "Recursion", "Storage classes"]],
        ["V", ["Structures and Unions", "Nested structures", "Arrays of structures", "Pointers to structures", "Bit fields"]],
    ]),
    ("B.Tech", "1-1", "Engineering Graphics", "R23ES03", 3, [
        ["I", ["Introduction", "Lines, lettering and dimensioning", "Geometrical constructions", "Constructing regular polygons"]],
        ["II", ["Orthographic Projections", "Reference planes", "Projections of points and lines", "Projections of planes"]],
        ["III", ["Projections of Solids", "Types of solids - polyhedra and solids of revolution", "Projections of solids in simple positions"]],
        ["IV", ["Sections of Solids", "Perpendicular and inclined section planes", "Sectional views and true shape of section"]],
        ["V", ["Conversion of Views", "Isometric to orthographic views", "Orthographic to isometric views", "Development of surfaces"]],
    ]),
    ("B.Tech", "1-1", "Basic Electrical and Electronics Engineering", "R23ES04", 3, [
        ["I", ["DC and AC Circuits", "Ohm's law, Kirchhoff's laws", "Series and parallel circuits", "Mesh and nodal analysis", "AC fundamentals, RMS and average values"]],
        ["II", ["Machines and Measuring Instruments", "DC machines - principle and types", "Transformers - principle", "AC machines overview", "Voltmeters, ammeters, wattmeters"]],
        ["III", ["Energy Resources, Electricity Bill and Safety Measures", "Conventional and renewable energy sources", "Electricity bill calculation", "Electrical safety and earthing"]],
        ["IV", ["Semiconductor Devices", "PN junction diode", "Rectifiers", "Zener diode", "BJT and FET basics"]],
        ["V", ["Basic Electronic Circuits and Instrumentation", "Amplifiers", "Oscillators", "Digital electronics basics", "Electronic instruments"]],
    ]),
    # ---- 1-2 ----
    ("B.Tech", "1-2", "Differential Equations and Vector Calculus", "R23BS02", 3, [
        ["I", ["Differential equations of first order and first degree", "Linear differential equations - Bernoulli's equations", "Exact equations", "Orthogonal trajectories"]],
        ["II", ["Linear differential equations of higher order", "Constant coefficients", "Method of variation of parameters", "Cauchy's and Legendre's equations"]],
        ["III", ["Partial Differential Equations", "Formation of PDEs", "First order PDEs - Lagrange's method", "Method of separation of variables"]],
        ["IV", ["Vector differentiation", "Gradient, divergence and curl", "Directional derivatives", "Vector identities"]],
        ["V", ["Vector integration", "Line, surface and volume integrals", "Green's theorem", "Stoke's theorem", "Gauss divergence theorem"]],
    ]),
    ("B.Tech", "1-2", "Engineering Physics", "R23BS03T", 3, [
        ["I", ["Wave Optics", "Interference in thin films", "Newton's rings", "Diffraction - Fresnel and Fraunhofer", "Polarization"]],
        ["II", ["Crystallography", "Space lattice and basis", "Bravais lattices", "Crystal structures", "Bragg's X-ray diffractometer"]],
        ["III", ["Dielectric and Magnetic Materials", "Dielectric constant and polarization", "Lorentz field and Claussius-Mosotti relation", "Magnetic materials and their classification"]],
        ["IV", ["Quantum Mechanics and Free electron theory", "Dual nature of matter", "Schrodinger's wave equation", "Particle in a potential well", "Classical and quantum free electron theory"]],
        ["V", ["Semiconductors", "Intrinsic and extrinsic semiconductors", "Hall effect", "Effective mass of electron", "Semiconductor devices"]],
    ]),
    ("B.Tech", "1-2", "Communicative English", "R23HS01T", 2, [
        ["I", ["Human Values", "A Power of a Plate of Rice by Ifeoma Okoye", "Comprehension and vocabulary building"]],
        ["II", ["Nature", "Night of the Scorpion by Nissim Ezekiel", "Indian contemporary poetry"]],
        ["III", ["Biography", "Steve Jobs", "Reading and summarizing skills"]],
        ["IV", ["Inspiration", "The Toys of Peace by Saki", "Critical analysis"]],
        ["V", ["Motivation", "The Power of Intrapersonal Communication", "Essay writing and presentation"]],
    ]),
    ("B.Tech", "1-2", "Basic Civil and Mechanical Engineering", "R23ES01", 3, [
        ["I", ["Basics of Civil Engineering", "Role of civil engineers in society", "Disciplines of civil engineering", "Building materials"]],
        ["II", ["Surveying", "Objectives of surveying", "Horizontal and angular measurements", "Levelling"]],
        ["III", ["Transportation Engineering", "Importance of transportation", "Highway, railway, airport engineering basics"]],
        ["IV", ["Introduction to Mechanical Engineering", "Role of mechanical engineering", "Manufacturing processes - casting, forming, joining, machining"]],
        ["V", ["Power Plants", "Working principle of steam, diesel, hydro and nuclear power plants"]],
    ]),
    ("B.Tech", "1-2", "Electrical Circuit Analysis-I", "R23PC01T", 3, [
        ["I", ["Introduction to Electrical Circuits", "Circuit elements and sources", "Kirchhoff's laws", "Source transformation", "Mesh and nodal analysis"]],
        ["II", ["Magnetic Circuits", "Magnetic flux, reluctance, mmf", "B-H curve", "Series and parallel magnetic circuits", "Comparison of electric and magnetic circuits"]],
        ["III", ["Single Phase Circuits", "R, L, C circuits", "RL, RC, RLC series and parallel circuits", "Power and power factor", "Resonance"]],
        ["IV", ["Resonance and Locus Diagrams", "Series and parallel resonance", "Q-factor and bandwidth", "Locus diagrams"]],
        ["V", ["Network Theorems (DC and AC)", "Superposition, Thevenin, Norton theorems", "Maximum power transfer theorem", "Reciprocity theorem", "Millman's theorem"]],
    ]),
]

# ---- semester visibility per entry type ----
# regular: all 8 sems (1-1, 1-2, 2-1, 2-2, 3-1, 3-2, 4-1, 4-2)
# lateral: 6 sems (2-1, 2-2, 3-1, 3-2, 4-1, 4-2)
ALL_SEMS = ["1-1", "1-2", "2-1", "2-2", "3-1", "3-2", "4-1", "4-2"]
LATERAL_SEMS = ["2-1", "2-2", "3-1", "3-2", "4-1", "4-2"]

def main():
    print("Backing up database...")
    shutil.copy(DB, DB + ".bak_v41")
    print("  backup -> eee.db.bak_v41")

    # 1. Add 1st year syllabus
    print("Adding 1-1 and 1-2 real subjects...")
    for prog, ys, subj, code, creds, units in REAL_SYLLABUS_1YR:
        exists = cur.execute(
            "SELECT id FROM syllabus WHERE program=? AND year_sem=? AND subject=?",
            (prog, ys, subj)).fetchone()
        if not exists:
            cur.execute(
                "INSERT INTO syllabus (program,year_sem,subject,code,credits,units) VALUES (?,?,?,?,?,?)",
                (prog, ys, subj, code, creds, json.dumps(units)))
    total = cur.execute("SELECT COUNT(*) FROM syllabus").fetchone()[0]
    print(f"  total syllabus records now: {total}")

    # 2. Add entry column to users
    cols = [r["name"] for r in cur.execute("PRAGMA table_info(users)").fetchall()]
    if "entry" not in cols:
        print("Adding users.entry column...")
        cur.execute("ALTER TABLE users ADD COLUMN entry TEXT DEFAULT 'regular'")
    else:
        print("users.entry column exists")

    # 3. Classify students: 2021 batch (21A31...) = regular, 2025 batch (25W65...) = lateral
    print("Classifying students by entry type...")
    students = cur.execute("SELECT id, username FROM users WHERE role='student'").fetchall()
    for s in students:
        if s["username"].startswith("25W"):
            entry = "lateral"
        elif s["username"].startswith("21A"):
            entry = "regular"
        else:
            entry = "regular"
        cur.execute("UPDATE users SET entry=? WHERE id=?", (entry, s["id"]))
        print(f"  {s['username']} -> {entry}")

    conn.commit()

    # 4. Show summary
    print("\n=== STUDENT ENTRY TYPES ===")
    for r in cur.execute("SELECT username, name, entry FROM users WHERE role='student' ORDER BY username"):
        print(f"  {r['username']} ({r['name']}): {r['entry']}")
    print("\n=== SEMESTERS AVAILABLE ===")
    for r in cur.execute("SELECT DISTINCT year_sem FROM syllabus ORDER BY year_sem"):
        print(f"  {r['year_sem']}")

    conn.close()
    print("\nDONE. 1st year syllabus + regular/lateral entry added.")

if __name__ == "__main__":
    main()

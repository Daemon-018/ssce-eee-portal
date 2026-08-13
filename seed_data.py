"""Sample data for EEE portal demo (JNTU-GV R23, 3-1 sem)."""

NOTICES = [
    ("Mid-I Examinations Schedule Released",
     "Mid Semester-I examinations for 3-1 will be held from 18 Aug to 25 Aug 2026. "
     "Attend without fail; bring your JNTU-GV hall ticket and ID card.",
     "Exams", "2026-08-12"),
    ("Industrial Visit - Power Grid Substation, Ravada",
     "IV for III EEE on 29 Aug 2026, 9:00 AM. Bus departs from college main gate. "
     "Submit ₹200 to the class representative by 25 Aug. Permission letters from parents required.",
     "Industrial Visit", "2026-08-10"),
    ("Workshop: MATLAB & Simulink for Power Systems",
     "One-day hands-on workshop on 5 Sep 2026, EEE Seminar Hall, 10 AM. "
     "Conducted by industry experts. Certificate provided. Limited to 60 seats - register at dept office.",
     "Workshop", "2026-08-08"),
    ("Attendance below 65% - Warning",
     "Students with attendance below 65% must meet the class advisor before 15 Aug. "
     "As per JNTU-GV norms, <75% attendance bars you from semester exams.",
     "Attendance", "2026-08-05"),
    ("M.Tech Power Electronics - Admissions Open",
     "M.Tech Power Electronics 2026-27 admissions open. Intake 9 (Category A) + 3 (Category B). "
     "Contact the EEE department office for application details.",
     "Admissions", "2026-07-28"),
]

TIMETABLE = [
    # (day 1=Mon..6=Sat, period 1..7, subject, faculty, room)
    (1, 1, "Power System Analysis - II", "Dr. Kanthi Andhavarapu", "Room 204"),
    (1, 2, "Electrical Machine Design", "Dr. Rajselvan C", "Room 204"),
    (1, 3, "Control Systems", "Mr. Simma Gopi", "Room 204"),
    (1, 4, "Microprocessors & Microcontrollers", "Ms. Majji Sai Sudha", "Lab-2"),
    (1, 5, "Digital Signal Processing", "Mr. P. Bhargav", "Room 204"),
    (1, 6, "Lunch", "", ""),
    (1, 7, "EMA Lab", "Dr. Rajselvan C", "Machines Lab"),

    (2, 1, "Electrical Machine Design", "Dr. Rajselvan C", "Room 204"),
    (2, 2, "Power System Analysis - II", "Dr. Kanthi Andhavarapu", "Room 204"),
    (2, 3, "Digital Signal Processing", "Mr. P. Bhargav", "Room 204"),
    (2, 4, "Control Systems", "Mr. Simma Gopi", "Room 204"),
    (2, 5, "Power Electronics - II", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (2, 6, "Lunch", "", ""),
    (2, 7, "DSP Lab", "Mr. P. Bhargav", "DSP Lab"),

    (3, 1, "Control Systems", "Mr. Simma Gopi", "Room 204"),
    (3, 2, "Microprocessors & Microcontrollers", "Ms. Majji Sai Sudha", "Room 204"),
    (3, 3, "Power System Analysis - II", "Dr. Kanthi Andhavarapu", "Room 204"),
    (3, 4, "Power Electronics - II", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (3, 5, "Electrical Machine Design", "Dr. Rajselvan C", "Room 204"),
    (3, 6, "Lunch", "", ""),
    (3, 7, "MPMC Lab", "Ms. Majji Sai Sudha", "MPMC Lab"),

    (4, 1, "Digital Signal Processing", "Mr. P. Bhargav", "Room 204"),
    (4, 2, "Power Electronics - II", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (4, 3, "Power System Analysis - II", "Dr. Kanthi Andhavarapu", "Room 204"),
    (4, 4, "Electrical Machine Design", "Dr. Rajselvan C", "Room 204"),
    (4, 5, "Microprocessors & Microcontrollers", "Ms. Majji Sai Sudha", "Room 204"),
    (4, 6, "Lunch", "", ""),
    (4, 7, "PSA Lab", "Dr. Kanthi Andhavarapu", "Power Systems Lab"),

    (5, 1, "Power Electronics - II", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (5, 2, "Digital Signal Processing", "Mr. P. Bhargav", "Room 204"),
    (5, 3, "Microprocessors & Microcontrollers", "Ms. Majji Sai Sudha", "Room 204"),
    (5, 4, "Control Systems", "Mr. Simma Gopi", "Room 204"),
    (5, 5, "Mentor Session / Sports", "", "Room 204"),
    (5, 6, "Lunch", "", ""),
    (5, 7, "Control Systems Lab", "Mr. Simma Gopi", "CS Lab"),

    (6, 1, "Power System Analysis - II", "Dr. Kanthi Andhavarapu", "Room 204"),
    (6, 2, "Electrical Machine Design", "Dr. Rajselvan C", "Room 204"),
    (6, 3, "Library / Self Study", "", "Library"),
    (6, 4, "Library / Self Study", "", "Library"),
    (6, 5, "", "", ""),
    (6, 6, "", "", ""),
    (6, 7, "", "", ""),
]

SYLLABUS = [
    ("Power System Analysis - II", "EE321", 4, [
        ("I", ["Per Unit Analysis", "Symmetrical Components", "Sequence Networks of Generators, Transformers and Lines"]),
        ("II", ["Symmetrical Fault Analysis", "Fault Current Computation", "Short Circuit Calculations"]),
        ("III", ["Unsymmetrical Fault Analysis", "LG, LL, LLG Faults", "Open Conductor Faults"]),
        ("IV", ["Power Flow Studies", "Gauss-Seidel, Newton-Raphson Methods", "Decoupled & Fast Decoupled Load Flow"]),
        ("V", ["Economic Operation of Power Systems", "Unit Commitment", "Hydro-thermal Scheduling"]),
        ("VI", ["Power System Stability", "Swing Equation", "Equal Area Criterion", "Improvement of Stability"]),
    ]),
    ("Power Electronics - II", "EE322", 4, [
        ("I", ["DC-DC Converters", "Buck, Boost, Buck-Boost", "Cuk Converters"]),
        ("II", ["Choppers and Applications", "Thyristorised Choppers", "Commutation Circuits"]),
        ("III", ["Inverters", "Single & Three Phase Inverters", "PWM Techniques"]),
        ("IV", ["AC Voltage Controllers", "Single & Three Phase Controllers", "Cycloconverters"]),
        ("V", ["Power Supplies", "SMPS", "UPS Systems"]),
        ("VI", ["Applications in Industry", "HVDC & FACTS Overview", "Renewable Integration"]),
    ]),
    ("Electrical Machine Design", "EE323", 4, [
        ("I", ["Principles of Design", "Magnetic Circuit Design", "Specific Electric & Magnetic Loadings"]),
        ("II", ["Design of DC Machines", "Output Equation", "Main Dimensions"]),
        ("III", ["Design of Transformers", "Core & Winding Design", "Cooling Systems"]),
        ("IV", ["Design of Induction Motors", "Stator & Rotor Design", "Squirrel Cage & Slip Ring"]),
        ("V", ["Design of Synchronous Machines", "Field Winding Design", "Damper Windings"]),
        ("VI", ["Computer Aided Machine Design", "Optimisation Techniques", "Thermal Design"]),
    ]),
    ("Control Systems", "EE324", 3, [
        ("I", ["Mathematical Modelling", "Transfer Function, Block Diagrams", "Signal Flow Graphs"]),
        ("II", ["Time Response Analysis", "Transient & Steady State Response", "Error Constants"]),
        ("III", ["Stability Analysis", "Routh-Hurwitz Criterion", "Root Locus"]),
        ("IV", ["Frequency Response Analysis", "Bode, Nyquist, Polar Plots", "Gain & Phase Margins"]),
        ("V", ["State Space Analysis", "Controllability & Observability", "State Feedback"]),
        ("VI", ["Compensators", "Lead, Lag, Lead-Lag", "PID Controllers"]),
    ]),
    ("Microprocessors & Microcontrollers", "EE325", 3, [
        ("I", ["8086 Architecture", "Registers, Addressing Modes", "Instruction Set"]),
        ("II", ["Assembly Language Programming", "Branching & Looping", "Data Transfer Operations"]),
        ("III", ["Peripheral Interfacing", "8255, 8259, 8253", "Memory Interfacing"]),
        ("IV", ["8051 Microcontroller", "Architecture & Timers", "Serial Communication"]),
        ("V", ["8051 Programming", "I/O Port Programming", "Interrupts"]),
        ("VI", ["Applications", "Stepper Motor Control", "DC Motor Control", "ADC/DAC Interfacing"]),
    ]),
    ("Digital Signal Processing", "EE326", 3, [
        ("I", ["Discrete Time Signals & Systems", "Z-Transform", "Difference Equations"]),
        ("II", ["DFT & FFT", "Properties of DFT", "Radix-2 FFT Algorithms"]),
        ("III", ["IIR Filter Design", "Butterworth & Chebyshev", "Bilinear Transformation"]),
        ("IV", ["FIR Filter Design", "Window Functions", "Frequency Sampling Method"]),
        ("V", ["Realisation Structures", "Direct, Cascade, Parallel", "Lattice Structures"]),
        ("VI", ["Applications", "Speech Processing", "Power System Signal Analysis"]),
    ]),
]

ATTENDANCE = {
    "Power System Analysis - II": (38, 44),
    "Power Electronics - II": (40, 44),
    "Electrical Machine Design": (36, 44),
    "Control Systems": (42, 44),
    "Microprocessors & Microcontrollers": (39, 44),
    "Digital Signal Processing": (33, 44),
}

# demo student roster (username, name, email, section, batch, cgpa)
STUDENTS = [
    ("21A31A0201", "K. Venkata Surya", "surya.21a31a0201@srisivani.edu.in", "A", "2021-25", 8.24),
    ("21A31A0202", "P. Lakshmi Prasanna", "lakshmi.21a31a0202@srisivani.edu.in", "A", "2021-25", 7.86),
    ("21A31A0203", "S. Raviteja", "raviteja.21a31a0203@srisivani.edu.in", "A", "2021-25", 7.42),
    ("21A31A0204", "B. Sai Kiran", "saikiran.21a31a0204@srisivani.edu.in", "A", "2021-25", 8.02),
    ("21A31A0205", "D. Naga Jyothi", "jyothi.21a31a0205@srisivani.edu.in", "B", "2021-25", 7.15),
    ("21A31A0206", "M. Harish Kumar", "harish.21a31a0206@srisivani.edu.in", "B", "2021-25", 6.98),
]

# demo students for all years
# 1st year = 2025 batch (lateral entry: 25W65A02xx) -> 1-1/1-2 syllabus
# 2nd year = 2024 batch (regular: 24A31A02xx)      -> 2-1/2-2 syllabus
# 3rd year = 2021 batch (regular: 21A31A02xx)      -> 3-1/3-2 syllabus
# 4th year = 2020 batch (regular: 20A31A02xx)      -> 4-1/4-2 syllabus
# tuple: (username, name, password, email, section, batch, cgpa)
NEW_STUDENTS = [
    # ---- 1st year (2025 batch, lateral) ----
    ("25W65A0201", "A. Sravani", "sravani@123", "sravani.25w65a0201@srisivani.edu.in", "A", "2025-29", 7.40),
    ("25W65A0202", "B. Vamsi Krishna", "vamsi@123", "vamsi.25w65a0202@srisivani.edu.in", "A", "2025-29", 6.90),
    ("25W65A0203", "Ch. Manasa", "manasa@123", "manasa.25w65a0203@srisivani.edu.in", "B", "2025-29", 7.80),
    ("25W65A0204", "D. Ravi Teja", "ravi@123", "ravi.25w65a0204@srisivani.edu.in", "B", "2025-29", 6.50),
    ("25W65A0205", "E. Bhavana", "bhavana@123", "bhavana.25w65a0205@srisivani.edu.in", "A", "2025-29", 8.10),
    ("25W65A0206", "G. Suresh", "suresh@123", "suresh.25w65a0206@srisivani.edu.in", "B", "2025-29", 7.20),
    ("25W65A0211", "G. Hemanth", "hemanth@123", "hemanth.25w65a0211@srisivani.edu.in", "", "2025-29", None),
    ("25W65A0226", "N. Yagnesh", "yagnesh@123", "yagnesh.25w65a0226@srisivani.edu.in", "", "2025-29", None),
    ("25W65A0228", "N. Poshan", "poshan@123", "poshan.25w65a0228@srisivani.edu.in", "", "2025-29", None),
    ("25W65A0231", "P. Harshith", "harshith@123", "harshith.25w65a0231@srisivani.edu.in", "", "2025-29", None),
    ("25W65A0236", "T. Akhil", "akhil@123", "akhil.25w65a0236@srisivani.edu.in", "", "2025-29", None),
    # ---- 2nd year (2024 batch, regular) ----
    ("24A31A0201", "H. Naga Sai", "nagasai@123", "nagasai.24a31a0201@srisivani.edu.in", "A", "2024-28", 7.60),
    ("24A31A0202", "I. Pooja", "pooja@123", "pooja.24a31a0202@srisivani.edu.in", "A", "2024-28", 8.30),
    ("24A31A0203", "J. Rakesh", "rakesh@123", "rakesh.24a31a0203@srisivani.edu.in", "B", "2024-28", 7.10),
    ("24A31A0204", "K. Sandhya", "sandhya@123", "sandhya.24a31a0204@srisivani.edu.in", "B", "2024-28", 6.80),
    ("24A31A0205", "M. Praveen Kumar", "praveenkumar@123", "praveenkumar.24a31a0205@srisivani.edu.in", "A", "2024-28", 7.90),
    ("24A31A0206", "N. Divya", "divya@123", "divya.24a31a0206@srisivani.edu.in", "B", "2024-28", 8.00),
    # ---- 4th year (2020 batch, regular) ----
    ("20A31A0201", "O. Satish", "satish@123", "satish.20a31a0201@srisivani.edu.in", "A", "2020-24", 8.50),
    ("20A31A0202", "P. Swathi", "swathi@123", "swathi.20a31a0202@srisivani.edu.in", "A", "2020-24", 7.70),
    ("20A31A0203", "R. Anil Kumar", "anil@123", "anil.20a31a0203@srisivani.edu.in", "B", "2020-24", 7.30),
    ("20A31A0204", "S. Lakshmi", "lakshmi@123", "lakshmi.20a31a0204@srisivani.edu.in", "B", "2020-24", 8.10),
    ("20A31A0205", "T. Venkatesh", "venkatesh@123", "venkatesh.20a31a0205@srisivani.edu.in", "A", "2020-24", 6.90),
    ("20A31A0206", "U. Meghana", "meghana@123", "meghana.20a31a0206@srisivani.edu.in", "B", "2020-24", 7.40),
]

# new faculty (username = email, password = <name>@123)
NEW_FACULTY = [
    ("praveen@gmail.com", "praveen@123", "Praveen", "praveen@gmail.com", "Assistant Professor", "EEE Dept"),
    ("bhanuchandra@gmail.com", "bhanuchandra@123", "Bhanuchandra", "bhanuchandra@gmail.com", "Assistant Professor", "EEE Dept"),
]

# per-student attendance: {username: {subject: (attended, total)}}
STUDENT_ATTENDANCE = {
    "21A31A0201": {
        "Power System Analysis - II": (38, 44), "Power Electronics - II": (40, 44),
        "Electrical Machine Design": (36, 44), "Control Systems": (42, 44),
        "Microprocessors & Microcontrollers": (39, 44), "Digital Signal Processing": (33, 44),
    },
    "21A31A0202": {
        "Power System Analysis - II": (41, 44), "Power Electronics - II": (38, 44),
        "Electrical Machine Design": (37, 44), "Control Systems": (40, 44),
        "Microprocessors & Microcontrollers": (42, 44), "Digital Signal Processing": (36, 44),
    },
    "21A31A0203": {
        "Power System Analysis - II": (35, 44), "Power Electronics - II": (39, 44),
        "Electrical Machine Design": (34, 44), "Control Systems": (37, 44),
        "Microprocessors & Microcontrollers": (38, 44), "Digital Signal Processing": (31, 44),
    },
    "21A31A0204": {
        "Power System Analysis - II": (39, 44), "Power Electronics - II": (41, 44),
        "Electrical Machine Design": (40, 44), "Control Systems": (41, 44),
        "Microprocessors & Microcontrollers": (36, 44), "Digital Signal Processing": (37, 44),
    },
    "21A31A0205": {
        "Power System Analysis - II": (36, 44), "Power Electronics - II": (35, 44),
        "Electrical Machine Design": (33, 44), "Control Systems": (38, 44),
        "Microprocessors & Microcontrollers": (37, 44), "Digital Signal Processing": (34, 44),
    },
    "21A31A0206": {
        "Power System Analysis - II": (32, 44), "Power Electronics - II": (36, 44),
        "Electrical Machine Design": (31, 44), "Control Systems": (35, 44),
        "Microprocessors & Microcontrollers": (34, 44), "Digital Signal Processing": (29, 44),
    },
    # ---- 1st year (1-1 subjects) ----
    "25W65A0201": {
        "Linear Algebra and Calculus": (30, 34), "Chemistry": (31, 34),
        "Introduction to Programming": (29, 34), "Engineering Graphics": (32, 34),
        "Basic Electrical and Electronics Engineering": (30, 34),
    },
    "25W65A0202": {
        "Linear Algebra and Calculus": (28, 34), "Chemistry": (30, 34),
        "Introduction to Programming": (27, 34), "Engineering Graphics": (31, 34),
        "Basic Electrical and Electronics Engineering": (29, 34),
    },
    "25W65A0203": {
        "Linear Algebra and Calculus": (31, 34), "Chemistry": (30, 34),
        "Introduction to Programming": (32, 34), "Engineering Graphics": (33, 34),
        "Basic Electrical and Electronics Engineering": (31, 34),
    },
    "25W65A0204": {
        "Linear Algebra and Calculus": (26, 34), "Chemistry": (28, 34),
        "Introduction to Programming": (25, 34), "Engineering Graphics": (27, 34),
        "Basic Electrical and Electronics Engineering": (26, 34),
    },
    "25W65A0205": {
        "Linear Algebra and Calculus": (32, 34), "Chemistry": (33, 34),
        "Introduction to Programming": (31, 34), "Engineering Graphics": (32, 34),
        "Basic Electrical and Electronics Engineering": (33, 34),
    },
    "25W65A0206": {
        "Linear Algebra and Calculus": (29, 34), "Chemistry": (30, 34),
        "Introduction to Programming": (28, 34), "Engineering Graphics": (29, 34),
        "Basic Electrical and Electronics Engineering": (30, 34),
    },
    # ---- 2nd year (2-2 subjects) ----
    "24A31A0201": {
        "Managerial Economics and Financial Analysis": (30, 36), "Analog Circuits": (32, 36),
        "Power Systems-I": (31, 36), "Induction and Synchronous Machines": (33, 36),
        "Control Systems": (32, 36),
    },
    "24A31A0202": {
        "Managerial Economics and Financial Analysis": (33, 36), "Analog Circuits": (34, 36),
        "Power Systems-I": (32, 36), "Induction and Synchronous Machines": (35, 36),
        "Control Systems": (33, 36),
    },
    "24A31A0203": {
        "Managerial Economics and Financial Analysis": (29, 36), "Analog Circuits": (30, 36),
        "Power Systems-I": (28, 36), "Induction and Synchronous Machines": (31, 36),
        "Control Systems": (29, 36),
    },
    "24A31A0204": {
        "Managerial Economics and Financial Analysis": (27, 36), "Analog Circuits": (28, 36),
        "Power Systems-I": (26, 36), "Induction and Synchronous Machines": (29, 36),
        "Control Systems": (27, 36),
    },
    "24A31A0205": {
        "Managerial Economics and Financial Analysis": (31, 36), "Analog Circuits": (32, 36),
        "Power Systems-I": (30, 36), "Induction and Synchronous Machines": (34, 36),
        "Control Systems": (31, 36),
    },
    "24A31A0206": {
        "Managerial Economics and Financial Analysis": (30, 36), "Analog Circuits": (31, 36),
        "Power Systems-I": (29, 36), "Induction and Synchronous Machines": (32, 36),
        "Control Systems": (30, 36),
    },
    # ---- 4th year (4-1 subjects) ----
    "20A31A0201": {
        "Power System Operation and Control": (30, 34), "Energy Management and Auditing": (31, 34),
        "HVDC Transmission": (32, 34), "FACTS": (30, 34),
        "Electric Vehicles": (33, 34), "Battery Management Systems": (31, 34),
        "Concepts of Smart Grid": (32, 34), "Concepts of Power Quality": (30, 34),
    },
    "20A31A0202": {
        "Power System Operation and Control": (29, 34), "Energy Management and Auditing": (30, 34),
        "HVDC Transmission": (31, 34), "FACTS": (28, 34),
        "Electric Vehicles": (30, 34), "Battery Management Systems": (29, 34),
        "Concepts of Smart Grid": (30, 34), "Concepts of Power Quality": (28, 34),
    },
    "20A31A0203": {
        "Power System Operation and Control": (27, 34), "Energy Management and Auditing": (28, 34),
        "HVDC Transmission": (29, 34), "FACTS": (26, 34),
        "Electric Vehicles": (28, 34), "Battery Management Systems": (27, 34),
        "Concepts of Smart Grid": (29, 34), "Concepts of Power Quality": (26, 34),
    },
    "20A31A0204": {
        "Power System Operation and Control": (31, 34), "Energy Management and Auditing": (32, 34),
        "HVDC Transmission": (30, 34), "FACTS": (31, 34),
        "Electric Vehicles": (33, 34), "Battery Management Systems": (32, 34),
        "Concepts of Smart Grid": (31, 34), "Concepts of Power Quality": (30, 34),
    },
    "20A31A0205": {
        "Power System Operation and Control": (26, 34), "Energy Management and Auditing": (27, 34),
        "HVDC Transmission": (28, 34), "FACTS": (25, 34),
        "Electric Vehicles": (27, 34), "Battery Management Systems": (26, 34),
        "Concepts of Smart Grid": (28, 34), "Concepts of Power Quality": (25, 34),
    },
    "20A31A0206": {
        "Power System Operation and Control": (28, 34), "Energy Management and Auditing": (29, 34),
        "HVDC Transmission": (30, 34), "FACTS": (27, 34),
        "Electric Vehicles": (29, 34), "Battery Management Systems": (28, 34),
        "Concepts of Smart Grid": (30, 34), "Concepts of Power Quality": (27, 34),
    },
}

# sample marks: {username: {subject: {"MID1": 22, "MID2": 25}}}  (max 30 each)
STUDENT_MARKS = {
    "21A31A0201": {
        "Power System Analysis - II": {"MID1": 24, "MID2": 22},
        "Power Electronics - II": {"MID1": 25, "MID2": 26},
        "Electrical Machine Design": {"MID1": 21, "MID2": 23},
        "Control Systems": {"MID1": 27, "MID2": 25},
        "Microprocessors & Microcontrollers": {"MID1": 22, "MID2": 20},
        "Digital Signal Processing": {"MID1": 19, "MID2": 21},
    },
    "21A31A0202": {
        "Power System Analysis - II": {"MID1": 23, "MID2": 24},
        "Power Electronics - II": {"MID1": 22, "MID2": 21},
        "Electrical Machine Design": {"MID1": 24, "MID2": 22},
        "Control Systems": {"MID1": 26, "MID2": 24},
        "Microprocessors & Microcontrollers": {"MID1": 21, "MID2": 23},
        "Digital Signal Processing": {"MID1": 20, "MID2": 18},
    },
    "21A31A0203": {
        "Power System Analysis - II": {"MID1": 18, "MID2": 20},
        "Power Electronics - II": {"MID1": 19, "MID2": 21},
        "Electrical Machine Design": {"MID1": 17, "MID2": 18},
        "Control Systems": {"MID1": 21, "MID2": 19},
        "Microprocessors & Microcontrollers": {"MID1": 16, "MID2": 18},
        "Digital Signal Processing": {"MID1": 15, "MID2": 17},
    },
    "21A31A0204": {
        "Power System Analysis - II": {"MID1": 25, "MID2": 26},
        "Power Electronics - II": {"MID1": 24, "MID2": 25},
        "Electrical Machine Design": {"MID1": 22, "MID2": 24},
        "Control Systems": {"MID1": 25, "MID2": 26},
        "Microprocessors & Microcontrollers": {"MID1": 23, "MID2": 22},
        "Digital Signal Processing": {"MID1": 21, "MID2": 23},
    },
    "21A31A0205": {
        "Power System Analysis - II": {"MID1": 20, "MID2": 19},
        "Power Electronics - II": {"MID1": 21, "MID2": 18},
        "Electrical Machine Design": {"MID1": 19, "MID2": 20},
        "Control Systems": {"MID1": 22, "MID2": 21},
        "Microprocessors & Microcontrollers": {"MID1": 18, "MID2": 17},
        "Digital Signal Processing": {"MID1": 17, "MID2": 16},
    },
    "21A31A0206": {
        "Power System Analysis - II": {"MID1": 16, "MID2": 18},
        "Power Electronics - II": {"MID1": 15, "MID2": 17},
        "Electrical Machine Design": {"MID1": 14, "MID2": 16},
        "Control Systems": {"MID1": 18, "MID2": 17},
        "Microprocessors & Microcontrollers": {"MID1": 15, "MID2": 14},
        "Digital Signal Processing": {"MID1": 13, "MID2": 15},
    },
    # ---- 1st year (1-1 subjects) ----
    "25W65A0201": {
        "Linear Algebra and Calculus": {"MID1": 22, "MID2": 24},
        "Chemistry": {"MID1": 25, "MID2": 23},
        "Introduction to Programming": {"MID1": 21, "MID2": 20},
        "Engineering Graphics": {"MID1": 26, "MID2": 24},
        "Basic Electrical and Electronics Engineering": {"MID1": 23, "MID2": 22},
    },
    "25W65A0202": {
        "Linear Algebra and Calculus": {"MID1": 18, "MID2": 19},
        "Chemistry": {"MID1": 20, "MID2": 21},
        "Introduction to Programming": {"MID1": 17, "MID2": 18},
        "Engineering Graphics": {"MID1": 19, "MID2": 20},
        "Basic Electrical and Electronics Engineering": {"MID1": 18, "MID2": 19},
    },
    "25W65A0203": {
        "Linear Algebra and Calculus": {"MID1": 24, "MID2": 25},
        "Chemistry": {"MID1": 23, "MID2": 24},
        "Introduction to Programming": {"MID1": 25, "MID2": 22},
        "Engineering Graphics": {"MID1": 26, "MID2": 25},
        "Basic Electrical and Electronics Engineering": {"MID1": 24, "MID2": 23},
    },
    "25W65A0204": {
        "Linear Algebra and Calculus": {"MID1": 15, "MID2": 16},
        "Chemistry": {"MID1": 17, "MID2": 18},
        "Introduction to Programming": {"MID1": 14, "MID2": 15},
        "Engineering Graphics": {"MID1": 16, "MID2": 17},
        "Basic Electrical and Electronics Engineering": {"MID1": 15, "MID2": 16},
    },
    "25W65A0205": {
        "Linear Algebra and Calculus": {"MID1": 26, "MID2": 27},
        "Chemistry": {"MID1": 25, "MID2": 26},
        "Introduction to Programming": {"MID1": 24, "MID2": 25},
        "Engineering Graphics": {"MID1": 27, "MID2": 26},
        "Basic Electrical and Electronics Engineering": {"MID1": 26, "MID2": 25},
    },
    "25W65A0206": {
        "Linear Algebra and Calculus": {"MID1": 20, "MID2": 21},
        "Chemistry": {"MID1": 21, "MID2": 20},
        "Introduction to Programming": {"MID1": 19, "MID2": 18},
        "Engineering Graphics": {"MID1": 22, "MID2": 21},
        "Basic Electrical and Electronics Engineering": {"MID1": 20, "MID2": 19},
    },
    # ---- 2nd year (2-2 subjects) ----
    "24A31A0201": {
        "Managerial Economics and Financial Analysis": {"MID1": 22, "MID2": 24},
        "Analog Circuits": {"MID1": 25, "MID2": 23},
        "Power Systems-I": {"MID1": 21, "MID2": 22},
        "Induction and Synchronous Machines": {"MID1": 24, "MID2": 25},
        "Control Systems": {"MID1": 23, "MID2": 24},
    },
    "24A31A0202": {
        "Managerial Economics and Financial Analysis": {"MID1": 26, "MID2": 25},
        "Analog Circuits": {"MID1": 27, "MID2": 26},
        "Power Systems-I": {"MID1": 24, "MID2": 25},
        "Induction and Synchronous Machines": {"MID1": 28, "MID2": 27},
        "Control Systems": {"MID1": 26, "MID2": 25},
    },
    "24A31A0203": {
        "Managerial Economics and Financial Analysis": {"MID1": 19, "MID2": 20},
        "Analog Circuits": {"MID1": 21, "MID2": 19},
        "Power Systems-I": {"MID1": 18, "MID2": 20},
        "Induction and Synchronous Machines": {"MID1": 20, "MID2": 21},
        "Control Systems": {"MID1": 19, "MID2": 18},
    },
    "24A31A0204": {
        "Managerial Economics and Financial Analysis": {"MID1": 17, "MID2": 18},
        "Analog Circuits": {"MID1": 18, "MID2": 17},
        "Power Systems-I": {"MID1": 16, "MID2": 18},
        "Induction and Synchronous Machines": {"MID1": 19, "MID2": 17},
        "Control Systems": {"MID1": 17, "MID2": 16},
    },
    "24A31A0205": {
        "Managerial Economics and Financial Analysis": {"MID1": 23, "MID2": 24},
        "Analog Circuits": {"MID1": 24, "MID2": 23},
        "Power Systems-I": {"MID1": 22, "MID2": 21},
        "Induction and Synchronous Machines": {"MID1": 25, "MID2": 24},
        "Control Systems": {"MID1": 23, "MID2": 22},
    },
    "24A31A0206": {
        "Managerial Economics and Financial Analysis": {"MID1": 21, "MID2": 22},
        "Analog Circuits": {"MID1": 23, "MID2": 21},
        "Power Systems-I": {"MID1": 20, "MID2": 19},
        "Induction and Synchronous Machines": {"MID1": 22, "MID2": 23},
        "Control Systems": {"MID1": 21, "MID2": 20},
    },
    # ---- 4th year (4-1 subjects) ----
    "20A31A0201": {
        "Power System Operation and Control": {"MID1": 26, "MID2": 27},
        "Energy Management and Auditing": {"MID1": 25, "MID2": 26},
        "HVDC Transmission": {"MID1": 24, "MID2": 25},
        "FACTS": {"MID1": 26, "MID2": 24},
        "Electric Vehicles": {"MID1": 27, "MID2": 26},
        "Battery Management Systems": {"MID1": 25, "MID2": 25},
        "Concepts of Smart Grid": {"MID1": 26, "MID2": 27},
        "Concepts of Power Quality": {"MID1": 24, "MID2": 25},
    },
    "20A31A0202": {
        "Power System Operation and Control": {"MID1": 23, "MID2": 24},
        "Energy Management and Auditing": {"MID1": 24, "MID2": 23},
        "HVDC Transmission": {"MID1": 22, "MID2": 23},
        "FACTS": {"MID1": 21, "MID2": 22},
        "Electric Vehicles": {"MID1": 24, "MID2": 23},
        "Battery Management Systems": {"MID1": 23, "MID2": 22},
        "Concepts of Smart Grid": {"MID1": 24, "MID2": 24},
        "Concepts of Power Quality": {"MID1": 22, "MID2": 21},
    },
    "20A31A0203": {
        "Power System Operation and Control": {"MID1": 20, "MID2": 21},
        "Energy Management and Auditing": {"MID1": 21, "MID2": 20},
        "HVDC Transmission": {"MID1": 19, "MID2": 20},
        "FACTS": {"MID1": 18, "MID2": 19},
        "Electric Vehicles": {"MID1": 21, "MID2": 20},
        "Battery Management Systems": {"MID1": 20, "MID2": 19},
        "Concepts of Smart Grid": {"MID1": 21, "MID2": 22},
        "Concepts of Power Quality": {"MID1": 19, "MID2": 18},
    },
    "20A31A0204": {
        "Power System Operation and Control": {"MID1": 25, "MID2": 26},
        "Energy Management and Auditing": {"MID1": 24, "MID2": 25},
        "HVDC Transmission": {"MID1": 23, "MID2": 24},
        "FACTS": {"MID1": 25, "MID2": 24},
        "Electric Vehicles": {"MID1": 26, "MID2": 25},
        "Battery Management Systems": {"MID1": 24, "MID2": 25},
        "Concepts of Smart Grid": {"MID1": 25, "MID2": 26},
        "Concepts of Power Quality": {"MID1": 23, "MID2": 24},
    },
    "20A31A0205": {
        "Power System Operation and Control": {"MID1": 18, "MID2": 19},
        "Energy Management and Auditing": {"MID1": 19, "MID2": 18},
        "HVDC Transmission": {"MID1": 17, "MID2": 18},
        "FACTS": {"MID1": 16, "MID2": 17},
        "Electric Vehicles": {"MID1": 19, "MID2": 18},
        "Battery Management Systems": {"MID1": 18, "MID2": 17},
        "Concepts of Smart Grid": {"MID1": 19, "MID2": 20},
        "Concepts of Power Quality": {"MID1": 17, "MID2": 16},
    },
    "20A31A0206": {
        "Power System Operation and Control": {"MID1": 22, "MID2": 23},
        "Energy Management and Auditing": {"MID1": 21, "MID2": 22},
        "HVDC Transmission": {"MID1": 20, "MID2": 21},
        "FACTS": {"MID1": 19, "MID2": 20},
        "Electric Vehicles": {"MID1": 22, "MID2": 21},
        "Battery Management Systems": {"MID1": 21, "MID2": 20},
        "Concepts of Smart Grid": {"MID1": 22, "MID2": 23},
        "Concepts of Power Quality": {"MID1": 20, "MID2": 19},
    },
}

SUBJECTS = [
    "Power System Analysis - II", "Power Electronics - II", "Electrical Machine Design",
    "Control Systems", "Microprocessors & Microcontrollers", "Digital Signal Processing",
]

# ============ v3: study materials ============
# (subject, title, kind, link)
STUDY_MATERIALS = [
    ("Power System Analysis - II", "Unit I - Per Unit Analysis & Symmetrical Components (Notes)", "notes", ""),
    ("Power System Analysis - II", "Fault Analysis - Complete Handwritten Notes (PDF)", "pdf", "#"),
    ("Power System Analysis - II", "Gauss-Seidel vs Newton-Raphson - Comparison PPT", "ppt", "#"),
    ("Power System Analysis - II", "Stability Analysis - Video Lectures (Playlist)", "video", "https://www.youtube.com/results?search_query=power+system+stability+swing+equation"),
    ("Power Electronics - II", "DC-DC Converters - Buck, Boost, Buck-Boost (Notes)", "notes", ""),
    ("Power Electronics - II", "Inverters & PWM Techniques - Unit III Notes", "notes", ""),
    ("Power Electronics - II", "SMPS & UPS - Reference Material (PDF)", "pdf", "#"),
    ("Power Electronics - II", "Choppers & Commutation - Video Lectures", "video", "https://www.youtube.com/results?search_query=choppers+power+electronics"),
    ("Electrical Machine Design", "Design of Transformers - Core & Winding (Notes)", "notes", ""),
    ("Electrical Machine Design", "Design of DC Machines - Output Equation Notes", "notes", ""),
    ("Electrical Machine Design", "Machine Design Data Book (PDF)", "pdf", "#"),
    ("Control Systems", "Unit I - Transfer Function & Block Diagrams (Notes)", "notes", ""),
    ("Control Systems", "Root Locus Technique - Step-by-step (PDF)", "pdf", "#"),
    ("Control Systems", "Bode & Nyquist Plots - Video Lectures", "video", "https://www.youtube.com/results?search_query=bode+plot+control+systems"),
    ("Microprocessors & Microcontrollers", "8086 Architecture & Instruction Set (Notes)", "notes", ""),
    ("Microprocessors & Microcontrollers", "8051 Programming Examples (PDF)", "pdf", "#"),
    ("Microprocessors & Microcontrollers", "Peripheral Interfacing - 8255, 8259 (PPT)", "ppt", "#"),
    ("Digital Signal Processing", "Z-Transform & Difference Equations (Notes)", "notes", ""),
    ("Digital Signal Processing", "DFT & FFT Algorithms - Notes", "notes", ""),
    ("Digital Signal Processing", "IIR / FIR Filter Design - Video Lectures", "video", "https://www.youtube.com/results?search_query=IIR+FIR+filter+design+dsp"),
]

# ============ v3: previous year question papers ============
# (subject, year, exam, download)
PYQ = [
    ("Power System Analysis - II", "2025", "Regular", "#"),
    ("Power System Analysis - II", "2024", "Regular", "#"),
    ("Power System Analysis - II", "2024", "Supply", "#"),
    ("Power System Analysis - II", "2023", "Regular", "#"),
    ("Power Electronics - II", "2025", "Regular", "#"),
    ("Power Electronics - II", "2024", "Regular", "#"),
    ("Power Electronics - II", "2023", "Supply", "#"),
    ("Electrical Machine Design", "2025", "Regular", "#"),
    ("Electrical Machine Design", "2024", "Regular", "#"),
    ("Electrical Machine Design", "2023", "Regular", "#"),
    ("Control Systems", "2025", "Regular", "#"),
    ("Control Systems", "2024", "Regular", "#"),
    ("Control Systems", "2024", "Supply", "#"),
    ("Control Systems", "2023", "Regular", "#"),
    ("Microprocessors & Microcontrollers", "2025", "Regular", "#"),
    ("Microprocessors & Microcontrollers", "2024", "Regular", "#"),
    ("Microprocessors & Microcontrollers", "2023", "Supply", "#"),
    ("Digital Signal Processing", "2025", "Regular", "#"),
    ("Digital Signal Processing", "2024", "Regular", "#"),
    ("Digital Signal Processing", "2023", "Regular", "#"),
]

# ============ v3: solved answers ============
# (subject, year, exam, link)
SOLVED_PAPERS = [
    ("Power System Analysis - II", "2024", "Regular", "#"),
    ("Power System Analysis - II", "2023", "Regular", "#"),
    ("Power Electronics - II", "2024", "Regular", "#"),
    ("Power Electronics - II", "2023", "Regular", "#"),
    ("Electrical Machine Design", "2024", "Regular", "#"),
    ("Control Systems", "2024", "Regular", "#"),
    ("Control Systems", "2023", "Regular", "#"),
    ("Microprocessors & Microcontrollers", "2024", "Regular", "#"),
    ("Digital Signal Processing", "2024", "Regular", "#"),
    ("Digital Signal Processing", "2023", "Regular", "#"),
]

# ============ v3: academic calendar ============
# (title, date, category, note)
ACADEMIC_CALENDAR = [
    ("Commencement of 3-1 Classes", "2026-06-15", "Academic", "Regular class work starts"),
    ("I Mid-Term Examinations", "2026-08-18", "Exams", "MID-1 for all 3-1 subjects"),
    ("I Mid Result Declaration", "2026-08-30", "Exams", ""),
    ("II Mid-Term Examinations", "2026-10-12", "Exams", "MID-2 for all 3-1 subjects"),
    ("Last Working Day", "2026-11-07", "Academic", "End of instruction"),
    ("Semester End (R23) Examinations", "2026-11-16", "Exams", "JNTU-GV regular exams"),
    ("Results Declaration", "2026-12-22", "Exams", "Expected date"),
    ("Supply (Backlog) Examinations", "2027-01-18", "Exams", "For failed subjects"),
    ("Commencement of 3-2 Classes", "2027-01-04", "Academic", "Next semester begins"),
]

# ============ v3: backlog tracker (per student) ============
# (username, subject, sem, attempts, cleared, cleared_date, note)
BACKLOGS = {
    "21A31A0201": [],
    "21A31A0202": [
        ("Electrical Machines - II", "2-2", 1, 1, "2026-03-10", "Cleared in supply exam"),
    ],
    "21A31A0203": [
        ("Power Systems - I", "2-2", 1, 0, "", "Appear in Jan 2027 supply"),
        ("Network Analysis", "2-1", 2, 0, "", "Second attempt - study regularly"),
    ],
    "21A31A0204": [],
    "21A31A0205": [
        ("Electrical Machines - II", "2-2", 1, 0, "", "Appear in Jan 2027 supply"),
    ],
    "21A31A0206": [
        ("Network Analysis", "2-1", 1, 0, "", "Appear in Jan 2027 supply"),
        ("Power Systems - I", "2-2", 1, 0, "", "Appear in Jan 2027 supply"),
        ("Control Systems", "2-2", 1, 0, "", "Extra class target"),
    ],
}

# ============ v3: exam notifications ============
# (title, body, exam_type, link)
EXAM_NOTIFICATIONS = [
    ("JNTU-GV R23 Semester End Examination - Time Table Released",
     "The schedule for 3-1 semester end (Regular) examinations is out. Download the timetable and verify your subjects.",
     "Regular", "#"),
    ("Supply (Backlog) Examinations - January 2027",
     "Applications for supply exams open from 20 Dec 2026. Apply online with the prescribed fee before the last date.",
     "Supply", "#"),
    ("I Mid-Term Examinations - Hall Ticket",
     "MID-1 hall tickets available from the department office. Bring your ID card to the exam hall.",
     "Regular", "#"),
    ("Practical Examinations (Lab Internals)",
     "Lab internals for all EEE labs scheduled from 5 Nov 2026. Record submission is compulsory.",
     "Regular", "#"),
]

# ============ v3: mentorship ============
# (username, mentor, last_meeting, next_meeting, notes)
MENTORSHIP = {
    "21A31A0201": ("Dr. G.T. Chandra Sekhar", "2026-08-05", "2026-09-02", "Academic progress on track. Continue consistent performance."),
    "21A31A0202": ("Dr. G.T. Chandra Sekhar", "2026-08-05", "2026-09-02", "Improve attendance in DSP. Practice numerical problems."),
    "21A31A0203": ("Dr. Rajselvan C", "2026-08-04", "2026-09-01", "Focus on clearing backlog subjects. Extra classes advised."),
    "21A31A0204": ("Dr. Kanthi Andhavarapu", "2026-08-06", "2026-09-03", "Good performance. Consider taking up technical paper presentation."),
    "21A31A0205": ("Dr. Rajselvan C", "2026-08-04", "2026-09-01", "Backlog - attend extra classes for Electrical Machines."),
    "21A31A0206": ("Dr. Kanthi Andhavarapu", "2026-08-06", "2026-09-03", "Multiple backlogs - weekly meeting with mentor scheduled."),
}

# ============ v3: job resources ============
# (category, title, description, link)
JOB_RESOURCES = [
    ("core-govt", "SSC JE (Electrical) - Staff Selection Commission",
     "Junior Engineer exam for Electrical discipline. Apply via ssc.gov.in. Includes Paper-I (Objective) + Paper-II (Conventional).",
     "https://ssc.gov.in"),
    ("core-govt", "RRB JE / ALP - Railway Recruitment Board",
     "Junior Engineer and Assistant Loco Pilot posts for Electrical. Notification from rrbcdg.gov.in.",
     "https://rrbcdg.gov.in"),
    ("core-govt", "APSPDCL / APTRANSCO - AP Power Sector",
     "Assistant Engineer / Junior Lineman recruitment by AP power utilities. Track apdcl.ap.gov.in for notifications.",
     "https://www.apdcl.ap.gov.in"),
    ("core-govt", "DRDO / ISRO / BARC Technical Posts",
     "Research and technical entry for EEE graduates through DRDO CEPTAM, ISRO Scientist/Engineer, BARC OCES.",
     "https://www.drdo.gov.in"),
    ("core-private", "L&T, Siemens, ABB, Schneider Electric",
     "Core EEE companies hiring for design, project and site engineering roles. Off-campus drives announced on company career pages.",
     "https://www.siemens.com"),
    ("core-private", "Tata Power, Adani, NTPC (via GATE)",
     "Power sector PSUs recruiting through GATE score. Electrical core roles in generation, transmission and distribution.",
     "https://www.tatapower.com"),
    ("noncore-govt", "IBPS PO / Clerk & SBI Exams",
     "Banking sector recruitment - eligibility for all graduates. Prepare with ibps.in notifications.",
     "https://www.ibps.in"),
    ("noncore-govt", "APPSC Group - I / II / IV",
     "Andhra Pradesh state government posts open to engineering graduates. Check psc.ap.gov.in.",
     "https://psc.ap.gov.in"),
    ("noncore-govt", "Defence - AFCAT / CDS / NDA & Police (SI/Constable)",
     "Defence and police recruitment for graduates. AFCAT via afcat.cdac.in.",
     "https://afcat.cdac.in"),
    ("noncore-private", "TCS NQT, Infosys, Wipro, Cognizant",
     "IT services companies hiring all branches through NQT / off-campus tests. Focus on aptitude + coding basics.",
     "https://www.tcs.com"),
    ("noncore-private", "Amazon, Deloitte, Accenture, Tech Mahindra",
     "Non-core IT and consulting roles open to EEE graduates. Off-campus drives throughout the year.",
     "https://www.accenture.com"),
    ("reasoning", "IndiaBix - Logical Reasoning",
     "Large question bank for logical and verbal reasoning with explanations.",
     "https://www.indiabix.com"),
    ("reasoning", "Testbook - Reasoning Practice",
     "Free daily reasoning quizzes and mock tests for govt exams.",
     "https://testbook.com"),
    ("aptitude", "IndiaBix - Quantitative Aptitude",
     "Aptitude questions with step-by-step solutions - core company test prep.",
     "https://www.indiabix.com/aptitude/questions-and-answers/"),
    ("aptitude", "GeeksforGeeks - Aptitude",
     "Aptitude practice and placement preparation articles.",
     "https://www.geeksforgeeks.org/aptitude-gq/"),
    ("arithmetic", "Speed Arithmetic - Math shortcut techniques",
     "Vedic math and speed calculation techniques for exams.",
     "https://www.cuemath.com/learn/vedic-maths/"),
    ("arithmetic", "Arithmetic Practice - Career Power",
     "Arithmetic questions for SSC / banking with shortcuts.",
     "https://careerpower.in/arithmetic-questions.html"),
    ("resume", "Resume Builder - Module",
     "Use the in-site Resume Builder to create your EEE resume step by step.",
     "/resume"),
]

# ============ v3: extra classes ============
# (subject, topic, date, time, room, targeted_to, notes)
EXTRA_CLASSES = [
    ("Power System Analysis - II", "Fault Analysis - Problem Solving", "2026-08-20", "5:00 - 6:30 PM", "Room 204", "backlog", "Numerical practice for symmetrical faults"),
    ("Power Electronics - II", "DC-DC Converters - Basics Refresher", "2026-08-22", "5:00 - 6:30 PM", "Room 204", "backlog", "Concepts + solved examples"),
    ("Control Systems", "Root Locus - Step by Step", "2026-08-27", "4:30 - 6:00 PM", "Room 204", "All", "Open to all students"),
    ("Digital Signal Processing", "DFT & FFT - Revision", "2026-09-03", "5:00 - 6:30 PM", "DSP Lab", "backlog", "For students below 75% in DSP internals"),
    ("Electrical Machine Design", "Transformer Design - Numerical Session", "2026-09-10", "5:00 - 6:30 PM", "Room 204", "backlog", "Practice design calculations"),
    ("Microprocessors & Microcontrollers", "8086 Assembly - Lab Practice", "2026-09-15", "4:30 - 6:00 PM", "MPMC Lab", "backlog", "Hands-on programming session"),
]

# ============ v3: syllabus tracker (units with progress) ============
# (subject, unit, status, covered_on)
SYLLABUS_TRACKER = [
    ("Power System Analysis - II", "I", "Completed", "2026-07-20"),
    ("Power System Analysis - II", "II", "Completed", "2026-08-05"),
    ("Power System Analysis - II", "III", "In Progress", ""),
    ("Power System Analysis - II", "IV", "Pending", ""),
    ("Power System Analysis - II", "V", "Pending", ""),
    ("Power System Analysis - II", "VI", "Pending", ""),
    ("Power Electronics - II", "I", "Completed", "2026-07-18"),
    ("Power Electronics - II", "II", "Completed", "2026-08-02"),
    ("Power Electronics - II", "III", "In Progress", ""),
    ("Power Electronics - II", "IV", "Pending", ""),
    ("Power Electronics - II", "V", "Pending", ""),
    ("Power Electronics - II", "VI", "Pending", ""),
    ("Electrical Machine Design", "I", "Completed", "2026-07-22"),
    ("Electrical Machine Design", "II", "Completed", "2026-08-08"),
    ("Electrical Machine Design", "III", "In Progress", ""),
    ("Electrical Machine Design", "IV", "Pending", ""),
    ("Electrical Machine Design", "V", "Pending", ""),
    ("Electrical Machine Design", "VI", "Pending", ""),
    ("Control Systems", "I", "Completed", "2026-07-15"),
    ("Control Systems", "II", "Completed", "2026-08-01"),
    ("Control Systems", "III", "In Progress", ""),
    ("Control Systems", "IV", "Pending", ""),
    ("Control Systems", "V", "Pending", ""),
    ("Control Systems", "VI", "Pending", ""),
    ("Microprocessors & Microcontrollers", "I", "Completed", "2026-07-19"),
    ("Microprocessors & Microcontrollers", "II", "Completed", "2026-08-04"),
    ("Microprocessors & Microcontrollers", "III", "In Progress", ""),
    ("Microprocessors & Microcontrollers", "IV", "Pending", ""),
    ("Microprocessors & Microcontrollers", "V", "Pending", ""),
    ("Microprocessors & Microcontrollers", "VI", "Pending", ""),
    ("Digital Signal Processing", "I", "Completed", "2026-07-17"),
    ("Digital Signal Processing", "II", "Completed", "2026-07-30"),
    ("Digital Signal Processing", "III", "In Progress", ""),
    ("Digital Signal Processing", "IV", "Pending", ""),
    ("Digital Signal Processing", "V", "Pending", ""),
    ("Digital Signal Processing", "VI", "Pending", ""),
]
#!/usr/bin/env python3
"""Migrate eee_site to REAL JNTUGV R23 EEE syllabus (from official PDF).

Replaces placeholder subjects with real ones across ALL tables,
adds full semester coverage (2-1 .. 4-1) to the syllabus table,
and remaps attendance/marks/timetable/study data to real subject names.

Usage: .venv/bin/python migrate_real_syllabus.py  (from ~/eee_site)
"""
import sqlite3, json, os, sys

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eee.db")

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# ---------------------------------------------------------------- real syllabus data
# (program, year_sem, subject, code, credits, units[[roman, [topics...]]])
# Codes follow R23 pattern (R23PC/PE/OE/LABxxx) - real titles/credits/units from official PDF
REAL_SYLLABUS = [
    # ---- 2-1 (for completeness) ----
    ("B.Tech", "2-1", "Complex Variables and Numerical Methods", "R23BS05", 3, [
        ["I", ["Functions of complex variable", "Cauchy-Riemann equations", "Analytic functions", "Milne Thomson method"]],
        ["II", ["Line integral", "Cauchy's integral theorem and formula", "Taylor's and Laurent's series", "Residues, Cauchy Residue theorem"]],
        ["III", ["Bisection method", "Iterative method", "Regula-falsi method", "Newton Raphson method"]],
        ["IV", ["Finite differences", "Newton's forward and backward interpolation", "Lagrange's formula"]],
        ["V", ["Taylor's series method", "Picard's method", "Euler's and modified Euler's methods", "Runge-Kutta methods (2nd and 4th order)"]],
    ]),
    ("B.Tech", "2-1", "Universal Human Values and Ethical Human Conduct", "R23HS02", 3, [
        ["I", ["Need for value education", "Basic human aspirations", "Continuous happiness and prosperity"]],
        ["II", ["Self-exploration", "Natural acceptance", "Harmony in the human being"]],
        ["III", ["Harmony in the family", "Trust and respect", "Understanding relationships"]],
        ["IV", ["Harmony in society", "Samadhan, Samridhi, Abhay, Sah-astitva"]],
        ["V", ["Professional ethics", "Competence and conscience", "Implications of holistic understanding"]],
    ]),
    ("B.Tech", "2-1", "Electromagnetic Field Theory", "R23PC201", 3, [
        ["I", ["Vector analysis", "Coordinate systems", "Gradient, divergence, curl"]],
        ["II", ["Electrostatic fields", "Coulomb's law", "Gauss's law", "Electric potential"]],
        ["III", ["Magnetostatics", "Biot-Savart law", "Ampere's law", "Magnetic flux density"]],
        ["IV", ["Maxwell's equations", "Time-varying fields", "Displacement current"]],
        ["V", ["Electromagnetic waves", "Plane waves", "Poynting theorem"]],
    ]),
    ("B.Tech", "2-1", "Electrical Circuit Analysis-II", "R23PC202", 3, [
        ["I", ["Network topology", "Graph theory", "Incidence matrices", "Duality"]],
        ["II", ["Two-port networks", "Z, Y, h, ABCD parameters", "Interconnection of two-port networks"]],
        ["III", ["Transient analysis", "RL, RC, RLC circuits", "Laplace transform applications"]],
        ["IV", ["Resonance", "Series and parallel resonance", "Q-factor and bandwidth"]],
        ["V", ["Three-phase circuits", "Balanced and unbalanced loads", "Power measurement"]],
    ]),
    ("B.Tech", "2-1", "DC Machines and Transformers", "R23PC203", 3, [
        ["I", ["DC generator principles", "EMF equation", "Armature reaction", "Commutation"]],
        ["II", ["DC motor characteristics", "Speed control", "Starting methods", "Braking"]],
        ["III", ["Transformer principles", "Equivalent circuits", "Testing", "Efficiency and regulation"]],
        ["IV", ["Three-phase transformers", "Vector groups", "Parallel operation", "Autotransformers"]],
        ["V", ["Instrument transformers", "CT and PT", "Cooling methods", "Transformer maintenance"]],
    ]),
    # ---- 2-2 REAL subjects ----
    ("B.Tech", "2-2", "Managerial Economics and Financial Analysis", "R23HS12", 2, [
        ["I", ["Introduction to Managerial Economics", "Demand analysis", "Elasticity of demand", "Demand forecasting"]],
        ["II", ["Production and Cost Analysis", "Production function", "Cost concepts", "Break-even analysis", "Economies of scale"]],
        ["III", ["Market Structures and Pricing", "Perfect competition, monopoly, oligopoly", "Pricing methods", "Price discrimination"]],
        ["IV", ["Financial Analysis", "Financial statements", "Ratio analysis", "Funds flow and cash flow analysis"]],
        ["V", ["Capital Budgeting", "Time value of money", "NPV, IRR, payback period", "Capital budgeting decisions"]],
    ]),
    ("B.Tech", "2-2", "Analog Circuits", "R23PC211", 3, [
        ["I", ["Diode Circuits", "Diode characteristics", "Rectifiers and filters", "Clippers and clampers", "Zener regulators"]],
        ["II", ["Transistor Amplifiers", "BJT biasing and stabilization", "Small signal analysis", "Common emitter, base, collector amplifiers"]],
        ["III", ["FET Amplifiers", "JFET and MOSFET characteristics", "Biasing", "Small signal FET amplifiers"]],
        ["IV", ["Feedback Amplifiers and Oscillators", "Feedback topologies", "Effect of feedback", "RC, LC and crystal oscillators"]],
        ["V", ["Power Amplifiers and Op-Amps", "Class A, B, AB, C amplifiers", "Op-amp characteristics", "Applications of op-amps"]],
    ]),
    ("B.Tech", "2-2", "Power Systems-I", "R23PC212", 3, [
        ["I", ["Power System Structure", "Generation, transmission, distribution", "Load characteristics", "Power plant economics"]],
        ["II", ["Thermal and Hydro Power Plants", "Layout and components", "Coal handling, combustion", "Hydroelectric plant types"]],
        ["III", ["Nuclear and Renewable Power Plants", "Nuclear reactor types", "Gas and diesel plants", "Solar, wind, biomass integration"]],
        ["IV", ["Transmission Systems", "AC and DC transmission", "Overhead and underground lines", "Distribution systems"]],
        ["V", ["Substations and Switchgear", "Types of substations", "Bus bar arrangements", "Isolators, CTs, PTs", "Lightning arresters"]],
    ]),
    ("B.Tech", "2-2", "Induction and Synchronous Machines", "R23PC213", 3, [
        ["I", ["Three-phase Induction Motors", "Construction and principle", "Equivalent circuit", "Torque-slip characteristics", "Starting methods"]],
        ["II", ["Speed Control of Induction Motors", "Stator voltage and frequency control", "Rotor resistance control", "Cascade operation", "Braking"]],
        ["III", ["Single-phase Induction Motors", "Double revolving field theory", "Split-phase, capacitor, shaded pole motors", "Applications"]],
        ["IV", ["Synchronous Generators", "Construction and principle", "EMF equation", "Armature reaction", "Voltage regulation (EMF, MMF, ZPF methods)"]],
        ["V", ["Synchronous Motors", "Principle of operation", "V-curves and inverted V-curves", "Hunting and damping", "Applications"]],
    ]),
    ("B.Tech", "2-2", "Control Systems", "R23PC214", 3, [
        ["I", ["Mathematical Modelling", "Transfer function", "Block diagrams and reduction", "Signal flow graphs", "Mason's gain formula"]],
        ["II", ["Time Response Analysis", "Transient and steady state response", "First and second order systems", "Error constants and steady state errors"]],
        ["III", ["Stability Analysis", "Concept of stability", "Routh-Hurwitz criterion", "Root locus technique"]],
        ["IV", ["Frequency Response Analysis", "Bode plots", "Nyquist criterion", "Polar plots", "Gain and phase margins"]],
        ["V", ["State Space Analysis and Compensators", "State space representation", "Controllability and observability", "Lead, lag, lead-lag compensators", "PID controllers"]],
    ]),
    # ---- 3-1 REAL subjects (Hari's current semester) ----
    ("B.Tech", "3-1", "Power Electronics", "R23PC301", 3, [
        ["I", ["Power Semi-Conductor Devices", "SCR - Two transistor analogy", "Static and Dynamic characteristics", "Turn on and Turn off Methods", "Triggering Methods (R, RC and UJT)", "Snubber circuit design", "Power MOSFET and IGBT"]],
        ["II", ["Single-phase AC-DC Converters", "Half-wave controlled rectifiers", "Fully controlled mid-point and bridge converter", "Continuous and Discontinuous conduction", "Effect of source inductance", "Single-phase Semi-Converter", "Dual converter"]],
        ["III", ["Three-phase AC-DC Converters & AC-AC Converters", "Three-phase half-wave rectifier", "Fully controlled rectifier with R and RL load", "Semi converter with R and RL load", "Single-phase AC-AC power control", "Single-phase step up/down Cycloconverter"]],
        ["IV", ["DC-DC Converters", "Basic Chopper", "Buck, Boost and Buck-Boost converters", "CCM and DCM analysis", "Volt-sec balance", "Output and inductor current ripple", "PWM control techniques"]],
        ["V", ["DC-AC Converters", "Square wave inverters", "Single and three phase inverters", "PWM inverters", "Voltage control and harmonic mitigation", "Current source inverters"]],
    ]),
    ("B.Tech", "3-1", "Digital Circuits", "R23PC302", 3, [
        ["I", ["Combinational logic circuits - I", "Canonical forms", "Boolean algebra simplification", "NAND and NOR implementations", "Karnaugh maps - 3 and 4 variables", "Quine-McCluskey minimization", "Adders and subtractors", "Binary comparators"]],
        ["II", ["Combinational logic circuits - II", "Decoders", "BCD and 7-segment decoders", "Multiplexers and demultiplexers", "Encoders and priority encoders", "ROM and programmable logic"]],
        ["III", ["Sequential logic circuits", "Flip-flops: SR, JK, D, T", "Master-slave and edge-triggered flip-flops", "Excitation tables", "Design of counters", "Johnson and ring counters", "Shift registers"]],
        ["IV", ["Sequential Circuit Design", "Mealy and Moore models", "State machine notation", "Synchronous sequential circuit analysis", "State diagrams and reduction", "Sequence detector circuits"]],
        ["V", ["Digital integrated circuits", "Logic levels and propagation delay", "Fan-out, fan-in, noise margin", "RTL and DTL circuits", "TTL and ECL", "CMOS and transmission gates"]],
    ]),
    ("B.Tech", "3-1", "Power Systems-II", "R23PC303", 3, [
        ["I", ["Transmission Line Parameters Calculations", "Line conductors and cables", "Resistance, inductance and capacitance", "GMD and GMR", "Transposition of lines"]],
        ["II", ["Performance Analysis of Transmission Lines", "Short, medium and long lines", "ABCD constants", "Voltage regulation", "Ferranti effect", "Power flow through lines"]],
        ["III", ["Power System Transients", "Switching transients", "Lightning transients", "Travelling waves", "Surge impedance loading", "Insulation coordination"]],
        ["IV", ["Corona and Effects of transmission lines", "Corona discharge", "Critical disruptive voltage", "Visual critical voltage", "Power loss due to corona", "Radio interference"]],
        ["V", ["Sag and Tension Calculations and Overhead Line Insulators", "Sag and tension in conductors", "Effect of wind and ice", "String efficiency", "Voltage distribution", "Insulator types and testing"]],
    ]),
    ("B.Tech", "3-1", "Signals and Systems", "R23PE301", 3, [
        ["I", ["Introduction", "Definition of signals and systems", "Classification of signals", "Classification of systems", "Basic operations on signals"]],
        ["II", ["Fourier Series and Fourier Transform", "Dirichlet conditions", "Trigonometric and exponential FS", "Properties of Fourier transform", "Parseval's theorem"]],
        ["III", ["Analysis of Linear Systems", "LTI systems", "Impulse response and convolution", "Causality and stability", "Differential equation representation"]],
        ["IV", ["Correlation", "Autocorrelation", "Cross-correlation", "Properties", "Energy and power spectral density"]],
        ["V", ["Laplace Transforms", "Region of convergence", "Properties of Laplace transform", "Inverse Laplace transform", "System analysis using Laplace transform"]],
    ]),
    ("B.Tech", "3-1", "Renewable Energy Sources", "R23OE301", 3, [
        ["I", ["Solar Energy", "Solar radiation and measurement", "Solar thermal collectors", "Solar photovoltaic systems", "Applications"]],
        ["II", ["Wind Energy", "Wind characteristics", "Wind turbines - types and components", "Power in the wind", "Wind farms and site selection"]],
        ["III", ["Biomass, Hydel and Geothermal Energy", "Biomass conversion technologies", "Biogas plants", "Small hydro power", "Geothermal energy systems"]],
        ["IV", ["Energy from Oceans, Waves and Tides", "OTEC", "Tidal power plants", "Wave energy converters", "Ocean thermal gradients"]],
        ["V", ["Chemical Energy Sources", "Fuel cells", "Hydrogen energy", "Battery technologies", "Energy storage systems"]],
    ]),
    ("B.Tech", "3-1", "Electrical Machine Design", "R23OE302", 3, [
        ["I", ["Fundamental Aspects of Electrical Machine Design", "Design factors", "Specific electric and magnetic loadings", "Thermal considerations", "Magnetic materials"]],
        ["II", ["Design of transformers", "Output equation", "Core and winding design", "Cooling systems", "Design of tank and cooling tubes"]],
        ["III", ["Design of DC Machines", "Output equation", "Main dimensions", "Armature design", "Field system design"]],
        ["IV", ["Design of Induction motors", "Output equation", "Stator and rotor design", "Squirrel cage and slip ring motors", "Dispersion coefficient"]],
        ["V", ["Design of Synchronous Machines", "Output equation", "Main dimensions", "Field winding design", "Damper windings", "Design of salient pole machines"]],
    ]),
    ("B.Tech", "3-1", "Intelligent Control Systems", "R23OE303", 3, [
        ["I", ["Introduction to Intelligent Control Systems", "Conventional vs intelligent control", "Expert systems", "Architecture of intelligent controllers"]],
        ["II", ["Artificial Neural Networks (ANNs)", "Biological neurons and models", "Perceptron", "Backpropagation algorithm", "ANN in control"]],
        ["III", ["Fuzzy Logic Systems", "Fuzzy sets and membership functions", "Fuzzy rules and inference", "Fuzzification and defuzzification", "Fuzzy PID controllers"]],
        ["IV", ["Genetic Algorithms (GAs)", "Chromosome representation", "Selection, crossover, mutation", "Fitness function", "GA in controller design"]],
        ["V", ["Hybrid Intelligent Systems and Applications", "Neuro-fuzzy systems", "GA-fuzzy systems", "Industrial applications", "Case studies"]],
    ]),
    # ---- 3-2 REAL subjects ----
    ("B.Tech", "3-2", "Electrical Measurements and Instrumentation", "R23PC311", 3, [
        ["I", ["Analog Ammeter and Voltmeters", "PMMC instruments", "Moving iron instruments", "Extension of range - shunts and multipliers", "Errors and compensation"]],
        ["II", ["Analog Wattmeters and Power Factor Meters", "Electrodynamometer wattmeter", "Low power factor wattmeter", "Energy meters", "Power factor meters"]],
        ["III", ["Measurements of Electrical parameters", "DC and AC bridges", "Wheatstone, Kelvin, Maxwell, Schering bridges", "Measurement of resistance, inductance, capacitance", "Q-meter"]],
        ["IV", ["Transducers", "Resistive, capacitive, inductive transducers", "LVDT", "Strain gauges", "Temperature transducers", "Piezoelectric transducers"]],
        ["V", ["Digital meters", "Digital voltmeters", "Digital frequency meters", "Digital multimeters", "Data acquisition systems", "Recorders and displays"]],
    ]),
    ("B.Tech", "3-2", "Microprocessors and Microcontrollers", "R23PC312", 3, [
        ["I", ["8086 Microprocessors and Assembly Language Programming", "Architecture of 8086", "Register organization", "Pipelining", "Memory segmentation", "Addressing modes", "Instruction set"]],
        ["II", ["8086 Operational Modes and Memory Interfacing", "Minimum and maximum modes", "Timing diagrams", "Procedures and macros", "Static RAM interfacing", "8255 PPI interfacing", "DMA"]],
        ["III", ["8051 Microcontroller", "Comparison of microprocessor and microcontroller", "8051 architecture", "Pin description", "Addressing modes and instruction set", "Timers, interrupts, UART"]],
        ["IV", ["Interfacing 8051 with Peripherals", "Matrix keypad", "LCD and seven-segment displays", "L293D motor driver", "Stepper motor", "ADC 0804 and DAC 0808"]],
        ["V", ["Sensor and Relay Interfacing with 8051", "Temperature sensor LM35", "Relay interfacing", "Case studies and practical applications"]],
    ]),
    ("B.Tech", "3-2", "Power System Analysis", "R23PC313", 3, [
        ["I", ["Circuit Topology", "Graph theory definitions", "Incidence matrices", "Ybus formation", "Per unit representation", "Impedance diagrams"]],
        ["II", ["Power Flow Studies", "Static power flow equations", "Gauss-Seidel method", "Newton-Raphson method", "Decoupled and fast decoupled methods", "3-bus numerical problems"]],
        ["III", ["Z-Bus Algorithm", "Formation of Zbus", "Modification algorithms", "Symmetrical fault analysis", "Fault current computation"]],
        ["IV", ["Symmetrical Components", "Sequence components", "Sequence networks", "LG, LL, LLG faults", "Open conductor faults"]],
        ["V", ["Power System Stability Analysis", "Swing equation", "Equal area criterion", "Steady state and transient stability", "Improvement of stability"]],
    ]),
    ("B.Tech", "3-2", "Switchgear and Protection", "R23PE311", 3, [
        ["I", ["Circuit Breakers", "Arc interruption theory", "Oil, air blast, SF6, vacuum breakers", "Rated characteristics", "Testing of circuit breakers"]],
        ["II", ["Electromagnetic Protection", "Overcurrent relays", "Directional relays", "Differential relays", "Distance relays", "Relay settings"]],
        ["III", ["Generator Protection", "Stator faults", "Rotor faults", "Loss of excitation", "Overheating protection", "Reverse power protection"]],
        ["IV", ["Feeder and Bus bar Protection & Static Relays", "Feeder protection", "Bus bar protection", "Static relays", "Microprocessor-based relays"]],
        ["V", ["Protection against over voltage and grounding", "Lightning arresters", "Surge protectors", "Neutral grounding", "Isolated and solid grounding", "Protection coordination"]],
    ]),
    ("B.Tech", "3-2", "Advanced Control Systems", "R23PE312", 3, [
        ["I", ["Controllability - Observability and Design of Pole Placement", "Concepts of controllability", "Observability", "Pole placement by state feedback", "Observer design"]],
        ["II", ["Nonlinear Systems", "Types of nonlinearities", "Describing function analysis", "Phase plane method", "Limit cycles"]],
        ["III", ["Stability analysis by Lyapunov Method", "Lyapunov stability theorems", "Lyapunov functions", "Stability of nonlinear systems"]],
        ["IV", ["Calculus of Variations", "Euler-Lagrange equation", "Functional minimization", "Transversality conditions"]],
        ["V", ["Optimal Control", "Optimal control problem", "Pontryagin's minimum principle", "Linear quadratic regulator", "Riccati equation"]],
    ]),
    ("B.Tech", "3-2", "Electric Drives", "R23PE313", 3, [
        ["I", ["Fundamentals of Electric Drives", "Dynamics of electric drives", "Load characteristics", "Four quadrant operation", "Selection of motors"]],
        ["II", ["Converter Fed DC Motor Drives", "Single and three phase converter drives", "Dual converter drives", "Rectifier control of DC motors"]],
        ["III", ["DC-DC Converter Fed DC Motor Drives", "Chopper controlled DC drives", "Motoring and braking", "Regenerative braking"]],
        ["IV", ["Control of 3-phase Induction motor Drives", "Stator voltage control", "V/f control", "Rotor resistance control", "Vector control concepts"]],
        ["V", ["Control of Synchronous Motor Drives", "Synchronous motor drives", "Brushless DC drives", "Permanent magnet synchronous motor drives"]],
    ]),
    ("B.Tech", "3-2", "Digital Signal Processing", "R23PE314", 3, [
        ["I", ["Introduction to Digital Signal Processing", "Discrete time signals and systems", "Z-transform", "Difference equations", "Sampling and aliasing"]],
        ["II", ["Discrete Fourier Transforms and FFT Algorithms", "DFT and its properties", "Linear and circular convolution", "Radix-2 FFT", "DIT and DIF algorithms"]],
        ["III", ["Design and Realizations of IIR Digital Filters", "Butterworth and Chebyshev approximations", "Bilinear transformation", "Impulse invariance", "Realization structures"]],
        ["IV", ["Design and Realizations of FIR Digital Filters", "Window functions", "Frequency sampling method", "Linear phase FIR filters", "Realization structures"]],
        ["V", ["Multirate Digital Signal Processing", "Decimation and interpolation", "Polyphase filters", "Multirate filter banks", "Applications"]],
    ]),
    ("B.Tech", "3-2", "High Voltage Engineering", "R23PE315", 3, [
        ["I", ["Break down phenomenon in Gaseous and Vacuum", "Townsend's theory", "Streamer theory", "Paschen's law", "Vacuum breakdown"]],
        ["II", ["Break down phenomenon in Liquids", "Conduction and breakdown in liquids", "Suspended particle theory", "Cavitation theory", "Transformer oil testing"]],
        ["III", ["Generation of High DC voltages", "Rectifier circuits", "Cockcroft-Walton voltage multiplier", "Van de Graaff generator", "Electrostatic generators"]],
        ["IV", ["Generation of Impulse voltages", "Impulse voltage waves", "Marx circuit", "Impulse current generation", "Tripping and triggering"]],
        ["V", ["Measurement of High DC and AC Voltages", "Sphere gaps", "Potential dividers", "Peak voltmeters", "Electrostatic voltmeters", "Schering bridge for HV"]],
    ]),
    # ---- 4-1 REAL subjects ----
    ("B.Tech", "4-1", "Power System Operation and Control", "R23PC401", 3, [
        ["I", ["Economic Operation of Power Systems", "Heat rate and cost curves", "Incremental fuel cost", "Optimum generation allocation", "Loss coefficients"]],
        ["II", ["Hydrothermal Scheduling", "Hydroelectric plant models", "Scheduling problems", "Short term hydrothermal scheduling"]],
        ["III", ["Unit Commitment", "Need and constraints", "Cost function formulation", "Priority ordering", "Dynamic programming solution"]],
        ["IV", ["Load Frequency Control", "Single and two area systems", "Turbine and governor models", "P-I controllers", "Automatic generation control"]],
        ["V", ["Reactive Power Control and Compensation", "Voltage regulation", "Shunt and series compensation", "FACTS overview", "Compensation of transmission lines"]],
    ]),
    ("B.Tech", "4-1", "Energy Management and Auditing", "R23PC402", 2, [
        ["I", ["Energy Management Principles", "Energy audit types", "Energy conservation act", "Energy economics"]],
        ["II", ["Electrical Energy Audit", "Power factor improvement", "Demand side management", "Energy efficient motors and lighting"]],
        ["III", ["Energy Monitoring and Targeting", "Benchmarking", "Energy performance indicators", "Data analysis techniques"]],
        ["IV", ["Energy Efficient Technologies", "Variable speed drives", "Cogeneration", "Waste heat recovery", "Energy storage"]],
        ["V", ["Case Studies", "Industrial energy audits", "Commercial building audits", "Reporting and implementation"]],
    ]),
    ("B.Tech", "4-1", "HVDC Transmission", "R23PE401", 3, [
        ["I", ["Introduction to HVDC", "Comparison of AC and DC transmission", "Types of HVDC links", "Economics of HVDC"]],
        ["II", ["Converters", "Line commutated converters", "Voltage source converters", "Converter circuits", "Firing angle control"]],
        ["III", ["HVDC Control", "Constant current and constant power control", "Current and extinction angle control", "Power reversal"]],
        ["IV", ["Harmonics and Filters", "Harmonics in HVDC systems", "AC and DC filters", "Reactive power requirements"]],
        ["V", ["Multi-terminal HVDC", "MTDC systems", "Control and protection", "HVDC applications in India"]],
    ]),
    ("B.Tech", "4-1", "FACTS", "R23PE402", 3, [
        ["I", ["Introduction to FACTS", "Transmission line compensation", "Series and shunt compensation", "Power flow control"]],
        ["II", ["Static Var Compensators", "SVC configurations", "TCR and TSC", "SVC characteristics", "Voltage control applications"]],
        ["III", ["Thyristor Controlled Series Compensator", "TCSC principles", "GCSC and TSSC", "Subsynchronous resonance mitigation"]],
        ["IV", ["STATCOM", "Voltage source converters", "STATCOM characteristics", "Comparison with SVC"]],
        ["V", ["UPFC and Applications", "UPFC principle and control", "SSSC", "FACTS controller coordination", "Case studies"]],
    ]),
    ("B.Tech", "4-1", "Electric Vehicles", "R23PE403", 3, [
        ["I", ["Introduction", "History and evolution of EVs", "EV vs ICE vehicles", "EV market and policy"]],
        ["II", ["Components of Electric Vehicles", "EV architecture", "Battery packs and BMS", "Power converters", "Charging systems"]],
        ["III", ["Motors for Electric Vehicles", "DC motors", "Induction motors", "PMSM and BLDC motors", "Motor controllers"]],
        ["IV", ["Hybrid Electric Vehicles", "HEV architectures", "Series, parallel and series-parallel", "Plug-in hybrids", "Energy management strategies"]],
        ["V", ["Energy Sources for Electric Vehicles", "Batteries: Li-ion, NiMH, Lead-acid", "Fuel cells", "Supercapacitors", "Battery charging and fast charging"]],
    ]),
    ("B.Tech", "4-1", "Battery Management Systems", "R23OE401", 3, [
        ["I", ["Battery Fundamentals", "Cell chemistry and parameters", "SOC, SOH, SOE estimation", "Battery modeling"]],
        ["II", ["Battery Monitoring", "Voltage, current and temperature sensing", "Cell balancing - passive and active", "Battery protection circuits"]],
        ["III", ["SOC and SOH Estimation", "Coulomb counting", "Kalman filtering", "Impedance spectroscopy"]],
        ["IV", ["BMS Architectures", "Centralized and distributed BMS", "Communication protocols (CAN, SMBus)", "BMS software and algorithms"]],
        ["V", ["BMS Applications", "EV battery packs", "Grid storage systems", "Thermal management", "Safety and standards"]],
    ]),
    ("B.Tech", "4-1", "Concepts of Smart Grid", "R23OE402", 3, [
        ["I", ["Introduction to Smart Grid", "Smart grid vision", "Smart grid vs conventional grid", "Smart grid technologies"]],
        ["II", ["Smart Metering and AMI", "Smart meters", "Advanced metering infrastructure", "Two-way communication"]],
        ["III", ["Distribution Automation", "SCADA in distribution", "Distribution management systems", "Outage management"]],
        ["IV", ["Demand Response and DER", "Demand response programs", "Distributed energy resources", "Microgrids and islanding"]],
        ["V", ["Smart Grid Communications and Cyber Security", "Communication architectures", "IoT in smart grids", "Cyber security challenges"]],
    ]),
    ("B.Tech", "4-1", "Concepts of Power Quality", "R23OE403", 3, [
        ["I", ["Introduction to Power Quality", "PQ problems and their impact", "Transients, sags, swells, interruptions", "PQ standards and indices"]],
        ["II", ["Voltage Sags and Swells", "Sources of sags and swells", "Characteristics", "Mitigation techniques", "DVR"]],
        ["III", ["Harmonics", "Harmonic sources", "Effects of harmonics", "Passive and active filters", "IEEE 519"]],
        ["IV", ["Unbalance and Flicker", "Voltage unbalance", "Flicker measurement", "Mitigation"]],
        ["V", ["Power Quality Monitoring and Mitigation", "PQ monitoring instruments", "Case studies", "UPQC and custom power devices"]],
    ]),
]

# ---------------------------------------------------------------- mapping old -> new subject names
SUBJECT_MAP = {
    "Power System Analysis - II": "Power Systems-II",
    "Power Electronics - II": "Power Electronics",
    "Electrical Machine Design": "Electrical Machine Design",
    "Control Systems": "Control Systems",
    "Microprocessors & Microcontrollers": "Microprocessors and Microcontrollers",
    "Digital Signal Processing": "Digital Signal Processing",
}

# ---------------------------------------------------------------- real 3-1 timetable (Mon-Sat x 7 periods)
# (day, period, subject, faculty, room)
REAL_TIMETABLE = [
    (1, 1, "Power Electronics", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (1, 2, "Power Systems-II", "Praveen", "Room 204"),
    (1, 3, "Digital Circuits", "Bhanuchandra", "Room 204"),
    (1, 4, "Renewable Energy Sources", "Dr. G.T. Chandra Sekhar", "Room 205"),
    (1, 5, "Power Electronics Lab", "Praveen", "Lab 1"),
    (1, 6, "Power Electronics Lab", "Praveen", "Lab 1"),
    (1, 7, "Soft Skills", "Bhanuchandra", "Room 205"),
    (2, 1, "Power Electronics", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (2, 2, "Digital Circuits", "Bhanuchandra", "Room 204"),
    (2, 3, "Power Systems-II", "Praveen", "Room 204"),
    (2, 4, "Signals and Systems", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (2, 5, "Analog and Digital Circuits Lab", "Bhanuchandra", "Lab 2"),
    (2, 6, "Analog and Digital Circuits Lab", "Bhanuchandra", "Lab 2"),
    (2, 7, "Tinkering Lab", "Praveen", "Lab 3"),
    (3, 1, "Power Systems-II", "Praveen", "Room 204"),
    (3, 2, "Power Electronics", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (3, 3, "Renewable Energy Sources", "Dr. G.T. Chandra Sekhar", "Room 205"),
    (3, 4, "Digital Circuits", "Bhanuchandra", "Room 204"),
    (3, 5, "Power Electronics Lab", "Praveen", "Lab 1"),
    (3, 6, "Power Electronics Lab", "Praveen", "Lab 1"),
    (3, 7, "Tinkering Lab", "Praveen", "Lab 3"),
    (4, 1, "Digital Circuits", "Bhanuchandra", "Room 204"),
    (4, 2, "Power Electronics", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (4, 3, "Signals and Systems", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (4, 4, "Power Systems-II", "Praveen", "Room 204"),
    (4, 5, "Analog and Digital Circuits Lab", "Bhanuchandra", "Lab 2"),
    (4, 6, "Analog and Digital Circuits Lab", "Bhanuchandra", "Lab 2"),
    (4, 7, "Soft Skills", "Bhanuchandra", "Room 205"),
    (5, 1, "Power Systems-II", "Praveen", "Room 204"),
    (5, 2, "Digital Circuits", "Bhanuchandra", "Room 204"),
    (5, 3, "Power Electronics", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (5, 4, "Renewable Energy Sources", "Dr. G.T. Chandra Sekhar", "Room 205"),
    (5, 5, "Signals and Systems", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (5, 6, "Soft Skills", "Bhanuchandra", "Room 205"),
    (5, 7, "Tinkering Lab", "Praveen", "Lab 3"),
    (6, 1, "Renewable Energy Sources", "Dr. G.T. Chandra Sekhar", "Room 205"),
    (6, 2, "Power Electronics", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (6, 3, "Power Systems-II", "Praveen", "Room 204"),
    (6, 4, "Digital Circuits", "Bhanuchandra", "Room 204"),
    (6, 5, "Signals and Systems", "Dr. G.T. Chandra Sekhar", "Room 204"),
    (6, 6, "Soft Skills", "Bhanuchandra", "Room 205"),
    (6, 7, "Tinkering Lab", "Praveen", "Lab 3"),
]

# ---------------------------------------------------------------- do it
def main():
    print("Backing up database...")
    import shutil
    shutil.copy(DB, DB + ".bak_real")
    print("  backup -> eee.db.bak_real")

    # 1. Wipe and reload syllabus with real data
    print("Rebuilding syllabus table (real R23 data)...")
    cur.execute("DELETE FROM syllabus")
    for prog, ys, subj, code, creds, units in REAL_SYLLABUS:
        cur.execute(
            "INSERT INTO syllabus (program,year_sem,subject,code,credits,units) VALUES (?,?,?,?,?,?)",
            (prog, ys, subj, code, creds, json.dumps(units)),
        )
    print(f"  inserted {len(REAL_SYLLABUS)} real subject records")

    # 2. Rename subjects in all data tables
    print("Renaming subjects across data tables...")
    for table in ["attendance", "marks", "study_materials", "pyq", "solved_papers",
                  "syllabus_tracker", "extra_classes"]:
        for old, new in SUBJECT_MAP.items():
            if old == new:
                continue
            cur.execute(f"UPDATE {table} SET subject=? WHERE subject=?", (new, old))
        # report distinct names now
        rows = cur.execute(f"SELECT DISTINCT subject FROM {table}").fetchall()
        print(f"  {table}: {[r[0] for r in rows]}")

    # 3. Rebuild timetable with real 3-1 schedule
    print("Rebuilding 3-1 timetable...")
    cur.execute("DELETE FROM timetable WHERE program='B.Tech' AND year_sem='3-1'")
    for day, period, subj, fac, room in REAL_TIMETABLE:
        cur.execute(
            "INSERT INTO timetable (program,year_sem,day,period,subject,faculty,room) VALUES ('B.Tech','3-1',?,?,?,?,?)",
            (day, period, subj, fac, room),
        )
    print(f"  inserted {len(REAL_TIMETABLE)} slots")

    conn.commit()
    conn.close()
    print("\nDONE. Real R23 syllabus + timetable + data rename complete.")

if __name__ == "__main__":
    main()

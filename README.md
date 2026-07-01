# 🔬 HND Electronics & Physics Laboratory Platform

> An interactive, browser-based academic simulation platform for HND Physics and Electronics students.  
> Built with **Python · Streamlit · Plotly**

---

## About

This platform provides four virtual laboratory practicals covering core HND Electronics and Physics topics. Students log in with their matriculation number, work through each practical's theory, simulation, and assessment, and receive an auto-graded score. A performance dashboard tracks results across all four practicals.

---

## Practicals

| # | Topic | Type |
|---|---|---|
| P1 | Forward & Reverse Bias Characteristics of Si and Ge Diodes | Manual data entry + I-V curve tracer |
| P2 | Half-Wave & Full-Wave Rectification | Live waveform simulation |
| P3 | Zener Diode Shunt Voltage Stabilizer | Auto-calculation + regulation plot |
| P4 | BJT Common-Emitter Characteristics & Load Line Analysis | Family of curves + Q-point |

Each practical contains:
- **Theory** — concept explanation, key equations, and circuit diagram (downloadable SVG)
- **Simulation** — interactive plots and computed parameters
- **Assessment** — 5 multiple-choice questions, one attempt, auto-graded out of 100

---

## Features

- Student login via Matriculation Number
- Sidebar navigation with live score summary per practical
- Auto-graded assessments (pass mark: 50/100)
- Performance dashboard with bar chart, grade table, and overall recommendation
- Full CSV analytics log (timestamped actions and scores), downloadable from the dashboard
- Circuit diagrams downloadable as SVG files

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/your-org/hnd-electronics-lab.git
cd hnd-electronics-lab

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run hnd_electronics_lab.py
```

Open `http://localhost:8501` and enter your Matriculation Number to begin.

---

## Requirements

```
streamlit>=1.30.0
numpy>=1.24.0
pandas>=2.0.0
plotly>=5.18.0
```

---

## Project Structure

```
hnd-electronics-lab/
├── hnd_electronics_lab.py     # Main application
├── requirements.txt
├── README.md
└── hnd_lab_analytics.csv      # Auto-generated log (git-ignored)
```

---

## Analytics Log Schema

| Column | Description |
|---|---|
| `Timestamp` | Date and time of the event |
| `Student_ID` | Matriculation number |
| `Action` | Event type (e.g. `P1_Assessment`, `Platform_Login`) |
| `Detail` | Action metadata (score, parameter values, etc.) |

---

## License

MIT — free to use and modify for educational purposes.

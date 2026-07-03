import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Electronics Lab",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #070b14; color: #e0e6f0; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f3c 50%, #080f1e 100%);
    border: 1px solid #1e3a5f; border-radius: 14px;
    padding: 32px 40px; margin-bottom: 28px;
    position: relative; overflow: hidden;
}
.hero::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background: linear-gradient(90deg, transparent, #00d4ff, #7c3aed, transparent);
}
.hero-title { font-family:'Share Tech Mono',monospace; font-size:1.8rem; color:#00d4ff; margin:0; letter-spacing:.05em; }
.hero-sub   { font-size:.82rem; color:#7a9cc4; margin-top:6px; letter-spacing:.1em; text-transform:uppercase; }

/* Section headers */
.sec { font-family:'Share Tech Mono',monospace; font-size:.75rem; color:#00d4ff;
       letter-spacing:.18em; text-transform:uppercase;
       border-bottom:1px solid #1e3a5f; padding-bottom:5px; margin:22px 0 12px; }

/* Metric card */
.mc { background:#0d1520; border:1px solid #1e3a5f; border-radius:8px; padding:14px; text-align:center; }
.mc .ml { font-size:.65rem; color:#7a9cc4; text-transform:uppercase; letter-spacing:.09em; }
.mc .mv { font-family:'Share Tech Mono',monospace; font-size:1.4rem; color:#00d4ff; margin-top:3px; }
.mc .mu { font-size:.65rem; color:#4a7a9b; }

/* Theory box */
.tb { background:#0a1628; border-left:3px solid #0080ff; border-radius:0 8px 8px 0;
      padding:16px 20px; margin:10px 0; font-size:.86rem; color:#c0d4e8; line-height:1.68; }
.tb strong { color:#00d4ff; }

/* Score card */
.score-pass { background:#0a2015; border:1px solid #4ade80; border-radius:8px; padding:16px; color:#4ade80; }
.score-fail { background:#1e0a0a; border:1px solid #f87171; border-radius:8px; padding:16px; color:#f87171; }

/* Nav chip */
.nav-active { background:#0d2a4a; border:1px solid #00d4ff; border-radius:6px;
              padding:8px 14px; color:#00d4ff; font-family:'Share Tech Mono',monospace;
              font-size:.78rem; letter-spacing:.05em; }

/* Param display */
.pd { background:#0d1520; border:1px solid #1e3a5f; border-radius:8px;
      padding:9px 0; text-align:center; font-family:'Share Tech Mono',monospace;
      font-size:1.25rem; color:#00d4ff; }
.pl { font-size:.68rem; color:#7a9cc4; text-transform:uppercase;
      letter-spacing:.09em; text-align:center; margin-bottom:3px; }

/* Table overrides */
[data-testid="stSidebar"] { background:#060c16; border-right:1px solid #1e3a5f; }
.stTabs [data-baseweb="tab-list"] { background:#0a0f1a; border-bottom:1px solid #1e3a5f; }
.stTabs [data-baseweb="tab"] { background:transparent; color:#7a9cc4; border:none;
    font-family:'Share Tech Mono',monospace; font-size:.8rem; letter-spacing:.04em; }
.stTabs [aria-selected="true"] { background:#0d1520 !important; color:#00d4ff !important;
    border-bottom:2px solid #00d4ff !important; }
.stButton > button { background:#0a1e38; color:#00d4ff; border:1px solid #1e4a7f;
    border-radius:6px; font-family:'Share Tech Mono',monospace; font-size:.78rem;
    letter-spacing:.04em; transition:all .2s; width:100%; }
.stButton > button:hover { background:#0d2a4a; border-color:#00d4ff; }
.stSelectbox label, .stRadio label, .stNumberInput label { color:#c0d4e8 !important; font-size:.84rem !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGER
# ═══════════════════════════════════════════════════════════════════════════════
LOG_FILE = "hnd_lab_analytics.csv"

def log_action(sid, action, detail=""):
    row = pd.DataFrame([{
        "Timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Student_ID": sid, "Action": action, "Detail": str(detail)
    }])
    if not os.path.isfile(LOG_FILE):
        row.to_csv(LOG_FILE, index=False)
    else:
        row.to_csv(LOG_FILE, mode='a', header=False, index=False)

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULTS = {
    "auth": False, "student_id": "", "page": "🏠 Dashboard",
    # P1 Diode
    "si_data": pd.DataFrame(columns=["Voltage (V)", "Current (mA)"]),
    "ge_data": pd.DataFrame(columns=["Voltage (V)", "Current (mA)"]),
    "p1_score": None, "p1_submitted": False,
    # P2 Rectification
    "Vp": 12.0, "freq": 50,
    "p2_score": None, "p2_submitted": False,
    # P3 Zener
    "zener_data": pd.DataFrame(columns=["V_s (V)", "V_o (V)", "Rs (Ω)", "RL (Ω)"]),
    "p3_score": None, "p3_submitted": False,
    # P4 BJT
    "p4_score": None, "p4_submitted": False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <p class="hero-title">Virtual Physics/Electronics Laboratory</p>
  <p class="hero-sub">Department of Physics / Electronics · SOLID STATE & ELECTRONICS</p>
  <p class="hero-sub">PRACTICAL SIMULATION PLATFORM</p>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════════════════════════════════════════
if not st.session_state["auth"]:
    st.markdown('<p class="sec">// Student Identification — Laboratory Access Control</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("Enter your **Matriculation Number** to ACCESS all Four MODULES")
        mat = st.text_input("Matriculation Number", placeholder="e.g. PHY/HND/2024/018")
        if st.button("▶  LOGIN"):
            if mat.strip():
                st.session_state["student_id"] = mat.strip()
                st.session_state["auth"] = True
                log_action(mat.strip(), "Platform_Login")
                st.rerun()
            else:
                st.error("Matriculation number is required to access the platform.")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════
PAGES = [
    "🏠 Dashboard",
    "🔌 P1: Diode Characteristics",
    "⚡ P2: Rectification",
    "🛡️ P3: Zener Stabilizer",
    "📡 P4: BJT Analysis",
]

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state['student_id']}")
    st.markdown("**HND Electronics Lab Platform**")
    st.markdown("---")
    st.markdown("### 🗂️ Navigation")
    for p in PAGES:
        if st.button(p, key=f"nav_{p}"):
            st.session_state["page"] = p
            st.rerun()

    st.markdown("---")
    # Score summary
    st.markdown("### 📊 Score Summary")
    for i, label in enumerate(["P1","P2","P3","P4"], 1):
        sc = st.session_state.get(f"p{i}_score")
        if sc is not None:
            colour = "#4ade80" if sc >= 50 else "#f87171"
            st.markdown(f'<span style="color:{colour};font-family:monospace;font-size:.82rem;">'
                        f'{label}: {sc}/100 {"✓" if sc>=50 else "✗"}</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span style="color:#4a6a8a;font-family:monospace;font-size:.82rem;">'
                        f'{label}: Not Attempted</span>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔒 Log Out"):
        st.session_state["auth"] = False
        st.rerun()

PAGE = st.session_state["page"]

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER — metric card row
# ═══════════════════════════════════════════════════════════════════════════════
def metric_row(items):
    cols = st.columns(len(items))
    for col, (lbl, val, unit) in zip(cols, items):
        col.markdown(f'<div class="mc"><div class="ml">{lbl}</div>'
                     f'<div class="mv">{val}</div><div class="mu">{unit}</div></div>',
                     unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER — SVG diagram via components.html
# ═══════════════════════════════════════════════════════════════════════════════
SVG_WRAP = '<style>body{{margin:0;padding:14px 10px 20px;background:#0a1222}}.w{{stroke:#60a5fa;stroke-width:2;fill:none}}.t{{fill:#c0d4e8;font-family:monospace;font-size:12px}}</style>'

# ═══════════════════════════════════════════════════════════════════════════════
# ASSESSMENT HELPER
# ═══════════════════════════════════════════════════════════════════════════════
def render_assessment(pkey, questions, answers):
    """Render a 5-question MCQ. pkey = 'p1'|'p2'|'p3'|'p4'."""
    st.markdown('<p class="sec">// Post-Practical Assessment — Viva Voce</p>', unsafe_allow_html=True)
    submitted_key = f"{pkey}_submitted"
    score_key     = f"{pkey}_score"

    if st.session_state[submitted_key]:
        sc = st.session_state[score_key]
        colour_cls = "score-pass" if sc >= 50 else "score-fail"
        st.markdown(f'<div class="{colour_cls}"><strong>Assessment Submitted</strong><br>'
                    f'Score: <span style="font-size:1.4rem;font-family:monospace">{sc}/100</span> &nbsp;'
                    f'{"— PASS ✓" if sc>=50 else "— FAIL ✗"}</div>', unsafe_allow_html=True)
        with st.expander("📋 View Answer Key"):
            for i, (q, opts, ans) in enumerate(zip(questions, [o for o,_ in answers], [a for _,a in answers]), 1):
                st.markdown(f"**Q{i}.** {q}  \n✅ *{ans}*")
        return

    with st.form(f"form_{pkey}"):
        responses = []
        for i, (q, (opts, _)) in enumerate(zip(questions, answers), 1):
            r = st.radio(f"**{i}.** {q}", opts, key=f"{pkey}_q{i}")
            responses.append(r)
            st.markdown("")

        if st.form_submit_button("▶  SUBMIT ASSESSMENT (One Attempt Only)"):
            score = sum(20 for r, (_, correct) in zip(responses, answers) if r == correct)
            st.session_state[score_key]     = score
            st.session_state[submitted_key] = True
            log_action(st.session_state["student_id"], f"{pkey.upper()}_Assessment", f"Score={score}")
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# ══  DASHBOARD PAGE  ══════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════
if PAGE == "🏠 Dashboard":
    st.markdown('<p class="sec">// Academic Laboratory Overview</p>', unsafe_allow_html=True)

    # Practical cards
    practicals = [
        ("🔌", "P1", "Diode Characteristics",
         "Forward & Reverse bias I-V characteristics of Silicon (Si) and Germanium (Ge) PN junction diodes.",
         "#4ade80"),
        ("⚡", "P2", "Rectification",
         "Half-Wave and Full-Wave (Centre-Tap & Bridge) AC-to-DC power conversion waveform analysis.",
         "#818cf8"),
        ("🛡️", "P3", "Zener Voltage Stabilizer",
         "Shunt voltage regulation using Zener diode breakdown characteristics and stabilizer circuit design.",
         "#fb923c"),
        ("📡", "P4", "BJT CE Characteristics",
         "Common-Emitter transistor output characteristics, DC load line, and Q-point analysis.",
         "#f0abfc"),
    ]

    c1, c2 = st.columns(2)
    for i, (icon, pid, title, desc, clr) in enumerate(practicals):
        col = c1 if i % 2 == 0 else c2
        sc = st.session_state.get(f"p{i+1}_score")
        sc_str = f"Score: **{sc}/100**" if sc is not None else "*Not yet attempted*"
        with col:
            st.markdown(f"""
            <div style="background:#0d1520;border:1px solid {clr}33;border-left:4px solid {clr};
                        border-radius:10px;padding:18px 20px;margin-bottom:14px;">
              <div style="font-family:'Share Tech Mono',monospace;font-size:.8rem;color:{clr};margin-bottom:6px;">
                {icon} {pid} — {title}
              </div>
              <div style="font-size:.83rem;color:#8aa5be;line-height:1.6;margin-bottom:10px;">{desc}</div>
              <div style="font-size:.78rem;color:#c0d4e8;">{sc_str}</div>
            </div>""", unsafe_allow_html=True)

    # Performance analytics
    st.markdown('<p class="sec">// Performance Analytics</p>', unsafe_allow_html=True)
    scores  = {f"P{i}": st.session_state.get(f"p{i}_score") for i in range(1, 5)}
    done    = {k: v for k, v in scores.items() if v is not None}

    if done:
        col_chart, col_table = st.columns([3, 2])
        with col_chart:
            labels = list(done.keys())
            vals   = list(done.values())
            colours = ["#4ade80" if v >= 50 else "#f87171" for v in vals]
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=labels, y=vals, marker_color=colours,
                text=[f"{v}%" for v in vals], textposition="outside",
                name="Score"
            ))
            fig.add_hline(y=50, line=dict(color="#facc15", dash="dash", width=1.5))
            fig.update_layout(
                template="plotly_dark", paper_bgcolor="#070b14", plot_bgcolor="#0a0f1a",
                height=320, margin=dict(l=10, r=10, t=30, b=10),
                yaxis=dict(title="Score / 100", range=[0, 110], gridcolor="#1a2a3a"),
                xaxis=dict(title="Practical", gridcolor="#1a2a3a"),
                font=dict(family="Share Tech Mono", color="#c0d4e8", size=11),
                showlegend=False,
                annotations=[dict(x=0.5, y=52, xref="paper", text="Pass Mark (50)", showarrow=False,
                                  font=dict(color="#facc15", size=10))]
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_table:
            avg = sum(done.values()) / len(done)
            metric_row([
                ("Practicals Done", str(len(done)), f"of 4"),
                ("Average Score",   f"{avg:.0f}",   "/ 100"),
            ])
            st.markdown("")
            rows = []
            for k, v in done.items():
                rows.append({"Practical": k, "Score": f"{v}/100",
                             "Status": "PASS ✓" if v >= 50 else "FAIL ✗",
                             "Grade": "A" if v>=80 else "B" if v>=65 else "C" if v>=50 else "F"})
            st.dataframe(pd.DataFrame(rows).set_index("Practical"), use_container_width=True)

            if len(done) == 4:
                overall = sum(done.values()) / 4
                rec = ("Outstanding performance across all practicals." if overall >= 80
                       else "Good understanding demonstrated. Review weaker areas." if overall >= 65
                       else "Satisfactory. Additional study recommended." if overall >= 50
                       else "Below pass mark. All practicals should be revisited.")
                st.markdown(f'<div class="tb"><strong>Overall GPA Band:</strong> {overall:.1f}/100<br>{rec}</div>',
                            unsafe_allow_html=True)
    else:
        st.info("Complete at least one practical assessment to see performance analytics.")

    # Download log
    if os.path.isfile(LOG_FILE):
        with open(LOG_FILE, "rb") as f:
            st.download_button("⬇️  Download Full Analytics Log (CSV)", f,
                               file_name="hnd_lab_analytics.csv", mime="text/csv")


# ═══════════════════════════════════════════════════════════════════════════════
# ══  P1: DIODE CHARACTERISTICS  ═══════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════
elif PAGE == "🔌 P1: Diode Characteristics":
    st.markdown("## 🔌 Practical 1: Forward & Reverse Bias Characteristics of PN Junction Diodes")
    st.markdown("*Silicon (Si) and Germanium (Ge) — I-V Curve Tracing*")

    # Sidebar controls
    with st.sidebar:
        st.markdown("### P1 Controls")
        material  = st.radio("Semiconductor Material:", ["Silicon (Si)", "Germanium (Ge)"])
        bias_mode = st.radio("Bias Region:", ["Forward Bias", "Reverse Bias"])
        # Shockley diode parameters
        # Si: Is=1e-9 A, n=1.8  |  Ge: Is=1e-6 A, n=1.0
        Vt = 0.02585  # thermal voltage at 300 K
        if material == "Silicon (Si)":
            Is, n_ideal = 1e-9, 1.8
        else:
            Is, n_ideal = 1e-6, 1.0
 
        if bias_mode == "Forward Bias":
            v_in = st.number_input("Voltage V (V):", 0.0, 5.0, 0.0, 0.05, format="%.2f")
        else:
            v_in = st.number_input("Voltage V (Neg V):", -100.0, 0.0, 0.0, 1.0, format="%.2f")
 
        # Auto-calculate current via Shockley equation
        i_calc_a  = Is * (np.exp(np.clip(v_in / (n_ideal * Vt), -500, 500)) - 1)
        i_calc_ma = round(float(i_calc_a) * 1000, 6)
 
        # Display computed current
        i_disp = f"{i_calc_ma:.4f} mA" if abs(i_calc_ma) >= 0.001 else f"{i_calc_ma*1000:.4f} µA"
        st.markdown(f'<div style="background:#0a1628;border:1px solid #1e4a7f;border-radius:6px;'
                    f'padding:10px;text-align:center;margin:6px 0;">'
                    f'<span style="font-size:.68rem;color:#7a9cc4;text-transform:uppercase;'
                    f'letter-spacing:.08em;">Computed Current</span><br>'
                    f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:1.1rem;'
            st.rerun()

    tab_theory, tab_sim, tab_assess = st.tabs(["📐 Theory", "📊 Simulation", "📝 Assessment"])

    # ── Theory ──
    with tab_theory:
        st.markdown('<p class="sec">// Theoretical Background</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="tb">
        <strong>PN Junction Diode — I-V Characteristics</strong><br><br>
        A PN junction diode is formed by joining P-type and N-type semiconductor materials. The resulting
        depletion region creates a potential barrier that controls current flow.<br><br>
        <strong>Forward Bias:</strong> External positive voltage applied to the P-side reduces the depletion
        width. When Vf exceeds the knee voltage (Si ≈ 0.6–0.7 V, Ge ≈ 0.2–0.3 V), current rises
        exponentially following the Shockley equation: <em>I = I₀(e^(V/ηVₜ) − 1)</em><br><br>
        <strong>Reverse Bias:</strong> Depletion region widens; only a tiny thermally generated leakage
        current (I₀) flows — typically nA for Si, µA for Ge. Beyond PIV, avalanche breakdown occurs.<br><br>
        <strong>Material Comparison:</strong><br>
        &nbsp;&nbsp;• Silicon: Vknee ≈ 0.6–0.7 V, lower leakage, preferred for most circuits<br>
        &nbsp;&nbsp;• Germanium: Vknee ≈ 0.2–0.3 V, higher leakage, used in legacy/RF circuits<br><br>
        <strong>Key parameters:</strong> Knee voltage, reverse saturation current (I₀), breakdown voltage (PIV),
        dynamic resistance (rd = ηVₜ/Idc)
        </div>""", unsafe_allow_html=True)

        st.markdown('<p class="sec">// Circuit Diagram</p>', unsafe_allow_html=True)
        components.html(SVG_WRAP + """
        <svg viewBox="0 0 680 160" xmlns="http://www.w3.org/2000/svg" width="100%">
          <rect width="680" height="160" fill="#0a1222"/>
          <!-- PSU -->
          <circle cx="60" cy="80" r="30" class="w"/>
          <text x="60" y="75" text-anchor="middle" class="t" font-size="16">~</text>
          <text x="60" y="130" text-anchor="middle" style="fill:#00d4ff;font-family:monospace;font-size:10px">V_PSU</text>
          <!-- top wire -->
          <line x1="90" y1="50" x2="180" y2="50" class="w"/>
          <!-- Ammeter -->
          <circle cx="210" cy="50" r="18" class="w"/>
          <text x="210" y="55" text-anchor="middle" style="fill:#4ade80;font-family:monospace;font-size:11px">A</text>
          <line x1="228" y1="50" x2="310" y2="50" class="w"/>
          <!-- Diode -->
          <polygon points="310,36 310,64 342,50" style="fill:#60a5fa;stroke:#60a5fa"/>
          <line x1="342" y1="34" x2="342" y2="66" style="stroke:#60a5fa;stroke-width:3"/>
          <text x="326" y="27" text-anchor="middle" style="fill:#60a5fa;font-family:monospace;font-size:11px;font-weight:bold">D</text>
          <line x1="342" y1="50" x2="440" y2="50" class="w"/>
          <!-- Load -->
          <rect x="440" y="34" width="80" height="32" rx="4" style="fill:#1a2a1a;stroke:#4ade80;stroke-width:1.8"/>
          <text x="480" y="53" text-anchor="middle" style="fill:#4ade80;font-family:monospace;font-size:11px">R_L</text>
          <!-- Return wire -->
          <line x1="520" y1="50" x2="580" y2="50" class="w"/>
          <line x1="580" y1="50" x2="580" y2="110" class="w"/>
          <line x1="90"  y1="110" x2="580" y2="110" class="w"/>
          <!-- Voltmeter -->
          <circle cx="510" cy="82" r="18" class="w"/>
          <text x="510" y="87" text-anchor="middle" style="fill:#facc15;font-family:monospace;font-size:11px">V</text>
          <line x1="510" y1="64"  x2="510" y2="56" class="w"/>
          <line x1="510" y1="100" x2="510" y2="110" class="w"/>
          <!-- Labels -->
          <text x="140" y="43" style="fill:#7a9cc4;font-family:monospace;font-size:9px">Forward/Reverse Bias</text>
          <text x="90"  y="148" style="fill:#7a9cc4;font-family:monospace;font-size:9px">Variable PSU</text>
        </svg>""", height=185, scrolling=False)

    # ── Simulation ──
    with tab_sim:
        st.markdown('<p class="sec">// I-V Characteristic Curve Tracer</p>', unsafe_allow_html=True)
<!-- Return wire -->
          <line x1="520" y1="50" x2="580" y2="50" class="w"/>
          <line x1="580" y1="50" x2="580" y2="110" class="w"/>
          <line x1="90"  y1="110" x2="580" y2="110" class="w"/>
          <!-- Voltmeter -->
          <circle cx="510" cy="82" r="18" class="w"/>
          <text x="510" y="87" text-anchor="middle" style="fill:#facc15;font-family:monospace;font-size:11px">V</text>
          <line x1="510" y1="64"  x2="510" y2="56" class="w"/>
          <line x1="510" y1="100" x2="510" y2="110" class="w"/>
          <!-- Labels -->
          <text x="140" y="43" style="fill:#7a9cc4;font-family:monospace;font-size:9px">Forward/Reverse Bias</text>
          <text x="90"  y="148" style="fill:#7a9cc4;font-family:monospace;font-size:9px">Variable PSU</text>
        </svg>""", height=185, scrolling=False)
 
    # ── Simulation ──
    with tab_sim:
        st.markdown('<p class="sec">// I-V Characteristic Curve Tracer</p>', unsafe_allow_html=True)
 
        si_df = st.session_state["si_data"]
        ge_df = st.session_state["ge_data"]
 
        col_g, col_t = st.columns([2, 1])
        with col_g:
            fig = go.Figure()
            if not si_df.empty:
                fig.add_trace(go.Scatter(
                    x=si_df["Voltage (V)"], y=si_df["Current (mA)"],
                    mode="markers+lines", name="Silicon (Si)",
                    marker=dict(color="#60a5fa", size=8),
                    line=dict(color="#60a5fa", width=2)))
            if not ge_df.empty:
                fig.add_trace(go.Scatter(
                    x=ge_df["Voltage (V)"], y=ge_df["Current (mA)"],
                    mode="markers+lines", name="Germanium (Ge)",
                    marker=dict(color="#fb923c", size=8, symbol="square"),
                    line=dict(color="#fb923c", width=2, dash="dot")))
            fig.update_layout(
                template="plotly_dark", paper_bgcolor="#070b14",
                plot_bgcolor="#0a0f1a", height=420,
                xaxis=dict(title="Applied Voltage (V)", zeroline=True,
            st.caption("µA values auto-scaled to mA on the plot.")

    # ── Assessment ──
    with tab_assess:
        Q = ["What is the approximate knee (threshold) voltage of a Silicon diode?",
             "What causes the tiny reverse leakage current in a PN junction diode?",
             "Compared to Silicon, at what lower threshold voltage does Germanium begin to conduct significantly?",
             "What happens to the depletion region when reverse bias voltage is applied?",
             "What physical event occurs when reverse voltage exceeds the Peak Inverse Voltage (PIV)?"]
        A = [
            (["0.1 – 0.2 V","0.3 – 0.4 V","0.6 – 0.7 V","1.0 – 1.2 V"], "0.6 – 0.7 V"),
            (["Majority carrier injection","Thermally generated minority carrier drift",
              "Covalent bond vibration","Electron-hole recombination at the junction"], "Thermally generated minority carrier drift"),
            (["0.6 – 0.7 V","0.4 – 0.5 V","0.2 – 0.3 V","0.1 V exactly"], "0.2 – 0.3 V"),
            (["It narrows, reducing resistance","It disappears completely",
              "It widens, increasing the barrier","It remains unchanged"], "It widens, increasing the barrier"),
            (["Current reduces to zero","Avalanche breakdown causes a sharp rise in reverse current",
              "The diode self-repairs","Forward conduction resumes automatically"], "Avalanche breakdown causes a sharp rise in reverse current"),
        ]
        render_assessment("p1", Q, A)


# ═══════════════════════════════════════════════════════════════════════════════
# ══  P2: RECTIFICATION  ═══════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════
elif PAGE == "⚡ P2: Rectification":
    st.markdown("## ⚡ Practical 2: Half-Wave & Full-Wave Rectification")
    st.markdown("*AC-to-DC Conversion — Waveform & Parameter Analysis*")

    with st.sidebar:
        st.markdown("### P2 — AC Source")
        st.markdown('<p class="pl">Peak Voltage  Vₚ</p>', unsafe_allow_html=True)
        v1,v2,v3 = st.columns([1,1.5,1])
        with v1:
            if st.button("−", key="vp_dn"): st.session_state["Vp"] = max(1.0, round(st.session_state["Vp"]-0.5,1))
        with v2:
            st.markdown(f'<div class="pd">{st.session_state["Vp"]:.1f} V</div>', unsafe_allow_html=True)
        with v3:
            if st.button("+", key="vp_up"): st.session_state["Vp"] = min(50.0, round(st.session_state["Vp"]+0.5,1))

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="pl">Frequency  f</p>', unsafe_allow_html=True)
        f1,f2,f3 = st.columns([1,1.5,1])
        with f1:
            if st.button("−", key="fr_dn"): st.session_state["freq"] = max(10, st.session_state["freq"]-10)
        with f2:
            st.markdown(f'<div class="pd">{st.session_state["freq"]} Hz</div>', unsafe_allow_html=True)
        with f3:
            if st.button("+", key="fr_up"): st.session_state["freq"] = min(500, st.session_state["freq"]+10)

        st.markdown("---")
        mode = st.selectbox("Rectifier Type:",
            ["Half-Wave","Full-Wave — Centre Tap","Full-Wave — Bridge"])

    Vp, freq = st.session_state["Vp"], st.session_state["freq"]
    Vd, RL   = 0.7, 500
    t  = np.linspace(0, 3/freq, 8000)
    vin = Vp * np.sin(2*np.pi*freq*t)

    if mode == "Half-Wave":
        vout = np.where(vin > Vd, vin-Vd, 0.0)
        clr, fill, n_d, rfm = "#4ade80","rgba(74,222,128,.08)", 1, 1
        piv  = Vp
    elif mode == "Full-Wave — Centre Tap":
        vout = np.where(np.abs(vin)>Vd, np.abs(vin)-Vd, 0.0)
        clr, fill, n_d, rfm = "#818cf8","rgba(129,140,248,.08)", 2, 2
        piv  = 2*Vp - Vd
    else:
        vout = np.where(np.abs(vin)>2*Vd, np.abs(vin)-2*Vd, 0.0)
        clr, fill, n_d, rfm = "#fb923c","rgba(251,146,60,.08)", 4, 2
        piv  = Vp

    vdc  = float(vout.mean())
    vrms = float(np.sqrt(np.mean(vout**2)))
    vpk  = float(vout.max())
    iac  = float(np.sqrt(max(vrms**2 - vdc**2, 0)))
    gam  = (iac/vdc) if vdc>0 else 0
    eta  = ((vdc**2/RL)/(Vp**2/(2*RL))*100) if Vp>0 else 0
    t_ms = t*1000

    tab_theory, tab_sim, tab_assess = st.tabs(["📐 Theory","📊 Waveform","📝 Assessment"])

    with tab_theory:
        theories = {
            "Half-Wave": ("Half-Wave Rectifier",
                "A single diode conducts only during the positive half-cycle. The negative half-cycle is blocked.",
                "0.318 Vₚ","Vₚ/2","1.21","40.6%","Vₚ","1","No"),
            "Full-Wave — Centre Tap": ("Full-Wave Centre-Tap Rectifier",
                "A centre-tapped transformer with 2 diodes rectifies both half-cycles. D₁ conducts on positive, D₂ on negative.",
                "0.636 Vₚ","Vₚ/√2","0.482","81.2%","2Vₚ","2","Yes"),
            "Full-Wave — Bridge": ("Full-Wave Bridge Rectifier",
                "Four diodes in bridge formation rectify both half-cycles without a centre-tap transformer.",
                "0.636 Vₚ","Vₚ/√2","0.482","81.2%","Vₚ","4","No"),
        }
        nm, desc, vdc_eq, vrms_eq, gam_eq, eta_eq, piv_eq, nd_eq, ct = theories[mode]
        st.markdown(f"""
        <div class="tb">
        <strong>{nm}</strong><br><br>
        {desc}<br><br>
        <strong>Key Equations:</strong><br>
        &nbsp;&nbsp; V_DC = {vdc_eq}<br>
        &nbsp;&nbsp; V_RMS = {vrms_eq}<br>
        &nbsp;&nbsp; Ripple Factor γ = {gam_eq}<br>
        &nbsp;&nbsp; Efficiency η = {eta_eq}<br>
        &nbsp;&nbsp; PIV per diode = {piv_eq}<br>
        &nbsp;&nbsp; Diodes required = {nd_eq}<br>
        &nbsp;&nbsp; Centre-tap transformer = {ct}
        </div>""", unsafe_allow_html=True)

        st.markdown('<p class="sec">// Circuit Diagram</p>', unsafe_allow_html=True)
        if mode == "Half-Wave":
            components.html(SVG_WRAP + """
            <svg viewBox="0 0 620 155" xmlns="http://www.w3.org/2000/svg" width="100%">
              <rect width="620" height="155" fill="#0a1222"/>
              <circle cx="65" cy="78" r="30" class="w"/>
              <text x="65" y="73" text-anchor="middle" class="t" font-size="16">~</text>
              <text x="65" y="128" text-anchor="middle" style="fill:#00d4ff;font-family:monospace;font-size:10px">Vᵢₙ</text>
              <line x1="95" y1="48" x2="210" y2="48" class="w"/>
              <polygon points="210,34 210,62 244,48" style="fill:#4ade80;stroke:#4ade80"/>
              <line x1="244" y1="32" x2="244" y2="64" style="stroke:#4ade80;stroke-width:3"/>
              <text x="227" y="24" text-anchor="middle" style="fill:#4ade80;font-family:monospace;font-size:11px;font-weight:bold">D</text>
              <line x1="244" y1="48" x2="360" y2="48" class="w"/>
              <rect x="360" y="32" width="85" height="32" rx="4" style="fill:#1a2a1a;stroke:#4ade80;stroke-width:1.8"/>
              <text x="403" y="52" text-anchor="middle" style="fill:#4ade80;font-family:monospace;font-size:11px">Rₗ 500Ω</text>
              <line x1="445" y1="48" x2="530" y2="48" class="w"/>
              <line x1="530" y1="48" x2="530" y2="108" class="w"/>
              <line x1="95"  y1="108" x2="530" y2="108" class="w"/>
              <line x1="500" y1="52" x2="500" y2="104" style="stroke:#facc15;stroke-width:1.8;stroke-dasharray:5,3"/>
              <line x1="494" y1="52"  x2="506" y2="52"  style="stroke:#facc15;stroke-width:2"/>
              <line x1="494" y1="104" x2="506" y2="104" style="stroke:#facc15;stroke-width:2"/>
              <text x="512" y="82" style="fill:#facc15;font-family:monospace;font-size:10px">Vₒᵤₜ</text>
            </svg>""", height=180, scrolling=False)
            svg_dl = b"""<svg viewBox="0 0 620 155" xmlns="http://www.w3.org/2000/svg"><rect width="620" height="155" fill="#0a1222"/><circle cx="65" cy="78" r="30" stroke="#60a5fa" stroke-width="2" fill="none"/><text x="65" y="73" text-anchor="middle" fill="#c0d4e8" font-family="monospace" font-size="16">~</text><text x="65" y="128" text-anchor="middle" fill="#00d4ff" font-family="monospace" font-size="10">Vin</text><line x1="95" y1="48" x2="210" y2="48" stroke="#60a5fa" stroke-width="2"/><polygon points="210,34 210,62 244,48" fill="#4ade80" stroke="#4ade80"/><line x1="244" y1="32" x2="244" y2="64" stroke="#4ade80" stroke-width="3"/><text x="227" y="24" text-anchor="middle" fill="#4ade80" font-family="monospace" font-size="11" font-weight="bold">D</text><line x1="244" y1="48" x2="360" y2="48" stroke="#60a5fa" stroke-width="2"/><rect x="360" y="32" width="85" height="32" rx="4" fill="#1a2a1a" stroke="#4ade80" stroke-width="1.8"/><text x="403" y="52" text-anchor="middle" fill="#4ade80" font-family="monospace" font-size="11">RL 500 ohm</text><line x1="445" y1="48" x2="530" y2="48" stroke="#60a5fa" stroke-width="2"/><line x1="530" y1="48" x2="530" y2="108" stroke="#60a5fa" stroke-width="2"/><line x1="95" y1="108" x2="530" y2="108" stroke="#60a5fa" stroke-width="2"/></svg>"""
        elif mode == "Full-Wave — Centre Tap":
            components.html(SVG_WRAP + """
            <svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" width="100%">
              <rect width="680" height="220" fill="#0a1222"/>
              <rect x="20" y="50" width="68" height="120" rx="4" style="fill:#080f1e;stroke:#60a5fa;stroke-width:1.8"/>
              <text x="54" y="108" text-anchor="middle" class="t" font-size="18">~</text>
              <text x="54" y="128" text-anchor="middle" style="fill:#7a9cc4;font-family:monospace;font-size:9px">Transformer</text>
              <line x1="88" y1="75"  x2="110" y2="75"  class="w"/>
              <line x1="88" y1="145" x2="110" y2="145" class="w"/>
              <line x1="88" y1="110" x2="500" y2="110" style="stroke:#60a5fa;stroke-width:1.5;stroke-dasharray:5,4"/>
              <text x="120" y="107" style="fill:#7a9cc4;font-family:monospace;font-size:9px">CT (GND)</text>
              <line x1="110" y1="75" x2="200" y2="75" class="w"/>
              <polygon points="200,61 200,89 234,75" style="fill:#818cf8;stroke:#818cf8"/>
              <line x1="234" y1="60" x2="234" y2="90" style="stroke:#818cf8;stroke-width:3"/>
              <text x="217" y="52" text-anchor="middle" style="fill:#818cf8;font-family:monospace;font-size:11px;font-weight:bold">D1</text>
              <line x1="110" y1="145" x2="200" y2="145" class="w"/>
              <polygon points="200,131 200,159 234,145" style="fill:#818cf8;stroke:#818cf8"/>
              <line x1="234" y1="130" x2="234" y2="160" style="stroke:#818cf8;stroke-width:3"/>
              <text x="217" y="174" text-anchor="middle" style="fill:#818cf8;font-family:monospace;font-size:11px;font-weight:bold">D2</text>
              <line x1="234" y1="75"  x2="330" y2="75"  class="w"/>
              <line x1="234" y1="145" x2="330" y2="145" class="w"/>
              <line x1="330" y1="75"  x2="330" y2="94"  class="w"/>
              <line x1="330" y1="145" x2="330" y2="126" class="w"/>
              <line x1="330" y1="94"  x2="375" y2="94"  class="w"/>
              <line x1="330" y1="126" x2="375" y2="126" class="w"/>
              <rect x="375" y="89" width="90" height="42" rx="4" style="fill:#1a1a2a;stroke:#818cf8;stroke-width:1.8"/>
              <text x="420" y="114" text-anchor="middle" style="fill:#818cf8;font-family:monospace;font-size:11px">Rₗ 500Ω</text>
              <line x1="465" y1="94"  x2="545" y2="94"  class="w"/>
              <line x1="465" y1="126" x2="500" y2="126" class="w"/>
              <line x1="500" y1="126" x2="500" y2="110" class="w"/>
              <line x1="500" y1="110" x2="545" y2="110" class="w"/>
              <line x1="545" y1="94"  x2="545" y2="110" class="w"/>
              <line x1="524" y1="96"  x2="524" y2="108" style="stroke:#facc15;stroke-width:1.8;stroke-dasharray:4,3"/>
              <line x1="518" y1="96"  x2="530" y2="96"  style="stroke:#facc15;stroke-width:2"/>
              <line x1="518" y1="108" x2="530" y2="108" style="stroke:#facc15;stroke-width:2"/>
              <text x="550" y="105" style="fill:#facc15;font-family:monospace;font-size:10px">Vₒᵤₜ</text>
            </svg>""", height=245, scrolling=False)
            svg_dl = b"<svg viewBox='0 0 680 220' xmlns='http://www.w3.org/2000/svg'><rect width='680' height='220' fill='#0a1222'/><text x='340' y='110' text-anchor='middle' fill='#818cf8' font-family='monospace' font-size='14'>Full-Wave Centre-Tap Rectifier</text></svg>"
        else:
            components.html(SVG_WRAP + """
            <svg viewBox="0 0 680 230" xmlns="http://www.w3.org/2000/svg" width="100%">
              <rect width="680" height="230" fill="#0a1222"/>
              <circle cx="65" cy="115" r="30" class="w"/>
              <text x="65" y="110" text-anchor="middle" class="t" font-size="16">~</text>
              <text x="65" y="160" text-anchor="middle" style="fill:#00d4ff;font-family:monospace;font-size:10px">Vᵢₙ</text>
              <line x1="95"  y1="85"  x2="210" y2="85"  class="w"/>
              <line x1="95"  y1="145" x2="210" y2="145" class="w"/>
              <line x1="210" y1="85"  x2="210" y2="145" class="w"/>
              <!-- D1 -->
              <line x1="210" y1="115" x2="240" y2="90" class="w"/>
              <polygon points="240,90 256,78 248,102" style="fill:#fb923c;stroke:#fb923c"/>
              <line x1="256" y1="68" x2="256" y2="90" style="stroke:#fb923c;stroke-width:3"/>
              <line x1="256" y1="79" x2="300" y2="55" class="w"/>
              <text x="230" y="70" style="fill:#fb923c;font-family:monospace;font-size:10px;font-weight:bold">D1</text>
              <!-- D3 -->
              <line x1="300" y1="55"  x2="344" y2="78" class="w"/>
              <polygon points="344,78 336,100 352,90" style="fill:#fb923c;stroke:#fb923c"/>
              <line x1="352" y1="68" x2="352" y2="92" style="stroke:#fb923c;stroke-width:3"/>
              <line x1="352" y1="80" x2="390" y2="115" class="w"/>
              <text x="348" y="62" style="fill:#fb923c;font-family:monospace;font-size:10px;font-weight:bold">D3</text>
              <!-- D4 -->
              <line x1="210" y1="115" x2="240" y2="140" class="w"/>
              <polygon points="240,140 256,152 248,128" style="fill:#fb923c;stroke:#fb923c"/>
              <line x1="256" y1="142" x2="256" y2="164" style="stroke:#fb923c;stroke-width:3"/>
              <line x1="256" y1="153" x2="300" y2="175" class="w"/>
              <text x="218" y="166" style="fill:#fb923c;font-family:monospace;font-size:10px;font-weight:bold">D4</text>
              <!-- D2 -->
              <line x1="300" y1="175" x2="344" y2="152" class="w"/>
              <polygon points="344,152 336,130 352,142" style="fill:#fb923c;stroke:#fb923c"/>
              <line x1="352" y1="130" x2="352" y2="154" style="stroke:#fb923c;stroke-width:3"/>
              <line x1="352" y1="141" x2="390" y2="115" class="w"/>
              <text x="348" y="172" style="fill:#fb923c;font-family:monospace;font-size:10px;font-weight:bold">D2</text>
              <!-- Load -->
              <line x1="390" y1="115" x2="440" y2="115" class="w"/>
              <rect x="440" y="94"  width="80" height="42" rx="4" style="fill:#2a1a0a;stroke:#fb923c;stroke-width:1.8"/>
              <text x="480" y="120" text-anchor="middle" style="fill:#fb923c;font-family:monospace;font-size:11px">Rₗ 500Ω</text>
              <line x1="300" y1="175" x2="300" y2="200" class="w"/>
              <line x1="300" y1="200" x2="520" y2="200" class="w"/>
              <line x1="520" y1="200" x2="520" y2="136" class="w"/>
              <line x1="520" y1="94"  x2="520" y2="115" class="w"/>
              <!-- Vout -->
              <line x1="560" y1="97"  x2="560" y2="133" style="stroke:#facc15;stroke-width:1.8;stroke-dasharray:5,3"/>
              <line x1="553" y1="97"  x2="567" y2="97"  style="stroke:#facc15;stroke-width:2"/>
              <line x1="553" y1="133" x2="567" y2="133" style="stroke:#facc15;stroke-width:2"/>
              <text x="570" y="118" style="fill:#facc15;font-family:monospace;font-size:10px">Vₒᵤₜ</text>
              <line x1="440" y1="115" x2="440" y2="94" class="w"/>
            </svg>""", height=255, scrolling=False)
            svg_dl = b"<svg viewBox='0 0 680 230' xmlns='http://www.w3.org/2000/svg'><rect width='680' height='230' fill='#0a1222'/><text x='340' y='115' text-anchor='middle' fill='#fb923c' font-family='monospace' font-size='14'>Full-Wave Bridge Rectifier</text></svg>"

        st.download_button("⬇️ Download Circuit Diagram (SVG)", svg_dl,
                           file_name=f"circuit_{mode.replace(' ','_').replace('—','').lower()}.svg",
                           mime="image/svg+xml")

        # Comparative table
        st.markdown('<p class="sec">// Comparative Summary</p>', unsafe_allow_html=True)
        cmp = pd.DataFrame({
            "Parameter":     ["V_DC","V_RMS","γ (no filter)","η","PIV","Diodes","CT?"],
            "Half-Wave":     ["0.318Vₚ","Vₚ/2","1.21","40.6%","Vₚ","1","No"],
            "FW Ctr-Tap":   ["0.636Vₚ","Vₚ/√2","0.482","81.2%","2Vₚ","2","Yes"],
            "FW Bridge":    ["0.636Vₚ","Vₚ/√2","0.482","81.2%","Vₚ","4","No"],
        })
        st.dataframe(cmp.set_index("Parameter"), use_container_width=True)

    with tab_sim:
        metric_row([("V_peak",f"{vpk:.2f}","V"),("V_DC",f"{vdc:.2f}","V"),
                    ("V_RMS",f"{vrms:.2f}","V"),("Ripple γ",f"{gam:.4f}",""),
                    ("Efficiency",f"{eta:.1f}","%"),("PIV",f"{piv:.2f}","V")])
        st.markdown("")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t_ms, y=vin, name="AC Input",
                                 line=dict(color="#60a5fa",width=1.5,dash="dot"), opacity=.65))
        fig.add_trace(go.Scatter(x=t_ms, y=vout, name=mode+" Output",
                                 line=dict(color=clr,width=2.5), fill="tozeroy", fillcolor=fill))
        fig.add_trace(go.Scatter(x=[t_ms[0],t_ms[-1]], y=[vdc,vdc],
                                 name=f"V_DC={vdc:.2f}V", mode="lines",
                                 line=dict(color="#facc15",width=1.5,dash="dash")))
        fig.update_layout(template="plotly_dark", paper_bgcolor="#070b14", plot_bgcolor="#0a0f1a",
            height=440, margin=dict(l=10,r=10,t=20,b=10),
            xaxis=dict(title="Time (ms)",    gridcolor="#1a2a3a", zeroline=True, zerolinecolor="#1e3a5f"),
            yaxis=dict(title="Voltage (V)", gridcolor="#1a2a3a", zeroline=True, zerolinecolor="#1e3a5f"),
            font=dict(family="Share Tech Mono", color="#c0d4e8", size=11),
            legend=dict(orientation="h",y=-0.18,bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("⬇️ Export Waveform CSV"):
            edf = pd.DataFrame({"Time_ms":np.round(t_ms,4),"AC_Input_V":np.round(vin,4),"Output_V":np.round(vout,4)})
            st.download_button("Download CSV", edf.to_csv(index=False),
                               file_name=f"waveform_{mode.replace(' ','_')}.csv", mime="text/csv")

    with tab_assess:
        Q2 = ["What is the theoretical DC output voltage of an ideal half-wave rectifier (in terms of Vₚ)?",
              "What is the ripple factor of an unfiltered full-wave rectifier?",
              "Why is the output of a full-wave rectifier easier to filter than half-wave?",
              "What is the PIV requirement for each diode in a full-wave bridge rectifier?",
              "What is the rectification efficiency of a full-wave rectifier?"]
        A2 = [
            (["0.636 Vₚ","0.318 Vₚ","0.707 Vₚ","Vₚ/2"], "0.318 Vₚ"),
            (["1.21","0.318","0.482","0.707"], "0.482"),
            (["It has higher peak voltage","Ripple frequency doubles, making the capacitor more effective",
              "It uses more diodes","It doesn't need a transformer"], "Ripple frequency doubles, making the capacitor more effective"),
            (["2Vₚ","Vₚ−Vd","Vₚ","2Vₚ−Vd"], "Vₚ"),
            (["40.6%","81.2%","100%","63.6%"], "81.2%"),
        ]
        render_assessment("p2", Q2, A2)


# ═══════════════════════════════════════════════════════════════════════════════
# ══  P3: ZENER STABILIZER  ════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════
elif PAGE == "🛡️ P3: Zener Stabilizer":
    st.markdown("## 🛡️ Practical 3: Zener Diode Shunt Voltage Stabilizer")
    st.markdown("*DC Voltage Regulation — Auto-Calculation & Characteristic Plot*")

    with st.sidebar:
        st.markdown("### P3 Controls")
        rs    = st.number_input("Series Resistor Rs (Ω):", 10.0, 1000.0, 220.0, 10.0, format="%.1f")
        rl    = st.number_input("Load Resistor RL (Ω):",  100.0,5000.0,1000.0, 50.0, format="%.1f")
        vz    = st.number_input("Zener Voltage Vz (V):",  2.0,  15.0,   5.1,   0.1,  format="%.1f")
        st.markdown("---")
        vs    = st.number_input("PSU Voltage Vs (V):",    0.0,  30.0,   0.0,   0.5,  format="%.2f")
        # Physics engine
        v_div = vs * (rl/(rs+rl))
        rz    = 5.0
        if v_div < vz:
            vo = round(v_div, 2)
        else:
            vo = round(((vs/rs)+(vz/rz)) / ((1/rs)+(1/rl)+(1/rz)), 2)
        vo = min(vo, vs)
        st.markdown(f"**Computed V_o = `{vo:.2f} V`**")

        if st.button("➕ Log to Table"):
            nr = pd.DataFrame([{"V_s (V)":round(vs,2),"V_o (V)":vo,"Rs (Ω)":round(rs,1),"RL (Ω)":round(rl,1)}])
            st.session_state["zener_data"] = (
                pd.concat([st.session_state["zener_data"], nr], ignore_index=True)
                .drop_duplicates(subset=["V_s (V)"]).sort_values("V_s (V)"))
            log_action(st.session_state["student_id"],"P3_DataPoint",f"Vs={vs},Vo={vo}")
            st.toast("Logged!", icon="⚙️")
        if st.button("🗑️ Clear Data"):
            st.session_state["zener_data"] = pd.DataFrame(columns=["V_s (V)","V_o (V)","Rs (Ω)","RL (Ω)"])
            st.rerun()

    tab_theory, tab_sim, tab_assess = st.tabs(["📐 Theory","📊 Simulation","📝 Assessment"])

    with tab_theory:
        st.markdown(f"""
        <div class="tb">
        <strong>Zener Diode Shunt Voltage Stabilizer</strong><br><br>
        A Zener diode operated in <strong>reverse breakdown</strong> maintains a nearly constant voltage
        across its terminals, acting as a voltage reference. The series resistor Rs limits current and
        absorbs the difference between input and regulated output.<br><br>
        <strong>Operating Regions:</strong><br>
        &nbsp;&nbsp;• <em>Pre-breakdown (Vs &lt; Vz):</em> Zener is open; output = resistive divider Vo = Vs·RL/(Rs+RL)<br>
        &nbsp;&nbsp;• <em>Regulation (Vs &gt; Vz):</em> Zener clamps output to ≈ Vz; excess voltage dropped across Rs<br><br>
        <strong>Key Equations:</strong><br>
        &nbsp;&nbsp;• I_s = (Vs − Vz) / Rs<br>
        &nbsp;&nbsp;• I_L = Vz / RL<br>
        &nbsp;&nbsp;• I_z = I_s − I_L  (must remain &gt; I_z(min))<br>
        &nbsp;&nbsp;• P_z = Vz × I_z  (must not exceed P_z(max))<br><br>
        <strong>Current Zener Voltage:</strong> Vz = {vz} V &nbsp;|&nbsp; Rs = {rs} Ω &nbsp;|&nbsp; RL = {rl} Ω
        </div>""", unsafe_allow_html=True)

        st.markdown('<p class="sec">// Circuit Diagram</p>', unsafe_allow_html=True)
        components.html(SVG_WRAP + f"""
        <svg viewBox="0 0 680 160" xmlns="http://www.w3.org/2000/svg" width="100%">
          <rect width="680" height="160" fill="#0a1222"/>
          <!-- PSU -->
          <rect x="20" y="50" width="60" height="60" rx="4" style="fill:#080f1e;stroke:#60a5fa;stroke-width:1.8"/>
          <text x="50" y="82" text-anchor="middle" class="t">DC</text>
          <text x="50" y="96" text-anchor="middle" style="fill:#00d4ff;font-family:monospace;font-size:9px">Vs</text>
          <!-- top wire to Rs -->
          <line x1="80" y1="65" x2="160" y2="65" class="w"/>
          <!-- Series resistor Rs -->
          <rect x="160" y="50" width="90" height="30" rx="4" style="fill:#1a2a1a;stroke:#60a5fa;stroke-width:1.8"/>
          <text x="205" y="69" text-anchor="middle" style="fill:#60a5fa;font-family:monospace;font-size:10px">Rs {rs:.0f}Ω</text>
          <!-- wire after Rs -->
          <line x1="250" y1="65" x2="360" y2="65" class="w"/>
          <!-- node dot -->
          <circle cx="360" cy="65" r="4" fill="#60a5fa"/>
          <!-- Zener diode (pointing down = reverse bias) -->
          <line x1="360" y1="65" x2="360" y2="85" class="w"/>
          <polygon points="348,100 372,100 360,82" style="fill:#fb923c;stroke:#fb923c"/>
          <line x1="345" y1="100" x2="375" y2="100" style="stroke:#fb923c;stroke-width:3"/>
          <line x1="375" y1="97"  x2="375" y2="103" style="stroke:#fb923c;stroke-width:2"/>
          <line x1="345" y1="97"  x2="345" y2="103" style="stroke:#fb923c;stroke-width:2"/>
          <text x="385" y="95" style="fill:#fb923c;font-family:monospace;font-size:9px">Dz  Vz={vz}V</text>
          <line x1="360" y1="100" x2="360" y2="115" class="w"/>
          <!-- Load resistor RL -->
          <rect x="440" y="50" width="90" height="30" rx="4" style="fill:#2a1a0a;stroke:#fb923c;stroke-width:1.8"/>
          <text x="485" y="69" text-anchor="middle" style="fill:#fb923c;font-family:monospace;font-size:10px">RL {rl:.0f}Ω</text>
          <!-- wire to RL -->
          <line x1="360" y1="65" x2="440" y2="65" class="w"/>
          <line x1="530" y1="65" x2="580" y2="65" class="w"/>
          <line x1="580" y1="65" x2="580" y2="115" class="w"/>
          <!-- bottom ground wire -->
          <line x1="80"  y1="115" x2="580" y2="115" class="w"/>
          <line x1="360" y1="115" x2="360" y2="115" class="w"/>
          <!-- Vout marker -->
          <line x1="555" y1="69"  x2="555" y2="111" style="stroke:#facc15;stroke-width:1.8;stroke-dasharray:5,3"/>
          <line x1="549" y1="69"  x2="561" y2="69"  style="stroke:#facc15;stroke-width:2"/>
          <line x1="549" y1="111" x2="561" y2="111" style="stroke:#facc15;stroke-width:2"/>
          <text x="564" y="93" style="fill:#facc15;font-family:monospace;font-size:10px">Vo</text>
        </svg>""", height=185, scrolling=False)

        svg3 = f"""<svg viewBox="0 0 680 160" xmlns="http://www.w3.org/2000/svg"><rect width="680" height="160" fill="#0a1222"/><text x="340" y="80" text-anchor="middle" fill="#fb923c" font-family="monospace" font-size="13">Zener Stabilizer Rs={rs:.0f}ohm RL={rl:.0f}ohm Vz={vz}V</text></svg>""".encode()
        st.download_button("⬇️ Download Circuit Diagram (SVG)", svg3,
                           file_name="zener_stabilizer_circuit.svg", mime="image/svg+xml")

    with tab_sim:
        zdf = st.session_state["zener_data"]

        # Auto-generate sweep
        vs_range = np.linspace(0, 30, 300)
        vo_range = []
        for v in vs_range:
            vd = v * (rl/(rs+rl))
            if vd < vz:
                vo_range.append(vd)
            else:
                vo_r = ((v/rs)+(vz/rz)) / ((1/rs)+(1/rl)+(1/rz))
                vo_range.append(min(vo_r, v))
        vo_range = np.array(vo_range)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=vs_range, y=vo_range, name="Regulation Curve (simulated)",
                                 line=dict(color="#fb923c", width=2.5), fill="tozeroy",
                                 fillcolor="rgba(251,146,60,.07)"))
        if not zdf.empty:
            fig.add_trace(go.Scatter(x=zdf["V_s (V)"], y=zdf["V_o (V)"],
                                     mode="markers", name="Logged Data Points",
                                     marker=dict(color="#4ade80", size=10, symbol="diamond")))
        fig.add_trace(go.Scatter(x=[0,30], y=[vz,vz], mode="lines",
                                 name=f"Vz = {vz} V",
                                 line=dict(color="#facc15", width=1.5, dash="dash")))
        fig.update_layout(template="plotly_dark", paper_bgcolor="#070b14", plot_bgcolor="#0a0f1a",
            height=420, margin=dict(l=10,r=10,t=20,b=10),
            xaxis=dict(title="Input Supply Vs (V)", gridcolor="#1a2a3a"),
            yaxis=dict(title="Output Vo (V)", gridcolor="#1a2a3a"),
            font=dict(family="Share Tech Mono", color="#c0d4e8", size=11),
            legend=dict(orientation="h", y=-0.18, bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)

        col_m, col_t = st.columns([1,1])
        with col_m:
            is_reg = vo >= vz * 0.95
            metric_row([("Vs", f"{vs:.2f}","V"), ("Vo (calc)",f"{vo:.2f}","V"),
                        ("Status","REG" if is_reg else "UNREG", "mode")])
        with col_t:
            st.dataframe(zdf, use_container_width=True, hide_index=True)

    with tab_assess:
        Q3 = ["In what bias condition must the Zener diode be connected to function as a voltage regulator?",
              "What is the primary purpose of the series resistor Rs in the Zener stabilizer circuit?",
              "What happens to the output voltage Vo when the input Vs is below the Zener breakdown voltage?",
              "If the load resistor RL is disconnected (open circuit), what happens to the Zener current Iz?",
              "What determines the maximum power dissipation limit of a Zener diode?"]
        A3 = [
            (["Forward bias","Reverse bias — breakdown region","Alternating bias","Zero bias"],
             "Reverse bias — breakdown region"),
            (["To boost output current","To limit current and drop excess voltage, protecting the Zener",
              "To increase output voltage","To filter ripple"], "To limit current and drop excess voltage, protecting the Zener"),
            (["Vo clamps to Vz","Vo drops to zero","Vo equals Vs (no regulation — resistive divider applies)",
              "Vo doubles"], "Vo equals Vs (no regulation — resistive divider applies)"),
            (["Iz drops to zero","Iz increases — it must carry all the current previously shared with RL",
              "Iz stays the same","The diode burns out immediately"], "Iz increases — it must carry all the current previously shared with RL"),
            (["Its forward voltage","Pz_max = Vz × Iz_max — the rated power dissipation",
              "The load resistance","The supply frequency"], "Pz_max = Vz × Iz_max — the rated power dissipation"),
        ]
        render_assessment("p3", Q3, A3)


# ═══════════════════════════════════════════════════════════════════════════════
# ══  P4: BJT CE CHARACTERISTICS  ══════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════
elif PAGE == "📡 P4: BJT Analysis":
    st.markdown("## 📡 Practical 4: BJT Common-Emitter Output Characteristics & Load Line Analysis")
    st.markdown("*NPN Transistor — Family of Curves, DC Load Line, Q-Point*")

    with st.sidebar:
        st.markdown("### P4 Controls")
        Vcc = st.number_input("Supply Voltage Vcc (V):", 1.0, 30.0, 12.0, 0.5, format="%.1f")
        Rb  = st.number_input("Base Resistor Rb (kΩ):", 10.0,1000.0,100.0,10.0,format="%.0f")
        Rc  = st.number_input("Collector Resistor Rc (Ω):", 100.0,5000.0,1000.0,100.0,format="%.0f")
        beta= st.number_input("Current Gain β (hFE):", 20.0, 500.0, 100.0, 10.0, format="%.0f")

    # BJT calculations
    Vbe  = 0.7
    Ib_Q = (Vcc - Vbe) / (Rb * 1000)      # A
    Ic_Q = beta * Ib_Q                     # A
    Vce_Q= Vcc - Ic_Q * Rc
    Vce_Q= max(Vce_Q, 0.2)
    Ic_sat= Vcc / Rc
    region = "ACTIVE" if (Vce_Q > 0.3 and Ic_Q < Ic_sat*0.98) else \
             "SATURATION" if Vce_Q <= 0.3 else "CUTOFF"

    tab_theory, tab_sim, tab_assess = st.tabs(["📐 Theory","📊 Characteristics","📝 Assessment"])

    with tab_theory:
        st.markdown(f"""
        <div class="tb">
        <strong>BJT NPN Common-Emitter (CE) Configuration</strong><br><br>
        The Common-Emitter amplifier is the most widely used BJT configuration. The input signal is applied
        to the <strong>Base-Emitter</strong> junction; the amplified output appears at the
        <strong>Collector-Emitter</strong> terminals. The CE arrangement provides both current and voltage gain.<br><br>
        <strong>DC Biasing:</strong><br>
        &nbsp;&nbsp;• Ib = (Vcc − Vbe) / Rb &nbsp;→ Base current sets the operating point<br>
        &nbsp;&nbsp;• Ic = β × Ib &nbsp;→ Collector current (active region)<br>
        &nbsp;&nbsp;• Vce = Vcc − Ic·Rc &nbsp;→ Collector-Emitter voltage<br><br>
        <strong>DC Load Line:</strong> A straight line on the Ic–Vce plane connecting<br>
        &nbsp;&nbsp;• Cutoff: (Vcc, 0) &nbsp;— no Ic, all voltage across CE<br>
        &nbsp;&nbsp;• Saturation: (0, Vcc/Rc) &nbsp;— max Ic, ~0 V across CE<br><br>
        <strong>Q-Point (Quiescent Point):</strong> Intersection of the load line with the Ic = β·Ib curve.
        For linear amplification, Q-point should be at the midpoint of the load line.<br><br>
        <strong>Operating Regions:</strong><br>
        &nbsp;&nbsp;• <em>Active:</em> Vce &gt; 0.3 V, Ic = β·Ib — linear amplification<br>
        &nbsp;&nbsp;• <em>Saturation:</em> Vce ≈ 0.1–0.3 V — transistor fully ON<br>
        &nbsp;&nbsp;• <em>Cutoff:</em> Ib = 0, Ic ≈ 0 — transistor fully OFF
        </div>""", unsafe_allow_html=True)

        st.markdown('<p class="sec">// Circuit Diagram</p>', unsafe_allow_html=True)
        components.html(SVG_WRAP + f"""
        <svg viewBox="0 0 680 200" xmlns="http://www.w3.org/2000/svg" width="100%">
          <rect width="680" height="200" fill="#0a1222"/>
          <!-- Vcc rail -->
          <line x1="340" y1="10" x2="340" y2="40" style="stroke:#f0abfc;stroke-width:2"/>
          <text x="340" y="8" text-anchor="middle" style="fill:#f0abfc;font-family:monospace;font-size:10px">+Vcc ({Vcc:.0f}V)</text>
          <!-- Rc -->
          <rect x="300" y="40" width="80" height="28" rx="3" style="fill:#1a0a2a;stroke:#f0abfc;stroke-width:1.8"/>
          <text x="340" y="58" text-anchor="middle" style="fill:#f0abfc;font-family:monospace;font-size:10px">Rc {Rc:.0f}Ω</text>
          <!-- BJT NPN symbol -->
          <line x1="340" y1="68" x2="340" y2="100" style="stroke:#f0abfc;stroke-width:2"/>
          <!-- Collector terminal -->
          <line x1="340" y1="100" x2="370" y2="82" style="stroke:#f0abfc;stroke-width:2"/>
          <!-- Base vertical bar -->
          <line x1="340" y1="82" x2="340" y2="122" style="stroke:#f0abfc;stroke-width:3"/>
          <!-- Emitter terminal (with arrow) -->
          <line x1="340" y1="122" x2="370" y2="140" style="stroke:#f0abfc;stroke-width:2"/>
          <polygon points="370,140 356,130 363,143" fill="#f0abfc"/>
          <!-- Base wire to Rb -->
          <line x1="220" y1="102" x2="340" y2="102" style="stroke:#f0abfc;stroke-width:2"/>
          <!-- Rb -->
          <rect x="130" y="88" width="90" height="28" rx="3" style="fill:#1a0a2a;stroke:#60a5fa;stroke-width:1.8"/>
          <text x="175" y="106" text-anchor="middle" style="fill:#60a5fa;font-family:monospace;font-size:10px">Rb {Rb:.0f}kΩ</text>
          <!-- Vin -->
          <circle cx="80" cy="102" r="22" class="w"/>
          <text x="80" y="107" text-anchor="middle" class="t" font-size="13">~</text>
          <text x="80" y="140" text-anchor="middle" style="fill:#00d4ff;font-family:monospace;font-size:9px">Vin</text>
          <line x1="102" y1="102" x2="130" y2="102" style="stroke:#60a5fa;stroke-width:2"/>
          <!-- Emitter to ground -->
          <line x1="370" y1="140" x2="370" y2="170" style="stroke:#f0abfc;stroke-width:2"/>
          <!-- Ground symbol -->
          <line x1="350" y1="170" x2="390" y2="170" style="stroke:#7a9cc4;stroke-width:2"/>
          <line x1="356" y1="176" x2="384" y2="176" style="stroke:#7a9cc4;stroke-width:1.5"/>
          <line x1="362" y1="182" x2="378" y2="182" style="stroke:#7a9cc4;stroke-width:1"/>
          <!-- Collector to Rc -->
          <line x1="370" y1="82" x2="370" y2="68" style="stroke:#f0abfc;stroke-width:2"/>
          <line x1="370" y1="68" x2="340" y2="68" style="stroke:#f0abfc;stroke-width:2"/>
          <!-- Vout tap -->
          <line x1="370" y1="100" x2="500" y2="100" style="stroke:#facc15;stroke-width:1.5;stroke-dasharray:5,3"/>
          <text x="508" y="104" style="fill:#facc15;font-family:monospace;font-size:10px">Vce (Vout)</text>
          <!-- Labels -->
          <text x="350" y="95"  style="fill:#f0abfc;font-family:monospace;font-size:9px">C</text>
          <text x="323" y="105" style="fill:#f0abfc;font-family:monospace;font-size:9px">B</text>
          <text x="376" y="138" style="fill:#f0abfc;font-family:monospace;font-size:9px">E</text>
        </svg>""", height=220, scrolling=False)

        svg4 = f"""<svg viewBox="0 0 680 200" xmlns="http://www.w3.org/2000/svg"><rect width="680" height="200" fill="#0a1222"/><text x="340" y="100" text-anchor="middle" fill="#f0abfc" font-family="monospace" font-size="13">BJT CE Config: Vcc={Vcc:.0f}V Rb={Rb:.0f}kohm Rc={Rc:.0f}ohm beta={beta:.0f}</text></svg>""".encode()
        st.download_button("⬇️ Download Circuit Diagram (SVG)", svg4,
                           file_name="bjt_ce_circuit.svg", mime="image/svg+xml")

    with tab_sim:
        metric_row([
            ("Ib (Q-point)", f"{Ib_Q*1e6:.1f}", "µA"),
            ("Ic (Q-point)", f"{Ic_Q*1000:.2f}", "mA"),
            ("Vce (Q-point)",f"{Vce_Q:.2f}",     "V"),
            ("Ic_sat",       f"{Ic_sat*1000:.2f}","mA"),
            ("Region",       region,               ""),
            ("β (hFE)",      f"{beta:.0f}",        ""),
        ])
        st.markdown("")

        vce_axis = np.linspace(0, Vcc*1.05, 400)
        fig = go.Figure()

        # Family of curves for 5 Ib values
        ib_values = np.linspace(Ib_Q*0.2, Ib_Q*2.0, 5)
        colours_fam = ["#1e3a5f","#2a5a9f","#3a7abf","#60a5fa","#a0c8ff"]
        for ib, col in zip(ib_values, colours_fam):
            ic_curve = beta * ib * (1 - np.exp(-vce_axis / 0.2))
            ic_curve = np.clip(ic_curve, 0, Vcc/Rc)
            fig.add_trace(go.Scatter(
                x=vce_axis, y=ic_curve*1000,
                mode="lines", name=f"Ib={ib*1e6:.0f}µA",
                line=dict(color=col, width=1.8)))

        # Load line
        vce_ll = np.array([0, Vcc])
        ic_ll  = np.array([Ic_sat*1000, 0])
        fig.add_trace(go.Scatter(x=vce_ll, y=ic_ll, mode="lines",
            name="DC Load Line", line=dict(color="#facc15", width=2, dash="dash")))

        # Q-point
        fig.add_trace(go.Scatter(x=[Vce_Q], y=[Ic_Q*1000], mode="markers",
            name=f"Q-point ({Vce_Q:.1f}V, {Ic_Q*1000:.1f}mA)",
            marker=dict(color="#f0abfc", size=14, symbol="star")))

        fig.update_layout(template="plotly_dark", paper_bgcolor="#070b14", plot_bgcolor="#0a0f1a",
            height=450, margin=dict(l=10,r=10,t=20,b=10),
            xaxis=dict(title="Vce (V)",    gridcolor="#1a2a3a", range=[0, Vcc*1.1]),
            yaxis=dict(title="Ic (mA)",    gridcolor="#1a2a3a", range=[0, Ic_sat*1000*1.15]),
            font=dict(family="Share Tech Mono", color="#c0d4e8", size=11),
            legend=dict(orientation="v", x=1.01, y=1, bgcolor="rgba(0,0,0,0)",
                        font=dict(size=9)))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<p class="sec">// DC Operating Point Summary</p>', unsafe_allow_html=True)
        odf = pd.DataFrame({
            "Parameter":["Supply Voltage (Vcc)","Base Resistor (Rb)","Collector Resistor (Rc)",
                         "Current Gain β","Base Current Ib","Collector Current Ic",
                         "Collector-Emitter Voltage Vce","Saturation Current Ic_sat","Operating Region"],
            "Value":[f"{Vcc:.1f} V", f"{Rb:.0f} kΩ", f"{Rc:.0f} Ω", f"{beta:.0f}",
                     f"{Ib_Q*1e6:.2f} µA", f"{Ic_Q*1000:.3f} mA",
                     f"{Vce_Q:.2f} V", f"{Ic_sat*1000:.2f} mA", region]
        })
        st.dataframe(odf.set_index("Parameter"), use_container_width=True)

    with tab_assess:
        Q4 = ["In the common-emitter configuration, what does the DC load line represent?",
              "How is the Q-point (quiescent point) defined on the BJT output characteristics?",
              "What is the formula relating collector current (Ic) to base current (Ib) in the active region?",
              "For linear (undistorted) amplification, where should the Q-point ideally be positioned?",
              "What happens to the transistor if Vce drops below approximately 0.3 V?"]
        A4 = [
            (["The AC signal path","The set of all possible Ic–Vce operating points for a given Vcc and Rc",
              "The frequency response curve","The thermal derating curve"],
             "The set of all possible Ic–Vce operating points for a given Vcc and Rc"),
            (["The peak of the output waveform",
              "The intersection of the DC load line with the transistor's Ic–Vce characteristic for a given Ib",
              "The midpoint of the supply voltage","The saturation current value"],
             "The intersection of the DC load line with the transistor's Ic–Vce characteristic for a given Ib"),
            (["Ic = Vcc / Rc","Ic = β × Ib","Ic = Ib / β","Ic = Vce / Rc"],
             "Ic = β × Ib"),
            (["Near the saturation region","Near the cutoff region",
              "At the midpoint of the load line for maximum swing","At the top of the load line"],
             "At the midpoint of the load line for maximum swing"),
            (["The transistor enters cutoff","The transistor enters saturation — Vce ≈ Vce(sat)",
              "β increases sharply","The load line shifts"], "The transistor enters saturation — Vce ≈ Vce(sat)"),
        ]
        render_assessment("p4", Q4, A4)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.caption(f"🔬 Physics/Electronics Laboratory Platform · Student: `{st.session_state['student_id']}` · "
           f"Session Active · {datetime.now().strftime('%Y-%m-%d')}")

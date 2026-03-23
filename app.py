"""
Asset Management Document Benchmarking Tool
"""

import sys, tempfile, json
from datetime import datetime
from pathlib import Path

if (Path(__file__).resolve().parent / "src").exists():
    sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF

from document_analysis_tool.ingestion import ingest
from document_analysis_tool.compliance import run_compliance
from document_analysis_tool.accessibility import run_accessibility
from document_analysis_tool.benchmarking.scoring import compute_benchmarking_scores
from document_analysis_tool.benchmarking.taxonomy import detect_taxonomy_coverage
from document_analysis_tool.benchmarking.esg_detector import assess_esg_needs
from document_analysis_tool.database import (
    init_db, register_user, authenticate_user, get_user_by_id,
    update_user_profile, change_password,
    create_session, validate_session, destroy_session,
    create_reset_code, verify_reset_code, reset_password,
    save_analysis, get_user_analyses, delete_analysis,
)

SESSION_FILE = Path(__file__).resolve().parent / "data" / ".session_token"

init_db()

# ═══════════════════════════════════════════════════════════════════════════
# Palette
# ═══════════════════════════════════════════════════════════════════════════
B6 = "#071935"; B5 = "#0342E4"
S4 = "#3A4051"; S3 = "#4A5267"
G4 = "#B0B8CB"; G3 = "#C3C9D9"
W = "#FFFFFF"; BG = "#F4F6F9"
GR5 = "#2E7D32"; GR4 = "#00C761"
RED = "#D32F2F"; AMB = "#F59E0B"

st.set_page_config(page_title="Document Benchmarking", page_icon="📊", layout="wide")

# ═══════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
*, html, body, [class*="css"], .stMarkdown, .stText, button, input, select, textarea,
[data-testid="stMetricValue"], [data-testid="stMetricLabel"],
.stTabs [data-baseweb="tab"], .stSelectbox div[data-baseweb="select"] span,
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}
.block-container {{ padding: 1rem 2rem 2rem; max-width: 1440px; background: {BG}; }}
[data-testid="stAppViewContainer"] {{ background: {BG}; }}

/* Sidebar */
[data-testid="stSidebar"] {{ background: {B6}; }}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown {{ color: {W} !important; }}
[data-testid="stSidebar"] .stSelectbox label {{ color: {G3} !important; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; }}
[data-testid="stSidebar"] div[data-baseweb="select"] {{ background: {W} !important; border-radius: 10px !important; border: none !important; }}
[data-testid="stSidebar"] div[data-baseweb="select"] span {{ color: {S4} !important; font-weight: 500 !important; }}
[data-testid="stSidebar"] div[data-baseweb="select"] svg {{ fill: {G4} !important; }}
[data-testid="stSidebar"] [data-testid="stTextInput"] input {{ background: {W} !important; color: {S4} !important; border-radius: 10px !important; border: 1px solid {G3} !important; }}
[data-testid="stSidebar"] button {{ border-radius: 10px !important; background: {W} !important; color: {B6} !important; font-weight: 600 !important; border: 1px solid {G3} !important; }}
[data-testid="stSidebar"] button:hover {{ background: {G3} !important; }}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{ gap: 0.2rem; background: {W}; border-radius: 14px; padding: 0.3rem; border: 1px solid {G3}; }}
.stTabs [data-baseweb="tab"] {{ border-radius: 10px; padding: 0.5rem 1rem; font-weight: 600; font-size: 0.78rem; color: {S4}; }}
.stTabs [aria-selected="true"] {{ background: {B5} !important; color: {W} !important; }}
.stTabs [data-baseweb="tab-panel"] {{ padding-top: 1.2rem; }}

/* Cards */
.k-card {{ background: {W}; border: 1px solid {G3}; border-radius: 16px; padding: 1.4rem; }}
.hero-card {{ background: {W}; border: 1px solid {G3}; border-radius: 18px; padding: 1.4rem 1.1rem; text-align: center; }}
.hero-card .hv {{ font-size: 2.5rem; font-weight: 800; line-height: 1.1; }}
.hero-card .hl {{ font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: {G4}; margin-bottom: 0.2rem; }}
.hero-card .hs {{ font-size: 0.76rem; color: {S3}; margin-top: 0.35rem; }}

.dp {{ background: {W}; border: 1px solid {G3}; border-radius: 14px; padding: 0.9rem; text-align: center; }}
.dp .ds {{ font-size: 1.7rem; font-weight: 800; }}
.dp .dn {{ font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: {S3}; }}
.dp .dl {{ font-size: 0.65rem; font-weight: 600; }}

.br {{ display: flex; align-items: center; gap: 0.6rem; margin: 0.35rem 0; }}
.br .bn {{ width: 110px; font-size: 0.76rem; font-weight: 600; color: {S4}; }}
.br .bt {{ flex: 1; height: 20px; background: #E8ECF1; border-radius: 10px; overflow: hidden; }}
.br .bf {{ height: 100%; border-radius: 10px; display: flex; align-items: center; justify-content: flex-end; padding-right: 7px; font-size: 0.65rem; font-weight: 700; color: {W}; }}

.fr {{ display: flex; align-items: flex-start; gap: 0.6rem; padding: 0.65rem 1rem; border-radius: 12px; margin: 0.25rem 0; border: 1px solid {G3}; background: {W}; }}
.fr.fp {{ border-left: 4px solid {GR4}; }}
.fr.ff {{ border-left: 4px solid {RED}; }}
.fr.fw {{ border-left: 4px solid {AMB}; }}
.fr .ft {{ font-weight: 600; font-size: 0.8rem; color: {B6}; }}
.fr .fm {{ font-size: 0.73rem; color: {S3}; }}
.fr .fs {{ font-size: 0.63rem; color: {G4}; }}
.badge {{ font-size: 0.58rem; padding: 0.1rem 0.4rem; border-radius: 20px; font-weight: 700; color: {W}; white-space: nowrap; }}
.bc {{ background: {RED}; }}
.bj {{ background: #E65100; }}
.bm {{ background: {AMB}; }}

.tt {{ background: {W}; border: 1px solid {G3}; border-radius: 14px; padding: 0.9rem; }}
.esg-b {{ border-radius: 14px; padding: 1.1rem 1.4rem; margin: 0.6rem 0; }}
.esg-n {{ background: #FFF8E1; border: 1px solid {AMB}; }}
.esg-g {{ background: #E8F5E9; border: 1px solid {GR4}; }}
.bsc {{ background: {W}; border: 1px solid {G3}; border-radius: 16px; padding: 1.2rem; }}
.rec {{ background: #E3F2FD; border-left: 4px solid {B5}; border-radius: 0 10px 10px 0; padding: 0.55rem 1rem; margin: 0.25rem 0; font-size: 0.8rem; color: {B6}; }}
.str {{ background: #E8F5E9; border-left: 4px solid {GR4}; border-radius: 0 10px 10px 0; padding: 0.55rem 1rem; margin: 0.25rem 0; font-size: 0.8rem; color: {GR5}; }}
.wk {{ background: #FFEBEE; border-left: 4px solid {RED}; border-radius: 0 10px 10px 0; padding: 0.55rem 1rem; margin: 0.25rem 0; font-size: 0.8rem; color: {RED}; }}
.sh {{ font-size: 1.05rem; font-weight: 700; color: {B6}; margin: 1.2rem 0 0.4rem; padding-bottom: 0.4rem; border-bottom: 2px solid {G3}; }}

/* Auth cards */
.auth-box {{ max-width: 420px; margin: 3rem auto; background: {W}; border: 1px solid {G3}; border-radius: 20px; padding: 2.5rem 2rem; }}
.auth-box h2 {{ color: {B6}; font-weight: 800; text-align: center; margin-bottom: 0.3rem; }}
.auth-box .sub {{ color: {S3}; font-size: 0.85rem; text-align: center; margin-bottom: 1.5rem; }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════════
DOC_TYPES = ["Fund Factsheet","Key Information Document (KID/KIID)","Prospectus / Offering Memo","Annual / Semi-Annual Report","Marketing Brochure","Product Guide","ESG / Sustainability Report","Performance Report","Investor Presentation","Pitchbook","Thought Leadership / White Paper","RFP / DDQ Response","Client Statement / Letter"]
JURISDICTIONS = {"EU":("EU","UCITS · PRIIPs · SFDR · MiFID II"),"UK":("UK","FCA · COBS · Consumer Duty"),"US":("US","SEC · 1940 Act · Marketing Rule"),"ZA":("South Africa","FSCA"),"AU":("Australia","ASIC")}
AUDIENCES = ["Retail","Professional / Advisor","Institutional"]
PEER_SET = ["BlackRock","Vanguard","Fidelity","J.P. Morgan AM","Goldman Sachs AM","PIMCO","Schroders","UBS AM","Amundi","Capital Group"]
DIM_ORDER = ["clarity","transparency","design","accessibility","compliance","usability"]
PILLAR_ORDER = ["completeness","consistency","compliance_pillar","quality","data_integrity"]
PCOL = {"completeness":B5,"consistency":"#7C3AED","compliance_pillar":GR4,"quality":AMB,"data_integrity":"#0891B2"}

# ═══════════════════════════════════════════════════════════════════════════
# Session state + auto-login from persisted token
# ═══════════════════════════════════════════════════════════════════════════
for k in ["user", "analyses", "page"]:
    if k not in st.session_state:
        st.session_state[k] = None if k == "user" else [] if k == "analyses" else "login"

if st.session_state.user is None and SESSION_FILE.exists():
    _token = SESSION_FILE.read_text().strip()
    if _token:
        _restored = validate_session(_token)
        if _restored:
            st.session_state.user = _restored
            st.session_state.page = "app"

# ═══════════════════════════════════════════════════════════════════════════
# Auth screens
# ═══════════════════════════════════════════════════════════════════════════
def show_login():
    st.markdown(f"""
    <div style="text-align:center;margin-top:2rem">
        <div style="font-size:2.5rem">📊</div>
        <div style="font-size:1.4rem;font-weight:800;color:{B6};margin-top:0.3rem">Document Benchmarking</div>
        <div style="font-size:0.85rem;color:{S3}">Asset Management · Investor Communications</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        st.markdown(f"## Sign In")
        st.markdown(f'<div class="sub">Access your document analysis library</div>', unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="you@company.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")

        if submitted:
            if email and password:
                user = authenticate_user(email, password)
                if user:
                    st.session_state.user = user
                    st.session_state.page = "app"
                    token = create_session(user["id"])
                    SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
                    SESSION_FILE.write_text(token)
                    _load_library()
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
            else:
                st.warning("Please enter email and password.")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Create account", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
        with c2:
            if st.button("Forgot password?", use_container_width=True):
                st.session_state.page = "forgot"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def show_register():
    st.markdown(f"""
    <div style="text-align:center;margin-top:2rem">
        <div style="font-size:2.5rem">📊</div>
        <div style="font-size:1.4rem;font-weight:800;color:{B6};margin-top:0.3rem">Create Account</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        st.markdown(f"## Register")
        st.markdown(f'<div class="sub">Set up your benchmarking account</div>', unsafe_allow_html=True)

        with st.form("register_form"):
            name = st.text_input("Full name", placeholder="Your Name")
            email = st.text_input("Email", placeholder="you@company.com")
            pw1 = st.text_input("Password", type="password", placeholder="Min 6 characters")
            pw2 = st.text_input("Confirm password", type="password", placeholder="Repeat password")
            submitted = st.form_submit_button("Register", use_container_width=True, type="primary")

        if submitted:
            if not name or not email or not pw1:
                st.warning("All fields are required.")
            elif len(pw1) < 6:
                st.warning("Password must be at least 6 characters.")
            elif pw1 != pw2:
                st.error("Passwords do not match.")
            else:
                user = register_user(email, name, pw1)
                if user:
                    st.session_state.user = user
                    st.session_state.page = "app"
                    token = create_session(user["id"])
                    SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
                    SESSION_FILE.write_text(token)
                    st.success("Account created!")
                    st.rerun()
                else:
                    st.error("Email already registered.")

        if st.button("Back to sign in", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def show_forgot():
    st.markdown(f"""
    <div style="text-align:center;margin-top:2rem">
        <div style="font-size:2.5rem">🔑</div>
        <div style="font-size:1.4rem;font-weight:800;color:{B6};margin-top:0.3rem">Reset Password</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)

        if not st.session_state.get("_reset_code_sent"):
            st.markdown(f"## Step 1")
            st.markdown(f'<div class="sub">Enter your email to receive a reset code</div>', unsafe_allow_html=True)

            with st.form("forgot_email_form"):
                email = st.text_input("Email", placeholder="you@company.com")
                submitted = st.form_submit_button("Send reset code", use_container_width=True, type="primary")

            if submitted:
                if not email:
                    st.warning("Please enter your email.")
                else:
                    code = create_reset_code(email)
                    if code:
                        st.session_state["_reset_email"] = email
                        st.session_state["_reset_code_sent"] = True
                        st.session_state["_reset_code_display"] = code
                        st.rerun()
                    else:
                        st.error("No account found with that email.")

        elif not st.session_state.get("_reset_verified"):
            st.markdown(f"## Step 2")
            st.markdown(f'<div class="sub">Enter the 6-digit code and set a new password</div>', unsafe_allow_html=True)

            code_display = st.session_state.get("_reset_code_display", "")
            st.info(f"Your reset code is: **{code_display}**\n\n_In production this would be sent to your email. The code expires in 15 minutes._")

            with st.form("forgot_reset_form"):
                code_input = st.text_input("Reset code", placeholder="6-digit code", max_chars=6)
                new_pw = st.text_input("New password", type="password", placeholder="Min 6 characters")
                confirm_pw = st.text_input("Confirm new password", type="password")
                submitted = st.form_submit_button("Reset password", use_container_width=True, type="primary")

            if submitted:
                reset_email = st.session_state.get("_reset_email", "")
                if not code_input or not new_pw:
                    st.warning("All fields are required.")
                elif len(new_pw) < 6:
                    st.warning("Password must be at least 6 characters.")
                elif new_pw != confirm_pw:
                    st.error("Passwords do not match.")
                elif not verify_reset_code(reset_email, code_input):
                    st.error("Invalid or expired reset code.")
                else:
                    if reset_password(reset_email, code_input, new_pw):
                        st.session_state["_reset_verified"] = True
                        st.rerun()
                    else:
                        st.error("Reset failed. Please try again.")

        else:
            st.markdown(f"## Done")
            st.success("Your password has been reset. You can now sign in with your new password.")
            for k in ["_reset_code_sent", "_reset_email", "_reset_code_display", "_reset_verified"]:
                st.session_state.pop(k, None)

        if st.button("Back to sign in", use_container_width=True):
            for k in ["_reset_code_sent", "_reset_email", "_reset_code_display", "_reset_verified"]:
                st.session_state.pop(k, None)
            st.session_state.page = "login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def _load_library():
    """Load saved analyses from DB into session state."""
    if st.session_state.user:
        rows = get_user_analyses(st.session_state.user["id"])
        loaded = []
        for r in rows:
            data = json.loads(r["results_json"]) if r["results_json"] else {}
            loaded.append({
                "db_id": r["id"],
                "filename": r["filename"],
                "doc_type": r["doc_type"] or "",
                "jurisdiction": r["jurisdiction"] or "",
                "audience": r["audience"] or "",
                "analysed_at": r["created_at"] or "",
                "overall": r["overall_score"] or 0,
                "compliance_pct": r["compliance_pct"] or 0,
                "accessibility_pct": r["accessibility_pct"] or 0,
                "esg_needed": bool(r["esg_needed"]),
                "esg_coverage": r["esg_coverage"] or 0,
                "saved": True,
                **data,
            })
        st.session_state.analyses = loaded


# ═══════════════════════════════════════════════════════════════════════════
# Auth gate
# ═══════════════════════════════════════════════════════════════════════════
if st.session_state.user is not None and not st.session_state.analyses:
    _load_library()

if st.session_state.page == "forgot" and st.session_state.user is None:
    show_forgot()
    st.stop()
if st.session_state.page == "login" or (st.session_state.user is None and st.session_state.page not in ("register", "forgot")):
    show_login()
    st.stop()
if st.session_state.page == "register" and st.session_state.user is None:
    show_register()
    st.stop()

user = st.session_state.user

# ═══════════════════════════════════════════════════════════════════════════
# Sidebar (logged in)
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"### 📊 Document Benchmarking")
    st.caption(f"Signed in as **{user['name']}**")

    sb1, sb2 = st.columns(2)
    with sb1:
        if st.button("Sign out", key="signout", use_container_width=True):
            if SESSION_FILE.exists():
                _tok = SESSION_FILE.read_text().strip()
                if _tok:
                    destroy_session(_tok)
                SESSION_FILE.unlink(missing_ok=True)
            st.session_state.user = None
            st.session_state.page = "login"
            st.session_state.analyses = []
            st.rerun()
    with sb2:
        _show_profile = st.button("Profile", key="profile_btn", use_container_width=True)

    if _show_profile or st.session_state.get("_profile_open"):
        st.session_state["_profile_open"] = True
        st.markdown("---")
        st.markdown(f"**Edit Profile**")
        with st.form("profile_form"):
            pf_name = st.text_input("Name", value=user["name"])
            pf_email = st.text_input("Email", value=user["email"])
            pf_save = st.form_submit_button("Save changes", use_container_width=True)
        if pf_save:
            updated = update_user_profile(user["id"], pf_name, pf_email)
            if updated:
                st.session_state.user = {**st.session_state.user, "name": updated["name"], "email": updated["email"]}
                st.success("Profile updated.")
                st.rerun()
            else:
                st.error("Email may already be in use.")

        st.markdown(f"**Change Password**")
        with st.form("password_form"):
            pw_cur = st.text_input("Current password", type="password")
            pw_new = st.text_input("New password", type="password", placeholder="Min 6 characters")
            pw_conf = st.text_input("Confirm new password", type="password")
            pw_save = st.form_submit_button("Update password", use_container_width=True)
        if pw_save:
            if not pw_cur or not pw_new:
                st.warning("All password fields are required.")
            elif len(pw_new) < 6:
                st.warning("New password must be at least 6 characters.")
            elif pw_new != pw_conf:
                st.error("New passwords do not match.")
            else:
                if change_password(user["id"], pw_cur, pw_new):
                    st.success("Password changed.")
                else:
                    st.error("Current password is incorrect.")

        if st.button("Close profile", key="close_prof", use_container_width=True):
            st.session_state["_profile_open"] = False
            st.rerun()

    st.markdown("---")
    jurisdiction = st.selectbox("Jurisdiction", list(JURISDICTIONS.keys()), format_func=lambda k: f"{JURISDICTIONS[k][0]} — {JURISDICTIONS[k][1]}")
    doc_type = st.selectbox("Document type", DOC_TYPES)
    audience = st.selectbox("Target audience", AUDIENCES)
    st.markdown("---")
    st.markdown("**Peer benchmark set**")
    pc1, pc2 = st.columns(2)
    for i, p in enumerate(PEER_SET):
        with (pc1 if i % 2 == 0 else pc2):
            st.caption(f"◆ {p}")

# ═══════════════════════════════════════════════════════════════════════════
# Header
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="background:linear-gradient(135deg,{B6} 0%,{S4} 55%,{B5} 100%);border-radius:18px;padding:1.8rem 2.5rem;color:{W};margin-bottom:1.2rem;">
    <div style="font-size:1.5rem;font-weight:800;letter-spacing:-0.02em">Welcome back, {user['name']}</div>
    <div style="font-size:0.82rem;opacity:0.75;margin-top:0.3rem">Upload and benchmark your investor-facing and marketing documents.</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# Multi-file upload
# ═══════════════════════════════════════════════════════════════════════════
uploaded_files = st.file_uploader("Upload documents", type=["pdf","docx"], accept_multiple_files=True, label_visibility="collapsed")

if uploaded_files:
    existing = {a["filename"] for a in st.session_state.analyses}
    new_files = [f for f in uploaded_files if f.name not in existing]
    if new_files:
        prog = st.progress(0, text="Analysing…")
        for idx, uf in enumerate(new_files):
            prog.progress((idx+1)/len(new_files), text=f"Analysing {uf.name}…")
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uf.name).suffix) as tmp:
                tmp.write(uf.getvalue()); temp_path = Path(tmp.name)
            doc = ingest(temp_path)
            if doc is None:
                continue
            cr = run_compliance(doc, jurisdiction)
            ar = run_accessibility(doc)
            tax = detect_taxonomy_coverage(doc.raw_text)
            bm = compute_benchmarking_scores(doc, cr, ar, tax)
            esg_r = assess_esg_needs(doc.raw_text)
            now = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Serialisable subset for DB
            results_data = {
                "cr": cr, "ar": ar,
                "tax": [{"id":t.id,"label":t.label,"icon":t.icon,"present":t.present,"matched_keywords":t.matched_keywords,"coverage_pct":t.coverage_pct} for t in tax],
                "bm_dims": {k:{"score":v.score,"label":v.label,"colour":v.colour,"details":v.details} for k,v in bm.dimensions.items()},
                "bm_pillars": {k:{"pillar":v.pillar,"score":v.score,"label":v.label,"details":v.details} for k,v in bm.pillars.items()},
                "bm_strengths": bm.strengths, "bm_weaknesses": bm.weaknesses, "bm_recommendations": bm.recommendations,
                "bm_overall": bm.overall_score,
                "esg": {"needs":esg_r.needs_esg_content,"confidence":esg_r.confidence,"reasons":esg_r.reasons,
                        "sensitive":esg_r.sensitive_sectors_found,"positive":esg_r.positive_sectors_found,
                        "regulatory":esg_r.regulatory_signals_found,"strategy":esg_r.strategy_signals_found,
                        "has_esg":esg_r.has_esg_content,"coverage":esg_r.esg_coverage_score,"missing":esg_r.missing_esg_elements},
            }

            db_id = save_analysis(
                user_id=user["id"], filename=uf.name, doc_type=doc_type,
                jurisdiction=jurisdiction, audience=audience,
                overall_score=bm.overall_score, compliance_pct=cr.get("compliance_score",0),
                accessibility_pct=ar.get("accessibility_score",0),
                esg_needed=esg_r.needs_esg_content, esg_coverage=esg_r.esg_coverage_score,
                results_json=results_data,
            )
            st.session_state.analyses.append({
                "db_id": db_id, "filename": uf.name, "doc_type": doc_type,
                "jurisdiction": jurisdiction, "audience": audience, "analysed_at": now,
                "overall": bm.overall_score, "compliance_pct": cr.get("compliance_score",0),
                "accessibility_pct": ar.get("accessibility_score",0),
                "esg_needed": esg_r.needs_esg_content, "esg_coverage": esg_r.esg_coverage_score,
                "saved": True, **results_data,
            })
        prog.empty()

if not st.session_state.analyses and not uploaded_files:
    st.markdown(f"""
    <div style="text-align:center;padding:3rem 2rem;background:{W};border:2px dashed {G3};border-radius:18px;margin-top:1rem">
        <div style="font-size:2.5rem">📄</div>
        <div style="font-size:1rem;font-weight:700;color:{B6};margin-top:0.5rem">Upload PDF or Word documents</div>
        <div style="font-size:0.8rem;color:{G4};margin-top:0.3rem">Upload multiple files. Each will be analysed and saved to your library.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════
# PDF helper
# ═══════════════════════════════════════════════════════════════════════════
def gen_pdf(e: dict) -> bytes:
    pdf = FPDF(); pdf.add_page(); pdf.set_auto_page_break(auto=True, margin=15)
    _sys_fonts = Path("/System/Library/Fonts/Supplemental")
    _arial_uni = _sys_fonts / "Arial Unicode.ttf"
    _arial_bold = _sys_fonts / "Arial Bold.ttf"
    if _arial_uni.exists():
        pdf.add_font("arialuni", "", str(_arial_uni), uni=True)
        pdf.add_font("arialuni", "B", str(_arial_bold if _arial_bold.exists() else _arial_uni), uni=True)
        F = "arialuni"
    else:
        F = "Helvetica"
    pdf.set_font(F,"B",18); pdf.cell(0,12,"Document Benchmarking Report",new_x="LMARGIN",new_y="NEXT")
    pdf.set_font(F,"",10); pdf.cell(0,6,f"File: {e['filename']}  |  Type: {e['doc_type']}  |  Jurisdiction: {e['jurisdiction']}  |  Date: {e['analysed_at']}",new_x="LMARGIN",new_y="NEXT")
    pdf.ln(6); pdf.set_font(F,"B",13); pdf.cell(0,8,"Scores",new_x="LMARGIN",new_y="NEXT")
    pdf.set_font(F,"",10); pdf.cell(0,6,f"Overall: {e['overall']:.1f}/5   |   Compliance: {e['compliance_pct']:.0f}%   |   Accessibility: {e['accessibility_pct']:.0f}%   |   ESG: {e['esg_coverage']:.0f}%",new_x="LMARGIN",new_y="NEXT")
    pdf.ln(4)
    dims = e.get("bm_dims",{})
    if dims:
        pdf.set_font(F,"B",12); pdf.cell(0,8,"Dimensions (1-5)",new_x="LMARGIN",new_y="NEXT"); pdf.set_font(F,"",10)
        for did in DIM_ORDER:
            d = dims.get(did,{})
            pdf.cell(0,6,f"  {d.get('label','')}: {d.get('score',0):.1f}",new_x="LMARGIN",new_y="NEXT")
    cr = e.get("cr",{})
    if cr.get("results"):
        pdf.ln(4); pdf.set_font(F,"B",12); pdf.cell(0,8,"Compliance",new_x="LMARGIN",new_y="NEXT"); pdf.set_font(F,"",9)
        for r in cr["results"]:
            st_txt = "PASS" if r.get("passed") else "FAIL"
            pdf.cell(0,5,f"  [{st_txt}] {r.get('name','')} - {r.get('message','')}",new_x="LMARGIN",new_y="NEXT")
    ar = e.get("ar",{})
    if ar.get("results"):
        pdf.ln(4); pdf.set_font(F,"B",12); pdf.cell(0,8,"Accessibility",new_x="LMARGIN",new_y="NEXT"); pdf.set_font(F,"",9)
        for r in ar["results"]:
            st_txt = "PASS" if r.get("passed") else "FAIL"
            pdf.cell(0,5,f"  [{st_txt}] {r.get('name',r.get('check',''))} - {r.get('message','')}",new_x="LMARGIN",new_y="NEXT")
    recs = e.get("bm_recommendations",[])
    if recs:
        pdf.ln(4); pdf.set_font(F,"B",12); pdf.cell(0,8,"Recommendations",new_x="LMARGIN",new_y="NEXT"); pdf.set_font(F,"",9)
        for r in recs:
            pdf.cell(0,5,f"  > {r}",new_x="LMARGIN",new_y="NEXT")
    return bytes(pdf.output())

# ═══════════════════════════════════════════════════════════════════════════
# Library / data table
# ═══════════════════════════════════════════════════════════════════════════
main_tabs = st.tabs(["📚 Library", "🔍 Document Detail"])

with main_tabs[0]:
    analyses = st.session_state.analyses
    st.markdown(f'<div class="sh">Document Library ({len(analyses)} documents)</div>', unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        tf = st.multiselect("Filter by type", sorted(set(a["doc_type"] for a in analyses)), key="lib_tf")
    with fc2:
        jf = st.multiselect("Filter by jurisdiction", sorted(set(a["jurisdiction"] for a in analyses)), key="lib_jf")
    with fc3:
        sb = st.selectbox("Sort by", ["Date (newest)","Date (oldest)","Name (A–Z)","Name (Z–A)","Overall ↓","Overall ↑","Compliance ↓","Accessibility ↓"], key="lib_sb")

    filtered = analyses[:]
    if tf: filtered = [a for a in filtered if a["doc_type"] in tf]
    if jf: filtered = [a for a in filtered if a["jurisdiction"] in jf]
    sm = {"Date (newest)":("analysed_at",True),"Date (oldest)":("analysed_at",False),"Name (A–Z)":("filename",False),"Name (Z–A)":("filename",True),"Overall ↓":("overall",True),"Overall ↑":("overall",False),"Compliance ↓":("compliance_pct",True),"Accessibility ↓":("accessibility_pct",True)}
    sk, sr = sm.get(sb,("analysed_at",True))
    filtered.sort(key=lambda a: a.get(sk,""), reverse=sr)

    rows = [{"Document":a["filename"],"Type":a["doc_type"],"Jurisdiction":a["jurisdiction"],"Audience":a["audience"],"Overall":a["overall"],"Compliance":f"{a['compliance_pct']:.0f}%","Accessibility":f"{a['accessibility_pct']:.0f}%","ESG":("Yes" if a["esg_needed"] else "No"),"Date":a["analysed_at"],"Saved":"✅"if a.get("saved") else "—"} for a in filtered]
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True, height=min(420, 52+len(rows)*38))

    st.markdown("")
    ec1, ec2, ec3 = st.columns([3,1,1])
    with ec1:
        exp_doc = st.selectbox("Select document", [a["filename"] for a in filtered] if filtered else ["—"], key="exp_sel")
    with ec2:
        if st.button("📥 Export PDF", key="exp_btn", use_container_width=True):
            entry = next((a for a in filtered if a["filename"] == exp_doc), None)
            if entry:
                st.download_button("⬇ Download", data=gen_pdf(entry), file_name=f"benchmark_{exp_doc.rsplit('.',1)[0]}.pdf", mime="application/pdf", key="dl_pdf")
    with ec3:
        if st.button("🗑 Remove", key="del_btn", use_container_width=True):
            entry = next((a for a in filtered if a["filename"] == exp_doc), None)
            if entry and entry.get("db_id"):
                delete_analysis(entry["db_id"], user["id"])
                st.session_state.analyses = [a for a in st.session_state.analyses if a.get("db_id") != entry["db_id"]]
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# Detail view
# ═══════════════════════════════════════════════════════════════════════════
with main_tabs[1]:
    if not st.session_state.analyses:
        st.info("Upload documents to see detailed analysis.")
        st.stop()

    sel = st.selectbox("Select document", [a["filename"] for a in st.session_state.analyses], key="det_sel")
    e = next((a for a in st.session_state.analyses if a["filename"] == sel), None)
    if not e:
        st.stop()

    dims = e.get("bm_dims", {})
    pillars = e.get("bm_pillars", {})
    cr = e.get("cr", {})
    ar = e.get("ar", {})
    tax_list = e.get("tax", [])
    esg = e.get("esg", {})

    detail_tabs = st.tabs(["Overview","Radar & Heatmap","Taxonomy","Compliance","Accessibility","ESG","BSC","Insights"])

    with detail_tabs[0]:
        c1,c2,c3,c4 = st.columns(4)
        ov = e["overall"]
        oc = GR4 if ov>=3.5 else AMB if ov>=2.5 else RED
        with c1: st.markdown(f'<div class="hero-card"><div class="hl">Overall</div><div class="hv" style="color:{oc}">{ov:.1f}<span style="font-size:1rem;color:{G4}">/5</span></div></div>', unsafe_allow_html=True)
        cp = e["compliance_pct"]; cc = GR4 if cp>=75 else AMB if cp>=50 else RED
        with c2: st.markdown(f'<div class="hero-card"><div class="hl">Compliance</div><div class="hv" style="color:{cc}">{cp:.0f}%</div><div class="hs">{cr.get("passed_count",0)}/{cr.get("total_count",0)} rules</div></div>', unsafe_allow_html=True)
        ap = e["accessibility_pct"]; ac = GR4 if ap>=75 else AMB if ap>=50 else RED
        with c3: st.markdown(f'<div class="hero-card"><div class="hl">Accessibility</div><div class="hv" style="color:{ac}">{ap:.0f}%</div><div class="hs">{ar.get("passed_count",0)}/{ar.get("total_count",0)} checks</div></div>', unsafe_allow_html=True)
        tp = sum(1 for t in tax_list if t.get("present",False)); tc = GR4 if tp>=8 else AMB if tp>=5 else RED
        with c4: st.markdown(f'<div class="hero-card"><div class="hl">Taxonomy</div><div class="hv" style="color:{tc}">{tp}<span style="font-size:1rem;color:{G4}">/{len(tax_list)}</span></div></div>', unsafe_allow_html=True)

        if dims:
            st.markdown(f'<div class="sh">Six-Dimension Evaluation</div>', unsafe_allow_html=True)
            dc = st.columns(6)
            for i,did in enumerate(DIM_ORDER):
                d = dims.get(did,{})
                with dc[i]:
                    col = d.get("colour",G4)
                    st.markdown(f'<div class="dp"><div class="ds" style="color:{col}">{d.get("score",0):.1f}</div><div class="dn">{did.title()}</div><div class="dl" style="color:{col}">{d.get("label","")}</div></div>', unsafe_allow_html=True)

        if pillars:
            st.markdown(f'<div class="sh">Five-Pillar Framework</div>', unsafe_allow_html=True)
            for pid in PILLAR_ORDER:
                p = pillars.get(pid,{})
                c = PCOL.get(pid,B5); w = max(p.get("score",0),2)
                st.markdown(f'<div class="br"><div class="bn">{p.get("pillar","")}</div><div class="bt"><div class="bf" style="width:{w}%;background:{c}">{p.get("score",0):.0f}%</div></div></div>', unsafe_allow_html=True)

    with detail_tabs[1]:
        if dims:
            labels = [dims.get(d,{}).get("label",d.title()) for d in DIM_ORDER]
            # Use dimension names for radar labels
            labels = [d.title() for d in DIM_ORDER]
            vals = [dims.get(d,{}).get("score",0) for d in DIM_ORDER]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=vals+[vals[0]], theta=labels+[labels[0]], fill="toself", name="Document", line=dict(color=B5, width=2.5), fillcolor="rgba(3,66,228,0.1)"))
            fig.add_trace(go.Scatterpolar(r=[3]*7, theta=labels+[labels[0]], name="Competitive", line=dict(color=G4, dash="dash", width=1)))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,5],tickvals=[1,2,3,4,5],gridcolor=G3)), showlegend=True, height=420, margin=dict(t=30,b=30,l=60,r=60), font=dict(family="Plus Jakarta Sans",size=12), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

            hv = [[dims.get(d,{}).get("score",0) for d in DIM_ORDER]]
            fig_hm = go.Figure(data=go.Heatmap(z=hv,x=labels,y=["Score"],colorscale=[[0,RED],[0.5,AMB],[1,GR4]],zmin=1,zmax=5,text=[[f"{v:.1f}" for v in hv[0]]],texttemplate="%{text}",textfont=dict(size=14,color="white"),showscale=False))
            fig_hm.update_layout(height=130,margin=dict(t=10,b=10,l=10,r=10),yaxis=dict(visible=False),font=dict(family="Plus Jakarta Sans"))
            st.plotly_chart(fig_hm, use_container_width=True)

    with detail_tabs[2]:
        st.markdown(f'<div class="sh">Taxonomy Coverage</div>', unsafe_allow_html=True)
        tc1,tc2 = st.columns(2)
        for i,t in enumerate(tax_list):
            with (tc1 if i%2==0 else tc2):
                bc = GR4 if t.get("coverage_pct",0)>=50 else AMB if t.get("coverage_pct",0)>=20 else RED if t.get("present") else G3
                st.markdown(f'<div class="tt"><div style="display:flex;align-items:center;gap:0.5rem"><span>{t.get("icon","📄")}</span><span style="font-weight:700;font-size:0.82rem;color:{B6}">{t.get("label","")}</span><span style="margin-left:auto;font-size:0.75rem;font-weight:700;color:{bc}">{t.get("coverage_pct",0):.0f}%</span></div></div>', unsafe_allow_html=True)
                st.progress(min(t.get("coverage_pct",0)/100, 1.0))
                if t.get("matched_keywords"):
                    st.caption(", ".join(t["matched_keywords"][:6]))

    with detail_tabs[3]:
        st.markdown(f'<div class="sh">Compliance — {JURISDICTIONS.get(e["jurisdiction"],("",""))[0]}</div>', unsafe_allow_html=True)
        if cr.get("error"):
            st.warning(cr["error"])
        elif cr.get("results"):
            mc1,mc2,mc3 = st.columns(3)
            mc1.metric("Score",f"{cr.get('compliance_score',0):.0f}%"); mc2.metric("Passed",cr.get("passed_count",0)); mc3.metric("Failed",cr.get("failed_count",0))
            for r in cr["results"]:
                sev = r.get("severity","medium"); cls = "fp" if r.get("passed") else "ff"; icon = "✅" if r.get("passed") else "❌"
                bcls = "bc" if sev=="high" else ("bj" if sev=="major" else "bm")
                st.markdown(f'<div class="fr {cls}"><div>{icon}</div><div style="flex:1"><div class="ft">{r.get("name",r.get("rule_id",""))}</div><div class="fm">{r.get("message","")}</div></div><div><span class="badge {bcls}">{sev.upper()}</span></div></div>', unsafe_allow_html=True)

    with detail_tabs[4]:
        st.markdown(f'<div class="sh">Accessibility</div>', unsafe_allow_html=True)
        ac1,ac2,ac3 = st.columns(3)
        ac1.metric("Score",f"{ar.get('accessibility_score',0):.0f}%"); ac2.metric("Critical",ar.get("critical_failures",0)); ac3.metric("Major/Minor",f"{ar.get('major_failures',0)}/{ar.get('minor_failures',0)}")
        cats = {}
        for r in ar.get("results",[]):
            cats.setdefault(r.get("category","Other"),[]).append(r)
        for cn,checks in cats.items():
            st.markdown(f"**{cn}**")
            for r in checks:
                cls = "fp" if r["passed"] else ("ff" if r["severity"]=="critical" else "fw"); icon = "✅" if r["passed"] else "❌"
                bcls = "bc" if r["severity"]=="critical" else ("bj" if r["severity"]=="major" else "bm")
                st.markdown(f'<div class="fr {cls}"><div>{icon}</div><div style="flex:1"><div class="ft">{r.get("name",r.get("check",""))}</div><div class="fm">{r.get("message","")}</div><div class="fs">{r.get("standard","")} · {r.get("wcag_criterion","")}</div></div><div><span class="badge {bcls}">{r["severity"].upper()}</span></div></div>', unsafe_allow_html=True)

    with detail_tabs[5]:
        st.markdown(f'<div class="sh">ESG Assessment</div>', unsafe_allow_html=True)
        if esg.get("needs"):
            st.markdown(f'<div class="esg-b esg-n"><div style="font-weight:700;color:{B6}">⚠️ ESG content likely needed ({esg.get("confidence","")})</div><div style="font-size:0.8rem;color:{S3};margin-top:0.2rem">{"; ".join(esg.get("reasons",[])[:3])}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="esg-b esg-g"><div style="font-weight:700;color:{B6}">✅ No strong ESG requirement ({esg.get("confidence","")})</div></div>', unsafe_allow_html=True)
        ec1,ec2 = st.columns(2)
        ec1.metric("ESG coverage",f"{esg.get('coverage',0):.0f}%")
        ec2.metric("Sensitive sectors",len(esg.get("sensitive",[])))
        for m in esg.get("missing",[]):
            st.markdown(f'<div class="rec">• {m}</div>', unsafe_allow_html=True)

    with detail_tabs[6]:
        st.markdown(f'<div class="sh">Balanced Scorecard</div>', unsafe_allow_html=True)
        bsc_data = [("👤","Customer",B5,["Clarity","Usability","Accessibility"],["clarity","usability","accessibility"]),("⚙️","Internal Process","#7C3AED",["Compliance","Consistency","Governance"],["compliance"]),("🌱","Learning & Growth",GR4,["ESG depth","Innovation","Thought leadership"],[]),("💰","Financial",AMB,["Efficiency","Scalability","Cost"],[]),]
        bc1,bc2 = st.columns(2)
        for i,(icon,title,col,metrics,dim_ids) in enumerate(bsc_data):
            with (bc1 if i%2==0 else bc2):
                st.markdown(f'<div class="bsc" style="border-top:4px solid {col}"><div style="font-size:1.2rem">{icon}</div><div style="font-weight:700;font-size:0.85rem;color:{B6};margin-top:0.2rem">{title}</div><div style="font-size:0.75rem;color:{S3};margin-top:0.4rem;line-height:1.6">{"<br>".join("• "+m for m in metrics)}</div></div>', unsafe_allow_html=True)
                if dim_ids and dims:
                    scores = [dims.get(d,{}).get("score",0) for d in dim_ids]
                    if scores: st.metric(title, f"{sum(scores)/len(scores):.1f} / 5")
                else:
                    st.caption("_Requires workflow data_")
                st.markdown("")

    with detail_tabs[7]:
        sw1,sw2 = st.columns(2)
        with sw1:
            st.markdown(f'<div class="sh">Strengths</div>', unsafe_allow_html=True)
            for s in e.get("bm_strengths",["None detected"]):
                st.markdown(f'<div class="str">✅ {s}</div>', unsafe_allow_html=True)
        with sw2:
            st.markdown(f'<div class="sh">Weaknesses</div>', unsafe_allow_html=True)
            for w in e.get("bm_weaknesses",["None detected"]):
                st.markdown(f'<div class="wk">❌ {w}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sh">Recommendations</div>', unsafe_allow_html=True)
        for r in e.get("bm_recommendations",[]):
            st.markdown(f'<div class="rec">→ {r}</div>', unsafe_allow_html=True)

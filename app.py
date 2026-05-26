import streamlit as st
import subprocess
import os
import glob
import base64
import shutil

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tube2Book · Media to eBook",
    page_icon="📔",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state init ────────────────────────────────────────────────────────
if "current_step_idx" not in st.session_state:
    st.session_state.current_step_idx = -1
if "step_statuses" not in st.session_state:
    st.session_state.step_statuses = ["waiting"] * 5
if "generated_pdf" not in st.session_state:
    st.session_state.generated_pdf = None
if "pipeline_phase" not in st.session_state:
    st.session_state.pipeline_phase = "idle" # Options: idle, processing, completed

steps_config = [
    {"num": "01", "title": "Fetch Media", "cmd": "python -m scripts.fetch_playlist"},
    {"num": "02", "title": "Extract Transcripts", "cmd": "python -m scripts.extract_transcripts"},
    {"num": "03", "title": "Generate Chapters", "cmd": "python -m scripts.generate_chapters"},
    {"num": "04", "title": "Compile Book", "cmd": "python -m scripts.compile_book"},
    {"num": "05", "title": "Export PDF", "cmd": "python -m scripts.export_pdf"},
]

# ── Helper: Clean target directories ──
def clear_previous_assets():
    """Removes previous data and output directories to guarantee a fresh start."""
    for folder in ["data", "output"]:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
            except Exception as e:
                st.sidebar.error(f"Cleaning notice: {e}")

# ── Reset Callback Function ──
def handle_new_project_reset():
    """Safely purges folders, wipes active pipeline memory, and resets input keys."""
    clear_previous_assets()
    st.session_state.current_step_idx = -1
    st.session_state.step_statuses = ["waiting"] * 5
    st.session_state.generated_pdf = None
    st.session_state.pipeline_phase = "idle"
    if "youtube_input" in st.session_state:
        st.session_state.youtube_input = ""

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #f3f0f7;
}

.stApp {
    background: #09070f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(147, 51, 234, 0.15) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(192, 132, 252, 0.08) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

.hero {
    text-align: center;
    padding: 3.5rem 0 1.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #a855f7;
    margin-bottom: 1rem;
    opacity: 0.9;
}
.hero h1 {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: clamp(3rem, 8vw, 5.5rem); 
    font-weight: 800;
    line-height: 0.95;
    letter-spacing: -0.04em;
    background: linear-gradient(180deg, #ffffff 0%, #d8d2e2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0px 4px 10px rgba(0, 0, 0, 0.4);
    margin: 0 0 1.5rem;
    padding-bottom: 0.1em;
}
.hero h1 span { color: #c084fc; }
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #b3acc0;
    margin: 0 auto;
    line-height: 1.65;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.3), transparent);
    margin: 2rem 0;
}

/* Input Boxes */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(168, 85, 247, 0.25) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #c084fc !important;
    box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.15) !important;
}
.processing-input .stTextInput > div > div > input {
    border: 1px solid rgba(239, 68, 68, 0.8) !important;
    box-shadow: 0 0 12px rgba(239, 68, 68, 0.25) !important;
}
.completed-input .stTextInput > div > div > input {
    border: 1px solid rgba(34, 197, 94, 0.8) !important;
    box-shadow: 0 0 12px rgba(34, 197, 94, 0.25) !important;
}

.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #a855f7 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #a855f7 0%, #7e22ce 100%) !important;
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    box-shadow: 0 4px 20px rgba(147, 51, 234, 0.3) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(147, 51, 234, 0.45) !important;
}

.action-buttons-wrapper {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
    width: 100%;
}
.generate-btn-container { flex: 3; }
.reset-btn-container { flex: 1; }

.reset-btn-container .stButton > button {
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
    box-shadow: 0 4px 20px rgba(34, 197, 94, 0.3) !important;
}
.reset-btn-container .stButton > button:hover {
    box-shadow: 0 8px 28px rgba(34, 197, 94, 0.45) !important;
}

/* Step Cards */
.step-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.step-card.active { 
    border-color: rgba(239, 68, 68, 0.6) !important; 
    background: rgba(239, 68, 68, 0.04) !important; 
}
.step-card.done { 
    border-color: rgba(34, 197, 94, 0.5) !important; 
    background: rgba(34, 197, 94, 0.04) !important; 
}

.step-card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: rgba(255,255,255,0.03); }
.step-card.active::before { background: #ef4444 !important; }
.step-card.done::before   { background: #22c55e !important; }

.step-header { display: flex; flex-direction: column; align-items: flex-start; gap: 0.2rem; }
.step-num { font-family: 'DM Mono', monospace; font-size: 0.6rem; color: #a855f7; opacity: 0.7; }
.step-card.active .step-num { color: #ef4444 !important; }
.step-card.done .step-num { color: #22c55e !important; }

.step-title { font-family: 'Syne', sans-serif; font-size: 0.82rem; font-weight: 700; color: #ffffff; }
.step-status { font-family: 'DM Mono', monospace; font-size: 0.6rem; margin-top: 0.2rem; }
.status-waiting  { color: #4b4458; }
.status-running  { color: #ef4444 !important; font-weight: bold; }
.status-done     { color: #22c55e !important; }

.result-panel { background: rgba(255,255,255,0.015); border: 1px solid rgba(168, 85, 247, 0.2); border-radius: 16px; padding: 2rem; margin-top: 1.5rem; }
.panel-label { font-family: 'DM Mono', monospace; font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 1.2rem; color: #c084fc; padding-bottom: 0.7rem; border-bottom: 1px solid rgba(168, 85, 247, 0.15); }
.preview-container { max-height: 750px; overflow-y: auto; border-radius: 10px; padding: 10px; background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.05); }
.section-heading { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700; color: #ffffff; margin: 2rem 0 1rem; }
.notice { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #5c556b; text-align: center; margin-top: 3rem; }
</style>
""", unsafe_allow_html=True)

# ── Helper: Step card rendering ───────────────────────────────────────────────
def render_step_card(num: str, title: str, state: str):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● IN PROGRESS", "status-running"),
        "done":    ("✓ COMPLETED",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Automated Conversion Pipeline</div>
    <h1>Tube2Book</h1>
    <p class="hero-sub">Transform YouTube Playlists or Individual Videos into beautifully formatted eBooks.</p>
</div>
""", unsafe_allow_html=True)

# Pipeline grid layout
col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)
cols = [col_p1, col_p2, col_p3, col_p4, col_p5]
for idx, step in enumerate(steps_config):
    with cols[idx]:
        render_step_card(step["num"], step["title"], st.session_state.step_statuses[idx])

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Setup Dynamic Border Wrapper Class
is_running = st.session_state.current_step_idx >= 0
is_completed = st.session_state.pipeline_phase == "completed"

border_wrapper_class = "default-input"
if st.session_state.pipeline_phase == "processing":
    border_wrapper_class = "processing-input"
elif st.session_state.pipeline_phase == "completed":
    border_wrapper_class = "completed-input"

# Render input layout
st.markdown(f'<div class="{border_wrapper_class}">', unsafe_allow_html=True)
media_url = st.text_input(
    "YouTube Playlist or Video URL",
    placeholder="https://www.youtube.com/playlist?list=... OR https://www.youtube.com/watch?v=...",
    key="youtube_input",
    disabled=is_running
)
st.markdown('</div>', unsafe_allow_html=True)

# Operational Button Architecture
st.markdown('<div class="action-buttons-wrapper">', unsafe_allow_html=True)

if is_completed:
    col_gen, col_reset = st.columns([3, 1])
    with col_gen:
        st.markdown('<div class="generate-btn-container">', unsafe_allow_html=True)
        st.button("🔮   Generate New eBook", use_container_width=True, disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_reset:
        st.markdown('<div class="reset-btn-container">', unsafe_allow_html=True)
        st.button("✨   Start New Project", use_container_width=True, on_click=handle_new_project_reset)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="generate-btn-container">', unsafe_allow_html=True)
    run_btn = st.button("🔮   Generate eBook from Source Asset", use_container_width=True, disabled=is_running)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Pipeline Loop Core ────────────────────────────────────────────────────────
if not is_completed and run_btn:
    if not media_url.strip():
        st.warning("Please enter a valid YouTube Playlist or Video URL first.")
    else:
        clear_previous_assets()
        st.session_state.current_step_idx = 0
        st.session_state.step_statuses = ["waiting"] * 5
        st.session_state.generated_pdf = None
        st.session_state.pipeline_phase = "processing"
        st.rerun()

if 0 <= st.session_state.current_step_idx < 5:
    current_idx = st.session_state.current_step_idx
    step_info = steps_config[current_idx]
    
    if st.session_state.step_statuses[current_idx] != "running":
        st.session_state.step_statuses[current_idx] = "running"
        st.rerun()
    
    with st.spinner(f"Processing Step {step_info['num']}: {step_info['title']}..."):
        custom_env = os.environ.copy()
        custom_env["PLAYLIST_URL"] = media_url
        
        result = subprocess.run(
            step_info["cmd"],
            shell=True,
            env=custom_env
        )
        
        if result.returncode == 0:
            st.session_state.step_statuses[current_idx] = "done"
            st.session_state.current_step_idx += 1
            st.rerun()
        else:
            # Fatal Step Breakdown Protection: Clears all following steps on error
            st.session_state.step_statuses = ["waiting"] * 5
            st.session_state.current_step_idx = -1
            st.session_state.pipeline_phase = "idle"
            st.error(f"Execution critically failed at Step {step_info['num']}: {step_info['title']}. Subsequent steps halted.")

if st.session_state.current_step_idx == 5:
    st.session_state.current_step_idx = -1
    st.session_state.pipeline_phase = "completed"
    
    target_pdfs = glob.glob("*.pdf") + glob.glob("output/*.pdf")
    if target_pdfs:
        st.session_state.generated_pdf = target_pdfs[0]
    st.rerun()

# ── Preview & Download Actions ────────────────────────────────────────────────
if st.session_state.generated_pdf and os.path.exists(st.session_state.generated_pdf):
    st.markdown('<div class="section-heading">Generated eBook Asset</div>', unsafe_allow_html=True)
    
    with open(st.session_state.generated_pdf, "rb") as f:
        pdf_bytes = f.read()
        
    col_actions, _ = st.columns([1, 2])
    with col_actions:
        st.download_button(
            label="⬇️   Download Completed eBook (PDF)",
            data=pdf_bytes,
            file_name=os.path.basename(st.session_state.generated_pdf),
            mime="application/pdf",
            use_container_width=True
        )
        
    st.markdown("""<div class="result-panel"><div class="panel-label">Live Preview</div>""", unsafe_allow_html=True)
    
    # Render PDF within custom frame using Base64
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800rem" style="border:1px solid rgba(168,85,247,0.2); border-radius:10px;"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""<div class="notice">Tube2Book · Modular Python Automation Engine</div>""", unsafe_allow_html=True)
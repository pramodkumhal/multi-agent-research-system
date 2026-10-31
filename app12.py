import time
import html

import streamlit as st

from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain, revision_chain

# Page configuration
st.set_page_config(
    page_title="MindForge · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --primary: #2457d6;
    --primary-strong: #1d4ed8;
    --accent-teal: #0f766e;
    --accent-green: #2f855a;
    --accent-orange: #d97706;
    --bg: #f5f7fb;
    --surface: #ffffff;
    --surface-alt: #eef3f9;
    --text: #1f2937;
    --muted: #5f6b7a;
    --border: #d8e0ea;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
    color-scheme: light; /* stops the browser painting form text white via prefers-color-scheme */
}

.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(36,87,214,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(15,118,110,0.08) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

.hero {
    text-align: center;
    min-height: 52vh;
    padding: 3.5rem 0 2.5rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--primary);
    margin-bottom: 1rem;
    opacity: 0.9;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: var(--text);
    margin: 0 0 3rem;
}
.hero h1 span { color: var(--primary); }
.hero-sub {
    font-weight: 300;
    color: var(--muted);
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
}
.hero-metrics {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-top: 1.5rem;
}
.hero-metrics span {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    border: 1px solid var(--border);
    background: rgba(255,255,255,0.9);
    padding: 0.45rem 0.75rem;
    border-radius: 999px;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(36,87,214,0.28), transparent);
    margin: 2rem 0;
}

.input-card {
    background: rgba(255,255,255,0.95);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    margin-left: auto;
    margin-right: auto;
    backdrop-filter: blur(8px);
}

.center-shell { max-width: 840px; margin: 0 auto; }

.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    caret-color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
/* data-testid selector as a fallback, more stable across Streamlit versions */
div[data-testid="stTextInput"] input {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    caret-color: var(--text) !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: var(--muted) !important;
    -webkit-text-fill-color: var(--muted) !important;
    opacity: 1 !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(36,87,214,0.12) !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--primary) !important;
    font-weight: 500 !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--accent-teal) 100%) !important;
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    box-shadow: 0 4px 20px rgba(36,87,214,0.22) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(36,87,214,0.28) !important;
    opacity: 0.95 !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.step-card {
    background: rgba(255,255,255,0.95);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 0.6rem 0.6rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.step-card.active { border-color: rgba(36,87,214,0.35); background: rgba(36,87,214,0.05); }
.step-card.done    { border-color: rgba(47,133,90,0.28); background: rgba(47,133,90,0.05); }
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 14px 0 0 14px;
    background: var(--border);
    transition: background 0.3s;
}
.step-card.active::before { background: var(--primary); }
.step-card.done::before   { background: var(--accent-green); }
.step-card.error::before  { background: #dc2626; }

.step-header { display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.3rem; }
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    color: var(--primary);
    opacity: 0.7;
}
.step-title { font-family: 'Syne', sans-serif; font-size: 0.95rem; font-weight: 700; color: var(--text); }
.step-status { margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.68rem; letter-spacing: 0.1em; }
.status-waiting { color: var(--muted); }
.status-running { color: var(--accent-orange); }
.status-done    { color: var(--accent-green); }
.status-error   { color: #dc2626; }

.result-panel {
    background: rgba(255,255,255,0.96);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
    color: var(--text);
}
.result-panel h1, .result-panel h2, .result-panel h3, .result-panel h4, .result-panel h5,
.result-panel h6, .result-panel p, .result-panel li, .result-panel a,
.result-panel strong, .result-panel em { color: var(--text) !important; }
.result-panel-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--primary);
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(36,87,214,0.15);
}
.result-content {
    font-size: 0.92rem;
    line-height: 1.8;
    color: var(--text);
    white-space: pre-wrap;
    font-family: 'DM Sans', sans-serif;
}

.report-panel {
    background: rgba(255,255,255,0.98);
    border: 1px solid rgba(36,87,214,0.18);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
    color: #1f2937 !important;
}
.report-panel, .report-panel * { color: #1f2937 !important; }

.feedback-panel {
    background: rgba(255,255,255,0.98);
    border: 1px solid rgba(15,118,110,0.18);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
    color: #1f2937 !important;
}
.feedback-panel, .feedback-panel * { color: #1f2937 !important; }

.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
}
.panel-label.orange { color: var(--primary); border-bottom: 1px solid rgba(36,87,214,0.15); }
.panel-label.green  { color: var(--accent-green); border-bottom: 1px solid rgba(47,133,90,0.15); }

.stSpinner > div { color: var(--primary) !important; }

details summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    color: var(--muted) !important;
    letter-spacing: 0.1em !important;
    cursor: pointer;
}

.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text);
    margin: 2rem 0 1rem;
}

.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.08em;
}

h1, h2, h3, h4, h5, h6 { color: var(--text) !important; }

/* st.container(key="...") renders a real DOM wrapper (div.st-key-<key>) that
   actually nests its children — unlike opening/closing a raw <div> across
   separate st.markdown() calls, which does NOT nest content from other
   elements (each st element renders into its own isolated node, so the
   browser auto-closes the dangling <div> and the styling below never
   reached the report text before). */
.st-key-draft_panel, .st-key-final_panel {
    background: rgba(255,255,255,0.98) !important;
    border: 1px solid rgba(36,87,214,0.18) !important;
    border-radius: 16px !important;
    padding: 1.6rem 2rem !important;
    margin-top: 1rem !important;
}
.st-key-draft_panel *, .st-key-final_panel *,
.st-key-draft_panel p, .st-key-final_panel p,
.st-key-draft_panel li, .st-key-final_panel li,
.st-key-draft_panel h1, .st-key-draft_panel h2, .st-key-draft_panel h3,
.st-key-final_panel h1, .st-key-final_panel h2, .st-key-final_panel h3,
.st-key-draft_panel strong, .st-key-final_panel strong {
    color: #1f2937 !important;
}
</style>
""", unsafe_allow_html=True)


STEPS_ORDER = ["search", "reader", "writer", "critic", "revision"]


def to_text(value) -> str:
    """Normalize agent/chain output into a plain string.

    Newer LangChain/Anthropic message `.content` is not guaranteed to be a
    str — it can be a list of content blocks like [{"type": "text",
    "text": "..."}], which is what crashed html.escape() with
    'list object has no attribute replace'. Everything gets flattened here,
    once, right when it's captured, so nothing downstream has to think
    about the shape again.
    """
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(str(item.get("text") or item.get("content") or item))
            else:
                parts.append(str(item))
        return "\n".join(p for p in parts if p)
    return str(value)


def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
        "error":   ("✗ ERROR",  "status-error"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done", "error": "error"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>" + desc + "</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# Session state initialization
_DEFAULTS = {
    "results": {},
    "running": False,
    "done": False,
    "current_step": "",
    "start_time": None,
    "error_step": None,
    "saved_topic": "",
}
for key, default in _DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default


# Hero section
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi Agent Research System</div>
    <h1>Mind<span>Forge</span></h1>
    <p class="hero-sub">
        Specialized Multi agents collaborate to search, scrape, write, critique,
        and revise a polished research report on any topic.
    </p>
    <div class="hero-metrics">
        <span>Search</span>
        <span>Reader</span>
        <span>Writer</span>
        <span>Critic</span>
        <span>Revision</span>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# Layout: centered input and pipeline
st.markdown('<div class="center-shell">', unsafe_allow_html=True)
st.markdown('<div class="input-card">', unsafe_allow_html=True)


def reset_state():
    """Callback to reset all session state — runs before widgets are instantiated."""
    for key, default in _DEFAULTS.items():
        st.session_state[key] = default
    st.session_state.topic_input = ""


col1, col2 = st.columns([3.6, 1])
with col1:
    topic = st.text_input(
        "Research Topic",
        placeholder="Artificial General Intelligence in 2026",
        key="topic_input",
        label_visibility="visible",
        disabled=st.session_state.running,
    )
with col2:
    col_run, col_reset = st.columns(2)
    with col_run:
        run_btn = st.button("⚡  Run", use_container_width=True,
                             disabled=st.session_state.running or not topic.strip())
    with col_reset:
        st.button("↻ Reset", use_container_width=True, on_click=reset_state)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

pipeline_placeholder = st.empty()


def get_step_status(step: str) -> str:
    """Status of a single pipeline step. Simpler & O(1) vs the old O(n^2) scan."""
    r = st.session_state.results
    if step in r or (step == "revision" and "final_report" in r):
        return "done"
    if st.session_state.error_step == step:
        return "error"
    if st.session_state.current_step == step:
        return "running"
    return "waiting"


def render_pipeline():
    elapsed = ""
    if st.session_state.running and st.session_state.start_time:
        elapsed = f" ({int(time.time() - st.session_state.start_time)}s)"

    with pipeline_placeholder.container():
        step_card("01", "Search Agent", get_step_status("search"), "Gathers recent web information")
        step_card("02", "Reader Agent", get_step_status("reader"), "Scrapes & extracts deep content")
        step_card("03", "Writer Chain", get_step_status("writer"), "Drafts the full research report")
        step_card("04", "Critic Chain", get_step_status("critic"), "Reviews & scores the report")
        step_card("05", "Revision Chain", get_step_status("revision"),
                   "Refines the report using critique" + elapsed)


render_pipeline()
st.markdown('</div>', unsafe_allow_html=True)


# Run pipeline
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.session_state.start_time = time.time()
        st.session_state.saved_topic = topic
        st.session_state.error_step = None
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = st.session_state.results
    topic_val = st.session_state.saved_topic

    next_step = next((s for s in STEPS_ORDER if s not in results), None)

    if next_step:
        st.session_state.current_step = next_step
        render_pipeline()

        try:
            if next_step == "search":
                with st.spinner("🔍  Search Agent is working…"):
                    search_agent = build_search_agent()
                    sr = search_agent.invoke({
                        "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
                    })
                    results["search"] = to_text(sr["messages"][-1].content)

            elif next_step == "reader":
                with st.spinner("📄  Reader Agent is scraping top resources…"):
                    reader_agent = build_reader_agent()
                    rr = reader_agent.invoke({
                        "messages": [("user",
                            f"Based on the following search results about '{topic_val}', "
                            f"pick the most relevant URL and scrape it for deeper content.\n\n"
                            f"Search Results:\n{results['search'][:800]}"
                        )]
                    })
                    results["reader"] = to_text(rr["messages"][-1].content)

            elif next_step == "writer":
                with st.spinner("✍️  Writer is drafting the report…"):
                    research_combined = (
                        f"SEARCH RESULTS:\n{results['search']}\n\n"
                        f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
                    )
                    results["writer"] = to_text(writer_chain.invoke({
                        "topic": topic_val,
                        "research": research_combined
                    }))

            elif next_step == "critic":
                with st.spinner("🧐  Critic is reviewing the report…"):
                    results["critic"] = to_text(critic_chain.invoke({"report": results["writer"]}))

            elif next_step == "revision":
                with st.spinner("🛠️  Revision Chain is polishing the report…"):
                    results["revision"] = to_text(revision_chain.invoke({
                        "report": results["writer"],
                        "feedback": results["critic"]
                    }))

            st.session_state.results = results
            st.session_state.current_step = ""
            st.rerun()

        except Exception as e:
            st.session_state.error_step = next_step
            st.session_state.current_step = ""
            render_pipeline()
            st.error(f"❌ Error in {next_step} step: {str(e)}")
            st.session_state.running = False
    else:
        st.session_state.running = False
        st.session_state.done = True
        st.rerun()


# Results display
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{html.escape(to_text(r["search"]))}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{html.escape(to_text(r["reader"]))}</div></div>', unsafe_allow_html=True)

    if "writer" in r and ("revision" not in r and "final_report" not in r):
        with st.container(key="draft_panel"):
            st.markdown('<div class="panel-label orange">📝 Draft Research Report</div>', unsafe_allow_html=True)
            st.write(r["writer"])

    if "revision" in r or "final_report" in r:
        final_content = to_text(r.get("revision") or r.get("final_report"))
        with st.container(key="final_panel"):
            st.markdown('<div class="panel-label orange">Final Report</div>', unsafe_allow_html=True)
            st.write(final_content)


# Footer
st.markdown("""
<div class="notice">
    MindForge · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & ENHANCED UI STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Operation Civilian Re-Entry | MVS 100",
    page_icon="🎖",
    layout="wide",
)

st.markdown(
    """
<style>
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        color: #38BDF8;
        margin-bottom: 4px;
        letter-spacing: -0.02em;
    }
    .sub-header {
        font-size: 1.15rem;
        color: #94A3B8;
        margin-bottom: 24px;
    }
    /* Fixed height flexbox cards to align buttons evenly */
    .choice-card-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        height: 280px; /* Uniform height for alignment */
        box-sizing: border-box;
    }
    .card-box {
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .card-green {
        background-color: #064E3B;
        border: 1px solid #059669;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        color: #ECFDF5;
    }
    .card-yellow {
        background-color: #78350F;
        border: 1px solid #D97706;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        color: #FEF3C7;
    }
    .card-red {
        background-color: #7F1D1D;
        border: 1px solid #DC2626;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        color: #FEF2F2;
    }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# CHARACTER DEFINITIONS & 4-METRIC TRACKING
# -----------------------------------------------------------------------------
CHARACTERS = {
    "ALEX": {
        "name": "Alex Vance",
        "rank": "Master Sergeant",
        "service": "Active Duty — Infantry / Operations Specialist",
        "background": (
            "Married with children; spouse managed domestic operations and"
            " household decisions through multiple long combat deployments."
        ),
        "challenge": (
            "Translating direct leadership into consensus-driven corporate"
            " culture; renegotiating household authority and overcoming"
            " military cultural stoicism."
        ),
        "stats": {"CT": 45, "SR": 40, "CE": 40, "SI": 50},
    },
    "MORGAN": {
        "name": "Morgan Ellis",
        "rank": "Captain",
        "service": "Active Duty — Logistics & Supply Chain Officer",
        "background": (
            "Dual-career household (no children); partner holds a demanding"
            " corporate leadership position in a major city."
        ),
        "challenge": (
            "Re-aligning executive expectations (managing large military"
            " operational budgets vs. corporate office politics);"
            " balancing partner's career priorities with transition friction."
        ),
        "stats": {"CT": 60, "SR": 45, "CE": 35, "SI": 45},
    },
}

# Initialize Session State
if "state" not in st.session_state:
    st.session_state.state = "CHAR_SELECT"
if "char_key" not in st.session_state:
    st.session_state.char_key = None
if "path" not in st.session_state:
    st.session_state.path = []
if "stats" not in st.session_state:
    st.session_state.stats = {"CT": 50, "SR": 50, "CE": 50, "SI": 50}
if "choice_history" not in st.session_state:
    st.session_state.choice_history = []
if "current_node" not in st.session_state:
    st.session_state.current_node = "START"


def apply_choice(
    ct_change,
    sr_change,
    ce_change,
    si_change,
    next_node,
    choice_id,
    choice_summary,
    feedback_text,
    eval_type,
):
    st.session_state.stats["CT"] = max(
        0, min(100, st.session_state.stats["CT"] + ct_change)
    )
    st.session_state.stats["SR"] = max(
        0, min(100, st.session_state.stats["SR"] + sr_change)
    )
    st.session_state.stats["CE"] = max(
        0, min(100, st.session_state.stats["CE"] + ce_change)
    )
    st.session_state.stats["SI"] = max(
        0, min(100, st.session_state.stats["SI"] + si_change)
    )

    st.session_state.choice_history.append(
        {
            "node": st.session_state.current_node,
            "choice_id": choice_id,
            "summary": choice_summary,
            "feedback": feedback_text,
            "eval_type": eval_type,
        }
    )
    st.session_state.current_node = next_node
    st.rerun()


# -----------------------------------------------------------------------------
# MAIN APP FLOW
# -----------------------------------------------------------------------------
st.markdown(
    '<div class="main-header">Operation Civilian Re-Entry</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">MVS 100: Military Transition & Human Systems'
    " Simulation</div>",
    unsafe_allow_html=True,
)

if st.session_state.state == "CHAR_SELECT":
    st.markdown("### Select Your Transition Profile")
    st.write(
        "Choose a profile to begin your transition journey. Each candidate"
        " presents unique leadership, household, and career dynamics."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
        <div class="card-box">
            <h3>{CHARACTERS['ALEX']['name']}</h3>
            <p><b>Rank:</b> {CHARACTERS['ALEX']['rank']}</p>
            <p><b>Service:</b> {CHARACTERS['ALEX']['service']}</p>
            <p><b>Background:</b> {CHARACTERS['ALEX']['background']}</p>
            <p><b>Challenge:</b> {CHARACTERS['ALEX']['challenge']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("Select Alex Vance", use_container_width=True):
            st.session_state.char_key = "ALEX"
            st.session_state.stats = CHARACTERS["ALEX"]["stats"].copy()
            st.session_state.state = "SIMULATION"
            st.rerun()

    with col2:
        st.markdown(
            f"""
        <div class="card-box">
            <h3>{CHARACTERS['MORGAN']['name']}</h3>
            <p><b>Rank:</b> {CHARACTERS['MORGAN']['rank']}</p>
            <p><b>Service:</b> {CHARACTERS['MORGAN']['service']}</p>
            <p><b>Background:</b> {CHARACTERS['MORGAN']['background']}</p>
            <p><b>Challenge:</b> {CHARACTERS['MORGAN']['challenge']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("Select Morgan Ellis", use_container_width=True):
            st.session_state.char_key = "MORGAN"
            st.session_state.stats = CHARACTERS["MORGAN"]["stats"].copy()
            st.session_state.state = "SIMULATION"
            st.rerun()

elif st.session_state.state == "SIMULATION":
    # Sidebar for stats
    st.sidebar.markdown("### Status Metrics")
    stats = st.session_state.stats
    st.sidebar.metric("Career Translation (CT)", f"{stats['CT']}%")
    st.sidebar.metric("Social/Relational (SR)", f"{stats['SR']}%")
    st.sidebar.metric("Cultural Equity (CE)", f"{stats['CE']}%")
    st.sidebar.metric("Self-Identity (SI)", f"{stats['SI']}%")

    if st.sidebar.button("Restart Simulation"):
        st.session_state.state = "CHAR_SELECT"
        st.session_state.current_node = "START"
        st.session_state.choice_history = []
        st.rerun()

    # Simple placeholder loop for node handling
    st.markdown(f"**Current Simulation Node:** `{st.session_state.current_node}`")
    st.write(
        "Simulation engine active. Choices are now presented neutrally without"
        " giveaway headers."
    )
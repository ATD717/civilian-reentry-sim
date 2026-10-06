import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & ENHANCED UI STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Operation Civilian Re-Entry | MVS 100",
    page_icon="🎖️",
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
    st.session_state.path.append(choice_id)
    st.session_state.choice_history.append(
        {
            "node": next_node,
            "choice_id": choice_id,
            "summary": choice_summary,
            "feedback": feedback_text,
            "eval_type": eval_type,  # "green", "yellow", or "red"
            "deltas": {
                "CT": ct_change,
                "SR": sr_change,
                "CE": ce_change,
                "SI": si_change,
            },
        }
    )
    st.session_state.state = next_node
    st.rerun()


# -----------------------------------------------------------------------------
# SIDEBAR DASHBOARD WITH VISUAL BAR CHART
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🎖 MVS 100 Project")
    st.markdown("**Author:** Austin Dodd")
    st.markdown("**Course:** MVS 100: Introduction to Military Studies")
    st.divider()

    if st.session_state.char_key and st.session_state.char_key in CHARACTERS:
        char = CHARACTERS[st.session_state.char_key]
        st.markdown(f"### 📋 Dossier: {char['name']}")
        st.write(f"**Rank:** {char['rank']}")
        st.write(f"**Service:** {char['service']}")
        st.divider()

        st.markdown("### 📊 4-Domain Metrics")
        stats = st.session_state.stats

        st.write(f"**Career Translation (CT):** {stats['CT']}%")
        st.progress(stats["CT"])

        st.write(f"**Social & Rel. (SR):** {stats['SR']}%")
        st.progress(stats["SR"])

        st.write(f"**Community Eng. (CE):** {stats['CE']}%")
        st.progress(stats["CE"])

        st.write(f"**Self-Identity (SI):** {stats['SI']}%")
        st.progress(stats["SI"])

        st.divider()

    if st.button("🔄 Reset Simulation", use_container_width=True):
        st.session_state.state = "CHAR_SELECT"
        st.session_state.char_key = None
        st.session_state.path = []
        st.session_state.stats = {"CT": 50, "SR": 50, "CE": 50, "SI":
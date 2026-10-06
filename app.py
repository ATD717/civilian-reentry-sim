import pandas as pd
import streamlit as st

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
    .choice-card-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        height: 290px;
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
        "rank": "Gunnery Sergeant",
        "service": "Active Duty — Criminal Investigator",
        "background": (
            "Married with children; spouse managed domestic operations and"
            " household decisions through active-duty service."
        ),
        "challenge": (
            "Translating direct leadership into civilian environments;"
            " renegotiating household authority and managing institutional"
            " transition."
        ),
        "stats": {"CT": 45, "SR": 40, "CE": 40, "SI": 50},
    },
    "MORGAN": {
        "name": "Morgan Ellis",
        "rank": "Captain",
        "service": "Active Duty — Logistics & Supply Chain Officer",
        "background": (
            "Dual-career household (no children); partner holds a demanding"
            " corporate leadership position."
        ),
        "challenge": (
            "Re-aligning executive expectations (managing military"
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
            "node": st.session_state.state,
            "choice_id": choice_id,
            "summary": choice_summary,
            "feedback": feedback_text,
            "eval_type": eval_type,
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
# SIDEBAR DASHBOARD
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
        st.session_state.stats = {"CT": 50, "SR": 50, "CE": 50, "SI": 50}
        st.session_state.choice_history = []
        st.rerun()


def get_current_char():
    key = st.session_state.get("char_key")
    if key in CHARACTERS:
        return CHARACTERS[key]
    return CHARACTERS["ALEX"]


# =============================================================================
# SCREEN 1: CHARACTER SELECTION & FRAMEWORK
# =============================================================================
if st.session_state.state == "CHAR_SELECT":
    st.markdown(
        "<div class='main-header'>OPERATION CIVILIAN RE-ENTRY</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='sub-header'>An Interactive 24-Month Reintegration"
        " Simulation & Research Model</div>",
        unsafe_allow_html=True,
    )

    with st.expander(
        "📖 View Research Question, Thesis & Academic Framework", expanded=True
    ):
        st.markdown("""
* **Research Question:** *"How do the operational, cultural, and psychological experiences of military service shape a veteran's post-service reintegration across their employment, social relationships, community engagement, and self-identity?"*
* **Thesis Statement:** *"The military-to-civilian transition cannot be accurately modeled as a single administrative event or linear job-placement milestone; rather, it is a prolonged, 24-month existential and cultural reorganization where pre-service identity, institutional friction with American bureaucratic systems (DOD/VA), and domestic role renegotiation dictate long-term post-service stability."*
* **Core Framework:** Synthesizing Schuetz's (1945) Homecoming theory, Zoli et al. (2015) institutional friction, and Mobbs & Bonanno (2018) transition stress.
        """)

    st.divider()
    st.subheader("Select a Service Member Dossier")
    cols = st.columns(2)

    for idx, (key, char) in enumerate(CHARACTERS.items()):
        with cols[idx]:
            st.markdown(
                f"<div class='card-box'>"
                f"<h3>{char['name']}</h3>"
                f"<p><b>{char['rank']}</b> — <i>{char['service']}</i></p>"
                f"<p><b>Background:</b> {char['background']}</p>"
                f"<p><b>Key Challenge:</b> {char['challenge']}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

            if st.button(
                f"Select {char['name'].split()[0]}",
                key=f"sel_{key}",
                use_container_width=True,
                type="primary",
            ):
                st.session_state.char_key = key
                st.session_state.stats = char["stats"].copy()
                st.session_state.choice_history = []
                st.session_state.state = "NODE_1"
                st.rerun()


# =============================================================================
# NODE 1: MONTH 2 — SELF-IDENTITY & UNIFORM SEPARATION
# =============================================================================
elif st.session_state.state == "NODE_1":
    char = get_current_char()
    st.progress(
        16, text="Node 1 of 6: Month 2 — Self-Identity & Uniform Separation"
    )

    st.warning(
        "**🔬 Academic Citation & Research Analysis**\n\n"
        "*Source: Smith & True (2014) — Warring Identities*\n\n"
        "Transitioning out of a total military institution triggers an acute"
        " existential shock. As Alfred Schuetz (1945) observed in 'The"
        " Homecomer,' the returning service member expects home to remain"
        " static, while discovering both the home environment and their own"
        " internal identity have fundamentally shifted. Stripping the uniform"
        " removes immediate institutional validation."
    )

    st.markdown(
        f"### Month 2: The Initial Drop — {char['name']} ({char['rank']})"
    )
    st.write(
        "The retirement ceremony is two months behind you. The DD-214 is framed,"
        " but the physical absence of the uniform and chain of command creates"
        " an immediate vacuum. You experience alienation when engaging with"
        " local civilian systems and peers."
    )

    st.markdown("#### Choose Your Initial Reintegration Strategy:")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """<div class='choice-card-container'><div>
            <h4>Choice A</h4>
            <p>Immediately jump into high-intensity corporate interviews, translating military leadership into executive buzzwords without processing identity loss.</p></div>""",
            unsafe_allow_html=True,
        )
        if st.button(
            "Execute Choice A", key="n1_a", use_container_width=True
        ):
            apply_choice(
                15,
                -10,
                -5,
                -15,
                "NODE_2",
                "N1_A",
                "Choice A",
                "Secured quick interviews, but suppressing identity shift"
                " caused severe burnout and family friction.",
                "yellow",
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            """<div class='choice-card-container'><div>
            <h4>Choice B</h4>
            <p>Take 90 days of complete pause from job hunting. Focus on family reconnection and mapping personal values before entering the civilian labor market.</p></div>""",
            unsafe_allow_html=True,
        )
        if st.button(
            "Execute Choice B", key="n1_b", use_container_width=True
        ):
            apply_choice(
                -5,
                20,
                10,
                20,
                "NODE_2",
                "N1_B",
                "Choice B",
                "Financial reserves dipped, but establishing a strong"
                " domestic foundation preserved relationships and identity.",
                "green",
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown(
            """<div class='choice-card-container'><div>
            <h4>Choice C</h4>
            <p>Withdraw from social contact and attempt to independently navigate VA healthcare and credential translation to prove you don't need assistance.</p></div>""",
            unsafe_allow_html=True,
        )
        if st.button(
            "Execute Choice C", key="n1_c", use_container_width=True
        ):
            apply_choice(
                -15,
                -20,
                -15,
                -25,
                "NODE_2",
                "N1_C",
                "Choice C",
                "Rugged individualism backfired against bureaucratic VA"
                " roadblocks, isolating you from your support network.",
                "red",
            )
        st.markdown("</div>", unsafe_allow_html=True)


# =============================================================================
# NODE 2: MONTH 6 — INSTITUTIONAL FRICTION & EMPLOYMENT
# =============================================================================
elif st.session_state.state == "NODE
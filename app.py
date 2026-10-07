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
        "service": "Active Duty — Criminal Investigator / Infantry",
        "background": (
            "Married with children; spouse managed domestic operations and"
            " household decisions through multiple demanding operational cycles."
        ),
        "challenge": (
            "Translating direct leadership into civilian consensus-driven"
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
        st.session_state.stats = {"CT": 50, "SR": 50, "CE": 50, "SI": 50}
        st.session_state.choice_history = []
        st.rerun()


def get_current_char():
    key = st.session_state.get("char_key")
    if key in CHARACTERS:
        return CHARACTERS[key]
    return CHARACTERS["ALEX"]


# -----------------------------------------------------------------------------
# SCREEN 1: CHARACTER SELECTION & ACADEMIC FRAMEWORK
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# NODE 1: MONTH 2 — SELF-IDENTITY & UNIFORM SEPARATION (Correct Answer: Option C)
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_1":
    char = get_current_char()
    st.progress(
        14, text="Node 1 of 7: Month 2 — Self-Identity & Uniform Separation"
    )

    st.warning(
        "**🔬 Academic Citation & Research Analysis**\n\n"
        "*Source: Smith & True (2014) — Warring Identities*\n\n"
        "Transitioning out of a total military institution triggers"
        " psychological friction between martial self-concept and civilian"
        " individualism. Reconstructing a stable post-identity requires"
        " confronting the immediate loss of rank, title, and mission."
    )

    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.header(f"Month 2: Stripping the Uniform — {char['name']}")
    with h_col2:
        if st.button("⬅ Back to Dossiers"):
            st.session_state.state = "CHAR_SELECT"
            st.rerun()

    st.info(
        "You have been out of uniform for two months. Stripped of your rank"
        " insignia and daily operational structure, you find yourself answering"
        " civilian acquaintances with vague descriptions of your past service."
        " You feel an internal loss of purpose and professional validation."
    )

    st.subheader("How do you handle the initial loss of identity and structure?")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='card-box'><h3>Option A</h3>"
            "<p>Isolate yourself socially, relying solely on your own internal"
            " discipline to push through the transition without seeking"
            " external validation or veteran networks.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n1_a", use_container_width=True):
            apply_choice(
                0,
                -10,
                -10,
                -15,
                "NODE_2",
                "A",
                "Isolate yourself socially, relying solely on your own internal discipline to push through the transition without seeking external validation or veteran networks.",
                (
                    "**[HIGH RISK / RED]** Reflects withdrawal and suppressed"
                    " identity conflict. Smith & True (2014) identify isolation"
                    " as a primary driver of acute transition stress and"
                    " identity fragmentation."
                ),
                "red",
            )

    with c2:
        st.markdown(
            "<div class='card-box'><h3>Option B</h3>"
            "<p>Immerse yourself immediately in civilian recreational hobbies"
            " and casual entertainment to distract yourself from thinking about"
            " your military past.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n1_b", use_container_width=True):
            apply_choice(
                5,
                0,
                0,
                5,
                "NODE_2",
                "B",
                "Immerse yourself immediately in civilian recreational hobbies and casual entertainment to distract yourself from thinking about your military past.",
                (
                    "**[CAUTION / YELLOW]** Temporary avoidance provides"
                    " short-term relief but delays confronting deep-seated"
                    " identity reorganization, leaving root transition friction"
                    " unaddressed."
                ),
                "yellow",
            )

    with c3:
        st.markdown(
            "<div class='card-box'><h3>Option C</h3>"
            "<p>Connect proactively with a local veteran mentorship group to"
            " openly discuss the psychological shift of leaving service and"
            " redefine your personal core values.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n1_c", use_container_width=True):
            apply_choice(
                5,
                10,
                15,
                20,
                "NODE_2",
                "C",
                "Connect proactively with a local veteran mentorship group to openly discuss the psychological shift of leaving service and redefine your personal core values.",
                (
                    "**[BEST PRACTICE / GREEN]** Aligns with Smith & True (2014)"
                    " and Demers (2011). Proactive peer engagement successfully"
                    " bridges the gap between military and civilian identity"
                    " markers."
                ),
                "green",
            )

# -----------------------------------------------------------------------------
# NODE 2: MONTH 4 — SOCIAL RELATIONSHIPS & HOUSEHOLD ROLE RENEGOTIATION (Correct Answer: Option A)
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_2":
    char = get_current_char()
    st.progress(
        28, text="Node 2 of 7: Month 4 — Household Role Renegotiation"
    )

    st.warning(
        "**🔬 Academic Citation & Research Analysis**\n\n"
        "*Source: Schuetz (1945) / Demers (2011)*\n\n"
        "Schuetz's Homecoming theory demonstrates that home is not a static"
        " haven. Spouses and partners have adapted to manage household"
        " operations independently during deployments, requiring active"
        " relational role renegotiation."
    )

    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.header(f"Month 4: Domestic Boundaries & Expectations — {char['name']}")
    with h_col2:
        if st.button("⬅ Back to Dossiers", key="b_n2"):
            st.session_state.state = "CHAR_SELECT"
            st.rerun()

    st.info(
        "Four months post-discharge, friction arises over household routines."
        " Your partner notes that you are attempting to manage domestic life"
        " like a military unit rather than an equal partnership."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='card-box'><h3>Option A</h3>"
            "<p>Initiate a structured weekly household check-in where both you"
            " and your partner explicitly map out responsibilities, financial"
            " goals, and personal expectations.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n2_a", use_container_width=True):
            apply_choice(
                0,
                20,
                5,
                10,
                "NODE_3",
                "A",
                "Initiate a structured weekly household check-in where both you and your partner explicitly map out responsibilities, financial goals, and personal expectations.",
                (
                    "**[BEST PRACTICE / GREEN]** Directly addresses Schuetz's"
                    " (1945) homecoming friction by replacing military command"
                    " hierarchy with intentional, collaborative role"
                    " renegotiation."
                ),
                "green",
            )

    with c2:
        st.markdown(
            "<div class='card-box'><h3>Option B</h3>"
            "<p>Step back from domestic choices entirely, leaving all decisions"
            " to your partner while focusing strictly on personal job"
            " applications.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n2_b", use_container_width=True):
            apply_choice(
                5,
                -15,
                0,
                -5,
                "NODE_3",
                "B",
                "Step back from domestic choices entirely, leaving all decisions to your partner while focusing strictly on personal job applications.",
                (
                    "**[HIGH RISK / RED]** Abdicating domestic"
                    " responsibility creates emotional detachment and fails to"
                    " establish an equal partnership, violating Demers's (2011)"
                    " findings on domestic cohesion."
                ),
                "red",
            )

    with c3:
        st.markdown(
            "<div class='card-box'><h3>Option C</h3>"
            "<p>Keep your internal stress private and avoid discussing"
            " household roles further, believing time will naturally smooth"
            " out the tension.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n2_c", use_container_width=True):
            apply_choice(
                0,
                -20,
                -5,
                -10,
                "NODE_3",
                "C",
                "Keep your internal stress private and avoid discussing household roles further, believing time will naturally smooth out the tension.",
                (
                    "**[HIGH RISK / RED]** Suppressing stress compounds"
                    " domestic alienation. Romaniuk et al. (2020) highlight"
                    " unaddressed communication gaps as a major predictor of"
                    " post-service strain."
                ),
                "red",
            )

# -----------------------------------------------------------------------------
# NODE 3: MONTH 6 — FINANCIAL BUDGETING & VA BENEFITS TRANSITION (Restored Question 1)
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_3":
    char = get_current_char()
    st.progress(
        42, text="Node 3 of 7: Month 6 — Financial & Benefits Budgeting"
    )

    st.warning(
        "**🔬 Academic Citation & Research Analysis**\n\n"
        "*Source: Mobbs & Bonanno (2018) / Zoli et al. (2015)*\n\n"
        "Financial anxiety is one of the leading triggers of early transition"
        " friction. Navigating GI Bill stipends, terminal leave payouts, and"
        " adjusting to civilian cash flow cycles requires proactive financial"
        " planning rather than reactive spending."
    )

    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.header(f"Month 6: The Cash Flow Gap — {char['name']}")
    with h_col2:
        if st.button("⬅ Back to Dossiers", key="b_n3"):
            st.session_state.state = "CHAR_SELECT"
            st.rerun()

    st.info(
        "Six months post-separation, terminal leave payouts have cleared, but"
        " your first standard civilian payroll cycle leaves a 3-week gap."
        " Household expenses are tight, and credit card balances are starting"
        " to creep up."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='card-box'><h3>Option A</h3>"
            "<p>Rely on high-interest revolving credit lines to maintain your"
            " family's current lifestyle while waiting for the next pay"
            " cycle.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n3_a", use_container_width=True):
            apply_choice(
                -10,
                -10,
                0,
                -5,
                "NODE_4",
                "A",
                "Rely on high-interest revolving credit lines to maintain your family's current lifestyle while waiting for the next pay cycle.",
                (
                    "**[HIGH RISK / RED]** Exacerbates financial strain and"
                    " creates long-term debt burdens, directly compounding"
                    " transition stress (*Mobbs & Bonanno, 2018*)."
                ),
                "red",
            )

    with c2:
        st.markdown(
            "<div class='card-box'><h3>Option B</h3>"
            "<p>Build a strict 90-day zero-based cash flow budget with your"
            " spouse, cutting non-essential subscriptions and tapping emergency"
            " savings.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n3_b", use_container_width=True):
            apply_choice(
                15,
                15,
                5,
                10,
                "NODE_4",
                "B",
                "Build a strict 90-day zero-based cash flow budget with your spouse, cutting non-essential subscriptions and tapping emergency savings.",
                (
                    "**[BEST PRACTICE / GREEN]** Proactive financial management"
                    " mitigates early transition shock and establishes family"
                    " alignment around monetary goals (*Zoli et al., 2015*)."
                ),
                "green",
            )

    with c3:
        st.markdown(
            "<div class='card-box'><h3>Option C</h3>"
            "<p>Ignore the cash flow discrepancy and hope incoming paychecks"
            " naturally cover outstanding balances over time.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n3_c", use_container_width=True):
            apply_choice(
                -5,
                -5,
                0,
                -5,
                "NODE_4",
                "C",
                "Ignore the cash flow discrepancy and hope incoming paychecks naturally cover outstanding balances over time.",
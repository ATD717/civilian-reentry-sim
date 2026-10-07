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

# Robust Session State Initialization & Fallbacks
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


def get_current_char():
    key = st.session_state.get("char_key")
    if key and key in CHARACTERS:
        return CHARACTERS[key]
    return CHARACTERS["ALEX"]


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
    if "stats" not in st.session_state:
        st.session_state.stats = {"CT": 50, "SR": 50, "CE": 50, "SI": 50}

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

    if "path" not in st.session_state:
        st.session_state.path = []
    st.session_state.path.append(choice_id)

    if "choice_history" not in st.session_state:
        st.session_state.choice_history = []
    st.session_state.choice_history.append(
        {
            "node": next_node,
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
# SIDEBAR DASHBOARD WITH VISUAL BAR CHART
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🎖 MVS 100 Project")
    st.markdown("**Author:** Austin Dodd")
    st.markdown("**Course:** MVS 100: Introduction to Military Studies")
    st.divider()

    if st.session_state.get("char_key") and st.session_state.char_key in CHARACTERS:
        char = CHARACTERS[st.session_state.char_key]
        st.markdown(f"### 📋 Dossier: {char['name']}")
        st.write(f"**Rank:** {char['rank']}")
        st.write(f"**Service:** {char['service']}")
        st.divider()

        st.markdown("### 📊 4-Domain Metrics")
        stats = st.session_state.get(
            "stats", {"CT": 50, "SR": 50, "CE": 50, "SI": 50}
        )

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
- **Research Question:** *"How do the operational, cultural, and psychological experiences of military service shape a veteran's post-service reintegration across their employment, social relationships, community engagement, and self-identity?"*
- **Thesis Statement:** *"The military-to-civilian transition cannot be accurately modeled as a single administrative event or linear job-placement milestone; rather, it is a prolonged, 24-month existential and cultural reorganization where pre-service identity, institutional friction with American bureaucratic systems (DOD/VA), and domestic role renegotiation dictate long-term post-service stability."*
- **Core Framework:** Synthesizing Schuetz's (1945) Homecoming theory, Zoli et al. (2015) institutional friction, and Mobbs & Bonanno (2018) transition stress.
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
# NODE 1: MONTH 2 — SELF-IDENTITY & UNIFORM SEPARATION
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
# NODE 2: MONTH 4 — SOCIAL RELATIONSHIPS & HOUSEHOLD ROLE RENEGOTIATION
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
# NODE 3: MONTH 6 — FINANCIAL BUDGETING & VA BENEFITS TRANSITION
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
                (
                    "**[CAUTION / YELLOW]** Passive financial management leads"
                    " to preventable monetary friction and unnecessary family"
                    " anxiety."
                ),
                "yellow",
            )

# -----------------------------------------------------------------------------
# NODE 4: MONTH 9 — CAREER & WORKPLACE COMMUNICATION
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_4":
    char = get_current_char()
    st.progress(
        57, text="Node 4 of 7: Month 9 — Corporate Culture & Team Friction"
    )

    st.warning(
        "**🔬 Academic Citation & Research Analysis**\n\n"
        "*Source: Zoli, Maury, & Fay (2015)*\n\n"
        "Military operational culture relies on direct communication and SOPs."
        " In civilian corporate spaces, this often clashes with"
        " consensus-building and indirect office politics."
    )

    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.header(f"Month 9: The Project Deadlock — {char['name']}")
    with h_col2:
        if st.button("⬅ Back to Dossiers", key="b_n4"):
            st.session_state.state = "CHAR_SELECT"
            st.rerun()

    st.info(
        "Nine months into your civilian career, a major cross-functional"
        " project stalls because two department leads disagree on resource"
        " allocation. Your manager asks for your approach."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='card-box'><h3>Option A</h3>"
            "<p>Issue a formal project tracking matrix with rigid deadlines and"
            " public accountability check-ins for all department leads.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n4_a", use_container_width=True):
            apply_choice(
                -10,
                -5,
                0,
                5,
                "NODE_5",
                "A",
                "Issue a formal project tracking matrix with rigid deadlines and public accountability check-ins for all department leads.",
                (
                    "**[HIGH RISK / RED]** Illustrates institutional"
                    " mismatch (Zoli et al., 2015). Forcing top-down military"
                    " SOPs onto civilian peers creates cultural resistance and"
                    " damages workplace relationships."
                ),
                "red",
            )

    with c2:
        st.markdown(
            "<div class='card-box'><h3>Option B</h3>"
            "<p>Hold informal, one-on-one alignment discussions with each"
            " leader outside meetings to understand constraints and co-create"
            " a compromise.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n4_b", use_container_width=True):
            apply_choice(
                25,
                10,
                10,
                10,
                "NODE_5",
                "B",
                "Hold informal, one-on-one alignment discussions with each leader outside meetings to understand constraints and co-create a compromise.",
                (
                    "**[BEST PRACTICE / GREEN]** Demonstrates successful"
                    " translation of leadership skills into civilian corporate"
                    " currency by mastering consensus-building (*Zoli et al.,"
                    " 2015*)."
                ),
                "green",
            )

    with c3:
        st.markdown(
            "<div class='card-box'><h3>Option C</h3>"
            "<p>Focus strictly on your own deliverables, letting the project"
            " owner manage stakeholder friction without your direct"
            " intervention.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n4_c", use_container_width=True):
            apply_choice(
                -15,
                0,
                -5,
                -5,
                "NODE_5",
                "C",
                "Focus strictly on your own deliverables, letting the project owner manage stakeholder friction without your direct intervention.",
                (
                    "**[CAUTION / YELLOW]** Siloing stalls professional"
                    " growth and underutilizes valuable leadership capacity,"
                    " leading to underemployment friction."
                ),
                "yellow",
            )

# -----------------------------------------------------------------------------
# NODE 5: MONTH 12 — COMMUNITY ENGAGEMENT & CIVIC SERVICE
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_5":
    char = get_current_char()
    st.progress(
        71,
        text="Node 5 of 7: Month 12 — Community Embedding & Civic Service",
    )

    st.warning(
        "**🔬 Academic Citation & Research Analysis**\n\n"
        "*Source: Demers (2011) — Community Reintegration*\n\n"
        "Civilian community networks often lack cultural competency regarding"
        " military service, leading to isolation. Active civic engagement and"
        " local community embedding are critical for bridging this gap."
    )

    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.header(f"Month 12: Local Embedding — {char['name']}")
    with h_col2:
        if st.button("⬅ Back to Dossiers", key="b_n5"):
            st.session_state.state = "CHAR_SELECT"
            st.rerun()

    st.info(
        "One year post-discharge, you realize your life is split strictly"
        " between your workplace and your immediate household. You feel"
        " disconnected from your broader local town/city community."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='card-box'><h3>Option A</h3>"
            "<p>Volunteer to lead a local youth mentorship or community"
            " resilience program, translating your leadership skills into civic"
            " action.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n5_a", use_container_width=True):
            apply_choice(
                10,
                10,
                25,
                15,
                "NODE_6",
                "A",
                "Volunteer to lead a local youth mentorship or community resilience program, translating your leadership skills into civic action.",
                (
                    "**[BEST PRACTICE / GREEN]** Directly fulfills Demers's"
                    " (2011) recommendation for active civic embedding,"
                    " bridging the military-civilian cultural divide."
                ),
                "green",
            )

    with c2:
        st.markdown(
            "<div class='card-box'><h3>Option B</h3>"
            "<p>Join an exclusively veteran-focused social club online, keeping"
            " your local civic engagement minimal and staying within familiar"
            " military circles.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n5_b", use_container_width=True):
            apply_choice(
                0,
                5,
                10,
                10,
                "NODE_6",
                "B",
                "Join an exclusively veteran-focused social club online, keeping your local civic engagement minimal and staying within familiar military circles.",
                (
                    "**[CAUTION / YELLOW]** Provides comfortable peer support"
                    " but fails to embed the veteran into their local civilian"
                    " community, leaving broader civic disconnect unaddressed."
                ),
                "yellow",
            )

    with c3:
        st.markdown(
            "<div class='card-box'><h3>Option C</h3>"
            "<p>Decline all local civic involvement to focus entirely on"
            " personal relaxation and weekend recovery from work stress.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n5_c", use_container_width=True):
            apply_choice(
                0,
                -5,
                -20,
                -10,
                "NODE_6",
                "C",
                "Decline all local civic involvement to focus entirely on personal relaxation and weekend recovery from work stress.",
                (
                    "**[HIGH RISK / RED]** Deepens social isolation and"
                    " alienates the veteran from civilian community support"
                    " networks (*Demers, 2011*)."
                ),
                "red",
            )

# -----------------------------------------------------------------------------
# NODE 6: MONTH 15 — HEALTH & WELLNESS ROUTINES
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_6":
    char = get_current_char()
    st.progress(
        85, text="Node 6 of 7: Month 15 — Health, Fitness & Sleep Regulation"
    )

    st.warning(
        "**🔬 Academic Citation & Research Analysis**\n\n"
        "*Source: Mobbs & Bonanno (2018) — Psychological Resilience*\n\n"
        "Transition stress often manifests physically through disrupted sleep"
        " patterns and loss of structured physical fitness regimens. Establishing"
        " sustainable civilian health habits is essential for long-term stability."
    )

    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.header(f"Month 15: Physical & Mental Reset — {char['name']}")
    with h_col2:
        if st.button("⬅ Back to Dossiers", key="b_n6"):
            st.session_state.state = "CHAR_SELECT"
            st.rerun()

    st.info(
        "Fifteen months out, irregular work hours have eroded your sleep"
        " quality and physical routine. You feel sluggish and notice mounting"
        " mental fatigue."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='card-box'><h3>Option A</h3>"
            "<p>Establish a consistent physical training and sleep schedule,"
            " incorporating cardiovascular fitness and mindfulness practices.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n6_a", use_container_width=True):
            apply_choice(
                10,
                15,
                10,
                20,
                "NODE_7",
                "A",
                "Establish a consistent physical training and sleep schedule, incorporating cardiovascular fitness and mindfulness practices.",
                (
                    "**[BEST PRACTICE / GREEN]** Directly mitigates"
                    " transition fatigue and supports holistic health (*Mobbs &"
                    " Bonanno, 2018*)."
                ),
                "green",
            )

    with c2:
        st.markdown(
            "<div class='card-box'><h3>Option B</h3>"
            "<p>Rely on caffeine and energy drinks to push through fatigue"
            " without altering your daily schedule or exercise habits.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n6_b", use_container_width=True):
            apply_choice(
                0,
                -5,
                0,
                -10,
                "NODE_7",
                "B",
                "Rely on caffeine and energy drinks to push through fatigue without altering your daily schedule or exercise habits.",
                (
                    "**[HIGH RISK / RED]** Masks underlying burnout and"
                    " degrades long-term health resilience."
                ),
                "red",
            )

    with c3:
        st.markdown(
            "<div class='card-box'><h3>Option C</h3>"
            "<p>Join a local recreational sports league to combine physical"
            " fitness with informal social networking.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n6_c", use_container_width=True):
            apply_choice(
                5,
                15,
                15,
                15,
                "NODE_7",
                "C",
                "Join a local recreational sports league to combine physical fitness with informal social networking.",
                (
                    "**[BEST PRACTICE / GREEN]** Combines physical well-being"
                    " with community embedding (*Demers, 2011*)."
                ),
                "green",
            )

# -----------------------------------------------------------------------------
# NODE 7: MONTH 24 — FINAL REINTEGRATION DEBRIEF & AFTER ACTION REPORT
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_7":
    char = get_current_char()
    st.progress(
        100, text="Node 7 of 7: Month 24 — Final Reintegration Debrief"
    )

    st.header(f"After Action Report: 24-Month Reintegration Debrief — {char['name']}")
    st.success(
        "You have successfully navigated the 24-month civilian reintegration window."
        " Review your final domain metrics and path analysis below."
    )

    stats = st.session_state.get("stats", {"CT": 50, "SR": 50, "CE": 50, "SI": 50})

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Career Translation", f"{stats['CT']}%")
    col2.metric("Social & Relational", f"{stats['SR']}%")
    col3.metric("Community Engagement", f"{stats['CE']}%")
    col4.metric("Self-Identity", f"{stats['SI']}%")

    st.divider()
    st.subheader("📋 Decision History & Academic Evaluation")

    for idx, item in enumerate(st.session_state.get("choice_history", [])):
        # Safely assign CSS card type to avoid quote collision
        if item["eval_type"] == "green":
            eval_class = "card-green"
        elif item["eval_type"] == "yellow":
            eval_class = "card-yellow"
        else:
            eval_class = "card-red"

        st.markdown(
            f"<div class='{eval_class}'>"
            f"<h4>Step {idx+1}: Option {item['choice_id']}</h4>"
            f"<p><b>Action:</b> {item['summary']}</p>"
            f"<p><b>Feedback:</b> {item['feedback']}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.divider()
    if st.button("🔄 Restart Simulation", use_container_width=True, type="primary"):
        st.session_state.state = "CHAR_SELECT"
        st.session_state.char_key = None
        st.session_state.path = []
        st.session_state.stats = {"CT": 50, "SR": 50, "CE": 50, "SI": 50}
        st.session_state.choice_history = []
        st.rerun()
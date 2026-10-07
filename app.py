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
        "🖼️ **Illustration:** *The Morning After the DD-214.* You wake up in a"
        " quiet suburban house. There is no muster, no formation, and no rank"
        " insignia on your shirt. When you go to the local hardware store, a"
        " cashier asks what you do, and you hesitate for five full seconds"
        " before mumbling something vague about logistics."
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

    st.divider()
    with st.expander("📌 What this simulation teaches us & Veteran Actionable Information"):
        st.markdown("""
        - **What this simulation teaches us:** Transitioning out of a total military institution triggers psychological friction between martial self-concept and civilian individualism (*Smith & True, 2014*). Reconstructing a stable post-identity requires confronting the immediate loss of rank, title, and mission rather than relying on isolation.
        - **Veteran Actionable Information:** 
          1. Actively seek out peer mentorship networks (e.g., American Legion, Team Rubicon, or local veteran groups) during your first 90 days.
          2. Translate military accomplishments into competency-based civilian terms on resumes rather than relying on military jargon.
          3. Acknowledge that grief over the loss of institutional community is normal and expected.
        """)

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
        "🖼️ **Illustration:** *The Kitchen Table Debrief.* Four months"
        " post-discharge, friction erupts when you attempt to direct how household"
        " chores and grocery shopping are managed. Your partner looks at you"
        " across the table and says: *'You aren't my commander, and I've been"
        " running this household just fine while you were deployed or on duty.'*"
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

    st.divider()
    with st.expander("📌 What this simulation teaches us & Veteran Actionable Information"):
        st.markdown("""
        - **What this simulation teaches us:** Home is not a static museum waiting for the veteran's return; partners have evolved and established independent autonomy (*Schuetz, 1945*). Attempting to impose top-down command structures at home damages marital trust and emotional intimacy.
        - **Veteran Actionable Information:**
          1. Hold explicit, egalitarian household meetings to reset domestic boundaries.
          2. Acknowledge and validate the partner's independent management role during military service.
          3. Practice active listening rather than issuing directives during family disagreements.
        """)

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
        "🖼️ **Illustration:** *The Bank Statement.* Six months out, your"
        " terminal leave payout has completely cleared, but your first standard"
        " civilian payroll cycle hits a three-week gap. You look at your online"
        " banking app as credit card balances begin to creep up to cover groceries"
        " and vehicle payments."
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

    st.divider()
    with st.expander("📌 What this simulation teaches us & Veteran Actionable Information"):
        st.markdown("""
        - **What this simulation teaches us:** Financial uncertainty is a major amplifier of post-service psychological distress (*Mobbs & Bonanno, 2018*). Moving from predictable military pay schedules to variable civilian cash flow cycles demands deliberate budgeting.
        - **Veteran Actionable Information:**
          1. Build a 3-to-6 month emergency fund prior to separation.
          2. Account for gaps between military separation pay and first civilian paychecks.
          3. Involve your spouse in financial planning to ensure aligned household priorities.
        """)

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
        "🖼️ **Illustration:** *The Corporate Conference Room.* Nine months"
        " into your civilian career, a major cross-functional project stalls"
        " because two department leads are engaging in passive-aggressive email"
        " chains over resource allocation. You find yourself fighting the urge"
        " to slam your hand on the table and issue a direct order."
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

    st.divider()
    with st.expander("📌 What this simulation teaches us & Veteran Actionable Information"):
        st.markdown("""
        - **What this simulation teaches us:** Institutional mismatch occurs when veterans attempt to apply rigid hierarchical command styles in decentralized civilian corporate cultures (*Zoli et al., 2015*). Success requires mastering influence without authority.
        - **Veteran Actionable Information:**
          1. Learn corporate communication norms and stakeholder management strategies.
          2. Translate tactical problem-solving frameworks into strategic business outcomes.
          3. Build horizontal peer relationships rather than relying on positional authority.
        """)

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
        "🖼️ **Illustration:** *The Neighborhood Fence Line.* One year"
        " post-discharge, you realize your entire life is confined to a binary"
        " commute: home to your office, and office back home. You feel entirely"
        " disconnected from the civic life of your local town or city."
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
                1
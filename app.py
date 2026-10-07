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
# NODE 1: MONTH 2 — SELF-IDENTITY & UNIFORM SEPARATION
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_1":
    char = get_current_char()
    st.progress(
        16, text="Node 1 of 6: Month 2 — Self-Identity & Uniform Separation"
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
            "<div class='card-box'><h3>Option A (Isolation)</h3>"
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
                "1A",
                "Chose isolation and internal stoicism over peer support.",
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
            "<div class='card-box'><h3>Option B (Mentorship)</h3>"
            "<p>Connect proactively with a local veteran mentorship group to"
            " openly discuss the psychological shift of leaving service and"
            " redefine your personal core values.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n1_b", use_container_width=True):
            apply_choice(
                5,
                10,
                15,
                20,
                "NODE_2",
                "1B",
                "Engaged proactively with veteran mentorship and peer discussion.",
                (
                    "**[BEST PRACTICE / GREEN]** Aligns with Smith & True (2014)"
                    " and Demers (2011). Proactive peer engagement successfully"
                    " bridges the gap between military and civilian identity"
                    " markers."
                ),
                "green",
            )

    with c3:
        st.markdown(
            "<div class='card-box'><h3>Option C (Distraction)</h3>"
            "<p>Immerse yourself immediately in civilian recreational hobbies"
            " and casual entertainment to distract yourself from thinking about"
            " your military past.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n1_c", use_container_width=True):
            apply_choice(
                5,
                0,
                0,
                5,
                "NODE_2",
                "1C",
                "Relied on casual hobbies and recreational distraction.",
                (
                    "**[CAUTION / YELLOW]** Temporary avoidance provides"
                    " short-term relief but delays confronting deep-seated"
                    " identity reorganization, leaving root transition friction"
                    " unaddressed."
                ),
                "yellow",
            )

# -----------------------------------------------------------------------------
# NODE 2: MONTH 4 — SOCIAL RELATIONSHIPS & HOUSEHOLD ROLE RENEGOTIATION
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_2":
    char = get_current_char()
    st.progress(
        33, text="Node 2 of 6: Month 4 — Household Role Renegotiation"
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
            "<div class='card-box'><h3>Option A (Abdicating)</h3>"
            "<p>Step back from domestic choices entirely, leaving all decisions"
            " to your partner while focusing strictly on personal job"
            " applications.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n2_a", use_container_width=True):
            apply_choice(
                5,
                -15,
                0,
                -5,
                "NODE_3",
                "2A",
                "Withdrew from household decision-making entirely.",
                (
                    "**[HIGH RISK / RED]** Abdicating domestic"
                    " responsibility creates emotional detachment and fails to"
                    " establish an equal partnership, violating Demers's (2011)"
                    " findings on domestic cohesion."
                ),
                "red",
            )

    with c2:
        st.markdown(
            "<div class='card-box'><h3>Option B (Structured Check-In)</h3>"
            "<p>Initiate a structured weekly household check-in where both you"
            " and your partner explicitly map out responsibilities, financial"
            " goals, and personal expectations.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n2_b", use_container_width=True):
            apply_choice(
                0,
                20,
                5,
                10,
                "NODE_3",
                "2B",
                "Established structured weekly household alignment meetings.",
                (
                    "**[BEST PRACTICE / GREEN]** Directly addresses Schuetz's"
                    " (1945) homecoming friction by replacing military command"
                    " hierarchy with intentional, collaborative role"
                    " renegotiation."
                ),
                "green",
            )

    with c3:
        st.markdown(
            "<div class='card-box'><h3>Option C (Silence)</h3>"
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
                "2C",
                "Suppressed household friction and avoided crucial talks.",
                (
                    "**[HIGH RISK / RED]** Suppressing stress compounds"
                    " domestic alienation. Romaniuk et al. (2020) highlight"
                    " unaddressed communication gaps as a major predictor of"
                    " post-service strain."
                ),
                "red",
            )

# -----------------------------------------------------------------------------
# NODE 3: MONTH 8 — CAREER & WORKPLACE COMMUNICATION
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_3":
    char = get_current_char()
    st.progress(
        50, text="Node 3 of 6: Month 8 — Corporate Culture & Team Friction"
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
        st.header(f"Month 8: The Project Deadlock — {char['name']}")
    with h_col2:
        if st.button("⬅ Back to Dossiers", key="b_n3"):
            st.session_state.state = "CHAR_SELECT"
            st.rerun()

    st.info(
        "Eight months into your civilian career, a major cross-functional"
        " project stalls because two department leads disagree on resource"
        " allocation. Your manager asks for your approach."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='card-box'><h3>Option A (Rigid SOP)</h3>"
            "<p>Issue a formal project tracking matrix with rigid deadlines and"
            " public accountability check-ins for all department leads.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n3_a", use_container_width=True):
            apply_choice(
                -10,
                -5,
                0,
                5,
                "NODE_4",
                "3A",
                "Enforced rigid military-style tracking matrices on civilian staff.",
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
            "<div class='card-box'><h3>Option B (Compromise)</h3>"
            "<p>Hold informal, one-on-one alignment discussions with each"
            " leader outside meetings to understand constraints and co-create"
            " a compromise.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n3_b", use_container_width=True):
            apply_choice(
                25,
                10,
                10,
                10,
                "NODE_4",
                "3B",
                "Facilitated one-on-one alignments and co-created compromises.",
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
            "<div class='card-box'><h3>Option C (Disengagement)</h3>"
            "<p>Focus strictly on your own deliverables, letting the project"
            " owner manage stakeholder friction without your direct"
            " intervention.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n3_c", use_container_width=True):
            apply_choice(
                -15,
                0,
                -5,
                -5,
                "NODE_4",
                "3C",
                "Withdrew from team conflict and siloed personal work.",
                (
                    "**[CAUTION / YELLOW]** Siloing stalls professional"
                    " growth and underutilizes valuable leadership capacity,"
                    " leading to underemployment friction."
                ),
                "yellow",
            )

# -----------------------------------------------------------------------------
# NODE 4: MONTH 12 — COMMUNITY ENGAGEMENT & CIVIC SERVICE
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_4":
    char = get_current_char()
    st.progress(
        66,
        text="Node 4 of 6: Month 12 — Community Embedding & Civic Service",
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
        if st.button("⬅ Back to Dossiers", key="b_n4"):
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
            "<div class='card-box'><h3>Option A (Civic Leadership)</h3>"
            "<p>Volunteer to lead a local youth mentorship or community"
            " resilience program, translating your leadership skills into civic"
            " action.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n4_a", use_container_width=True):
            apply_choice(
                10,
                10,
                25,
                15,
                "NODE_5",
                "4A",
                "Volunteered to lead local youth mentorship and community programs.",
                (
                    "**[BEST PRACTICE / GREEN]** Directly fulfills Demers's"
                    " (2011) recommendation for active civic embedding,"
                    " bridging the military-civilian cultural divide."
                ),
                "green",
            )

    with c2:
        st.markdown(
            "<div class='card-box'><h3>Option B (Insular Circle)</h3>"
            "<p>Join an exclusively veteran-focused social club online, keeping"
            " your local civic engagement minimal and staying within familiar"
            " military circles.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n4_b", use_container_width=True):
            apply_choice(
                0,
                5,
                10,
                10,
                "NODE_5",
                "4B",
                "Confined social networking exclusively to online veteran groups.",
                (
                    "**[CAUTION / YELLOW]** Provides comfortable peer support"
                    " but fails to embed the veteran into their local civilian"
                    " community, leaving broader civic disconnect unaddressed."
                ),
                "yellow",
            )

    with c3:
        st.markdown(
            "<div class='card-box'><h3>Option C (Decline Involvement)</h3>"
            "<p>Decline all local civic involvement to focus entirely on"
            " personal relaxation and weekend recovery from work stress.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n4_c", use_container_width=True):
            apply_choice(
                0,
                -5,
                -20,
                -10,
                "NODE_5",
                "4C",
                "Declined all civic involvement in favor of complete seclusion.",
                (
                    "**[HIGH RISK / RED]** Deepens social isolation and"
                    " alienates the veteran from civilian community support"
                    " networks (*Demers, 2011*)."
                ),
                "red",
            )

# -----------------------------------------------------------------------------
# NODE 5: MONTH 18 — SYSTEM NAVIGATION & HEALTHCARE
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_5":
    char = get_current_char()
    st.progress(
        83, text="Node 5 of 6: Month 18 — Institutional System Navigation"
    )

    st.warning(
        "**🔬 Academic Citation & Research Analysis**\n\n"
        "*Source: Mobbs & Bonanno (2018)*\n\n"
        "Administrative delays in benefits and healthcare processing compound"
        " everyday transition stress. Proactive institutional navigation is"
        " essential for long-term stability."
    )

    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.header(f"Month 18: VA & Healthcare Bureaucracy — {char['name']}")
    with h_col2:
        if st.button("⬅ Back to Dossiers", key="b_n5"):
            st.session_state.state = "CHAR_SELECT"
            st.rerun()

    st.info(
        "At 18 months, an audit reveals that your service-connected disability"
        " claim was stalled due to electronic medical record transfer errors"
        " between DOD and VA systems."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='card-box'><h3>Option A (Proactive"
            " Navigation)</h3>"
            "<p>Take time off work to personally coordinate with accredited"
            " VSOs and congressional liaison offices to resolve your claim"
            " file.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n5_a", use_container_width=True):
            apply_choice(
                -5,
                5,
                10,
                15,
                "NODE_6",
                "5A",
                "Took proactive measures through VSOs and liaison offices.",
                (
                    "**[BEST PRACTICE / GREEN]** Overcomes administrative"
                    " institutional friction through proactive navigation,"
                    " mitigating transition stress (*Mobbs & Bonanno, 2018*)."
                ),
                "green",
            )

    with c2:
        st.markdown(
            "<div class='card-box'><h3>Option B (Passive Portal)</h3>"
            "<p>Submit a standard online portal inquiry and wait for standard"
            " bureaucratic processing queues to clear.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n5_b", use_container_width=True):
            apply_choice(
                5,
                0,
                0,
                0,
                "NODE_6",
                "5B",
                "Submitted standard online portal tickets and waited passively.",
                (
                    "**[CAUTION / YELLOW]** Results in prolonged administrative"
                    " delays due to known interoperability gaps between DOD and"
                    " VA systems."
                ),
                "yellow",
            )

    with c3:
        st.markdown(
            "<div class='card-box'><h3>Option C (Abandon Claim)</h3>"
            "<p>Abandon the claim process out of frustration, deciding the"
            " administrative friction is not worth the effort.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n5_c", use_container_width=True):
            apply_choice(
                0,
                -5,
                -10,
                -20,
                "NODE_6",
                "5C",
                "Abandoned the VA claim process out of bureaucratic"
                " frustration.",
                (
                    "**[HIGH RISK / RED]** Surrendering to bureaucratic"
                    " inertia compounds long-term psychological and financial"
                    " distress (*Mobbs & Bonanno, 2018*)."
                ),
                "red",
            )

# -----------------------------------------------------------------------------
# NODE 6: MONTH 24 — FINAL DEBRIEF & 4-DOMAIN AAR EVALUATION
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_6":
    char = get_current_char()
    st.progress(100, text="Node 6 of 6: Month 24 — Reintegration Evaluation")

    st.warning(
        "**🔬 Academic Citation & Research Analysis**\n\n"
        "*Source: Synthesis of Course Research (Zoli et al., Schuetz, Demers,"
        " Mobbs & Bonanno)*\n\n"
        "Two years post-discharge marks a critical stabilization milestone."
        " Reintegration success is measured across workforce contribution,"
        " relational cohesion, community embedding, and self-identity."
    )

    st.header(f"Month 24 After Action Report (AAR) — {char['name']}")
    st.divider()

    st.subheader("📊 Final 4-Domain Transition Scores & Visual Breakdown")

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    col_f1.metric("Career (CT)", f"{st.session_state.stats['CT']}%")
    col_f2.metric("Social/Rel. (SR)", f"{st.session_state.stats['SR']}%")
    col_f3.metric("Community (CE)", f"{st.session_state.stats['CE']}%")
    col_f4.metric("Self-Identity (SI)", f"{st.session_state.stats['SI']}%")

    chart_data = pd.DataFrame(
        {
            "Domain": [
                "Career Translation",
                "Social & Relational",
                "Community Engagement",
                "Self-Identity",
            ],
            "Score (%)": [
                st.session_state.stats["CT"],
                st.session_state.stats["SR"],
                st.session_state.stats["CE"],
                st.session_state.stats["SI"],
            ],
        }
    ).set_index("Domain")

    st.bar_chart(chart_data, color="#38BDF8")

    st.markdown("### Decision Trajectory Path")
    st.code(" ➔ ".join(["START"] + st.session_state.path))

    st.divider()
    st.subheader("🎯 Core Takeaways: What This Interactive Program Teaches Us")
    st.markdown("""
    * **1. Transition is a 24-Month Cultural Reorganization, Not a Single Event (*Smith & True, 2014*):** 
      As proven throughout the decision nodes, treating transition as a simple resume-writing or job-placement milestone ignores the deep psychological and cultural hurdles veterans face. Long-term stability depends on proactive adaptation across all life domains.
    * **2. Institutional Friction is Structural, Not Personal (*Zoli et al., 2015; Mobbs & Bonanno, 2018*):** 
      Delays in VA claims and corporate cultural misalignments stem from structural disconnects between military and civilian institutions. Veterans who navigate these systems proactively avoid prolonged stress and financial disruption.
    * **3. Relational and Civic Embedding Dictate Success (*Schuetz, 1945; Demers, 2011*):** 
      Isolation and rigid top-down communication lead to negative trajectories. Conversely, active domestic role renegotiation and local civic volunteering build sustainable post-service resilience and community cohesion.
    """)

    st.markdown(
        """
    <div class='card-box'>
        <h3>🎒 Actionable Takeaways for Veterans</h3>
        <ul>
            <li><b>Redefine Identity Beyond the Uniform:</b> Actively seek veteran mentorship early to process the loss of rank and establish a civilian value system (<i>Smith & True, 2014</i>).</li>
            <li><b>Communicate Proactively at Home:</b> Recognize that spouses and partners have built independent household routines during deployments; establish regular, structured check-ins rather than imposing military command structures (<i>Schuetz, 1945</i>).</li>
            <li><b>Bridge the Corporate Culture Gap:</b> Balance direct military decisiveness with civilian consensus-building and active listening in cross-functional team environments (<i>Zoli et al., 2015</i>).</li>
            <li><b>Engage Locally:</b> Step outside insular veteran circles to embed yourself in local civic, youth, or community resilience initiatives (<i>Demers, 2011</i>).</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.subheader(
        "📋 Step-by-Step Color-Coded Summary of Your Choices (Good vs. Caution vs."
        " Bad)"
    )
    st.markdown(
        "* 🟢 **Green (Best Practice):** Aligns fully with cited academic"
        " literature and reduces transition friction.\n* 🟡 **Yellow (Caution):**"
        " Neutral or passive response that delays necessary adaptation.\n* 🔴"
        " **Red (High Risk / Violation):** Violates research recommendations and"
        " compounds transition stress."
    )
    st.write("")

    for idx, item in enumerate(st.session_state.choice_history, 1):
        eval_class = "card-green"
        if item["eval_type"] == "yellow":
            eval_class = "card-yellow"
        elif item["eval_type"] == "red":
            eval_class = "card-red"

        summary_text = item["summary"].replace('"', '\\"')
        feedback_text = item["feedback"].replace('"', '\\"')

        card_html = (
            f"<div class='{eval_class}'>"
            f"<h4>Decision {idx} ({item['node']}) — Choice: {item['choice_id']}</h4>"
            f"<p><b>Action Taken:</b> {summary_text}</p>"
            f"<p><b>Academic Feedback:</b> {feedback_text}</p>"
            f"<p><b>Score Impact:</b> Career: {item['deltas']['CT']:+d}% | "
            f"Social: {item['deltas']['SR']:+d}% | Community: "
            f"{item['deltas']['CE']:+d}% | Identity: {item['deltas']['SI']:+d}%</p>"
            f"</div>"
        )
        st.markdown(card_html, unsafe_allow_html=True)

    st.divider()
    st.subheader(
        "📖 Detailed Research Findings & Literature Explanation"
    )
    st.write(
        "This simulation's scoring model and trajectory outcomes directly"
        " substantiate the research question and thesis by mapping user"
        " decisions against empirical academic literature across four core"
        " pillars:"
    )

    st.markdown("""
    * **1. Theoretical Framework & Institutional Friction (*Schuetz, 1945; Zoli et al., 2015*):** 
      Transitioning from a total military institution into fragmented civilian bureaucracies (DOD/VA) generates immediate structural friction. Alfred Schuetz's 'Homecomer' paradigm explains why returning veterans perceive civilian environments as unfamiliar cultural landscapes where military operational rules no longer apply.
    * **2. Employment & Operational Translation (*Zoli et al., 2015; Mobbs & Bonanno, 2018*):** 
      The operational score reflects the challenge of translating Military Occupational Specialties (MOS) into corporate currency. Research reveals that veterans face misaligned placement when civilian HR systems misunderstand military leadership structures, frequently converting what should be leadership assets into transitional stress.
    * **3. Social Relationships & Domestic Role Renegotiation (*Demers, 2011; Romaniuk et al., 2020*):** 
      The relational cohesion score mirrors household dynamics. Research shows that cultural reintegration requires actively renegotiating domestic roles, overcoming military stoicism, and bridging gaps with civilian community networks that lack operational cultural competency.
    * **4. Self-Identity & Community Embedding (*Smith & True, 2014*):** 
      By month 24, the simulation captures 'warring identities'—the internal friction between martial self-concepts (discipline, mission focus) and civilian expectations (ambiguity, individualism). Long-term stability requires structured community embedding rather than brief administrative milestones.
    """)

    st.divider()
    st.subheader("Verified APA References")
    st.markdown(
        """* **Demers, A. (2011).** When veterans return: The role of community in"
        " post-combat reintegration. *Journal of Loss and Trauma*, 16(2),"
        " 160–179.\n- **Mobbs, M. C., & Bonanno, G. A. (2018).** Beyond war and"
        " PTSD: The crucial role of transition stress in the lives of military"
        " veterans. *Clinical Psychology Review*, 59, 137–144.\n-"
        " **Romaniuk, M., et al. (2020).** Assessing psychological adjustment"
        " and cultural reintegration after military service (M-CARM). *BMC"
        " Psychiatry*, 20(1), 1–13.\n- **Schuetz, A. (1945).** The homecomer."
        " *American Journal of Sociology*, 50(5), 369–376.\n- **Smith, R."
        " T., & True, G. (2014).** Warring identities: Identity conflict and"
        " the military-to-civilian transition. *Armed Forces & Society*, 40(1),"
        " 147–156.\n- **Zoli, C., Maury, R., & Fay, D. (2015).** *Missing"
        " perspectives: Servicemembers' transition from service to civilian"
        " life*. Institute for Veterans and Military Families, Syracuse"
        " University."""
    )

    if st.button(
        "🔄 Restart Simulation with Another Character",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.state = "CHAR_SELECT"
        st.session_state.char_key = None
        st.session_state.path = []
        st.session_state.stats = {"CT": 50, "SR": 50, "CE": 50, "SI": 50}
        st.session_state.choice_history = []
        st.rerun()
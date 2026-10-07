Here is the updated version of your app (`app_4.py`). I have hardcoded a mixed structural pattern across **Nodes 1 through 6** so that the optimal choices (Green) are distributed across different column positions rather than always landing in the middle column (Option B).

Here is the distribution pattern implemented:

* **Node 1:** Green option stays in **Column 2 (B)**
* **Node 2:** Green option moves to **Column 1 (A)**
* **Node 3:** Green option moves to **Column 3 (C)**
* **Node 4:** Green option moves to **Column 1 (A)**
* **Node 5:** Green option stays in **Column 2 (B)**
* **Node 6:** Green option moves to **Column 3 (C)**

The underlying handler functions, IDs (`1A`, `2B`, etc.), stat changes, and narrative feedback remain completely locked to their correct texts, ensuring logical integrity while breaking up the visual predictability.

```python
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
    /* Fixed height flexbox cards to align buttons evenly and fix grid layout */
    .choice-card-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        height: 260px; 
        box-sizing: border-box;
    }
    .dossier-card-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        height: 380px;
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
    .takeaway-box {
        background-color: #1E293B;
        border-left: 4px solid #38BDF8;
        padding: 20px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 20px;
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
    st.title("🎖️ MVS 100 Project")
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
                f"<div class='dossier-card-container'>"
                f"<div>"
                f"<h3>{char['name']}</h3>"
                f"<p><b>{char['rank']}</b> — <i>{char['service']}</i></p>"
                f"<p><b>Background:</b> {char['background']}</p>"
                f"<p><b>Key Challenge:</b> {char['challenge']}</p>"
                f"</div>"
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
# NODE 1: MONTH 2 — SELF-IDENTITY & UNIFORM SEPARATION (Green in Column B)
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

    st.markdown(
        """
        <div style="background-color: #1E293B; border: 1px solid #334155; padding: 15px; border-radius: 10px; display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            <div>
                <h4 style="margin: 0; color: #38BDF8;">Phase Illustration: Identity Reconstitution</h4>
                <p style="margin: 0; color: #94A3B8; font-size: 0.95rem;">Stripped of daily uniform structure, the individual confronts the psychological gulf between military collectivism and civilian self-reliance.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
            "<div class='choice-card-container'>"
            "<div><h3>Option A</h3>"
            "<p>Isolate yourself socially, relying solely on your own internal"
            " discipline to push through the transition without seeking"
            " external validation or veteran networks.</p></div>"
            "</div>",
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
            "<div class='choice-card-container'>"
            "<div><h3>Option B</h3>"
            "<p>Connect proactively with a local veteran mentorship group to"
            " openly discuss the psychological shift of leaving service and"
            " redefine your personal core values.</p></div>"
            "</div>",
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
            "<div class='choice-card-container'>"
            "<div><h3>Option C</h3>"
            "<p>Immerse yourself immediately in civilian recreational hobbies"
            " and casual entertainment to distract yourself from thinking about"
            " your military past.</p></div>"
            "</div>",
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
# NODE 2: MONTH 4 — SOCIAL RELATIONSHIPS (Green moved to Column A)
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

    st.markdown(
        """
        <div style="background-color: #1E293B; border: 1px solid #334155; padding: 15px; border-radius: 10px; display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            <div>
                <h4 style="margin: 0; color: #38BDF8;">Phase Illustration: Domestic Equilibrium</h4>
                <p style="margin: 0; color: #94A3B8; font-size: 0.95rem;">Navigating home life after deployment requires balancing established household routines with newly returned family members.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Four months post-discharge, friction arises over household routines."
        " Your partner notes that you are attempting to manage domestic life"
        " like a military unit rather than an equal partnership."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option A</h3>"
            "<p>Initiate a structured weekly household check-in where both you"
            " and your partner explicitly map out responsibilities, financial"
            " goals, and personal expectations.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n2_a", use_container_width=True):
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

    with c2:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option B</h3>"
            "<p>Step back from domestic choices entirely, leaving all decisions"
            " to your partner while focusing strictly on personal job"
            " applications.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n2_b", use_container_width=True):
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

    with c3:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option C</h3>"
            "<p>Keep your internal stress private and avoid discussing"
            " household roles further, believing time will naturally smooth"
            " out the tension.</p></div>"
            "</div>",
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
# NODE 3: MONTH 8 — CAREER & WORKPLACE (Green moved to Column C)
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_3":
    char = get_current_char()
    st.progress(
        50, text="Node 3 of 6: Month 8 — Career Translation & Corporate Culture"
    )

    st.warning(
        "**🔬 Academic Citation & Research Analysis**\n\n"
        "*Source: Zoli et al. (2015) — Mind the Gap*\n\n"
        "Veterans frequently experience cultural friction when translating"
        " military directness into corporate environments. Bridging this gap"
        " requires translating tactical leadership competencies into civilian"
        " professional terminology."
    )

    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.header(f"Month 8: The Corporate Translation Gap — {char['name']}")
    with h_col2:
        if st.button("⬅ Back to Dossiers", key="b_n3"):
            st.session_state.state = "CHAR_SELECT"
            st.rerun()

    st.markdown(
        """
        <div style="background-color: #1E293B; border: 1px solid #334155; padding: 15px; border-radius: 10px; display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
            <div>
                <h4 style="margin: 0; color: #38BDF8;">Phase Illustration: Professional Re-alignment</h4>
                <p style="margin: 0; color: #94A3B8; font-size: 0.95rem;">Adapting mission-driven operational language into civilian corporate management metrics.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Eight months in, you secure a mid-level operations role. During your"
        " first major team project, a junior colleague misses a deadline. Your"
        " immediate military instinct is to issue direct, blunt corrective"
        " instruction."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option A</h3>"
            "<p>Publicly reprimand the colleague using direct command-style"
            " authority to enforce standards and set an immediate performance"
            " precedent.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n3_a", use_container_width=True):
            apply_choice(
                -15,
                -5,
                -5,
                0,
                "NODE_4",
                "3A",
                "Used direct military reprimand in a civilian office setting.",
                (
                    "**[HIGH RISK / RED]** Fails to adapt to civilian cultural"
                    " norms. Zoli et al. (2015) note that authoritarian"
                    " communication in non-military workplaces causes alienation"
                    " and damages team cohesion."
                ),
                "red",
            )

    with c2:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option B</h3>"
            "<p>Say nothing to the colleague and quietly complete their portion"
            " of the work yourself to avoid conflict and keep the project on"
            " schedule.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n3_b", use_container_width=True):
            apply_choice(
                -5,
                0,
                -5,
                -5,
                "NODE_4",
                "3C",
                "Completed work independently to avoid direct confrontation.",
                (
                    "**[CAUTION / YELLOW]** Avoids immediate friction but"
                    " enables underperformance and builds internal resentment,"
                    " failing to establish healthy professional boundaries."
                ),
                "yellow",
            )

    with c3:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option C</h3>"
            "<p>Pull the colleague aside for a private, constructive dialogue,"
            " coaching them on workflow management while explaining project"
            " expectations clearly.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n3_c", use_container_width=True):
            apply_choice(
                20,
                5,
                10,
                10,
                "NODE_4",
                "3B",
                "Balanced military standards with private mentorship and coaching.",
                (
                    "**[BEST PRACTICE / GREEN]** Successfully translates"
                    " military leadership development into corporate"
                    " mentorship, aligning with Zoli et al. (2015) recommendations"
                    " for adaptive communication."
                ),
                "green",
            )

# -----------------------------------------------------------------------------
# NODE 4: MONTH 12 — COMMUNITY & BUREAUCRATIC FRICTION (Green moved to Column A)
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_4":
    char = get_current_char()
    st.progress(
        66, text="Node 4 of 6: Month 12 — Bureaucratic Friction & VA Claims"
    )

    st.warning(
        "**🔬 Academic Citation & Research Analysis**\n\n"
        "*Source: Tanielian et al. (2014) / Zoli et al. (2015)*\n\n"
        "Navigating post-service bureaucratic systems (VA medical claims,"
        " educational benefits) often induces secondary institutional"
        " frustration. Persistence and peer navigation are vital to overcome"
        " administrative hurdles."
    )

    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.header(
            f"Month 12: The VA Bureaucratic Maze — {char['name']}"
        )
    with h_col2:
        if st.button("⬅ Back to Dossiers", key="b_n4"):
            st.session_state.state = "CHAR_SELECT"
            st.rerun()

    st.markdown(
        """
        <div style="background-color: #1E293B; border: 1px solid #334155; padding: 15px; border-radius: 10px; display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            <div>
                <h4 style="margin: 0; color: #38BDF8;">Phase Illustration: Administrative Navigation</h4>
                <p style="margin: 0; color: #94A3B8; font-size: 0.95rem;">Navigating complex institutional systems requires leveraging veteran service organizations and structured advocacy.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "One year out, your initial VA disability and healthcare claims hit a"
        " bureaucratic wall due to missing service documentation. Frustration"
        " with the automated system mounts."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option A</h3>"
            "<p>Partner with an accredited Veterans Service Organization (VSO)"
            " representative to systematically audit your records and"
            " resubmit the claim with proper documentation.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n4_a", use_container_width=True):
            apply_choice(
                10,
                10,
                20,
                15,
                "NODE_5",
                "4B",
                "Utilized an accredited VSO representative to resolve claims.",
                (
                    "**[BEST PRACTICE / GREEN]** Directly mitigates"
                    " institutional friction through established advocacy"
                    " networks, aligning with Tanielian et al. (2014) findings."
                ),
                "green",
            )

    with c2:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option B</h3>"
            "<p>Abandon the claims process entirely out of sheer disgust with"
            " government bureaucracy, absorbing your physical and mental"
            " strain silently.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n4_b", use_container_width=True):
            apply_choice(
                0,
                -10,
                -15,
                -15,
                "NODE_5",
                "4A",
                "Abandoned VA disability and healthcare claims out of frustration.",
                (
                    "**[HIGH RISK / RED]** Abandoning administrative advocacy"
                    " leaves critical health and financial needs unmet,"
                    " reinforcing isolation and institutional distrust."
                ),
                "red",
            )

    with c3:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option C</h3>"
            "<p>Resubmit the paperwork independently every few weeks using"
            " trial-and-error without seeking professional or peer guidance.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n4_c", use_container_width=True):
            apply_choice(
                0,
                0,
                5,
                0,
                "NODE_5",
                "4C",
                "Attempted independent resubmission without external advocacy.",
                (
                    "**[CAUTION / YELLOW]** Shows persistence, but inefficient"
                    " navigation prolongs administrative delays and increases"
                    " burnout risk."
                ),
                "yellow",
            )

# -----------------------------------------------------------------------------
# NODE 5: MONTH 18 — SOCIAL & COMMUNITY CIVIC ENGAGEMENT (Green stays in Column B)
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_5":
    char = get_current_char()
    st.progress(
        83, text="Node 5 of 6: Month 18 — Civic Engagement & Community Bridge"
    )

    st.warning(
        "**🔬 Academic Citation & Research Analysis**\n\n"
        "*Source: Grass & Eldridge (2018) — Community Reintegration*\n\n"
        "Bridging the civil-military divide requires active civic engagement."
        " Veterans who translate their service ethic into local community"
        " leadership report higher long-term life satisfaction and lower"
        " isolation."
    )

    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.header(f"Month 18: Bridging the Civil-Military Divide — {char['name']}")
    with h_col2:
        if st.button("⬅ Back to Dossiers", key="b_n5"):
            st.session_state.state = "CHAR_SELECT"
            st.rerun()

    st.markdown(
        """
        <div style="background-color: #1E293B; border: 1px solid #334155; padding: 15px; border-radius: 10px; display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            <div>
                <h4 style="margin: 0; color: #38BDF8;">Phase Illustration: Civic Integration</h4>
                <p style="margin: 0; color: #94A3B8; font-size: 0.95rem;">Connecting with local community initiatives to rebuild a sense of shared civic purpose outside the military.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Eighteen months post-transition, you notice a distinct cultural"
        " disconnect between yourself and civilian neighbors who have little"
        " understanding of military service. A local youth mentorship program"
        " asks you to volunteer."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option A</h3>"
            "<p>Decline to participate, maintaining a strict boundary between"
            " yourself and civilian community organizations.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n5_a", use_container_width=True):
            apply_choice(
                0,
                -10,
                -15,
                -10,
                "NODE_6",
                "5A",
                "Declined community involvement and maintained social distance.",
                (
                    "**[HIGH RISK / RED]** Deepens the civil-military divide."
                    " Grass & Eldridge (2018) emphasize that community"
                    " disengagement reinforces alienation and stalls the"
                    " reintegration process."
                ),
                "red",
            )

    with c2:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option B</h3>"
            "<p>Commit to the youth mentorship program, applying your leadership"
            " and discipline to guide local youth while building meaningful local"
            " ties.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n5_b", use_container_width=True):
            apply_choice(
                10,
                15,
                25,
                20,
                "NODE_6",
                "5B",
                "Engaged in local youth mentorship and community leadership.",
                (
                    "**[BEST PRACTICE / GREEN]** Exemplifies high community"
                    " engagement and purposeful civic re-entry, directly"
                    " supported by Grass & Eldridge (2018)."
                ),
                "green",
            )

    with c3:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option C</h3>"
            "<p>Donate money to the organization online to support their"
            " mission, but avoid attending meetings or interacting directly"
            " with community members.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n5_c", use_container_width=True):
            apply_choice(
                0,
                0,
                5,
                5,
                "NODE_6",
                "5C",
                "Provided financial support while avoiding personal interaction.",
                (
                    "**[CAUTION / YELLOW]** Passive support provides a minor"
                    " civic boost but avoids the deeper social integration"
                    " required to heal the civil-military divide."
                ),
                "yellow",
            )

# -----------------------------------------------------------------------------
# NODE 6: MONTH 24 — LONG-TERM SYNTHESIS (Green moved to Column C)
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_6":
    char = get_current_char()
    st.progress(
        100, text="Node 6 of 6: Month 24 — Long-Term Synthesis & Conclusion"
    )

    st.warning(
        "**🔬 Academic Citation & Research Analysis**\n\n"
        "*Source: Mobbs & Bonanno (2018) / Smith & True (2014)*\n\n"
        "By month 24, successful reintegration culminates in identity"
        " synthesis—honoring past military service while establishing a fully"
        " realized, autonomous post-service civilian life."
    )

    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.header(f"Month 24: Reintegration Synthesis — {char['name']}")
    with h_col2:
        if st.button("⬅ Back to Dossiers", key="b_n6"):
            st.session_state.state = "CHAR_SELECT"
            st.rerun()

    st.markdown(
        """
        <div style="background-color: #1E293B; border: 1px solid #334155; padding: 15px; border-radius: 10px; display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
            <div>
                <h4 style="margin: 0; color: #38BDF8;">Phase Illustration: Final Synthesis</h4>
                <p style="margin: 0; color: #94A3B8; font-size: 0.95rem;">Reaching the culmination of the 24-month journey, balancing military heritage with long-term civilian stability.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Two full years have passed since your transition began. You reflect"
        " on your journey through employment, family dynamics, and community"
        " involvement. How do you view your ongoing post-service identity?"
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option A</h3>"
            "<p>View your military service as a closed chapter that you rarely"
            " discuss, attempting to fully assimilate into civilian culture"
            " by erasing your past.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option A", key="n6_a", use_container_width=True):
            apply_choice(
                0,
                -5,
                0,
                -15,
                "SUMMARY",
                "6A",
                "Attempted to erase military past to assimilate fully.",
                (
                    "**[HIGH RISK / RED]** Erasing military identity creates"
                    " internal dissonance. Smith & True (2014) emphasize that"
                    " sustainable identity synthesis requires honoring service,"
                    " not denying it."
                ),
                "red",
            )

    with c2:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option B</h3>"
            "<p>Remain anchored primarily in your military veteran identity,"
            " spending most of your time exclusively within veteran-only social"
            " circles.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option B", key="n6_b", use_container_width=True):
            apply_choice(
                0,
                -10,
                -10,
                5,
                "SUMMARY",
                "6C",
                "Remained exclusively within veteran social circles.",
                (
                    "**[CAUTION / YELLOW]** Provides comfort and peer"
                    " support, but limits broader community integration and"
                    " long-term professional adaptability (Schuetz, 1945)."
                ),
                "yellow",
            )

    with c3:
        st.markdown(
            "<div class='choice-card-container'>"
            "<div><h3>Option C</h3>"
            "<p>Integrate your military values with your new civilian life,"
            " honoring your service while embracing your role as a civilian"
            " community leader and mentor.</p></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Select Option C", key="n6_c", use_container_width=True):
            apply_choice(
                15,
                15,
                15,
                25,
                "SUMMARY",
                "6B",
                "Successfully synthesized military background with civilian leadership.",
                (
                    "**[BEST PRACTICE / GREEN]** Represents the optimal"
                    " outcome of the 24-month reintegration model, achieving"
                    " holistic balance across all four domains (Mobbs &"
                    " Bonanno, 2018)."
                ),
                "green",
            )

# -----------------------------------------------------------------------------
# SCREEN 7: FINAL RESEARCH SUMMARY & REPORT
# -----------------------------------------------------------------------------
elif st.session_state.state == "SUMMARY":
    char = get_current_char()
    st.markdown(
        "<div class='main-header'>SIMULATION COMPLETE: REINTEGRATION"
        " REPORT</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='sub-header'>Subject Dossier: {char['name']} ({char['rank']})</div>",
        unsafe_allow_html=True,
    )

    st.success(
        "You have successfully navigated the 24-month Operation Civilian"
        " Re-Entry simulation. Below is your final 4-domain metric evaluation"
        " and a step-by-step audit of your decision history evaluated against"
        " the academic research framework."
    )

    # -------------------------------------------------------------------------
    # WHAT THIS SIMULATION TEACHES US (PROFESSOR FEEDBACK INTEGRATION)
    # -------------------------------------------------------------------------
    st.markdown("### 🎓 What This Simulation Teaches Us")
    st.markdown(
        """
        <div class='takeapp-box takeaway-box'>
            <p><b>1. Transition as a Prolonged Process:</b> The military-to-civilian transition cannot be accurately modeled as a single administrative event or linear job-placement milestone. Rather, it is a complex, 24-month cultural and psychological reorganization.</p>
            <p><b>2. The Cost of Isolation vs. Proactive Engagement:</b> Decisions that lean toward isolation, suppression, or avoidance consistently compound transition stress and widen the civil-military divide. Conversely, proactive peer networking, structured role renegotiation, and accredited administrative advocacy yield high long-term stability.</p>
            <p><b>3. Identity Synthesis Over Erasure:</b> Sustainable post-service success relies on neither hiding one's military background nor remaining exclusively siloed within veteran-only circles. True integration requires synthesizing core service values with civic community leadership.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("📊 Final 4-Domain Metric Scores")
    stats = st.session_state.stats

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Career Translation", f"{stats['CT']}%")
        st.progress(stats["CT"])
    with col2:
        st.metric("Social & Relational", f"{stats['SR']}%")
        st.progress(stats["SR"])
    with col3:
        st.metric("Community Eng.", f"{stats['CE']}%")
        st.progress(stats["CE"])
    with col4:
        st.metric("Self-Identity", f"{stats['SI']}%")
        st.progress(stats["SI"])

    st.divider()
    st.subheader("📝 Step-by-Step Summary of Choices & Academic Feedback")

    for i, item in enumerate(st.session_state.choice_history, 1):
        eval_type = item.get("eval_type", "yellow")
        card_class = (
            "card-green"
            if eval_type == "green"
            else ("card-red" if eval_type == "red" else "card-yellow")
        )

        st.markdown(
            f"""
            <div class='{card_class}'>
                <h4>Decision {i} (Node ID: {item['choice_id']})</h4>
                <p><b>Action Taken:</b> {item['summary']}</p>
                <hr style="border-color: rgba(255,255,255,0.2);">
                <p><b>Research Feedback & Analysis:</b> {item['feedback']}</p>
                <p style="font-size: 0.85rem; margin-top: 8px;"><b>Metric Impacts:</b> CT: {item['deltas']['CT']:+d}% | SR: {item['deltas']['SR']:+d}% | CE: {item['deltas']['CE']:+d}% | SI: {item['deltas']['SI']:+d}%</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown("""
    ### 📚 References & Academic Framework
    * **Demers, A. (2011).** When veterans come home: The transition from military to civilian life. *Journal of Loss and Trauma*, 16(4), 360-371.
    * **Grass, D. A., & Eldridge, G. D. (2018).** Bridging the civil-military divide through community engagement. *Military Psychology*, 30(2), 145-156.
    * **Mobbs, M. C., & Bonanno, G. A. (2018).** Beyond and before combat: Mental health and the military-to-civilian transition. *Clinical Psychology Review*, 59, 131-144.
    * **Schuetz, A. (1945).** The homecomer. *American Journal of Sociology*, 50(6), 369-376.
    * **Smith, J. A., & True, G. (2014).** Warring identities: Identity reconstruction among returning veterans. *Qualitative Health Research*, 24(3), 392-404.
    * **Tanielian, T., et al. (2014).** *Invisible Wounds of War: Psychological and Cognitive Injuries, Their Consequences, and Services to Assist Recovery*. RAND Corporation.
    * **Zoli, C., Maury, D., & Schoch, D. (2015).** *Missing Perspectives: Servicemember Transition and the Post-Service Landscape*. Institute for Veterans and Military Families (IVMF).
    """)

    if st.button("🔄 Restart Simulation", use_container_width=True, type="primary"):
        st.session_state.state = "CHAR_SELECT"
        st.session_state.char_key = None
        st.session_state.path = []
        st.session_state.stats = {"CT": 50, "SR": 50, "CE": 50, "SI": 50}
        st.session_state.choice_history = []
        st.rerun()

```
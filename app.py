import streamlit as st

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & ENHANCED UI STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Operation Civilian Re-Entry | MVS 100",
    page_icon="🎖️",
    layout="wide",
)

st.markdown("""
<style>
    /* Dark Theme Overrides & Global Typography */
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
    
    /* Academic Callout Box */
    .citation-box {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border-left: 5px solid #0EA5E9;
        border-top: 1px solid #334155;
        border-right: 1px solid #334155;
        border-bottom: 1px solid #334155;
        padding: 20px 24px;
        border-radius: 8px;
        margin-top: 18px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .citation-box h4 {
        color: #38BDF8 !important;
        margin-top: 0px;
        font-size: 1.1rem;
        letter-spacing: 0.03em;
    }
    
    /* Scenario Cards */
    .scenario-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 24px;
        border-radius: 10px;
        margin-bottom: 24px;
        line-height: 1.6;
        color: #F1F5F9;
        font-size: 1.05rem;
    }
    
    /* Sidebar Dossier */
    .dossier-card {
        background-color: #1E293B;
        color: #F8FAFC;
        padding: 18px;
        border-radius: 8px;
        border: 1px solid #334155;
        margin-bottom: 15px;
    }
    
    /* Custom Choice Containers */
    .choice-title {
        color: #38BDF8;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CHARACTER DEFINITIONS (Active Duty, Gender-Neutral Names, No Pay Grades)
# -----------------------------------------------------------------------------
CHARACTERS = {
    "ALEX": {
        "name": "Alex Vance",
        "rank": "Master Sergeant",
        "service": "Active Duty — Infantry / Operations Specialist",
        "background": "Married with children; spouse managed domestic operations and household decisions through multiple long combat deployments.",
        "challenge": "Translating direct leadership into consensus-driven corporate culture; renegotiating household authority and overcoming military cultural stoicism.",
        "stats": {"OT": 45, "RC": 40, "SNI": 50}
    },
    "MORGAN": {
        "name": "Morgan Ellis",
        "rank": "Captain",
        "service": "Active Duty — Logistics & Supply Chain Officer",
        "background": "Dual-career household (no children); partner holds a demanding corporate leadership position in a major city.",
        "challenge": "Re-aligning executive expectations (managing large military operational budgets vs. corporate office politics); balancing partner's career priorities with transition friction.",
        "stats": {"OT": 60, "RC": 45, "SNI": 40}
    }
}

# Initialize Session State
if "state" not in st.session_state:
    st.session_state.state = "CHAR_SELECT"
if "char_key" not in st.session_state:
    st.session_state.char_key = None
if "path" not in st.session_state:
    st.session_state.path = []
if "stats" not in st.session_state:
    st.session_state.stats = {"OT": 50, "RC": 50, "SNI": 50}

def apply_choice(ot_change, rc_change, sni_change, next_node, choice_id):
    st.session_state.stats["OT"] = max(0, min(100, st.session_state.stats["OT"] + ot_change))
    st.session_state.stats["RC"] = max(0, min(100, st.session_state.stats["RC"] + rc_change))
    st.session_state.stats["SNI"] = max(0, min(100, st.session_state.stats["SNI"] + sni_change))
    st.session_state.path.append(choice_id)
    st.session_state.state = next_node
    st.rerun()

# -----------------------------------------------------------------------------
# SIDEBAR DASHBOARD
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🎖️ MVS 100 UnFinal")
    st.markdown("**Author:** Austin T. Dodd")
    st.markdown("**Course:** Intro to Veteran Studies")
    st.markdown("**Instructor:** Professor Goff")
    st.divider()

    if st.session_state.char_key:
        char = CHARACTERS[st.session_state.char_key]
        st.markdown(f"### 📋 Active Dossier: {char['name']}")
        st.markdown(f"""
        <div class='dossier-card'>
            <b>Rank:</b> {char['rank']}<br>
            <b>Service:</b> {char['service']}<br><br>
            <b>Context:</b> {char['background']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Transition Metrics")
        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric("Operational", f"{st.session_state.stats['OT']}%")
        col_s2.metric("Relational", f"{st.session_state.stats['RC']}%")
        col_s3.metric("System Nav", f"{st.session_state.stats['SNI']}%")
        st.caption("OT: Operational Translation | RC: Relational Cohesion | SNI: System Navigation")
        st.divider()

    if st.button("🔄 Reset Simulation", use_container_width=True):
        st.session_state.state = "CHAR_SELECT"
        st.session_state.char_key = None
        st.session_state.path = []
        st.session_state.stats = {"OT": 50, "RC": 50, "SNI": 50}
        st.rerun()

# -----------------------------------------------------------------------------
# SCREEN 1: CHARACTER SELECTION
# -----------------------------------------------------------------------------
if st.session_state.state == "CHAR_SELECT":
    st.markdown('<p class="main-header">OPERATION CIVILIAN RE-ENTRY</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">An Interactive 24-Month Reintegration Simulation</p>', unsafe_allow_html=True)
    st.divider()

    st.subheader("Select a Service Member Dossier")
    st.markdown("Choose a subject to guide through their 24-month post-discharge transition journey:")

    cols = st.columns(2)
    for idx, (key, char) in enumerate(CHARACTERS.items()):
        with cols[idx]:
            st.markdown(f"### {char['name']}")
            st.write(f"**{char['rank']}** — *{char['service']}*")
            st.info(f"**Background:** {char['background']}")
            st.warning(f"**Key Challenge:** {char['challenge']}")
            
            if st.button(f"Select {char['name'].split()[0]}", key=f"sel_{key}", use_container_width=True, type="primary"):
                st.session_state.char_key = key
                st.session_state.stats = char['stats'].copy()
                st.session_state.state = "NODE_1"
                st.rerun()

# -----------------------------------------------------------------------------
# NODE 1: MONTH 1 — ADMINISTRATIVE & IMMEDIATE SEPARATION
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_1":
    char = CHARACTERS[st.session_state.char_key]
    st.progress(0.14, text="Node 1 of 7: Month 1 — Immediate Separation & Priorities")
    st.header(f"Month 1: The Administrative Handshake — {char['name']}")
    
    st.markdown("""
    <div class='scenario-card'>
    It is Week 2 post-discharge. Your active-duty service is complete, and your official discharge papers are in hand. 
    You receive a notification from the VA stating that your military electronic health records require manual verification before your primary care team can be assigned, creating a 60-day administrative delay.<br><br>
    Simultaneously, household setup, financial budgeting, and initial corporate networking opportunities demand your immediate focus.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("How do you allocate your primary focus during this first month?")

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("<div class='choice-title'>Option A</div>", unsafe_allow_html=True)
        st.write("Spend dedicated morning hours coordinating with veteran advocates, tracking medical verification queues, and securing official service documentation before taking on new external commitments.")
        if st.button("Select Option A", key="n1_a", use_container_width=True):
            apply_choice(ot_change=-5, rc_change=-5, sni_change=20, next_node="NODE_2", choice_id="1A")

    with c2:
        st.markdown("<div class='choice-title'>Option B</div>", unsafe_allow_html=True)
        st.write("Channel your energy into submitting corporate applications, attending virtual networking events, and interviewing, letting administrative records process in the background.")
        if st.button("Select Option B", key="n1_b", use_container_width=True):
            apply_choice(ot_change=20, rc_change=-5, sni_change=-10, next_node="NODE_2", choice_id="1B")

    with c3:
        st.markdown("<div class='choice-title'>Option C</div>", unsafe_allow_html=True)
        st.write("Prioritize home life, partner alignment, and establishing household routines during the first month, taking time to decompress before committing to rigid application or paperwork schedules.")
        if st.button("Select Option C", key="n1_c", use_container_width=True):
            apply_choice(ot_change=-10, rc_change=20, sni_change=-5, next_node="NODE_2", choice_id="1C")

# -----------------------------------------------------------------------------
# NODE 2: MONTH 3 — EARLY RELATIONSHIP & HOUSEHOLD DYNAMICS
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_2":
    char = CHARACTERS[st.session_state.char_key]
    st.progress(0.28, text="Node 2 of 7: Month 3 — Household Role Renegotiation")
    
    st.markdown("""
    <div class='citation-box'>
        <h4>🔬 Academic Citation & Research Analysis</h4>
        <b>Source: Schuetz (1945) — Homecoming Theory / Demers (2011)</b><br><br>
        Reintegration is relational rather than isolated. Schuetz's <i>Homecoming Theory</i> demonstrates that both the returning service member 
        and their home community evolve independently during separation. When a veteran returns, established household routines must be renegotiated. 
        Assuming the household can instantly resume past patterns or adapt to military-style domestic management leads to subtle marital friction.
    </div>
    """, unsafe_allow_html=True)

    st.header(f"Month 3: Domestic Boundaries & Expectations — {char['name']}")
    
    st.markdown("""
    <div class='scenario-card'>
    You have been home for ninety days. During your active service deployments, your partner managed all daily domestic choices, finances, and household logistics independently.<br><br>
    Lately, friction arises over daily routines and decision-making authority. After a disagreement regarding household schedules, your partner remarks that you are treating the home like a military unit rather than a shared partnership.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("How do you respond to this domestic friction?")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("<div class='choice-title'>Option A</div>", unsafe_allow_html=True)
        st.write("Step back from domestic management entirely, leaving daily decisions to your partner while focusing strictly on your personal work or job search tasks.")
        if st.button("Select Option A", key="n2_a", use_container_width=True):
            apply_choice(ot_change=5, rc_change=-15, sni_change=0, next_node="NODE_3", choice_id="2A")

    with c2:
        st.markdown("<div class='choice-title'>Option B</div>", unsafe_allow_html=True)
        st.write("Initiate a structured weekly household check-in where both you and your partner explicitly map out responsibilities, financial goals, and personal expectations.")
        if st.button("Select Option B", key="n2_b", use_container_width=True):
            apply_choice(ot_change=0, rc_change=20, sni_change=5, next_node="NODE_3", choice_id="2B")

    with c3:
        st.markdown("<div class='choice-title'>Option C</div>", unsafe_allow_html=True)
        st.write("Keep your internal stress private and avoid discussing household roles further, believing that time and routine will naturally smooth out the tension.")
        if st.button("Select Option C", key="n2_c", use_container_width=True):
            apply_choice(ot_change=0, rc_change=-20, sni_change=-5, next_node="NODE_3", choice_id="2C")

# -----------------------------------------------------------------------------
# NODE 3: MONTH 6 — WORKPLACE INTEGRATION & COMMUNICATION
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_3":
    char = CHARACTERS[st.session_state.char_key]
    st.progress(0.42, text="Node 3 of 7: Month 6 — Corporate Culture & Team Friction")

    st.markdown("""
    <div class='citation-box'>
        <h4>🔬 Academic Citation & Research Analysis</h4>
        <b>Source: Zoli, Maury, & Fay (2015) — IVMF / Syracuse University</b><br><br>
        Research indicates that military operational culture relies on rapid, direct communication, precise SOPs, and absolute command responsibility. 
        In civilian corporate spaces, this directness frequently clashes with norms centered on consensus-building and indirect feedback. 
        The inability of civilian HR systems to translate military leadership assets—combined with veteran frustration over corporate ambiguity—creates 
        a primary barrier to long-term post-service employment retention.
    </div>
    """, unsafe_allow_html=True)

    st.header(f"Month 6: The Project Review — {char['name']}")
    
    st.markdown("""
    <div class='scenario-card'>
    You are six months into your new corporate position. During a major cross-functional meeting, a key project deadline slips because two department leads disagree on resource allocation.<br><br>
    Your manager turns to you and asks how you would align the team to resolve the impasse and keep deliverables moving forward.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("<div class='choice-title'>Option A</div>", unsafe_allow_html=True)
        st.write("Establish a formal project tracking matrix with clear, documented ownership for every task, scheduling a joint review session where team leads publicly account for roadblocks.")
        if st.button("
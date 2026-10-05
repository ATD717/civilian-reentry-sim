import streamlit as st

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Operation Civilian Re-Entry | MVS 100",
    page_icon="🎖️",
    layout="wide",
)

st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 800; color: #1E293B; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; color: #64748B; margin-bottom: 20px; }
    .citation-box {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border-left: 5px solid #3B82F6;
        padding: 18px 22px;
        border-radius: 6px;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    .citation-box h4 { color: #60A5FA !important; margin-top: 0px; }
    .dossier-card {
        background-color: #0F172A;
        color: #F8FAFC;
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CHARACTER DEFINITIONS (All Active Duty, Gender-Neutral Names)
# -----------------------------------------------------------------------------
CHARACTERS = {
    "ALEX": {
        "name": "Alex Vance",
        "rank": "Gunnery Sergeant / SFC (E-7)",
        "service": "12 Years Active Duty — Infantry / Operations",
        "background": "Married with children; spouse managed domestic operations through multiple combat deployments.",
        "challenge": "Translating direct command leadership into consensus-driven corporate culture; renegotiating household authority and overcoming military stoicism.",
        "stats": {"OT": 45, "RC": 40, "SNI": 50}
    },
    "JORDAN": {
        "name": "Jordan Harper",
        "rank": "Specialist / Corporal (E-4)",
        "service": "4 Years Active Duty — Cyber Intelligence Analysis",
        "background": "Single, transitioning into a major urban technology hub away from primary family networks.",
        "challenge": "Navigating corporate ambiguity and underemployment; building a non-military peer network from scratch without established family infrastructure.",
        "stats": {"OT": 55, "RC": 50, "SNI": 35}
    },
    "MORGAN": {
        "name": "Morgan Ellis",
        "rank": "Captain (O-3)",
        "service": "6 Years Active Duty — Logistics & Supply Chain Officer",
        "background": "Dual-career household (no children); partner holds a demanding corporate leadership position.",
        "challenge": "Re-aligning executive expectations (managing large military budgets vs. entry-level corporate politics); balancing partner's career priorities with transition friction.",
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
        <div class="dossier-card">
            <b>Rank/Branch:</b> {char['rank']}<br>
            <b>Service:</b> {char['service']}<br>
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
    st.markdown('<p class="sub-header">A 24-Month Interactive Transition Simulation</p>', unsafe_allow_html=True)
    st.divider()

    st.subheader("Select a Service Member Dossier")
    st.markdown("Choose a subject to guide through their 24-month post-discharge transition journey:")

    cols = st.columns(3)
    for idx, (key, char) in enumerate(CHARACTERS.items()):
        with cols[idx]:
            st.markdown(f"### {char['name']}")
            st.write(f"**{char['rank']}**")
            st.write(f"*{char['service']}*")
            st.info(char['background'])
            st.warning(f"**Key Challenge:** {char['challenge']}")
            
            if st.button(f"Select {char['name'].split()[0]}", key=f"sel_{key}", use_container_width=True, type="primary"):
                st.session_state.char_key = key
                st.session_state.stats = char['stats'].copy()
                st.session_state.state = "PHASE_1"
                st.rerun()

# -----------------------------------------------------------------------------
# SCREEN 2: PHASE 1 (WEEKS 1–4 — DISCHARGE & SEPARATION)
# -----------------------------------------------------------------------------
elif st.session_state.state == "PHASE_1":
    char = CHARACTERS[st.session_state.char_key]
    st.progress(0.25, text="Phase 1/4: Immediate Separation (Weeks 1–4)")
    st.header(f"Phase 1: The Administrative & Relocation Handshake — {char['name']}")
    
    st.markdown("""
    **Setting:** Week 2 post-discharge. Your active-duty term is complete, and your DD-214 is in hand. 
    You are settling into your new residence when you receive a notification from the VA stating that your military electronic health records 
    require manual verification before your primary care team can be assigned, creating a 60-day backlog. 
    Meanwhile, household setup and career opportunities compete for your immediate focus.
    """)

    st.subheader("Decision Node 1: How do you prioritize your focus in the first 30 days?")

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("#### Option 1A: System & Structure Priority")
        st.write("Focus heavily on clearing the administrative backlog first. Spend dedicated morning hours coordinating with VSOs, tracking medical verification queues, and securing official documentation before taking on new external commitments.")
        if st.button("Choose 1A: System Priority", use_container_width=True):
            apply_choice(ot_change=-5, rc_change=-5, sni_change=20, next_node="PHASE_2_SYS", choice_id="1A")

    with c2:
        st.markdown("#### Option 1B: Workforce & Financial Momentum")
        st.write("Treat career placement as the urgent priority. Channel your energy into submitting job applications, attending networking calls, and interviewing, letting administrative processing run its course in the background.")
        if st.button("Choose 1B: Career Priority", use_container_width=True):
            apply_choice(ot_change=20, rc_change=-5, sni_change=-10, next_node="PHASE_2_EMP", choice_id="1B")

    with c3:
        st.markdown("#### Option 1C: Domestic & Relational Alignment")
        st.write("Focus primarily on home life, partner alignment, and establishing household routines during the first month, taking time to decompress before committing to rigid application or paperwork schedules.")
        if st.button("Choose 1C: Domestic Priority", use_container_width=True):
            apply_choice(ot_change=-10, rc_change=20, sni_change=-5, next_node="PHASE_2_DOM", choice_id="1C")

# -----------------------------------------------------------------------------
# SCREEN 3: PHASE 2 (MONTHS 2–6 — EMPLOYMENT & CULTURAL ADAPTATION)
# -----------------------------------------------------------------------------
elif st.session_state.state.startswith("PHASE_2"):
    char = CHARACTERS[st.session_state.char_key]
    st.progress(0.50, text="Phase 2/4: Employment & Cultural Adaptation (Months 2–6)")
    
    st.markdown("""
    <div class="citation-box">
        <h4>🔬 Academic Citation & Research Analysis</h4>
        <b>Source: Zoli, Maury, & Fay (2015) — IVMF / Syracuse University</b><br><br>
        Research indicates that military operational culture relies on rapid, direct communication, precise SOPs, and absolute command responsibility. 
        In civilian corporate spaces, this directness frequently clashes with norms centered on consensus-building and indirect feedback. 
        The inability of civilian HR systems to translate military leadership assets—combined with veteran frustration over corporate ambiguity—creates 
        a primary barrier to long-term post-service employment retention.
    </div>
    """, unsafe_allow_html=True)

    st.header(f"Phase 2: Corporate Integration & Team Dynamics — {char['name']}")
    
    st.markdown("""
    **Setting:** Month 4 Post-Discharge. You are in a cross-functional project meeting at your new workplace. 
    A key project milestone slipped because two department leads disagree on resource allocation and ownership. 
    The hiring manager/interviewer asks: *"How would you step in to align this team and keep the deliverable on track?"*
    """)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("#### Option 2A: Framework & Accountability Focus")
        st.write("Establish a formal project tracking matrix with clear, documented ownership for every task, scheduling a joint review session where team leads publicly walk through their commitments and roadblocks.")
        if st.button("Choose 2A: Framework Approach", use_container_width=True):
            apply_choice(ot_change=-10, rc_change=0, sni_change=5, next_node="PHASE_3_DIRECT", choice_id="2A")

    with c2:
        st.markdown("#### Option 2B: Relational & Diplomatic Focus")
        st.write("Hold informal, one-on-one alignment discussions with each department lead outside the main meeting to understand their individual constraints and co-create a compromise before updating the schedule.")
        if st.button("Choose 2B: Diplomatic Approach", use_container_width=True):
            apply_choice(ot_change=20, rc_change=10, sni_change=0, next_node="PHASE_3_CONSENSUS", choice_id="2B")

    with c3:
        st.markdown("#### Option 2C: Role Boundaries & Execution Focus")
        st.write("Focus on delivering your assigned components ahead of schedule while providing clear technical status updates to leadership, letting the project owner manage stakeholder friction.")
        if st.button("Choose 2C: Execution Approach", use_container_width=True):
            apply_choice(ot_change=-15, rc_change=-10, sni_change=-5, next_node="PHASE_3_PASSIVE", choice_id="2C")

# -----------------------------------------------------------------------------
# SCREEN 4: PHASE 3 (MONTHS 7–12 — DOMESTIC & COMMUNITY RE-ENTRY)
# -----------------------------------------------------------------------------
elif st.session_state.state.startswith("PHASE_3"):
    char = CHARACTERS[st.session_state.char_key]
    st.progress(0.75, text="Phase 3/4: Social & Community Adjustment (Months 7–12)")

    st.markdown("""
    <div class="citation-box">
        <h4>🔬 Academic Citation & Research Analysis</h4>
        <b>Source: Schuetz (1945) / Demers (2011) / Smith & True (2014)</b><br><br>
        Reintegration is relational, not isolated. Schuetz's <i>Homecoming Theory</i> notes that both the returning service member 
        and the home community evolve independently during separation. Military conditioning instills a 'cultural stoicism' and 
        collectivist bond that requires intentional renegotiation of domestic roles upon return to avoid long-term isolation or domestic strain.
    </div>
    """, unsafe_allow_html=True)

    st.header(f"Phase 3: Domestic & Social Adjustment — {char['name']}")
    
    st.markdown("""
    **Setting:** Month 9 Post-Discharge. Household and social routines have hit a plateau. 
    You notice that between work requirements and routine daily stress, you spend most of your free time decompressed alone or staying in touch with distant service friends online, 
    leading to subtle disconnects in local social and family life.
    """)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("#### Option 3A: Self-Reliant Space & Composure")
        st.write("Manage your personal stress independently through daily personal routines and quiet time, protecting your family and coworkers from your internal frustration while maintaining daily stability.")
        if st.button("Choose 3A: Self-Reliant Path", use_container_width=True):
            apply_choice(ot_change=0, rc_change=-20, sni_change=-10, next_node="PHASE_4_STOIC", choice_id="3A")

    with c2:
        st.markdown("#### Option 3B: Direct Personal Vulnerability")
        st.write("Initiate direct conversations with your partner or close family about your ongoing adjustment friction, proposing joint counseling or open family check-ins to recalibrate expectations together.")
        if st.button("Choose 3B: Vulnerability Path", use_container_width=True):
            apply_choice(ot_change=5, rc_change=25, sni_change=10, next_node="PHASE_4_OPEN", choice_id="3B")

    with c3:
        st.markdown("#### Option 3C: External Community & Shared Purpose")
        st.write("Channel your weekend energy into structured local civic projects or community service organizations, building a new network of peers through shared, action-oriented goals.")
        if st.button("Choose 3C: Civic Path", use_container_width=True):
            apply_choice(ot_change=10, rc_change=15, sni_change=15, next_node="PHASE_4_CIVIC", choice_id="3C")

# -----------------------------------------------------------------------------
# SCREEN 5: PHASE 4 & FINAL DEBRIEF (MONTHS 13–24)
# -----------------------------------------------------------------------------
elif st.session_state.state.startswith("PHASE_4"):
    char = CHARACTERS[st.session_state.char_key]
    st.progress(1.00, text="Phase 4/4: Long-Term Identity & Reintegration (Months 13–24)")

    st.markdown("""
    <div class="citation-box">
        <h4>🔬 Academic Citation & Research Analysis</h4>
        <b>Source: Mobbs & Bonanno (2018) / Romaniuk et al. (2020)</b><br><br>
        Mobbs & Bonanno argue that much of what is pathologized as clinical PTSD is actually 'transition stress'—an existential crisis 
        triggered by losing one's primary institution, social status, and structured purpose. Successful 24-month reintegration relies 
        on identity reconstruction outside military uniform constraints.
    </div>
    """, unsafe_allow_html=True)

    st.header(f"Month 24 After Action Report (AAR) — {char['name']}")
    st.divider()

    st.subheader("Final Transition Profile")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    col_f1.metric("Operational Translation", f"{st.session_state.stats['OT']}%")
    col_f2.metric("Relational Cohesion", f"{st.session_state.stats['RC']}%")
    col_f3.metric("System Navigation", f"{st.session_state.stats['SNI']}%")

    st.markdown("### Decision Trajectory Path")
    st.code(" ➔ ".join(["START"] + st.session_state.path))

    st.markdown("### Cumulative Academic Synthesis")
    
    ot_score = st.session_state.stats["OT"]
    rc_score = st.session_state.stats["RC"]
    sni_score = st.session_state.stats["SNI"]

    st.write(f"**Subject:** {char['name']} ({char['rank']})")
    
    if ot_score >= 60:
        st.success("**Workforce Domain:** Highly successful translation of military skill sets into civilian corporate value. Minimal friction regarding authority structures.")
    else:
        st.warning("**Workforce Domain:** Experiencing ongoing organizational ambiguity or underemployment friction. Indicates a need for better employer onboarding systems (*Zoli et al., 2015*).")

    if rc_score >= 60:
        st.success("**Domestic & Social Domain:** Strong relational cohesion established. Successfully negotiated role shifts and overcome military cultural stoicism (*Demers, 2011; Schuetz, 1945*).")
    else:
        st.error("**Domestic & Social Domain:** High social isolation or domestic strain noted. Highlights the risk of unaddressed military cultural stoicism (*Smith & True, 2014*).")

    if sni_score >= 60:
        st.success("**System Navigation & Identity Domain:** Proactive institutional navigation. Successfully established long-term healthcare access and reconstructed identity (*Mobbs & Bonanno, 2018*).")
    else:
        st.warning("**System Navigation & Identity Domain:** Administrative exhaustion or disengagement from DOD/VA support systems noted.")

    st.divider()
    st.subheader("Verified Academic References")
    st.markdown("""
    * **Demers, A. (2011).** When veterans return: The role of community in post-combat reintegration. *Journal of Loss and Trauma*, 16(2), 160–179.
    * **Mobbs, M. C., & Bonanno, G. A. (2018).** Beyond war and PTSD: The crucial role of transition stress in the lives of military veterans. *Clinical Psychology Review*, 59, 137–144.
    * **Romaniuk, M., et al. (2020).** Assessing psychological adjustment and cultural reintegration after military service (M-CARM). *BMC Psychiatry*, 20(1), 1–13.
    * **Schuetz, A. (1945).** The homecomer. *American Journal of Sociology*, 50(5), 369–376.
    * **Smith, R. T., & True, G. (2014).** Warring identities: Identity conflict and the military-to-civilian transition. *Armed Forces & Society*, 40(1), 147–156.
    * **Zoli, C., Maury, R., & Fay, D. (2015).** *Missing perspectives: Servicemembers' transition from service to civilian life*. Institute for Veterans and Military Families, Syracuse University.
    """)

    if st.button("🔄 Restart Simulation with Another Character", type="primary"):
        st.session_state.state = "CHAR_SELECT"
        st.session_state.char_key = None
        st.session_state.path = []
        st.session_state.stats = {"OT": 50, "RC": 50, "SNI": 50}
        st.rerun()
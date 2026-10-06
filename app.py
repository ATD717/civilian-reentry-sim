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
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CHARACTER DEFINITIONS & 4-METRIC TRACKING (Career, Social/Rel, Community, Identity)
# -----------------------------------------------------------------------------
CHARACTERS = {
    "ALEX": {
        "name": "Alex Vance",
        "rank": "Master Sergeant",
        "service": "Active Duty — Infantry / Operations Specialist",
        "background": "Married with children; spouse managed domestic operations and household decisions through multiple long combat deployments.",
        "challenge": "Translating direct leadership into consensus-driven corporate culture; renegotiating household authority and overcoming military cultural stoicism.",
        "stats": {"CT": 45, "SR": 40, "CE": 40, "SI": 50}
    },
    "MORGAN": {
        "name": "Morgan Ellis",
        "rank": "Captain",
        "service": "Active Duty — Logistics & Supply Chain Officer",
        "background": "Dual-career household (no children); partner holds a demanding corporate leadership position in a major city.",
        "challenge": "Re-aligning executive expectations (managing large military operational budgets vs. corporate office politics); balancing partner's career priorities with transition friction.",
        "stats": {"CT": 60, "SR": 45, "CE": 35, "SI": 45}
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
    st.session_state.stats = {"CT": 50, "SR": 50, "CE": 50, "SI": 50}

def apply_choice(ct_change, sr_change, ce_change, si_change, next_node, choice_id):
    st.session_state.stats["CT"] = max(0, min(100, st.session_state.stats["CT"] + ct_change))
    st.session_state.stats["SR"] = max(0, min(100, st.session_state.stats["SR"] + sr_change))
    st.session_state.stats["CE"] = max(0, min(100, st.session_state.stats["CE"] + ce_change))
    st.session_state.stats["SI"] = max(0, min(100, st.session_state.stats["SI"] + si_change))
    st.session_state.path.append(choice_id)
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

    if st.session_state.char_key:
        char = CHARACTERS[st.session_state.char_key]
        st.markdown(f"### 📋 Dossier: {char['name']}")
        st.write(f"**Rank:** {char['rank']}")
        st.write(f"**Service:** {char['service']}")
        st.divider()
        
        st.markdown("### 📊 4-Domain Metrics")
        st.metric("Career Translation (CT)", f"{st.session_state.stats['CT']}%")
        st.metric("Social & Rel. (SR)", f"{st.session_state.stats['SR']}%")
        st.metric("Community Eng. (CE)", f"{st.session_state.stats['CE']}%")
        st.metric("Self-Identity (SI)", f"{st.session_state.stats['SI']}%")
        st.divider()

    if st.button("🔄 Reset Simulation", use_container_width=True):
        st.session_state.state = "CHAR_SELECT"
        st.session_state.char_key = None
        st.session_state.path = []
        st.session_state.stats = {"CT": 50, "SR": 50, "CE": 50, "SI": 50}
        st.rerun()

# -----------------------------------------------------------------------------
# SCREEN 1: CHARACTER SELECTION & ACADEMIC FRAMEWORK
# -----------------------------------------------------------------------------
if st.session_state.state == "CHAR_SELECT":
    st.markdown("<div class='main-header'>OPERATION CIVILIAN RE-ENTRY</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>An Interactive 24-Month Reintegration Simulation & Research Model</div>", unsafe_allow_html=True)
    
    with st.expander("📖 View Research Question, Thesis & Academic Framework", expanded=True):
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
# NODE 1: MONTH 2 — SELF-IDENTITY & UNIFORM SEPARATION (New Self-Identity Question)
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_1":
    char = CHARACTERS[st.session_state.char_key]
    st.progress(0.16, text="Node 1 of 6: Month 2 — Self-Identity & Uniform Separation")
    
    st.warning("**🔬 Academic Citation & Research Analysis**\n\n*Source: Smith & True (2014) — Warring Identities*\n\nTransitioning out of a total military institution triggers a psychological friction between martial self-concept and civilian individualism. Reconstructing a stable post-identity requires confronting the immediate loss of rank, title, and mission.")

    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.header(f"Month 2: Stripping the Uniform — {char['name']}")
    with h_col2:
        if st.button("⬅ Back to Dossiers"):
            st.session_state.state = "CHAR_SELECT"
            st.rerun()
            
    st.info("You have been out of uniform for two months. Stripped of your rank insignia and daily operational structure, you find yourself answering civilian acquaintances with vague descriptions of your past service. You feel an internal loss of purpose and professional validation.")

    st.subheader("How do you handle the initial loss of identity and structure?")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Option A")
        st.write("Isolate yourself socially, relying solely on your own internal discipline to push through the transition without seeking external validation or veteran networks.")
        if st.button("Select Option A", key="n1_a", use_container_width=True):
            apply_choice(ct_change=0, sr_change=-10, ce_change=-10, si_change=-15, next_node="NODE_2", choice_id="1A")

    with c2:
        st.markdown("### Option B")
        st.write("Connect proactively with a local veteran mentorship group to openly discuss the psychological shift of leaving service and redefine your personal core values.")
        if st.button("Select Option B", key="n1_b", use_container_width=True):
            apply_choice(ct_change=5, sr_change=10, ce_change=15, si_change=20, next_node="NODE_2", choice_id="1B")

    with c3:
        st.markdown("### Option C")
        st.write("Immerse yourself immediately in civilian recreational hobbies and casual entertainment to distract yourself from thinking about your military past.")
        if st.button("Select Option C", key="n1_c", use_container_width=True):
            apply_choice(ct_change=5, sr_change=0, ce_change=0, si_change=5, next_node="NODE_2", choice_id="1C")

# -----------------------------------------------------------------------------
# NODE 2: MONTH 4 — SOCIAL RELATIONSHIPS & HOUSEHOLD ROLE RENEGOTIATION
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_2":
    char = CHARACTERS[st.session_state.char_key]
    st.progress(0.33, text="Node 2 of 6: Month 4 — Household Role Renegotiation")
    
    st.warning("**🔬 Academic Citation & Research Analysis**\n\n*Source: Schuetz (1945) / Demers (2011)*\n\nSchuetz's Homecoming theory demonstrates that home is not a static haven. Spouses and partners have adapted to manage household operations independently during deployments, requiring active relational role renegotiation.")

    st.header(f"Month 4: Domestic Boundaries & Expectations — {char['name']}")
    st.info("Four months post-discharge, friction arises over household routines. Your partner notes that you are attempting to manage domestic life like a military unit rather than an equal partnership.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Option A")
        st.write("Step back from domestic choices entirely, leaving all decisions to your partner while focusing strictly on personal job applications.")
        if st.button("Select Option A", key="n2_a", use_container_width=True):
            apply_choice(ct_change=5, sr_change=-15, ce_change=0, si_change=-5, next_node="NODE_3", choice_id="2A")

    with c2:
        st.markdown("### Option B")
        st.write("Initiate a structured weekly household check-in where both you and your partner explicitly map out responsibilities, financial goals, and personal expectations.")
        if st.button("Select Option B", key="n2_b", use_container_width=True):
            apply_choice(ct_change=0, sr_change=20, ce_change=5, si_change=10, next_node="NODE_3", choice_id="2B")

    with c3:
        st.markdown("### Option C")
        st.write("Keep your internal stress private and avoid discussing household roles further, believing time will naturally smooth out the tension.")
        if st.button("Select Option C", key="n2_c", use_container_width=True):
            apply_choice(ct_change=0, sr_change=-20, ce_change=-5, si_change=-10, next_node="NODE_3", choice_id="2C")

# -----------------------------------------------------------------------------
# NODE 3: MONTH 8 — CAREER & WORKPLACE COMMUNICATION
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_3":
    char = CHARACTERS[st.session_state.char_key]
    st.progress(0.50, text="Node 3 of 6: Month 8 — Corporate Culture & Team Friction")
    
    st.warning("**🔬 Academic Citation & Research Analysis**\n\n*Source: Zoli, Maury, & Fay (2015)*\n\nMilitary operational culture relies on direct communication and SOPs. In civilian corporate spaces, this often clashes with consensus-building and indirect office politics.")

    st.header(f"Month 8: The Project Deadlock — {char['name']}")
    st.info("Eight months into your civilian career, a major cross-functional project stalls because two department leads disagree on resource allocation. Your manager asks for your approach.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Option A")
        st.write("Issue a formal project tracking matrix with rigid deadlines and public accountability check-ins for all department leads.")
        if st.button("Select Option A", key="n3_a", use_container_width=True):
            apply_choice(ct_change=-10, sr_change=-5, ce_change=0, si_change=5, next_node="NODE_4", choice_id="3A")

    with c2:
        st.markdown("### Option B")
        st.write("Hold informal, one-on-one alignment discussions with each leader outside meetings to understand constraints and co-create a compromise.")
        if st.button("Select Option B", key="n3_b", use_container_width=True):
            apply_choice(ct_change=25, sr_change=10, ce_change=10, si_change=10, next_node="NODE_4", choice_id="3B")

    with c3:
        st.markdown("### Option C")
        st.write("Focus strictly on your own deliverables, letting the project owner manage stakeholder friction without your direct intervention.")
        if st.button("Select Option C", key="n3_c", use_container_width=True):
            apply_choice(ct_change=-15, sr_change=0, ce_change=-5, si_change=-5, next_node="NODE_4", choice_id="3C")

# -----------------------------------------------------------------------------
# NODE 4: MONTH 12 — COMMUNITY ENGAGEMENT & CIVIC SERVICE (New Community Question)
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_4":
    char = CHARACTERS[st.session_state.char_key]
    st.progress(0.66, text="Node 4 of 6: Month 12 — Community Embedding & Civic Service")
    
    st.warning("**🔬 Academic Citation & Research Analysis**\n\n*Source: Demers (2011) — Community Reintegration*\n\nCivilian community networks often lack cultural competency regarding military service, leading to isolation. Active civic engagement and local community embedding are critical for bridging this gap.")

    st.header(f"Month 12: Local Embedding — {char['name']}")
    st.info("One year post-discharge, you realize your life is split strictly between your workplace and your immediate household. You feel disconnected from your broader local town/city community.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Option A")
        st.write("Volunteer to lead a local youth mentorship or community resilience program, translating your leadership skills into civic action.")
        if st.button("Select Option A", key="n4_a", use_container_width=True):
            apply_choice(ct_change=10, sr_change=10, ce_change=25, si_change=15, next_node="NODE_5", choice_id="4A")

    with c2:
        st.markdown("### Option B")
        st.write("Join an exclusively veteran-focused social club online, keeping your local civic engagement minimal and staying within familiar military circles.")
        if st.button("Select Option B", key="n4_b", use_container_width=True):
            apply_choice(ct_change=0, sr_change=5, ce_change=10, si_change=10, next_node="NODE_5", choice_id="4B")

    with c3:
        st.markdown("### Option C")
        st.write("Decline all local civic involvement to focus entirely on personal relaxation and weekend recovery from work stress.")
        if st.button("Select Option C", key="n4_c", use_container_width=True):
            apply_choice(ct_change=0, sr_change=-5, ce_change=-20, si_change=-10, next_node="NODE_5", choice_id="4C")

# -----------------------------------------------------------------------------
# NODE 5: MONTH 18 — SYSTEM NAVIGATION & HEALTHCARE
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_5":
    char = CHARACTERS[st.session_state.char_key]
    st.progress(0.83, text="Node 5 of 6: Month 18 — Institutional System Navigation")
    
    st.warning("**🔬 Academic Citation & Research Analysis**\n\n*Source: Mobbs & Bonanno (2018)*\n\nAdministrative delays in benefits and healthcare processing compound everyday transition stress. Proactive institutional navigation is essential for long-term stability.")

    st.header(f"Month 18: VA & Healthcare Bureaucracy — {char['name']}")
    st.info("At 18 months, an audit reveals that your service-connected disability claim was stalled due to electronic medical record transfer errors between DOD and VA systems.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Option A")
        st.write("Take time off work to personally coordinate with accredited VSOs and congressional liaison offices to resolve your claim file.")
        if st.button("Select Option A", key="n5_a", use_container_width=True):
            apply_choice(ct_change=-5, sr_change=5, ce_change=10, si_change=15, next_node="NODE_6", choice_id="5A")

    with c2:
        st.markdown("### Option B")
        st.write("Submit a standard online portal inquiry and wait for standard bureaucratic processing queues to clear.")
        if st.button("Select Option B", key="n5_b", use_container_width=True):
            apply_choice(ct_change=5, sr_change=0, ce_change=0, si_change=0, next_node="NODE_6", choice_id="5B")

    with c3:
        st.markdown("### Option C")
        st.write("Abandon the claim process out of frustration, deciding the administrative friction is not worth the effort.")
        if st.button("Select Option C", key="n5_c", use_container_width=True):
            apply_choice(ct_change=0, sr_change=-5, ce_change=-10, si_change=-20, next_node="NODE_6", choice_id="5C")

# -----------------------------------------------------------------------------
# NODE 6: MONTH 24 — FINAL DEBRIEF & 4-DOMAIN AAR EVALUATION
# -----------------------------------------------------------------------------
elif st.session_state.state == "NODE_6":
    char = CHARACTERS[st.session_state.char_key]
    st.progress(1.00, text="Node 6 of 6: Month 24 — Reintegration Evaluation")

    st.warning("**🔬 Academic Citation & Research Analysis**\n\n*Source: Synthesis of Course Research (Zoli et al., Schuetz, Demers, Mobbs & Bonanno)*\n\nTwo years post-discharge marks a critical stabilization milestone. Reintegration success is measured across workforce contribution, relational cohesion, community embedding, and self-identity.")

    st.header(f"Month 24 After Action Report (AAR) — {char['name']}")
    st.divider()

    st.subheader("Final 4-Domain Transition Scores")
    
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    col_f1.metric("Career (CT)", f"{st.session_state.stats['CT']}%")
    col_f2.metric("Social/Rel. (SR)", f"{st.session_state.stats['SR']}%")
    col_f3.metric("Community (CE)", f"{st.session_state.stats['CE']}%")
    col_f4.metric("Self-Identity (SI)", f"{st.session_state.stats['SI']}%")

    st.markdown("### Decision Trajectory Path")
    st.code(" ➔ ".join(["START"] + st.session_state.path))

    st.markdown("### Comprehensive Academic Synthesis & Findings")
    
    ct_score = st.session_state.stats["CT"]
    sr_score = st.session_state.stats["SR"]
    ce_score = st.session_state.stats["CE"]
    si_score = st.session_state.stats["SI"]

    st.write(f"**Subject Dossier:** {char['name']} ({char['rank']})")
    
    if ct_score >= 60:
        st.success("**Career & Operational Translation (CT):** High proficiency in translating military proficiencies into civilian corporate value. Successfully navigated corporate cultural ambiguity (*Zoli et al., 2015*).")
    else:
        st.warning("**Career & Operational Translation (CT):** Experiencing ongoing underemployment friction or corporate cultural mismatch.")

    if sr_score >= 60:
        st.success("**Social & Relationships (SR):** Strong domestic and social cohesion established. Successfully renegotiated household roles and overcame military stoicism (*Schuetz, 1945; Demers, 2011*).")
    else:
        st.error("**Social & Relationships (SR):** Elevated social isolation or household strain identified.")

    if ce_score >= 60:
        st.success("**Community Engagement (CE):** Effective local civic embedding. Established strong community ties beyond insular veteran circles (*Demers, 2011*).")
    else:
        st.warning("**Community Engagement (CE):** Low community embedding; at risk of social alienation from civilian neighbors.")

    if si_score >= 60:
        st.success("**Self-Identity & Purpose (SI):** Successfully resolved 'warring identities' and established a stable post-service self-concept independent of military rank (*Smith & True, 2014*).")
    else:
        st.warning("**Self-Identity & Purpose (SI):** Unresolved identity displacement; ongoing struggle with post-service purpose.")

    st.divider()
    st.subheader("Verified APA References")
    st.markdown("""* **Demers, A. (2011).** When veterans return: The role of community in post-combat reintegration. *Journal of Loss and Trauma*, 16(2), 160–179.
- **Mobbs, M. C., & Bonanno, G. A. (2018).** Beyond war and PTSD: The crucial role of transition stress in the lives of military veterans. *Clinical Psychology Review*, 59, 137–144.
- **Romaniuk, M., et al. (2020).** Assessing psychological adjustment and cultural reintegration after military service (M-CARM). *BMC Psychiatry*, 20(1), 1–13.
- **Schuetz, A. (1945).** The homecomer. *American Journal of Sociology*, 50(5), 369–376.
- **Smith, R. T., & True, G. (2014).** Warring identities: Identity conflict and the military-to-civilian transition. *Armed Forces & Society*, 40(1), 147–156.
- **Zoli, C., Maury, R., & Fay, D. (2015).** *Missing perspectives: Servicemembers' transition from service to civilian life*. Institute for Veterans and Military Families, Syracuse University.""")

    if st.button("🔄 Restart Simulation with Another Character", type="primary", use_container_width=True):
        st.session_state.state = "CHAR_SELECT"
        st.session_state.char_key = None
        st.session_state.path = []
        st.session_state.stats = {"CT": 50, "SR": 50, "CE": 50, "SI": 50}
        st.rerun()
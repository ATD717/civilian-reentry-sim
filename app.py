import streamlit as st

# Set page layout and title
st.set_page_config(
    page_title="Operation Civilian Re-Entry | MVS 100",
    page_icon="🎖️",
    layout="wide",
)

# Custom Styling for Academic Callouts and Dossier Cards
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 20px;
    }
    .citation-box {
        background-color: #F8FAFC;
        border-left: 5px solid #2563EB;
        padding: 15px 20px;
        border-radius: 4px;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    .dossier-card {
        background-color: #0F172A;
        color: #F8FAFC;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State Variables
if "node" not in st.session_state:
    st.session_state.node = "START"
if "history" not in st.session_state:
    st.session_state.history = {}

# -----------------------------------------------------------------------------
# SIDEBAR: PROJECT OVERVIEW & METADATA
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🎖️ UnFinal Project")
    st.markdown("**Course:** MVS 100 — Intro to Veteran Studies")
    st.markdown("**Author:** Austin T. Dodd")
    st.markdown("**Instructor:** Professor Goff")
    st.markdown("**Date:** September 13, 2026")
    st.divider()
    
    st.markdown("### 📋 Character Dossier")
    st.markdown("""
    <div class="dossier-card">
        <b>Subject:</b> SFC / GySgt Alex Vance<br>
        <b>Service:</b> 12 Years Active Duty<br>
        <b>Specialty:</b> Combat Arms / Operations<br>
        <b>Status:</b> 30 Days Post-Discharge<br>
        <b>Objective:</b> Navigate employment, domestic dynamics, VA systems, and identity shift.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Reset Simulation"):
        st.session_state.node = "START"
        st.session_state.history = {}
        st.rerun()

# -----------------------------------------------------------------------------
# MAIN CONTENT AREA
# -----------------------------------------------------------------------------

# --- NODE: START ---
if st.session_state.node == "START":
    st.markdown('<p class="main-header">OPERATION CIVILIAN RE-ENTRY</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">An Interactive Transition Simulation</p>', unsafe_allow_html=True)
    st.divider()

    st.subheader("Central Research Question")
    st.info(
        "\"How do the operational, cultural, and psychological experiences of military "
        "service shape a veteran's post-service reintegration across their employment, "
        "social relationships, community engagement, and self-identity?\""
    )

    st.markdown("""
    ### Executive Summary & Simulation Overview
    The transition from military service to civilian life represents a profound ontological shift—moving an 
    individual from an institutionalized collective structure grounded in shared mission, hierarchy, and hyper-vigilance 
    to a decentralized, individualistic society.

    By participating in this interactive simulation, you will guide **SFC / GySgt Alex Vance** through critical 
    post-discharge decision nodes. Each decision illustrates how military conditioning interacts with civilian 
    workforce, family, and administrative environments.
    """)

    if st.button("🚀 Initialize Simulation", type="primary", use_container_width=True):
        st.session_state.node = "NODE_1"
        st.rerun()

# --- NODE 1: EMPLOYMENT ---
elif st.session_state.node == "NODE_1":
    st.progress(0.25, text="Phase 1/4: Employment & Operational Translation")
    st.header("Node 1: The First Job Interview")
    st.caption("Setting: Corporate Office | Position: Project Manager | 60 Days Post-Discharge")

    st.markdown("""
    You sit across from three civilian HR managers. You have managed multi-million-dollar equipment 
    inventories and led personnel in high-stakes operational environments. The lead interviewer smiles and asks:

    > **"Can you tell us about a time a project failed, who was at fault, and how you handled team conflict?"**
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Option A: Direct Operational Response")
        st.write(
            "\"A logistics plan failed because a junior leader failed to follow the SOP. "
            "I called an immediate After Action Review (AAR), addressed the breakdown directly, "
            "and re-established strict oversight protocols.\""
        )
        if st.button("Select Option A", key="n1_a", use_container_width=True):
            st.session_state.history["node1"] = "A"
            st.session_state.node = "NODE_2A"
            st.rerun()

    with col2:
        st.subheader("Option B: Adapted Civilian Response")
        st.write(
            "\"Unforeseen friction happened when a timeline slipped due to supply chain delays. "
            "Rather than placing individual blame, I worked with the team to identify process gaps "
            "and implemented a collaborative tracking tool.\""
        )
        if st.button("Select Option B", key="n1_b", use_container_width=True):
            st.session_state.history["node1"] = "B"
            st.session_state.node = "NODE_2B"
            st.rerun()

# --- NODE 2A: WORKPLACE AFTERMATH (DIRECT PATH) ---
elif st.session_state.node == "NODE_2A":
    st.progress(0.40, text="Phase 1/4: Employment & Operational Translation")
    st.header("Node 2A: Workplace Aftermath (Direct Path)")

    st.markdown("""
    <div class="citation-box">
        <h4>🔬 Academic Citation & Research Analysis</h4>
        <b>Source: Zoli, Maury, & Fay (2015) — IVMF / Syracuse University</b><br><br>
        Military operational culture relies on rapid, direct communication, precise SOPs, and absolute command responsibility. 
        In civilian corporate spaces, this directness frequently clashes with norms centered on consensus-building and indirect feedback. 
        The inability of civilian HR systems to translate military leadership—combined with veteran frustration over corporate ambiguity—creates 
        a primary barrier to long-term job retention.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **Current Status:** Hired, but experiencing organizational friction | 90 Days Post-Discharge
    
    Your team views your management style as 'intimidating' and 'overly rigid.' During a staff meeting, 
    coworkers debate a minor deadline for two hours without resolution. You know clear execution steps 
    could solve it in five minutes.
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Intervene Decisively: Take the whiteboard and assign tasks directly.", use_container_width=True):
            st.session_state.node = "NODE_3"
            st.rerun()
    with col2:
        if st.button("Step Back & Disengage: Stay silent and let the committee debate.", use_container_width=True):
            st.session_state.node = "NODE_3"
            st.rerun()

# --- NODE 2B: WORKPLACE AFTERMATH (ADAPTED PATH) ---
elif st.session_state.node == "NODE_2B":
    st.progress(0.40, text="Phase 1/4: Employment & Operational Translation")
    st.header("Node 2B: Workplace Aftermath (Adapted Path)")

    st.markdown("""
    <div class="citation-box">
        <h4>🔬 Academic Citation & Research Analysis</h4>
        <b>Source: Zoli, Maury, & Fay (2015) — IVMF / Syracuse University</b><br><br>
        Adapting communication styles helps bridge the initial hiring gap. However, research demonstrates that even when 
        veterans successfully navigate civilian interview expectations, underlying operational habits and expectations of clear 
        institutional purpose can lead to long-term cognitive friction in low-stakes workplace environments.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **Current Status:** Hired, navigating cultural adaptation | 90 Days Post-Discharge
    
    You adapted your communication, but struggle internally with a lack of clear mission focus. Your coworkers spend 
    lunch complaining about minor office policy updates. Having managed high-risk operations, you find it difficult to care 
    about low-stakes workplace grievances.
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Build External Veteran Networks: Seek local civic groups after hours.", use_container_width=True):
            st.session_state.node = "NODE_3"
            st.rerun()
    with col2:
        if st.button("Attempt to Educate Peers: Share military operational perspectives.", use_container_width=True):
            st.session_state.node = "NODE_3"
            st.rerun()

# --- NODE 3: HOMECOMING & DOMESTIC DYNAMICS ---
elif st.session_state.node == "NODE_3":
    st.progress(0.75, text="Phase 2/4: Social & Domestic Cultural Pillar")
    st.header("Node 3: The Homecoming & Domestic Dynamics")
    st.caption("Setting: Family Living Room | 6 Months Post-Discharge")

    st.markdown("""
    During your 12 years of service, your family established independent household routines. You find yourself 
    trying to run the home like a military unit—expecting immediate compliance, strict schedules, and emotional stoicism.

    At dinner, an argument breaks out over a minor routine. Your spouse states:
    > **"You aren't in command here anymore, and we aren't your squad."**
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Option A: Maintain Cultural Stoicism")
        st.write("Withdraw emotionally to your garage or office, feeling misunderstood by your family.")
        if st.button("Select Option A", key="n3_a", use_container_width=True):
            st.session_state.history["node3"] = "A"
            st.session_state.node = "NODE_4"
            st.rerun()

    with col2:
        st.subheader("Option B: Embrace Vulnerability")
        st.write("Admit you are struggling to turn off your operational mindset and ask how to re-integrate into family roles.")
        if st.button("Select Option B", key="n3_b", use_container_width=True):
            st.session_state.history["node3"] = "B"
            st.session_state.node = "NODE_4"
            st.rerun()

# --- NODE 4: ADMINISTRATIVE & PSYCHOLOGICAL JUNCTION ---
elif st.session_state.node == "NODE_4":
    st.progress(0.90, text="Phase 3/4: Identity Pillar & Federal Policy")
    st.header("Node 4: Administrative & Psychological Junction")

    st.markdown("""
    <div class="citation-box">
        <h4>🔬 Academic Citation & Research Analysis</h4>
        <b>Source: Schuetz (1945) / Demers (2011) / Smith & True (2014)</b><br><br>
        Reintegration is relational, not isolated. Schuetz's <i>Homecoming Theory</i> notes that both the returning service member 
        and the home community evolve independently during separation. Military conditioning instills a 'cultural stoicism' and 
        collectivist bond that requires intentional renegotiation of domestic roles upon return to avoid long-term marital strain.
    </div>
    """, unsafe_allow_html=True)

    st.caption("Setting: VA Regional Medical Center | 9 Months Post-Discharge")
    st.markdown("""
    You are establishing service-connected healthcare. Your DOD electronic medical records failed to transfer 
    seamlessly into the VA database, causing a 90-day administrative delay. Passed between three desks, you face administrative 
    exhaustion and a loss of identity.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Option A: Institutional Self-Advocacy")
        st.write("Utilize VSOs, congressional channels, and formal appeals to navigate the system.")
        if st.button("Select Option A", key="n4_a", use_container_width=True):
            st.session_state.node = "DEBRIEF"
            st.rerun()

    with col2:
        st.subheader("Option B: Disillusioned Disengagement")
        st.write("Walk out, deciding the administrative barrier is not worth the hassle.")
        if st.button("Select Option B", key="n4_b", use_container_width=True):
            st.session_state.node = "DEBRIEF"
            st.rerun()

# --- NODE: DEBRIEF & SYNTHESIS ---
elif st.session_state.node == "DEBRIEF":
    st.progress(1.00, text="Phase 4/4: Debrief & Final Synthesis")
    st.header("After Action Report: Synthesis & Findings")

    st.markdown("""
    <div class="citation-box">
        <h4>🔬 Academic Citation & Research Analysis</h4>
        <b>Source: Mobbs & Bonanno (2018) / Romaniuk et al. (2020)</b><br><br>
        Mobbs & Bonanno argue that much of what is pathologized as clinical PTSD is actually 'transition stress'—an existential crisis 
        triggered by losing one's primary institution, social status, and structured purpose. When administrative friction in the DOD-to-VA 
        pipeline disrupts healthcare and benefits access, it compounds economic instability and accelerates social withdrawal.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Cumulative Findings Across the Four Pillars")
    
    st.markdown("""
    1. **Employment (Operational):** Reintegration requires mutual translation. Veterans must adapt operational directness into civilian collaborative communication, while employers must build onboarding systems that recognize non-traditional military assets (*Zoli et al., 2015*).
    2. **Social Dynamics (Cultural):** Overcoming post-service isolation requires dismantling military cultural stoicism and recognizing family units as co-transitioners undergoing role renegotiation (*Schuetz, 1945; Demers, 2011*).
    3. **Community (Civic):** Veterans thrive when placed in structured, high-purpose civic environments that replicate the collective camaraderie of military service without requiring uniform constraints (*Romaniuk et al., 2020*).
    4. **Identity & Policy (Psychological/Administrative):** Society must resist medicalizing all transition stress as clinical pathology, focusing instead on identity reconstruction outside a total institution (*Mobbs & Bonanno, 2018; Smith & True, 2014*). Federal policy must streamline the DOD-to-VA electronic records transition to ensure stability during the critical first year post-service.
    """)

    st.divider()
    st.subheader("Verified References")
    st.markdown("""
    * **Demers, A. (2011).** When veterans return: The role of community in post-combat reintegration. *Journal of Loss and Trauma*, 16(2), 160–179.
    * **Mobbs, M. C., & Bonanno, G. A. (2018).** Beyond war and PTSD: The crucial role of transition stress in the lives of military veterans. *Clinical Psychology Review*, 59, 137–144.
    * **Romaniuk, M., et al. (2020).** Assessing psychological adjustment and cultural reintegration after military service (M-CARM). *BMC Psychiatry*, 20(1), 1–13.
    * **Schuetz, A. (1945).** The homecomer. *American Journal of Sociology*, 50(5), 369–376.
    * **Smith, R. T., & True, G. (2014).** Warring identities: Identity conflict and the military-to-civilian transition. *Armed Forces & Society*, 40(1), 147–156.
    * **Zoli, C., Maury, R., & Fay, D. (2015).** *Missing perspectives: Servicemembers' transition from service to civilian life*. Institute for Veterans and Military Families, Syracuse University.
    """)

    if st.button("🔄 Restart Simulation"):
        st.session_state.node = "START"
        st.session_state.history = {}
        st.rerun()
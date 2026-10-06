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
# NODE 1: MONTH 2 — SELF-IDENTITY & UNIFORM SEPARATION
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
# NODE 3: MONTH 8 — CARE
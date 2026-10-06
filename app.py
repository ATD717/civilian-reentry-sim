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
    /* Fixed height flexbox cards to align buttons evenly */
    .choice-card-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        height: 280px; /* Uniform height for alignment */
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
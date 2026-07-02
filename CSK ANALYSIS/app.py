import streamlit as st
from utils.helpers import inject_css
from utils.loader import load_players

# Page configuration must be the first command
st.set_page_config(
    page_title="CSK AI Strategy Lab",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified CSS styling
inject_css()

# Custom sidebar header rendering
st.sidebar.markdown("""
<div style="text-align: center; padding: 1.25rem 0.5rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 1rem;">
    <h2 style="color: #FFD305; font-size: 1.45rem; font-weight: 800; margin: 0 0 4px 0; text-transform: uppercase; letter-spacing: 0.03em;">CSK AI STRATEGY LAB</h2>
    <span style="color: #9CA3AF; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; font-weight: 500;">Pre-IPL 2026 Strategy Center</span>
</div>
""", unsafe_allow_html=True)

# Navigation definition with logical groupings
pg = st.navigation({
    "Core Analysis": [
        st.Page("pages/Dashboard.py", title="Analyst Dashboard", icon="📊"),
        st.Page("pages/Squad_Analysis.py", title="Squad Overview", icon="👥"),
        st.Page("pages/Player_Form.py", title="Player Form Analysis", icon="📈")
    ],
    "Tactical Planning": [
        st.Page("pages/Opponent_Analysis.py", title="Opponent Analysis", icon="🎯"),
        st.Page("pages/Venue_Analysis.py", title="Venue Analysis", icon="🏟️"),
        st.Page("pages/Playing_XI.py", title="AI Playing XI Generator", icon="🏏"),
        st.Page("pages/Strategy_Center.py", title="Strategy Center", icon="🧠")
    ],
    "Simulations & Reports": [
        st.Page("pages/Win_Prediction.py", title="Win Prediction Simulator", icon="🔮"),
        st.Page("pages/Coach_Report.py", title="Coach Tactical Report", icon="📋"),
        st.Page("pages/Settings.py", title="Dashboard Settings", icon="⚙️")
    ]
})

pg.run()

# Simple footer in the sidebar
st.sidebar.markdown("""
<div style="position: fixed; bottom: 10px; width: 220px; text-align: center; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 10px;">
    <span style="color: #52525b; font-size: 0.65rem; font-family: monospace;">v1.0.0-PROD | CSK AI Labs © 2026</span>
</div>
""", unsafe_allow_html=True)

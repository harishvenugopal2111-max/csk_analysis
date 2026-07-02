import streamlit as st
import pandas as pd
from utils.loader import get_venue_details
from utils.prediction import generate_playing_xi
from utils.helpers import section_header, status_badge

section_header("AI Playing XI Generator", "Generate specialized squad configurations dynamically matching match conditions")

# Input Controls Panel
st.markdown("""
<div style="background: rgba(13, 20, 38, 0.5); padding: 1rem 1.25rem; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 1.5rem;">
    <div style="font-size: 0.75rem; color: #9CA3AF; text-transform: uppercase; font-weight: 600; margin-bottom: 0.75rem;">Tactical Match Conditions</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    opponents = ["RCB", "MI", "GT", "SRH", "KKR", "RR", "PBKS", "DC", "LSG"]
    selected_opp = st.selectbox("Opponent Team", opponents)
with c2:
    venues = ["Chepauk (Chennai)", "Wankhede (Mumbai)", "Chinnaswamy (Bengaluru)", "Narendra Modi Stadium (Ahmedabad)"]
    selected_venue = st.selectbox("Select Venue", venues)
with c3:
    pitch_types = ["Balanced", "Spin Friendly", "Green / Pace Friendly", "Flat / Batting Friendly"]
    selected_pitch = st.selectbox("Pitch Condition", pitch_types)
with c4:
    weather_types = ["Sunny", "Overcast", "Humid / Dew", "Windy"]
    selected_weather = st.selectbox("Expected Weather", weather_types)

st.markdown("</div>", unsafe_allow_html=True)

# Generate Playing XI
xi = generate_playing_xi(selected_opp, selected_venue, selected_pitch, selected_weather)

# Render Captain & Vice Captain
st.markdown(f"""
<div style="display: flex; gap: 15px; margin-bottom: 1.5rem;">
    <div style="background: rgba(255, 211, 5, 0.1); border: 1px solid rgba(255, 211, 5, 0.4); padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.85rem; color: #FFD305; font-weight: 600;">
        👑 CAPTAIN: {xi['captain']}
    </div>
    <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.4); padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.85rem; color: #3B82F6; font-weight: 600;">
        🛡️ VICE-CAPTAIN: {xi['vice_captain']}
    </div>
</div>
""", unsafe_allow_html=True)

# Rendering the XI roles in cards
def render_player_group(title, subtitle, icon, players_list):
    st.markdown(f"""
    <div class="chart-wrap" style="margin-bottom: 1.25rem;">
        <div class="chart-title">{icon} {title}</div>
        <div class="chart-subtitle">{subtitle}</div>
        <div style="display: flex; flex-direction: column; gap: 0.85rem; margin-top: 0.5rem;">
    """, unsafe_allow_html=True)
    
    for p in players_list:
        st.markdown(f"""
        <div style="display: flex; align-items: flex-start; gap: 12px; padding: 0.75rem; background: rgba(0,0,0,0.12); border-radius: 8px; border: 1px solid rgba(255,255,255,0.03);">
            <div style="font-weight: 700; color: #FFD305; font-size: 0.85rem; min-width: 140px;">
                {p['player']}
            </div>
            <div style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.3;">
                {p['reason']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div></div>", unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    render_player_group("Opening Combination", "Aggressive start and balance", "⚡", xi["openers"])
    render_player_group("Middle Order", "Anchor play and spin counter-attacks", "🛡️", xi["middle_order"])
    render_player_group("Finishers", "Death overs hitting and boundary clearing", "🔥", xi["finishers"])

with col_right:
    render_player_group("Spin Bowlers", "Middle-overs restriction and carrom secrets", "🌀", xi["spinners"])
    render_player_group("Fast Bowlers", "New-ball swing and death-overs yorkers", "🚀", xi["pacers"])
    
    # Impact Player rendering
    impact_p = xi["impact_player"]
    st.markdown(f"""
    <div class="chart-wrap" style="border-color: rgba(16, 185, 129, 0.35);">
        <div class="chart-title" style="color: #10B981;">🔄 IMPACT PLAYER NOMINEE</div>
        <div class="chart-subtitle">Tactical substitution candidate based on match state</div>
        <div style="display: flex; align-items: flex-start; gap: 12px; padding: 0.75rem; background: rgba(16, 185, 129, 0.08); border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.25);">
            <div style="font-weight: 700; color: #10B981; font-size: 0.85rem; min-width: 140px;">
                {impact_p['player']}
            </div>
            <div style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.3;">
                {impact_p['reason']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

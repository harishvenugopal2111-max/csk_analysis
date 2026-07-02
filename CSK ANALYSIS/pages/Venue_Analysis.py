import streamlit as st
import pandas as pd
from utils.loader import get_venue_details
from utils.helpers import section_header, metric_card, status_badge
from utils.charts import plot_boundary_dimension_chart

section_header("Venue Strategic Analysis", "Assess boundary dimensions, pitch behavior, and squad adaptation")

# Dropdown
venues = [
    "Chepauk (Chennai)",
    "Wankhede (Mumbai)",
    "Chinnaswamy (Bengaluru)",
    "Narendra Modi Stadium (Ahmedabad)"
]
selected_venue = st.selectbox("Select Match Venue", venues)

# Load venue data
meta = get_venue_details(selected_venue)

# KPI row
c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Avg 1st Innings Score", f"{meta['FirstInnAvg']}", is_yellow=True)
with c2:
    metric_card("Avg Winning Score", f"{meta['WinScore']}", delta="Chasing target benchmark")
with c3:
    metric_card("Batting First Win %", f"{meta['BatFirstWin']}%", delta_type="up" if meta['BatFirstWin'] >= 50 else "down")
with c4:
    metric_card("Chasing Win %", f"{meta['ChaseWin']}%", delta_type="up" if meta['ChaseWin'] >= 50 else "down")

st.markdown("<br>", unsafe_allow_html=True)

# Grid Layout: Boundary & Pitch analysis
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-title">🏟️ Boundary Dimensions (meters)</div>
        <div class="chart-subtitle">Polar mapping of key fence distances</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(plot_boundary_dimension_chart(meta), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown(f"""
    <div class="chart-wrap" style="height: 100%;">
        <div class="chart-title">⚖️ Pitch & Bowling Assist Index</div>
        <div class="chart-subtitle">Evaluation of ball behavior and spin vs pace splits</div>
        <div style="margin-top: 1rem; margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 5px;">
                <span>Spin Friendliness</span><span style="color: #FFD305; font-weight: 700;">{meta['SpinPct']}%</span>
            </div>
            <div style="background: rgba(255,255,255,0.05); height: 8px; border-radius: 4px;">
                <div style="background: #FFD305; width: {meta['SpinPct']}%; height: 100%; border-radius: 4px;"></div>
            </div>
        </div>
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 5px;">
                <span>Pace Friendliness</span><span style="color: #3B82F6; font-weight: 700;">{meta['PacePct']}%</span>
            </div>
            <div style="background: rgba(255,255,255,0.05); height: 8px; border-radius: 4px;">
                <div style="background: #3B82F6; width: {meta['PacePct']}%; height: 100%; border-radius: 4px;"></div>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.15); padding: 1rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); font-size: 0.825rem; line-height: 1.4; margin-bottom: 1rem;">
            <strong>Pitch Profile:</strong><br>
            <span style="color: var(--text-muted);">{meta['PitchDesc']}</span>
        </div>
        
        <div style="background: rgba(0,0,0,0.15); padding: 1rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); font-size: 0.825rem; line-height: 1.4;">
            <strong>Recommended Bowling Style:</strong><br>
            <span style="color: #10B981; font-weight: 600;">{meta['RecommendedBowling']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Recommended Playing XI section
section_header("Recommended Squad for Venue", "Selected roster based on venue attributes")
st.markdown("""
<div class="chart-wrap">
    <div class="chart-title">🏏 Tactical Playing XI</div>
    <div class="chart-subtitle">Tailored combinations for ground dimensions and bounce heights</div>
    <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 0.5rem;">
""", unsafe_allow_html=True)

rec_xi_list = meta["RecommendedXI"]
for p in rec_xi_list:
    role_label = "Batter"
    if "C" in p:
        bg = "yellow"
    elif "WK" in p:
        bg = "blue"
    else:
        bg = "blue"
    st.markdown(status_badge(p, bg), unsafe_allow_html=True)

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

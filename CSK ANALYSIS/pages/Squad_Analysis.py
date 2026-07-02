import streamlit as st
import pandas as pd
from utils.loader import load_players
from utils.helpers import section_header, custom_table, status_badge
from utils.charts import plot_role_distribution, plot_age_distribution

# Load players
players_df = load_players()

section_header("Squad Analysis", "Comprehensive view of the Chennai Super Kings squad candidates for IPL 2026")

# Filters
st.markdown("""
<div style="background: rgba(13, 20, 38, 0.5); padding: 1rem 1.25rem; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 1.5rem;">
    <div style="font-size: 0.75rem; color: #9CA3AF; text-transform: uppercase; font-weight: 600; margin-bottom: 0.75rem;">Interactive Filters</div>
""", unsafe_allow_html=True)

# Streamlit columns for filter controls
f1, f2, f3 = st.columns(3)
with f1:
    roles_list = ["All Roles"] + list(players_df["Role"].unique())
    selected_role = st.selectbox("Filter by Playing Role", roles_list)
with f2:
    nats_list = ["All Nationalities", "Indian", "Overseas"]
    selected_nat = st.selectbox("Filter by Nationality", nats_list)
with f3:
    age_range = st.slider("Select Age Range", 18, 45, (18, 45))

st.markdown("</div>", unsafe_allow_html=True)

# Apply filters
filtered_df = players_df.copy()
if selected_role != "All Roles":
    filtered_df = filtered_df[filtered_df["Role"] == selected_role]
if selected_nat != "All Nationalities":
    filtered_df = filtered_df[filtered_df["Nationality"] == selected_nat]
filtered_df = filtered_df[(filtered_df["Age"] >= age_range[0]) & (filtered_df["Age"] <= age_range[1])]

# Squad Table Card
st.markdown("""
<div class="chart-wrap">
    <div class="chart-title">👥 CSK Current Candidate Squad</div>
    <div class="chart-subtitle">Listing matching squad players, styles, and career milestones</div>
""", unsafe_allow_html=True)

# Format table data
table_df = filtered_df.copy()
# Create custom rendering mapping
formats = {
    "Nationality": lambda val: status_badge("Overseas", "yellow") if val == "Overseas" else status_badge("Indian", "blue"),
    "Strike Rate": lambda val: f"{val:.1f}" if val > 0 else "-",
    "Economy": lambda val: f"{val:.2f}" if val > 0 else "-"
}

custom_table(
    table_df, 
    columns_map={
        "Player": "Player Name",
        "Role": "Playing Role",
        "Age": "Age",
        "Batting Style": "Batting",
        "Bowling Style": "Bowling",
        "Nationality": "Nat.",
        "Experience": "IPL Exp",
        "Career Runs": "Runs",
        "Career Wickets": "Wkts",
        "Strike Rate": "S/R",
        "Economy": "Econ"
    },
    formats=formats
)
st.markdown("</div>", unsafe_allow_html=True)

# Squad Distributions
st.markdown("<br>", unsafe_allow_html=True)
section_header("Squad Distributions & Balance", "Visualizing squad proportions")

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-title">🏏 Role Distribution</div>
        <div class="chart-subtitle">Count of players divided by role class</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(plot_role_distribution(players_df), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-title">📅 Age Profile Distribution</div>
        <div class="chart-subtitle">Count of players divided into age brackets</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(plot_age_distribution(players_df), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# AI Strength & Weakness Analysis
st.markdown("<br>", unsafe_allow_html=True)
section_header("AI Squad Strategy Report", "Automated roster balance insights")

c_strength, c_weakness = st.columns(2)

with c_strength:
    st.markdown("""
    <div class="alert-box alert-success">
        <h4 style="color: #10B981; margin: 0 0 8px 0; font-weight: 700;">🟢 Core Squad Strengths</h4>
        <ul style="color: #F3F4F6; font-size: 0.825rem; margin: 0; padding-left: 1.2rem;">
            <li style="margin-bottom: 6px;"><strong>All-round versatility:</strong> Possessing multiple elite all-rounders (Jadeja, Dube, Rachin, Moeen) offers immense depth, allowing CSK to play 8-9 batsmen.</li>
            <li style="margin-bottom: 6px;"><strong>Spin Bowling Control:</strong> Left-arm orthodox spinners (Jadeja, Santner) and mystery spinner (Theekshana) offer outstanding economy, especially at Chepauk.</li>
            <li style="margin-bottom: 6px;"><strong>Finishing Experience:</strong> The finishing duo of MS Dhoni and Ravindra Jadeja remains highly formidable in clutch situations.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with c_weakness:
    st.markdown("""
    <div class="alert-box alert-info" style="border-color: rgba(239, 68, 68, 0.25);">
        <h4 style="color: #EF4444; margin: 0 0 8px 0; font-weight: 700;">🔴 Core Squad Weaknesses</h4>
        <ul style="color: #F3F4F6; font-size: 0.825rem; margin: 0; padding-left: 1.2rem;">
            <li style="margin-bottom: 6px;"><strong>Ageing core players:</strong> Key strategists (Dhoni 44, Moeen 38, Jadeja 37) require careful workload management during hot schedules.</li>
            <li style="margin-bottom: 6px;"><strong>New Ball Pace Reliance:</strong> The new-ball swing is heavily reliant on Deepak Chahar. Any injury creates a vulnerability in taking early powerplay wickets.</li>
            <li style="margin-bottom: 6px;"><strong>Lack of Wrist Spin:</strong> The squad lacks a frontline leg-spinner, relying heavily on finger and carrom spin.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np
from utils.loader import load_matches, load_deliveries, load_players
from utils.helpers import metric_card, section_header
from utils.charts import (
    plot_season_performance, plot_runs_trend, 
    plot_wickets_trend, plot_team_comparison, plot_winning_percentage
)

# Load data
matches_df = load_matches()
deliveries_df = load_deliveries()
players_df = load_players()

# Title/Header
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(0, 43, 102, 0.45) 0%, rgba(13, 20, 38, 0.9) 100%); padding: 1.5rem 2rem; border-radius: 12px; border-left: 5px solid #FFD305; margin-bottom: 2rem;">
    <div style="font-size: 0.8rem; color: #FFD305; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em;">Welcome Coach & Strategy Staff</div>
    <h1 style="font-size: 2.15rem; font-weight: 800; color: #F3F4F6; margin: 0.2rem 0 0.5rem 0;">CSK AI Strategy Lab</h1>
    <p style="color: #9CA3AF; margin: 0; font-size: 0.88rem; max-width: 800px;">
        Simulating core team metrics, player profiles, and predictive matches model before the IPL 2026 campaign. Select tabs in the sidebar to review tactical matchups and venue parameters.
    </p>
</div>
""", unsafe_allow_html=True)

# ----------------- DATA COMPUTATIONS -----------------
csk_matches = matches_df[(matches_df["team1"] == "CSK") | (matches_df["team2"] == "CSK")]
total_matches = len(csk_matches)
total_wins = len(csk_matches[csk_matches["winner"] == "CSK"])
win_pct = round((total_wins / total_matches) * 100, 1) if total_matches > 0 else 0.0

# Average Scores
scores = []
for idx, row in csk_matches.iterrows():
    if row["team1"] == "CSK":
        scores.append(row["team1_score"])
    else:
        scores.append(row["team2_score"])
avg_score = round(np.mean(scores), 1) if scores else 0.0

# Powerplay & Death Score Computations
csk_batting = deliveries_df[deliveries_df["batting_team"] == "CSK"]
pp_deliveries = csk_batting[csk_batting["over"] < 6]
death_deliveries = csk_batting[csk_batting["over"] >= 16]

# PP runs = runs_off_bat + extras
pp_runs_per_match = pp_deliveries.groupby("match_id").apply(lambda x: x["runs_off_bat"].sum() + x["extras"].sum())
avg_pp_score = round(pp_runs_per_match.mean(), 1) if not pp_runs_per_match.empty else 0.0

death_runs_per_match = death_deliveries.groupby("match_id").apply(lambda x: x["runs_off_bat"].sum() + x["extras"].sum())
avg_death_score = round(death_runs_per_match.mean(), 1) if not death_runs_per_match.empty else 0.0

# Bowling economy
csk_bowling = deliveries_df[deliveries_df["bowling_team"] == "CSK"].copy()
csk_bowling["bowler_runs"] = csk_bowling["runs_off_bat"]
# Add wides/noballs to bowler runs
csk_bowling.loc[(csk_bowling["wides"] > 0) | (csk_bowling["noballs"] > 0), "bowler_runs"] += csk_bowling["extras"]

total_bowler_runs = csk_bowling["bowler_runs"].sum()
# Exclude wide balls from overs count
legal_balls = csk_bowling[csk_bowling["wides"] == 0]["ball"].count()
avg_economy = round((total_bowler_runs / legal_balls) * 6, 2) if legal_balls > 0 else 0.0

# ----------------- LAYOUT -----------------
section_header("Key Performance Metrics", "Overall performance figures across seasons 2021-2025")

# KPI row 1
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    metric_card("Total Matches", total_matches, is_yellow=True)
with kpi2:
    metric_card("Matches Won", total_wins, delta=f"+{total_wins} matches")
with kpi3:
    metric_card("Win Percentage", f"{win_pct}%", delta="Target: >60.0%", delta_type="up" if win_pct >= 55 else "down")
with kpi4:
    metric_card("Overall Avg Score", f"{avg_score} runs")

# KPI row 2
kpi5, kpi6, kpi7, kpi8 = st.columns(4)
with kpi5:
    metric_card("Avg Powerplay Score", f"{avg_pp_score}", delta="Ideal: 48.0+", delta_type="up" if avg_pp_score >= 45 else "down")
with kpi6:
    metric_card("Avg Death Score", f"{avg_death_score}", delta="Ideal: 55.0+", delta_type="up" if avg_death_score >= 52 else "down")
with kpi7:
    metric_card("Bowling Economy", f"{avg_economy}", delta="Ideal: <8.20", delta_type="up" if avg_economy <= 8.2 else "down")
with kpi8:
    squad_size = len(players_df)
    overseas_count = len(players_df[players_df["Nationality"] == "Overseas"])
    metric_card("Squad overview", f"{squad_size} Players", delta=f"{overseas_count} Overseas Candidates", delta_type="warn")

st.markdown("<br>", unsafe_allow_html=True)

# Grid Layout: Upcoming Match, Recent Form & Strength Meters
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown("""
    <div class="chart-wrap" style="height: 100%;">
        <div class="chart-title">🏟️ Upcoming Match Preview</div>
        <div class="chart-subtitle">Fixture 1 (Pre-season Strategy)</div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 1.5rem; background: rgba(0,0,0,0.15); border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.04);">
            <div style="text-align: center;">
                <span style="font-size: 1.8rem; font-weight: 700; color: #FFD305; display: block;">CSK</span>
                <span style="font-size: 0.72rem; color: #9CA3AF; text-transform: uppercase;">Chennai Super Kings</span>
            </div>
            <div style="text-align: center; border-left: 1px solid rgba(255,255,255,0.08); border-right: 1px solid rgba(255,255,255,0.08); padding: 0 2rem;">
                <span style="font-size: 0.95rem; font-weight: 700; color: #F3F4F6; display: block;">vs</span>
                <span style="font-size: 0.75rem; color: #10B981; font-weight: 600; display: block; margin-top: 5px;">CHEPAUK</span>
                <span style="font-size: 0.65rem; color: #9CA3AF;">IPL 2026 Season Opener</span>
            </div>
            <div style="text-align: center;">
                <span style="font-size: 1.8rem; font-weight: 700; color: #3B82F6; display: block;">MI</span>
                <span style="font-size: 0.72rem; color: #9CA3AF; text-transform: uppercase;">Mumbai Indians</span>
            </div>
        </div>
        <div style="margin-top: 1rem; font-size: 0.825rem; color: #9CA3AF;">
            <strong>Recent Head-to-Head Form:</strong> CSK has won 3 of the last 5 matches against Mumbai Indians.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="chart-wrap" style="height: 100%;">
        <div class="chart-title">⚖️ Team Strength & Weakness Index</div>
        <div class="chart-subtitle">AI Squad Evaluation (IPL 2026 Candidates)</div>
        <div style="margin-bottom: 0.8rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.78rem; margin-bottom: 3px;">
                <span>Powerplay Batting</span><span style="color: #10B981; font-weight: 600;">85% (Excellent)</span>
            </div>
            <div style="background: rgba(255,255,255,0.05); height: 6px; border-radius: 3px;">
                <div style="background: #10B981; width: 85%; height: 100%; border-radius: 3px;"></div>
            </div>
        </div>
        <div style="margin-bottom: 0.8rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.78rem; margin-bottom: 3px;">
                <span>Spin Containment (Middle Overs)</span><span style="color: #FFD305; font-weight: 600;">90% (Elite)</span>
            </div>
            <div style="background: rgba(255,255,255,0.05); height: 6px; border-radius: 3px;">
                <div style="background: #FFD305; width: 90%; height: 100%; border-radius: 3px;"></div>
            </div>
        </div>
        <div style="margin-bottom: 0.8rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.78rem; margin-bottom: 3px;">
                <span>Death Overs Yorks/Accuracy</span><span style="color: #FFD305; font-weight: 600;">78% (Strong)</span>
            </div>
            <div style="background: rgba(255,255,255,0.05); height: 6px; border-radius: 3px;">
                <div style="background: #FFD305; width: 78%; height: 100%; border-radius: 3px;"></div>
            </div>
        </div>
        <div>
            <div style="display: flex; justify-content: space-between; font-size: 0.78rem; margin-bottom: 3px;">
                <span>New Ball Swing Bowling</span><span style="color: #EF4444; font-weight: 600;">60% (Vulnerable)</span>
            </div>
            <div style="background: rgba(255,255,255,0.05); height: 6px; border-radius: 3px;">
                <div style="background: #EF4444; width: 60%; height: 100%; border-radius: 3px;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Visual Charts Section
section_header("Performance Analytics", "Visualizing matches data trends")

c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-title">📊 Season Win-Loss Record</div>
        <div class="chart-subtitle">Total matches played vs matches won and overall percentage</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(plot_season_performance(matches_df), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-title">📈 Scoring Runs Trend</div>
        <div class="chart-subtitle">CSK vs Opponent runs in last 15 matches</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(plot_runs_trend(matches_df), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-title">⚡ Bowler Wicket Trends & Economies</div>
        <div class="chart-subtitle">Top wicket-takers and their economy rates</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(plot_wickets_trend(deliveries_df), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-title">🛡️ Head-to-Head Comparison</div>
        <div class="chart-subtitle">CSK win share compared to major opponents</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(plot_team_comparison(matches_df), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

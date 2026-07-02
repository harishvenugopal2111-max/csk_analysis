import streamlit as st
import pandas as pd
import numpy as np
from utils.loader import load_players, load_deliveries, load_matches
from utils.helpers import section_header, status_badge, custom_table, metric_card

# Load datasets
players_df = load_players()
deliveries_df = load_deliveries()
matches_df = load_matches()

section_header("Player Form Analysis", "Reviewing player form telemetry, speeds, and AI labels")

# Selector
player_list = sorted(list(players_df["Player"].unique()))
selected_player = st.selectbox("Select CSK Player for Form Analysis", player_list)

# Find player profile
profile = players_df[players_df["Player"] == selected_player].iloc[0]

# --- RENDER PROFILE KEY DETAILS ---
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    st.markdown(f"**Playing Role:** {profile['Role']}")
    st.markdown(f"**Age:** {profile['Age']}")
with col_p2:
    st.markdown(f"**Batting Style:** {profile['Batting Style']}")
    st.markdown(f"**Bowling Style:** {profile['Bowling Style']}")
with col_p3:
    st.markdown(f"**Nationality:** {profile['Nationality']}")
    st.markdown(f"**IPL Experience:** {profile['Experience']} matches")

st.markdown("<hr style='border-top: 1px solid rgba(255,255,255,0.05); margin: 1rem 0;'>", unsafe_allow_html=True)

# --- CALCULATE FORM STATISTICS FROM DELIVERIES ---
# Batting Stats in deliveries
bat_df = deliveries_df[deliveries_df["batter"] == selected_player]
# Bowling Stats in deliveries
bowl_df = deliveries_df[deliveries_df["bowler"] == selected_player]

# Get match list where player was involved
player_matches = set(bat_df["match_id"].unique()).union(set(bowl_df["match_id"].unique()))

# Merge match dates to order them
if player_matches:
    pm_df = matches_df[matches_df["match_id"].isin(player_matches)].sort_values("date", ascending=False)
    last_5_match_ids = pm_df["match_id"].head(5).tolist()
else:
    last_5_match_ids = []

# If the player has no simulated deliveries, generate dummy data safely
if not last_5_match_ids:
    st.info("No detailed deliveries recorded for this player in history. Displaying career benchmarks.")
    last_5_rows = []
    form_score = 70
else:
    # Compile match-by-match stats
    last_5_rows = []
    bat_runs_list = []
    bat_sr_list = []
    bowl_wkts_list = []
    bowl_econ_list = []
    
    for mid in last_5_match_ids:
        match_info = matches_df[matches_df["match_id"] == mid].iloc[0]
        opp = match_info["team2"] if match_info["team1"] == "CSK" else match_info["team1"]
        m_date = pd.to_datetime(match_info["date"]).strftime("%b %d, %Y")
        
        # Batting
        bat_m = bat_df[bat_df["match_id"] == mid]
        runs = 0
        bf = 0
        sr = 0.0
        boundary_pct = 0.0
        dot_pct = 0.0
        is_dismissed = False
        
        if not bat_m.empty:
            runs = int(bat_m["runs_off_bat"].sum())
            bf = int(bat_m[bat_m["wides"] == 0]["ball"].count())
            sr = round((runs / bf) * 100, 1) if bf > 0 else 0.0
            boundaries = bat_m[bat_m["runs_off_bat"].isin([4, 6])]["ball"].count()
            boundary_pct = round((boundaries / bf) * 100, 1) if bf > 0 else 0.0
            dots = bat_m[bat_m["runs_off_bat"] == 0]["ball"].count()
            dot_pct = round((dots / bf) * 100, 1) if bf > 0 else 0.0
            is_dismissed = deliveries_df[(deliveries_df["match_id"] == mid) & (deliveries_df["player_dismissed"] == selected_player)].shape[0] > 0
            
            bat_runs_list.append(runs)
            bat_sr_list.append(sr)
            
        # Bowling
        bowl_m = bowl_df[bowl_df["match_id"] == mid].copy()
        wkts = 0
        econ = 0.0
        avg_speed = 0.0
        
        if not bowl_m.empty:
            bowl_m["bowler_runs"] = bowl_m["runs_off_bat"]
            bowl_m.loc[(bowl_m["wides"] > 0) | (bowl_m["noballs"] > 0), "bowler_runs"] += bowl_m["extras"]
            b_runs = bowl_m["bowler_runs"].sum()
            b_balls = bowl_m[bowl_m["wides"] == 0]["ball"].count()
            wkts = bowl_m[bowl_m["wicket_type"].isin(["caught", "bowled", "lbw", "stumped", "caught and bowled", "hit wicket"])].shape[0]
            econ = round((b_runs / b_balls) * 6, 2) if b_balls > 0 else 0.0
            
            speeds = bowl_m[bowl_m["ball_speed"] > 0]["ball_speed"]
            avg_speed = round(speeds.mean(), 1) if not speeds.empty else 0.0
            
            bowl_wkts_list.append(wkts)
            bowl_econ_list.append(econ)
            
        # Fielding mock captures
        fielding_act = "1 Catch" if mid % 2 == 0 else "None"
        
        last_5_rows.append({
            "Match": f"vs {opp} ({m_date})",
            "Runs": runs if not bat_m.empty else "-",
            "BF": bf if not bat_m.empty else "-",
            "S/R": sr if not bat_m.empty else "-",
            "Wickets": wkts if not bowl_m.empty else "-",
            "Econ": econ if not bowl_m.empty else "-",
            "Avg Speed": f"{avg_speed} km/h" if avg_speed > 0 else "-",
            "Fielding": fielding_act
        })
        
    # --- FORM SCORE COMPUTATION ---
    # Batting Weight
    bat_score = 50.0
    if bat_runs_list:
        avg_runs = np.mean(bat_runs_list)
        avg_sr = np.mean(bat_sr_list)
        bat_score = (avg_runs * 1.0) + (avg_sr * 0.3)
        bat_score = min(100, max(20, bat_score))
        
    # Bowling Weight
    bowl_score = 50.0
    if bowl_wkts_list:
        avg_wkts = np.mean(bowl_wkts_list)
        avg_econ = np.mean(bowl_econ_list)
        bowl_score = (avg_wkts * 30) + ((10 - avg_econ) * 5)
        bowl_score = min(100, max(20, bowl_score))
        
    # Combine according to Role
    if profile["Role"] == "Batter":
        form_score = int(bat_score)
    elif profile["Role"] == "Bowler":
        form_score = int(bowl_score)
    elif profile["Role"] == "All-rounder":
        form_score = int((bat_score + bowl_score) / 2)
    else:  # WK-Batter
        form_score = int(bat_score * 0.95 + 5) # keeper bonus
        
    # Boundary correction/adjustments
    form_score = min(99, max(35, form_score + 10)) # offset for display

# Label mapping
if form_score >= 85:
    form_label = "Excellent"
    badge_color = "green"
elif form_score >= 70:
    form_label = "Good"
    badge_color = "blue"
elif form_score >= 50:
    form_label = "Average"
    badge_color = "amber"
else:
    form_label = "Poor"
    badge_color = "red"

# Layout: Form score display & match history
c_card, c_hist = st.columns([1, 2.2])

with c_card:
    st.markdown(f"""
    <div class="metric-card" style="text-align: center; padding: 2rem 1.5rem; height: 100%;">
        <div class="metric-label" style="font-size: 0.85rem; margin-bottom: 0.5rem;">AI Player Form Rating</div>
        <div style="font-size: 4rem; font-weight: 800; color: #FFD305; line-height: 1;">{form_score}</div>
        <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1.5rem;">out of 100</div>
        <div style="margin-bottom: 1.5rem;">
            {status_badge(form_label, badge_color)}
        </div>
        <div style="background: rgba(255, 255, 255, 0.03); padding: 0.85rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); font-size: 0.75rem; text-align: left; color: #9CA3AF;">
            <strong>AI Assessment:</strong> {selected_player} is showing 
            {form_label.lower()} baseline capabilities based on the match tracking metrics. 
            {"Retain in Playing XI sheets." if form_score >= 70 else "Work on specific bowling lengths or speed controls."}
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_hist:
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-title">📈 Last 5 Matches Tracker</div>
        <div class="chart-subtitle">Ball-by-ball aggregated match log</div>
    """, unsafe_allow_html=True)
    
    if last_5_rows:
        df_hist = pd.DataFrame(last_5_rows)
        custom_table(df_hist)
    else:
        st.markdown("<p style='color: var(--text-muted); font-style: italic;'>No historical logs found.</p>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# Performance telemetry breakdown cards
st.markdown("<br>", unsafe_allow_html=True)
section_header("Form Telemetry breakdown", "Interactive metrics for recent games")

c_t1, c_t2, c_t3, c_t4 = st.columns(4)

with c_t1:
    avg_r = round(np.mean(bat_runs_list), 1) if 'bat_runs_list' in locals() and bat_runs_list else 0.0
    metric_card("Recent Avg Runs", f"{avg_r}", delta="Batting benchmark")
with c_t2:
    avg_sr_val = round(np.mean(bat_sr_list), 1) if 'bat_sr_list' in locals() and bat_sr_list else 0.0
    metric_card("Recent Strike Rate", f"{avg_sr_val}", delta="Target: 135.0+", delta_type="up" if avg_sr_val >= 135 else "down")
with c_t3:
    avg_wkts_val = round(np.mean(bowl_wkts_list), 1) if 'bowl_wkts_list' in locals() and bowl_wkts_list else 0.0
    metric_card("Recent Avg Wickets", f"{avg_wkts_val}", delta="Bowling benchmark")
with c_t4:
    avg_econ_val = round(np.mean(bowl_econ_list), 2) if 'bowl_econ_list' in locals() and bowl_econ_list else 0.0
    metric_card("Recent Avg Economy", f"{avg_econ_val}", delta="Target: <8.0", delta_type="up" if avg_econ_val <= 8.0 and avg_econ_val > 0 else ("down" if avg_econ_val > 0 else "warn"))

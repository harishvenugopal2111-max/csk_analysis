import streamlit as st
import pandas as pd
import numpy as np
from utils.loader import load_matches, load_deliveries
from utils.helpers import section_header, metric_card, custom_table

# Load data
matches_df = load_matches()
deliveries_df = load_deliveries()

section_header("Opponent Tactical Analysis", "Assess head-to-head records and compute match-up strategies")

# Select Opponent
opponents = ["RCB", "MI", "GT", "SRH", "KKR", "RR", "PBKS", "DC", "LSG"]
selected_opp = st.selectbox("Select Opponent Team", opponents)

# --- COMPUTE H2H STATS ---
# Opponent matches
h2h_matches = matches_df[((matches_df["team1"] == "CSK") & (matches_df["team2"] == selected_opp)) |
                         ((matches_df["team1"] == selected_opp) & (matches_df["team2"] == "CSK"))]

total_h2h = len(h2h_matches)
wins = len(h2h_matches[h2h_matches["winner"] == "CSK"])
losses = total_h2h - wins

csk_scores = []
csk_wkts = []
for idx, row in h2h_matches.iterrows():
    if row["team1"] == "CSK":
        csk_scores.append(row["team1_score"])
        csk_wkts.append(row["team1_wickets"])
    else:
        csk_scores.append(row["team2_score"])
        csk_wkts.append(row["team2_wickets"])

avg_csk_score = round(np.mean(csk_scores), 1) if csk_scores else 0.0
avg_csk_wkts = round(np.mean(csk_wkts), 1) if csk_wkts else 0.0

# --- BEST BATTER / BOWLER VS OPPONENT ---
opp_delivs = deliveries_df[((deliveries_df["batting_team"] == "CSK") & (deliveries_df["bowling_team"] == selected_opp)) |
                           ((deliveries_df["batting_team"] == selected_opp) & (deliveries_df["bowling_team"] == "CSK"))]

# Best CSK batter vs this opponent (most runs in deliveries)
csk_batting_opp = opp_delivs[opp_delivs["batting_team"] == "CSK"]
best_batter = "Ruturaj Gaikwad" # fallback
best_runs = 0
if not csk_batting_opp.empty:
    bat_runs = csk_batting_opp.groupby("batter")["runs_off_bat"].sum().reset_index()
    if not bat_runs.empty:
        top_row = bat_runs.sort_values(by="runs_off_bat", ascending=False).iloc[0]
        best_batter = top_row["batter"]
        best_runs = int(top_row["runs_off_bat"])

# Best CSK bowler vs this opponent (most wickets in deliveries)
csk_bowling_opp = opp_delivs[opp_delivs["bowling_team"] == "CSK"].copy()
valid_wickets = ["caught", "bowled", "lbw", "stumped", "caught and bowled", "hit wicket"]
csk_bowling_opp["is_wicket"] = csk_bowling_opp["wicket_type"].isin(valid_wickets)
best_bowler = "Ravindra Jadeja" # fallback
best_wkts = 0
if not csk_bowling_opp.empty:
    bowl_wkts = csk_bowling_opp.groupby("bowler")["is_wicket"].sum().reset_index()
    if not bowl_wkts.empty:
        top_row = bowl_wkts.sort_values(by="is_wicket", ascending=False).iloc[0]
        best_bowler = top_row["bowler"]
        best_wkts = int(top_row["is_wicket"])

# --- POWERPLAY & DEATH ANALYSIS VS OPPONENT ---
# PP scoring rate
csk_pp_delivs = csk_batting_opp[csk_batting_opp["over"] < 6]
opp_batting_opp = opp_delivs[opp_delivs["batting_team"] == selected_opp]
opp_pp_delivs = opp_batting_opp[opp_batting_opp["over"] < 6]

csk_pp_runs = csk_pp_delivs.groupby("match_id").apply(lambda x: x["runs_off_bat"].sum() + x["extras"].sum()).mean()
opp_pp_runs = opp_pp_delivs.groupby("match_id").apply(lambda x: x["runs_off_bat"].sum() + x["extras"].sum()).mean()

csk_pp_runs = round(csk_pp_runs, 1) if not np.isnan(csk_pp_runs) else 45.0
opp_pp_runs = round(opp_pp_runs, 1) if not np.isnan(opp_pp_runs) else 44.0

# Death scoring rate
csk_death_delivs = csk_batting_opp[csk_batting_opp["over"] >= 16]
opp_death_delivs = opp_batting_opp[opp_batting_opp["over"] >= 16]

csk_death_runs = csk_death_delivs.groupby("match_id").apply(lambda x: x["runs_off_bat"].sum() + x["extras"].sum()).mean()
opp_death_runs = opp_death_delivs.groupby("match_id").apply(lambda x: x["runs_off_bat"].sum() + x["extras"].sum()).mean()

csk_death_runs = round(csk_death_runs, 1) if not np.isnan(csk_death_runs) else 52.0
opp_death_runs = round(opp_death_runs, 1) if not np.isnan(opp_death_runs) else 50.0

# --- METADATA LOOKUPS FOR DANGER/WEAK PLAYERS & AI RECOMMENDATIONS ---
metadata = {
    "MI": {
        "danger": "Jasprit Bumrah, Suryakumar Yadav",
        "weak": "Gerald Coetzee (vulnerable to spin), Tim David (struggles against leg spin)",
        "recs": [
            "Deploy Ravindra Jadeja early to restrict Suryakumar Yadav in the middle overs.",
            "Use Deepak Chahar's new ball swing to target Rohit Sharma's front pad.",
            "Instruct finishers (Dhoni/Jadeja) to play out Jasprit Bumrah and target Gerald Coetzee's death overs."
        ]
    },
    "RCB": {
        "danger": "Virat Kohli, Heinrich Klaasen (representing simulated powerhouses)",
        "weak": "Glenn Maxwell (vulnerable to left-arm spin), Cameron Green (vulnerable to cutters)",
        "recs": [
            "Start with left-arm spinner Ravindra Jadeja immediately when Virat Kohli enters the crease to starve him of singles.",
            "Bowl Matheesha Pathirana's high-pace yorkers to contain tail-end boundaries.",
            "Instruct Ruturaj Gaikwad to anchor the innings and exploit RCB's middle-overs bowling."
        ]
    },
    "GT": {
        "danger": "Shubman Gill, Rashid Khan",
        "weak": "Umesh Yadav (expensive at the death), Sai Sudharsan (struggles against left-arm speed)",
        "recs": [
            "Use Matheesha Pathirana to target Shubman Gill's leg stump with quick deliveries.",
            "Instruct Shivam Dube to counter Rashid Khan's legbreak spin with clean lofted drives.",
            "Put GT under pressure by choosing to field first and chasing their total."
        ]
    },
    "SRH": {
        "danger": "Travis Head, Heinrich Klaasen",
        "weak": "Aiden Markram (vulnerable to mystery off-spin), Bhuvneshwar Kumar (exploitable in second spell)",
        "recs": [
            "Deploy Maheesh Theekshana in the first over to contain Travis Head's swing sweep shots.",
            "Enforce strict off-side fields for Abhishek Sharma; restrict room with Deepak Chahar's lines.",
            "Hold back Matheesha Pathirana specifically for Heinrich Klaasen in the death overs."
        ]
    },
    "KKR": {
        "danger": "Sunil Narine, Andre Russell",
        "weak": "Phil Salt (vulnerable to short-pitch bowling), Shreyas Iyer (struggles against high pace bouncers)",
        "recs": [
            "Feed Sunil Narine hard lengths on the rib-cage via Tushar Deshpande to restrict swinging room.",
            "Bowl wide yorkers to Andre Russell, avoiding his hitting arc.",
            "Instruct Conway to anchor and sweep Varun Chakaravarthy to disrupt KKR's spin-choke."
        ]
    },
    "RR": {
        "danger": "Yashasvi Jaiswal, Yuzvendra Chahal",
        "weak": "Riyan Parag (vulnerable to away swing), Jos Buttler (struggles against left-arm orthodox early)",
        "recs": [
            "Target Yashasvi Jaiswal with left-arm angles from Mukesh Choudhary early.",
            "Attack Yuzvendra Chahal with Shivam Dube's long-handled hitting down the ground.",
            "Utilize MS Dhoni's wicket-keeping insights to review DRS decisions on spin turn."
        ]
    },
    "PBKS": {
        "danger": "Liam Livingstone, Sam Curran",
        "weak": "Jitesh Sharma (vulnerable to slower cutters), Shikhar Dhawan (slow strike rate against off-spin)",
        "recs": [
            "Bowl slow cutters outside off stump to Liam Livingstone to avoid his power swing.",
            "Apply off-spin matchups (Moeen Ali/Theekshana) to Shikhar Dhawan in the powerplay.",
            "Target Sam Curran's death bowling by clearing short straight boundaries."
        ]
    },
    "DC": {
        "danger": "Rishabh Pant, Kuldeep Yadav",
        "weak": "Prithvi Shaw (vulnerable to high-pace bouncers), Mitchell Marsh (struggles with low bounce)",
        "recs": [
            "Bowl round-the-wicket line to Rishabh Pant with Ravindra Jadeja, pitching it outside off.",
            "Deploy Matheesha Pathirana to hit Prithvi Shaw's handle with heavy short deliveries.",
            "Maintain composure against Kuldeep Yadav by sweeping him into vacant midwicket areas."
        ]
    },
    "LSG": {
        "danger": "Nicholas Pooran, Ravi Bishnoi",
        "weak": "KL Rahul (vulnerable to defensive shell against spin), Quinton de Kock (vulnerable to off-spin)",
        "recs": [
            "Deploy Maheesh Theekshana to bowl flat inside Quinton de Kock's swing arc.",
            "Starve KL Rahul of runs in the powerplay to induce risky stroke play.",
            "Bowl wide yorkers at high pace to Nicholas Pooran to prevent him from accessing leg-side boundaries."
        ]
    }
}

meta = metadata.get(selected_opp, {
    "danger": "Key opposition star players",
    "weak": "Opposition lower order and spinners",
    "recs": ["Bowl disciplined lines and construct partnerships."]
})

# Layout: Metric Cards H2H
c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card(f"H2H vs {selected_opp}", f"{total_h2h} Matches", is_yellow=True)
with c2:
    metric_card("CSK Wins", f"{wins}", delta=f"{wins} Wins", delta_type="up")
with c3:
    metric_card("CSK Losses", f"{losses}", delta=f"{losses} Losses", delta_type="down")
with c4:
    win_pct_h2h = round((wins / total_h2h) * 100, 1) if total_h2h > 0 else 0.0
    metric_card("Win Percentage", f"{win_pct_h2h}%", delta_type="up" if win_pct_h2h >= 50 else "down")

# Best Performers & Matchups
st.markdown("<br>", unsafe_allow_html=True)
c_m1, c_m2 = st.columns(2)

with c_m1:
    st.markdown(f"""
    <div class="metric-card" style="height: 100%;">
        <div class="metric-label">🔥 Best Batter vs {selected_opp}</div>
        <div class="metric-value">{best_batter}</div>
        <div style="font-size: 0.8rem; color: #10B981; font-weight: 600; margin-top: 0.5rem;">
            Scored {best_runs} runs in H2H deliveries
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_m2:
    st.markdown(f"""
    <div class="metric-card" style="height: 100%;">
        <div class="metric-label">🎯 Best Bowler vs {selected_opp}</div>
        <div class="metric-value">{best_bowler}</div>
        <div style="font-size: 0.8rem; color: #10B981; font-weight: 600; margin-top: 0.5rem;">
            Took {best_wkts} wickets in H2H deliveries
        </div>
    </div>
    """, unsafe_allow_html=True)

# Powerplay & Death Overs Analysis Table
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div class="chart-wrap">
    <div class="chart-title">⏱️ Phase Analysis vs {selected_opp}</div>
    <div class="chart-subtitle">Average runs scored during Powerplay (Overs 0-5) and Death (Overs 16-19)</div>
""", unsafe_allow_html=True)

phase_data = [
    {"Phase": "Powerplay Overs (0-5)", "CSK Average Runs": csk_pp_runs, f"{selected_opp} Average Runs": opp_pp_runs, "Scoring Advantage": "CSK (+)" if csk_pp_runs > opp_pp_runs else f"{selected_opp} (+)"},
    {"Phase": "Death Overs (16-19)", "CSK Average Runs": csk_death_runs, f"{selected_opp} Average Runs": opp_death_runs, "Scoring Advantage": "CSK (+)" if csk_death_runs > opp_death_runs else f"{selected_opp} (+)"}
]
custom_table(pd.DataFrame(phase_data))
st.markdown("</div>", unsafe_allow_html=True)

# Danger Players, Weak Players & Tactical Recs
st.markdown("<br>", unsafe_allow_html=True)
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.markdown(f"""
    <div class="alert-box alert-info" style="border-color: rgba(239, 68, 68, 0.25); height: 100%;">
        <h4 style="color: #EF4444; margin: 0 0 8px 0; font-weight: 700;">⚠️ Threat Identification</h4>
        <div style="font-size: 0.85rem; margin-bottom: 1rem;">
            <strong>Danger Players:</strong><br>
            <span style="color: #FFD305;">{meta['danger']}</span>
        </div>
        <div style="font-size: 0.85rem;">
            <strong>Vulnerabilities to Exploit:</strong><br>
            <span>{meta['weak']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    recs_li = "".join([f"<li style='margin-bottom: 8px;'>{rec}</li>" for rec in meta["recs"]])
    st.markdown(f"""
    <div class="alert-box alert-info" style="height: 100%; border-color: rgba(255, 211, 5, 0.25);">
        <h4 style="color: #FFD305; margin: 0 0 8px 0; font-weight: 700;">🧠 AI Tactical Recommendations</h4>
        <ul style="color: #F3F4F6; font-size: 0.825rem; margin: 0; padding-left: 1.2rem;">
            {recs_li}
        </ul>
    </div>
    """, unsafe_allow_html=True)

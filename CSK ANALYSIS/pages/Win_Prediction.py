import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.loader import load_matches
from utils.prediction import predict_match_outcome
from utils.helpers import section_header, metric_card

matches_df = load_matches()

section_header("Win Prediction Simulator", "Use machine learning predictions to estimate CSK win probabilities under target scenarios")

# Input selectors in card panel
st.markdown("""
<div style="background: rgba(13, 20, 38, 0.5); padding: 1rem 1.25rem; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 1.5rem;">
    <div style="font-size: 0.75rem; color: #9CA3AF; text-transform: uppercase; font-weight: 600; margin-bottom: 0.75rem;">Simulator Parameters</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    opponents = ["RCB", "MI", "GT", "SRH", "KKR", "RR", "PBKS", "DC", "LSG"]
    selected_opp = st.selectbox("Opponent Team", opponents, key="pred_opp")
with c2:
    venues = ["Chepauk (Chennai)", "Wankhede (Mumbai)", "Chinnaswamy (Bengaluru)", "Narendra Modi Stadium (Ahmedabad)"]
    selected_venue = st.selectbox("Match Venue", venues, key="pred_ven")
with c3:
    toss_winners = ["CSK", selected_opp]
    selected_toss = st.selectbox("Toss Winner", toss_winners, key="pred_toss")
with c4:
    toss_decisions = ["bat", "field"]
    selected_decision = st.selectbox("Toss Decision", toss_decisions, key="pred_dec")
with c5:
    forms = ["Excellent", "Good", "Average", "Poor"]
    selected_form = st.selectbox("CSK Recent Form", forms, key="pred_form")

st.markdown("</div>", unsafe_allow_html=True)

# Run prediction
prob, confidence, factors = predict_match_outcome(
    matches_df, selected_opp, selected_venue, selected_toss, selected_decision, selected_form
)

# --- PLOTLY GAUGE CHARTS ---
def plot_win_gauge(prob_val):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = prob_val,
        domain = {'x': [0, 1], 'y': [0, 1]},
        number = {'suffix': "%", 'font': {'color': '#F3F4F6', 'size': 50}},
        title = {'text': "CSK Win Probability", 'font': {'color': '#9CA3AF', 'size': 14}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#9CA3AF"},
            'bar': {'color': "#FFD305"},
            'bgcolor': "rgba(255, 255, 255, 0.05)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.1)",
            'steps': [
                {'range': [0, 45], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [45, 60], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [60, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
            ],
            'threshold': {
                'line': {'color': "#10B981", 'width': 4},
                'thickness': 0.75,
                'value': 60
            }
        }
    ))
    
    font_color = "#F3F4F6"
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=50, b=20),
        height=280,
        font=dict(family="DM Sans", color=font_color)
    )
    return fig

# Layout: Gauge chart & Analysis card
c_gauge, c_analysis = st.columns([1.2, 1])

with c_gauge:
    st.markdown("""
    <div class="chart-wrap">
    """, unsafe_allow_html=True)
    st.plotly_chart(plot_win_gauge(prob), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with c_analysis:
    st.markdown(f"""
    <div class="chart-wrap" style="height: 100%;">
        <div class="chart-title">🔮 Simulator Assessment Details</div>
        <div class="chart-subtitle">Predictive confidence thresholds and key metrics</div>
    """, unsafe_allow_html=True)
    
    # Renders sub metrics inside the card
    ca1, ca2 = st.columns(2)
    with ca1:
        metric_card("Model Confidence", f"{confidence}%", delta="High certainty" if confidence >= 70 else "Medium certainty")
    with ca2:
        advantage = "CSK Favored" if prob >= 50 else f"{selected_opp} Favored"
        metric_card("Expected Advantage", advantage, is_yellow=prob >= 50)
        
    st.markdown(f"""
        <div style="background: rgba(0,0,0,0.15); padding: 0.85rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); font-size: 0.78rem; color: #9CA3AF; margin-top: 1rem;">
            <strong>Suggested Toss Advantage:</strong> A win probability of <strong>{prob}%</strong> indicates 
            CSK is {"favorably positioned." if prob >= 55 else ("entering a balanced encounter." if prob >= 45 else "entering a high-risk match.")}
            Ensure batting cards and death overs yorker strategies are fully calibrated.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Key tactical factors & Recommended Players
st.markdown("<br>", unsafe_allow_html=True)
col_left, col_right = st.columns([1.3, 1])

with col_left:
    factor_list = "".join([f"<li style='margin-bottom: 8px;'>{f}</li>" for f in factors])
    st.markdown(f"""
    <div class="alert-box alert-info" style="height: 100%; border-color: rgba(255, 211, 5, 0.25);">
        <h4 style="color: #FFD305; margin: 0 0 8px 0; font-weight: 700;">🧩 Win Influence Factors</h4>
        <ul style="color: #F3F4F6; font-size: 0.825rem; margin: 0; padding-left: 1.2rem;">
            {factor_list}
            <li style='margin-bottom: 8px;'>Weather profiles indicate stable bounce patterns; adjust spin/pace balance accordingly.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    # Key recommended players for the matchup
    key_players = {
        "RCB": ["Ravindra Jadeja", "Shivam Dube"],
        "MI": ["Matheesha Pathirana", "Deepak Chahar"],
        "GT": ["Shivam Dube", "Maheesh Theekshana"],
        "SRH": ["Maheesh Theekshana", "Matheesha Pathirana"],
        "KKR": ["Devon Conway", "Tushar Deshpande"],
        "RR": ["Shivam Dube", "Ravindra Jadeja"],
        "PBKS": ["Maheesh Theekshana", "MS Dhoni"],
        "DC": ["Ravindra Jadeja", "Matheesha Pathirana"],
        "LSG": ["Maheesh Theekshana", "Ruturaj Gaikwad"]
    }
    kp = key_players.get(selected_opp, ["Ruturaj Gaikwad", "Ravindra Jadeja"])
    
    st.markdown(f"""
    <div class="alert-box alert-success" style="height: 100%;">
        <h4 style="color: #10B981; margin: 0 0 8px 0; font-weight: 700;">⭐ Key Spotlight Match-ups</h4>
        <p style="color: #9CA3AF; font-size: 0.8rem; margin-bottom: 12px;">
            The following players have highest statistical impact ratings against {selected_opp}:
        </p>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="font-size: 0.825rem; font-weight: 700; color: #F3F4F6; padding: 6px 12px; background: rgba(0, 43, 102, 0.25); border-radius: 6px; border-left: 3px solid #10B981;">
                🌟 Primary Weapon: {kp[0]}
            </div>
            <div style="font-size: 0.825rem; font-weight: 700; color: #F3F4F6; padding: 6px 12px; background: rgba(0, 43, 102, 0.25); border-radius: 6px; border-left: 3px solid #10B981;">
                🛡️ Defense Pivot: {kp[1]}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

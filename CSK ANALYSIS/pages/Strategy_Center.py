import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.helpers import section_header, status_badge

section_header("Strategy Center", "Formulate phase-wise bowling rotations, batting cards, and field containment configurations")

# Select Strategy Scheme
st.markdown("""
<div style="background: rgba(13, 20, 38, 0.5); padding: 1rem 1.25rem; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 1.5rem;">
    <div style="font-size: 0.75rem; color: #9CA3AF; text-transform: uppercase; font-weight: 600; margin-bottom: 0.75rem;">Interactive Strategy Builder</div>
""", unsafe_allow_html=True)
c_sch = st.selectbox("Select Field Placement Layout", ["Spin-Choke Field (Chepauk Standard)", "Fast-Pace Containment (Away Standard)", "Powerplay Attack Field (New Ball)"])
st.markdown("</div>", unsafe_allow_html=True)

# --- PLOTLY CRICKET FIELD MAP ---
def plot_cricket_field(layout_type):
    # Create polar circles representing a cricket field
    theta = np.linspace(0, 2*np.pi, 100)
    # Boundaries
    r_boundary = 70
    r_30yard = 27
    
    fig = go.Figure()
    
    # Draw Boundary
    fig.add_trace(go.Scatter(
        x=r_boundary * np.cos(theta),
        y=r_boundary * np.sin(theta),
        mode='lines',
        line=dict(color="#FFD305", width=2.5),
        name="Boundary (70m)",
        hoverinfo='skip'
    ))
    
    # Draw 30-Yard Circle
    fig.add_trace(go.Scatter(
        x=r_30yard * np.cos(theta),
        y=r_30yard * np.sin(theta),
        mode='lines',
        line=dict(color="rgba(255, 255, 255, 0.2)", width=1.5, dash="dash"),
        name="30-Yard Circle",
        hoverinfo='skip'
    ))
    
    # Draw Pitch (center rectangle)
    fig.add_trace(go.Scatter(
        x=[-2, 2, 2, -2, -2],
        y=[-10, -10, 10, 10, -10],
        fill="toself",
        fillcolor="rgba(255, 211, 5, 0.15)",
        line=dict(color="#FFD305", width=1),
        name="Pitch",
        hoverinfo='skip'
    ))
    
    # Define placements based on layout
    placements = []
    if "Spin-Choke" in layout_type:
        placements = [
            {"name": "Keeper", "x": 0, "y": -15, "icon": "🧤"},
            {"name": "Slip", "x": 3, "y": -12, "icon": "👤"},
            {"name": "Short Fine Leg", "x": -15, "y": -12, "icon": "👤"},
            {"name": "Point", "x": 22, "y": 5, "icon": "👤"},
            {"name": "Cover", "x": 18, "y": 18, "icon": "👤"},
            {"name": "Mid-Wicket", "x": -20, "y": 12, "icon": "👤"},
            {"name": "Long On", "x": -12, "y": 62, "icon": "🏃"},
            {"name": "Long Off", "x": 12, "y": 62, "icon": "🏃"},
            {"name": "Deep Mid-Wicket", "x": -55, "y": 30, "icon": "🏃"}
        ]
    elif "Fast-Pace" in layout_type:
        placements = [
            {"name": "Keeper", "x": 0, "y": -22, "icon": "🧤"},
            {"name": "First Slip", "x": 4, "y": -18, "icon": "👤"},
            {"name": "Gully", "x": 15, "y": -12, "icon": "👤"},
            {"name": "Third Man", "x": 35, "y": -45, "icon": "🏃"},
            {"name": "Fine Leg", "x": -25, "y": -55, "icon": "🏃"},
            {"name": "Cover", "x": 20, "y": 15, "icon": "👤"},
            {"name": "Mid On", "x": -12, "y": 25, "icon": "👤"},
            {"name": "Deep Mid-Wicket", "x": -52, "y": 35, "icon": "🏃"},
            {"name": "Deep Cover", "x": 58, "y": 25, "icon": "🏃"}
        ]
    else: # Powerplay Attack
        placements = [
            {"name": "Keeper", "x": 0, "y": -20, "icon": "🧤"},
            {"name": "First Slip", "x": 4, "y": -16, "icon": "👤"},
            {"name": "Second Slip", "x": 8, "y": -14, "icon": "👤"},
            {"name": "Gully", "x": 12, "y": -10, "icon": "👤"},
            {"name": "Mid Off", "x": 18, "y": 22, "icon": "👤"},
            {"name": "Mid On", "x": -18, "y": 22, "icon": "👤"},
            {"name": "Square Leg", "x": -24, "y": -2, "icon": "👤"},
            {"name": "Point", "x": 24, "y": 2, "icon": "👤"},
            {"name": "Fine Leg", "x": -45, "y": -45, "icon": "🏃"}
        ]
        
    pxs = [p["x"] for p in placements]
    pys = [p["y"] for p in placements]
    pnames = [f"{p['icon']} {p['name']}" for p in placements]
    
    fig.add_trace(go.Scatter(
        x=pxs,
        y=pys,
        mode="markers+text",
        marker=dict(size=12, color="#FFD305", line=dict(color="#060B18", width=1.5)),
        text=pnames,
        textposition="top center",
        name="Fielder Positions",
        hovertext=[f"Position: {p['name']}" for p in placements],
        hoverinfo="text"
    ))
    
    font_color = "#F3F4F6"
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(visible=False, range=[-85, 85]),
        yaxis=dict(visible=False, range=[-85, 85]),
        showlegend=False,
        font=dict(family="DM Sans", color=font_color)
    )
    return fig

# Grid layout: Field Placement & Danger zones
c_field, c_zones = st.columns([1.3, 1])

with c_field:
    st.markdown(f"""
    <div class="chart-wrap">
        <div class="chart-title">🏟️ Interactive Field Placement Mapping</div>
        <div class="chart-subtitle">Displays placement coordinates on the 70m boundary circle ({layout_type:=c_sch})</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(plot_cricket_field(c_sch), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with c_zones:
    st.markdown("""
    <div class="chart-wrap" style="height: 100%;">
        <div class="chart-title">🎯 Pitch Danger & Safe Landing Zones</div>
        <div class="chart-subtitle">AI mapped spots on a standard 22-yard wicket</div>
        
        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.25); padding: 0.85rem; border-radius: 8px; font-size: 0.8rem; margin-bottom: 1rem;">
            <strong style="color: #EF4444;">🔴 Batting Danger Zones (Avoid Bowling Here)</strong><br>
            <span style="color: var(--text-muted);">
                - Slot length balls outside off stump (easily hit through cover/point).<br>
                - Half-volleys on leg stump (easily flicked behind square).
            </span>
        </div>
        
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.25); padding: 0.85rem; border-radius: 8px; font-size: 0.8rem; margin-bottom: 1rem;">
            <strong style="color: #10B981;">🟢 Batting Safe/Target Zones (Target These Spots)</strong><br>
            <span style="color: var(--text-muted);">
                - Fifth-stump line at good length (forces uncertainty/slips catch).<br>
                - Sandy patch near 4-meter length at Chepauk (induces variable bounce).
            </span>
        </div>
        
        <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.25); padding: 0.85rem; border-radius: 8px; font-size: 0.8rem;">
            <strong style="color: #3B82F6;">🔵 Death Overs Blockhole Zone</strong><br>
            <span style="color: var(--text-muted);">
                - Heel-crushing wide yorkers (6-8 inches outside off-stump tramline).
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Phase Strategies Details
st.markdown("<br>", unsafe_allow_html=True)
section_header("Phase Tactics Breakdown", "Strategic over-by-over plans")

st.markdown("""
<div class="chart-wrap">
    <div class="chart-title">⏱️ Match Phase Directives</div>
    <div class="chart-subtitle">Specific guidelines for Powerplay, Middle, and Death Overs</div>
""", unsafe_allow_html=True)

phase_data = [
    {
        "Match Phase": "Powerplay (Overs 0-5)",
        "Batting Strategy": "Exploit field restrictions. Ruturaj anchors while Conway clears infield. Target: 48-52 runs, max 1 wicket loss.",
        "Bowling Strategy": "Deploy Deepak Chahar and Mukesh Choudhary. Target new-ball swing. Pitch the ball up in the slip corridor to extract early catches."
    },
    {
        "Match Phase": "Middle Overs (Overs 6-15)",
        "Batting Strategy": "Utilize Shivam Dube to clear long boundaries against spin. Ravindra Jadeja preserves wickets. Target: 80-85 runs, pick off singles.",
        "Bowling Strategy": "Deploy Jadeja and Theekshana. Apply a strict 'Spin-Choke' with a deep mid-wicket. Starve opponents of boundary balls."
    },
    {
        "Match Phase": "Death Overs (Overs 16-20)",
        "Batting Strategy": "MS Dhoni to lead power clearing. Shardul Thakur provides cameos. Target: 55-60 runs. Attack bowlers with slower cutters.",
        "Bowling Strategy": "MATHEESHA PATHIRANA takes charge. Deliver 145km/h yorkers and slower ball cutters. Keep deep fielders at long-on and deep midwicket."
    }
]
custom_table(pd.DataFrame(phase_data))
st.markdown("</div>", unsafe_allow_html=True)

# Rotation Suggestions
st.markdown("<br>", unsafe_allow_html=True)
c_rot1, c_rot2 = st.columns(2)

with c_rot1:
    st.markdown("""
    <div class="chart-wrap" style="height: 100%;">
        <div class="chart-title">🏏 Recommended Batting Card</div>
        <div class="chart-subtitle">Order sequence adjusted for tactical match-ups</div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="font-size: 0.8rem; padding: 4px 8px; background: rgba(255,255,255,0.03); border-radius: 4px;"><strong>1. Ruturaj Gaikwad (C)</strong> - Right Hand Anchor</div>
            <div style="font-size: 0.8rem; padding: 4px 8px; background: rgba(255,255,255,0.03); border-radius: 4px;"><strong>2. Devon Conway (WK)</strong> - Left Hand Spin-Player</div>
            <div style="font-size: 0.8rem; padding: 4px 8px; background: rgba(255,255,255,0.03); border-radius: 4px;"><strong>3. Rachin Ravindra</strong> - Left Hand Pinch Hitter</div>
            <div style="font-size: 0.8rem; padding: 4px 8px; background: rgba(255,255,255,0.03); border-radius: 4px;"><strong>4. Shivam Dube</strong> - Left Hand Spin-Destroyer</div>
            <div style="font-size: 0.8rem; padding: 4px 8px; background: rgba(255,255,255,0.03); border-radius: 4px;"><strong>5. Ravindra Jadeja</strong> - Left Hand Utility Finisher</div>
            <div style="font-size: 0.8rem; padding: 4px 8px; background: rgba(255,255,255,0.03); border-radius: 4px;"><strong>6. MS Dhoni</strong> - Right Hand Finisher / Tactical Keeper</div>
            <div style="font-size: 0.8rem; padding: 4px 8px; background: rgba(255,255,255,0.03); border-radius: 4px;"><strong>7. Shardul Thakur</strong> - All-rounder Cameos</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_rot2:
    st.markdown("""
    <div class="chart-wrap" style="height: 100%;">
        <div class="chart-title">🌀 Recommended Bowling Rotation (20 Overs)</div>
        <div class="chart-subtitle">Match rotation diagram for standard defence</div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="font-size: 0.8rem; padding: 4px 8px; background: rgba(255,255,255,0.03); border-radius: 4px;"><strong>Overs 1-4:</strong> Deepak Chahar (2 overs) & Mukesh Choudhary (2 overs) - PP Swing</div>
            <div style="font-size: 0.8rem; padding: 4px 8px; background: rgba(255,255,255,0.03); border-radius: 4px;"><strong>Overs 5-6:</strong> Maheesh Theekshana (2 overs) - PP restriction</div>
            <div style="font-size: 0.8rem; padding: 4px 8px; background: rgba(255,255,255,0.03); border-radius: 4px;"><strong>Overs 7-12:</strong> Ravindra Jadeja (3 overs) & Mitchell Santner (3 overs) - Middle spin containment</div>
            <div style="font-size: 0.8rem; padding: 4px 8px; background: rgba(255,255,255,0.03); border-radius: 4px;"><strong>Overs 13-15:</strong> Shardul Thakur (2 overs) & Tushar Deshpande (1 over) - Partnership breaking</div>
            <div style="font-size: 0.8rem; padding: 4px 8px; background: rgba(255,255,255,0.03); border-radius: 4px;"><strong>Overs 16-18:</strong> Matheesha Pathirana (2 overs) & Tushar Deshpande (1 over) - Death Yorks</div>
            <div style="font-size: 0.8rem; padding: 4px 8px; background: rgba(255,255,255,0.03); border-radius: 4px;"><strong>Overs 19-20:</strong> Matheesha Pathirana (1 over) & Shardul Thakur (1 over) - Closing matches</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

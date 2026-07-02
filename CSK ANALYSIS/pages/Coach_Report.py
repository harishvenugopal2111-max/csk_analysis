import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime
from utils.loader import load_matches, get_venue_details
from utils.prediction import predict_match_outcome, generate_playing_xi
from utils.helpers import section_header, status_badge

# Load matches
matches_df = load_matches()

section_header("Coach Tactical Report", "Compile and export professional tactical PDF documents for coaching staff review")

# Inputs
st.markdown("""
<div style="background: rgba(13, 20, 38, 0.5); padding: 1rem 1.25rem; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 1.5rem;">
    <div style="font-size: 0.75rem; color: #9CA3AF; text-transform: uppercase; font-weight: 600; margin-bottom: 0.75rem;">Tactical Parameters for PDF Compile</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    opponents = ["RCB", "MI", "GT", "SRH", "KKR", "RR", "PBKS", "DC", "LSG"]
    selected_opp = st.selectbox("Opponent Team", opponents, key="rep_opp")
with c2:
    venues = ["Chepauk (Chennai)", "Wankhede (Mumbai)", "Chinnaswamy (Bengaluru)", "Narendra Modi Stadium (Ahmedabad)"]
    selected_venue = st.selectbox("Select Venue", venues, key="rep_ven")
with c3:
    pitch_types = ["Balanced", "Spin Friendly", "Green / Pace Friendly", "Flat / Batting Friendly"]
    selected_pitch = st.selectbox("Pitch Condition", pitch_types, key="rep_pit")
with c4:
    weather_types = ["Sunny", "Overcast", "Humid / Dew", "Windy"]
    selected_weather = st.selectbox("Expected Weather", weather_types, key="rep_wea")

st.markdown("</div>", unsafe_allow_html=True)

# Generate parameters
xi = generate_playing_xi(selected_opp, selected_venue, selected_pitch, selected_weather)
prob, confidence, factors = predict_match_outcome(
    matches_df, selected_opp, selected_venue, "CSK", "field", "Good"
)
venue_meta = get_venue_details(selected_venue)

# On-screen preview
st.markdown("""
<div class="chart-wrap">
    <div class="chart-title">📋 Tactical Report Summary Preview</div>
    <div class="chart-subtitle">Key metrics compiled for the PDF report</div>
""", unsafe_allow_html=True)

cp1, cp2, cp3 = st.columns(3)
with cp1:
    st.markdown(f"**Predicted Outcome:** CSK {prob}% Win chance")
    st.markdown(f"**Playing XI Captain:** {xi['captain']}")
with cp2:
    st.markdown(f"**Venue:** {selected_venue}")
    st.markdown(f"**Opponent:** {selected_opp}")
with cp3:
    st.markdown(f"**Pitch Behavior:** {selected_pitch}")
    st.markdown(f"**Impact Nominee:** {xi['impact_player']['player']}")

st.markdown("</div>", unsafe_allow_html=True)

# Custom FPDF compiler class
class CSKReportPDF(FPDF):
    def __init__(self, opponent, venue, pitch, weather, prob, xi, venue_meta):
        super().__init__()
        self.opp = opponent
        self.venue = venue
        self.pitch = pitch
        self.weather = weather
        self.prob = prob
        self.xi = xi
        self.v_meta = venue_meta
        self.set_author("CSK AI Strategy Lab")
        self.set_title(f"CSK Tactical Report vs {opponent}")

    def header(self):
        # Draw Navy Blue Header block
        self.set_fill_color(0, 43, 102) # CSK Navy Blue
        self.rect(0, 0, 210, 32, 'F')
        
        # CSK Yellow line
        self.set_fill_color(255, 211, 5) # CSK Yellow
        self.rect(0, 32, 210, 2, 'F')
        
        # Header text
        self.set_xy(10, 6)
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(255, 211, 5)
        self.cell(0, 8, "CHENNAI SUPER KINGS", ln=True)
        
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(243, 244, 246)
        self.cell(0, 6, f"AI STRATEGY CENTER | TACTICAL PREVIEW VS {self.opp}", ln=True)
        
        self.set_y(38)

    def footer(self):
        self.set_y(-18)
        # Yellow accent line
        self.set_fill_color(255, 211, 5)
        self.rect(0, 280, 210, 1, 'F')
        
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(107, 114, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}} | CSK AI Labs © 2026 | Confidential - Coach Staff Use Only", align="C")

    def build_report(self):
        self.alias_nb_pages()
        self.add_page()
        
        # Section 1: Match Parameters
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(0, 43, 102)
        self.cell(0, 8, "1. MATCH OVERVIEW & TELEMETRY", ln=True)
        self.ln(2)
        
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        
        col_w = 45
        self.cell(col_w, 7, "Opponent Team:", border=1, ln=False)
        self.set_font("Helvetica", "B", 10)
        self.cell(col_w, 7, f" {self.opp}", border=1, ln=True)
        
        self.set_font("Helvetica", "", 10)
        self.cell(col_w, 7, "Match Venue:", border=1, ln=False)
        self.set_font("Helvetica", "B", 10)
        self.cell(col_w, 7, f" {self.venue}", border=1, ln=True)
        
        self.set_font("Helvetica", "", 10)
        self.cell(col_w, 7, "Pitch Condition:", border=1, ln=False)
        self.set_font("Helvetica", "B", 10)
        self.cell(col_w, 7, f" {self.pitch}", border=1, ln=True)
        
        self.set_font("Helvetica", "", 10)
        self.cell(col_w, 7, "Weather Profile:", border=1, ln=False)
        self.set_font("Helvetica", "B", 10)
        self.cell(col_w, 7, f" {self.weather}", border=1, ln=True)
        
        self.set_font("Helvetica", "", 10)
        self.cell(col_w, 7, "AI Win Probability:", border=1, ln=False)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(16, 185, 129)
        self.cell(col_w, 7, f" CSK {self.prob}%", border=1, ln=True)
        
        self.ln(6)
        
        # Section 2: Playing XI
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(0, 43, 102)
        self.cell(0, 8, "2. RECOMMEND SQUAD - PLAYING XI", ln=True)
        self.ln(2)
        
        # Table of players
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 43, 102)
        self.set_text_color(255, 211, 5)
        self.cell(50, 7, " Playing Role", border=1, fill=True)
        self.cell(45, 7, " Player Selected", border=1, fill=True)
        self.cell(95, 7, " Tactical Rationale", border=1, fill=True, ln=True)
        
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(50, 50, 50)
        
        # Openers
        self.cell(50, 6, " Opening Pair", border=1)
        self.cell(45, 6, f" {self.xi['openers'][0]['player']}", border=1)
        self.cell(95, 6, f" {self.xi['openers'][0]['reason'][:60]}...", border=1, ln=True)
        self.cell(50, 6, " Opening Pair", border=1)
        self.cell(45, 6, f" {self.xi['openers'][1]['player']}", border=1)
        self.cell(95, 6, f" {self.xi['openers'][1]['reason'][:60]}...", border=1, ln=True)
        
        # Middle Order
        for idx, player in enumerate(self.xi["middle_order"]):
            self.cell(50, 6, f" Middle Order #{idx+1}", border=1)
            self.cell(45, 6, f" {player['player']}", border=1)
            self.cell(95, 6, f" {player['reason'][:60]}...", border=1, ln=True)
            
        # Finishers
        self.cell(50, 6, " Finisher / Keeper", border=1)
        self.cell(45, 6, f" {self.xi['finishers'][0]['player']}", border=1)
        self.cell(95, 6, f" {self.xi['finishers'][0]['reason'][:60]}...", border=1, ln=True)
        self.cell(50, 6, " Finisher / Keeper", border=1)
        self.cell(45, 6, f" {self.xi['finishers'][1]['player']}", border=1)
        self.cell(95, 6, f" {self.xi['finishers'][1]['reason'][:60]}...", border=1, ln=True)
        
        # Spinners
        self.cell(50, 6, " Spin Bowler", border=1)
        self.cell(45, 6, f" {self.xi['spinners'][0]['player']}", border=1)
        self.cell(95, 6, f" {self.xi['spinners'][0]['reason'][:60]}...", border=1, ln=True)
        self.cell(50, 6, " Spin Bowler", border=1)
        self.cell(45, 6, f" {self.xi['spinners'][1]['player']}", border=1)
        self.cell(95, 6, f" {self.xi['spinners'][1]['reason'][:60]}...", border=1, ln=True)
        
        # Pacers
        self.cell(50, 6, " Fast Bowler", border=1)
        self.cell(45, 6, f" {self.xi['pacers'][0]['player']}", border=1)
        self.cell(95, 6, f" {self.xi['pacers'][0]['reason'][:60]}...", border=1, ln=True)
        
        # Impact Player Nominee
        self.set_fill_color(240, 249, 244) # light green
        self.cell(50, 6, " * IMPACT PLAYER NOMINEE", border=1, fill=True)
        self.cell(45, 6, f" {self.xi['impact_player']['player']}", border=1, fill=True)
        self.cell(95, 6, f" {self.xi['impact_player']['reason'][:60]}...", border=1, fill=True, ln=True)
        
        self.ln(6)
        
        # Section 3: Phase Tactics
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(0, 43, 102)
        self.cell(0, 8, "3. PHASE TACTICS DIRECTIVES", ln=True)
        self.ln(2)
        
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(0, 0, 0)
        self.cell(0, 5, "Powerplay Phase (Overs 1-6):", ln=True)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(80, 80, 80)
        self.cell(0, 4, " - Instruct openers to focus on clearing infield. Utilize Deepak Chahar to bowl full lengths early on.", ln=True)
        self.cell(0, 4, " - Target matching batsmen profiles against bowler movement patterns.", ln=True)
        self.ln(2)
        
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(0, 0, 0)
        self.cell(0, 5, "Middle Overs Phase (Overs 7-15):", ln=True)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(80, 80, 80)
        self.cell(0, 4, " - Apply a strict 'Spin-Choke' utilizing Jadeja and Santner/Theekshana. Keep boundary dimensions large.", ln=True)
        self.cell(0, 4, " - Rotate bowling overs to maintain matchup leverage against off-side hitters.", ln=True)
        self.ln(2)
        
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(0, 0, 0)
        self.cell(0, 5, "Death Overs Phase (Overs 16-20):", ln=True)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(80, 80, 80)
        self.cell(0, 4, " - Matheesha Pathirana to bowl wide yorkers at high pace exceeding 143km/h.", ln=True)
        self.cell(0, 4, " - MS Dhoni to manage field configurations directly from behind the stumps.", ln=True)

# Generate PDF trigger
if st.button("🚀 Compile & Generate PDF Report", use_container_width=True):
    try:
        # Create PDF object
        pdf = CSKReportPDF(selected_opp, selected_venue, selected_pitch, selected_weather, prob, xi, venue_meta)
        pdf.build_report()
        
        # Save report
        report_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
        os.makedirs(report_dir, exist_ok=True)
        
        filename = f"CSK_Tactical_Report_{selected_opp}_{datetime.now().strftime('%d%m%Y_%H%M%S')}.pdf"
        filepath = os.path.join(report_dir, filename)
        
        pdf.output(filepath)
        
        st.success(f"Report compiled successfully: {filename}")
        
        # Expose download button
        with open(filepath, "rb") as f:
            pdf_data = f.read()
            
        st.download_button(
            label="📥 Download Coach PDF Report",
            data=pdf_data,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error compiling PDF report: {e}")

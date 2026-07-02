import os
import pandas as pd
import streamlit as st
import sqlite3

DATA_DIR = os.path.dirname(os.path.dirname(__file__))

def check_datasets():
    """Checks if the required CSVs exist; if not, triggers the generator."""
    required = ["players.csv", "matches.csv", "deliveries.csv"]
    missing = [f for f in required if not os.path.exists(os.path.join(DATA_DIR, f))]
    if missing:
        st.info(f"Missing datasets: {missing}. Triggering data generation...")
        import subprocess
        script_path = os.path.join(DATA_DIR, "scripts/generate_data.py")
        subprocess.run([".venv/Scripts/python", script_path], check=True)

@st.cache_data
def load_players():
    """Loads squad player statistics."""
    check_datasets()
    path = os.path.join(DATA_DIR, "players.csv")
    df = pd.read_csv(path)
    return df

@st.cache_data
def load_matches():
    """Loads historical IPL matches."""
    check_datasets()
    path = os.path.join(DATA_DIR, "matches.csv")
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df

@st.cache_data
def load_deliveries():
    """Loads ball-by-ball deliveries."""
    check_datasets()
    path = os.path.join(DATA_DIR, "deliveries.csv")
    df = pd.read_csv(path)
    return df

def get_venue_details(venue_name):
    """Returns detailed dimensions and features for standard venues."""
    venues_meta = {
        "Chepauk (Chennai)": {
            "FirstInnAvg": 165,
            "WinScore": 172,
            "SpinPct": 65,
            "PacePct": 35,
            "HighestScore": 246,
            "LowestScore": 70,
            "BatFirstWin": 60,
            "ChaseWin": 40,
            "OffBound": 66,
            "LegBound": 68,
            "StraightBound": 72,
            "PitchDesc": "Dry, abrasive surface that offers turn and grip to spinners. Slows down in 2nd innings.",
            "RecommendedBowling": "Spinners (Legbreak/Orthodox) & Bowlers with slower cutters",
            "RecommendedXI": [
                "Ruturaj Gaikwad (C)", "Devon Conway (WK)", "Rachin Ravindra", 
                "Shivam Dube", "Ravindra Jadeja", "MS Dhoni", "Mitchell Santner",
                "Shardul Thakur", "Deepak Chahar", "Maheesh Theekshana", "Matheesha Pathirana"
            ]
        },
        "Wankhede (Mumbai)": {
            "FirstInnAvg": 178,
            "WinScore": 182,
            "SpinPct": 30,
            "PacePct": 70,
            "HighestScore": 235,
            "LowestScore": 67,
            "BatFirstWin": 45,
            "ChaseWin": 55,
            "OffBound": 64,
            "LegBound": 65,
            "StraightBound": 68,
            "PitchDesc": "Red soil pitch with true bounce and carry. Excellent for batting under lights, swing in PP.",
            "RecommendedBowling": "Express Pacers, Swing Bowlers",
            "RecommendedXI": [
                "Ruturaj Gaikwad (C)", "Devon Conway (WK)", "Rachin Ravindra", 
                "Shivam Dube", "Ravindra Jadeja", "MS Dhoni", "Shardul Thakur",
                "Deepak Chahar", "Tushar Deshpande", "Mukesh Choudhary", "Matheesha Pathirana"
            ]
        },
        "Chinnaswamy (Bengaluru)": {
            "FirstInnAvg": 188,
            "WinScore": 194,
            "SpinPct": 25,
            "PacePct": 75,
            "HighestScore": 263,
            "LowestScore": 82,
            "BatFirstWin": 40,
            "ChaseWin": 60,
            "OffBound": 58,
            "LegBound": 60,
            "StraightBound": 64,
            "PitchDesc": "Flat deck with lightning fast outfield. Small boundaries make it a bowling graveyard.",
            "RecommendedBowling": "Pacers with hard length control, Mystery Spinners",
            "RecommendedXI": [
                "Ruturaj Gaikwad (C)", "Devon Conway (WK)", "Rachin Ravindra", 
                "Shivam Dube", "Ravindra Jadeja", "MS Dhoni", "Sameer Rizvi",
                "Shardul Thakur", "Deepak Chahar", "Maheesh Theekshana", "Matheesha Pathirana"
            ]
        },
        "Narendra Modi Stadium (Ahmedabad)": {
            "FirstInnAvg": 172,
            "WinScore": 178,
            "SpinPct": 45,
            "PacePct": 55,
            "HighestScore": 233,
            "LowestScore": 89,
            "BatFirstWin": 52,
            "ChaseWin": 48,
            "OffBound": 70,
            "LegBound": 72,
            "StraightBound": 75,
            "PitchDesc": "Large boundaries, dual pitch option (black/red soil). True bounce, good chasing ground.",
            "RecommendedBowling": "Hit-the-deck pacers, tall spinners who roll it fast",
            "RecommendedXI": [
                "Ruturaj Gaikwad (C)", "Devon Conway (WK)", "Rachin Ravindra", 
                "Shivam Dube", "Ravindra Jadeja", "MS Dhoni", "Shardul Thakur",
                "Deepak Chahar", "Tushar Deshpande", "Maheesh Theekshana", "Matheesha Pathirana"
            ]
        }
    }
    
    # Fallback for other venues
    clean_name = venue_name.split(" (")[0]
    for key in venues_meta:
        if clean_name in key:
            return venues_meta[key]
            
    # Default venue fallback
    return {
        "FirstInnAvg": 170,
        "WinScore": 175,
        "SpinPct": 40,
        "PacePct": 60,
        "HighestScore": 220,
        "LowestScore": 80,
        "BatFirstWin": 50,
        "ChaseWin": 50,
        "OffBound": 65,
        "LegBound": 66,
        "StraightBound": 70,
        "PitchDesc": "Balanced pitch offering assistance to both batters and bowlers with steady bounce.",
        "RecommendedBowling": "Balanced pace and spin",
        "RecommendedXI": [
            "Ruturaj Gaikwad (C)", "Devon Conway (WK)", "Rachin Ravindra", 
            "Shivam Dube", "Ravindra Jadeja", "MS Dhoni", "Shardul Thakur",
            "Deepak Chahar", "Tushar Deshpande", "Maheesh Theekshana", "Matheesha Pathirana"
        ]
    }

def get_db_connection():
    """Initializes SQLite database and returns connection."""
    db_path = os.path.join(DATA_DIR, "database/settings.db")
    conn = sqlite3.connect(db_path)
    # Ensure settings table exists
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    return conn

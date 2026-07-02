import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import streamlit as st

def train_win_predictor(matches_df):
    """
    Trains a Logistic Regression model dynamically on the matches history.
    Returns the trained model and label encoders for feature mapping.
    """
    # Feature engineering
    df = matches_df.copy()
    
    # Target: 1 if CSK wins, 0 otherwise
    df["csk_win"] = (df["winner"] == "CSK").astype(int)
    
    # Feature engineering: Opponent, Venue, Toss Winner, Toss Decision
    df["opponent"] = df.apply(lambda r: r["team2"] if r["team1"] == "CSK" else r["team1"], axis=1)
    df["is_home"] = (df["venue"] == "Chepauk (Chennai)").astype(int)
    df["toss_csk"] = (df["toss_winner"] == "CSK").astype(int)
    df["toss_bat"] = (df["toss_decision"] == "bat").astype(int)
    
    # Encoders
    le_opp = LabelEncoder()
    le_opp.fit(df["opponent"])
    
    le_venue = LabelEncoder()
    le_venue.fit(df["venue"])
    
    # Encode training data
    df["opp_enc"] = le_opp.transform(df["opponent"])
    df["venue_enc"] = le_venue.transform(df["venue"])
    
    X = df[["opp_enc", "venue_enc", "is_home", "toss_csk", "toss_bat"]]
    y = df["csk_win"]
    
    model = LogisticRegression(random_state=42)
    model.fit(X, y)
    
    return model, le_opp, le_venue

def predict_match_outcome(matches_df, opponent, venue, toss_winner, toss_decision, current_form="Good"):
    """
    Uses the trained model to predict CSK win probability.
    """
    try:
        model, le_opp, le_venue = train_win_predictor(matches_df)
        
        # Format input
        is_home = 1 if venue == "Chepauk (Chennai)" else 0
        toss_csk = 1 if toss_winner == "CSK" else 0
        toss_bat = 1 if toss_decision == "bat" else 0
        
        # Handle unseen category matching
        try:
            opp_enc = le_opp.transform([opponent])[0]
        except ValueError:
            opp_enc = 0
            
        try:
            venue_enc = le_venue.transform([venue])[0]
        except ValueError:
            venue_enc = 0
            
        input_data = pd.DataFrame([[opp_enc, venue_enc, is_home, toss_csk, toss_bat]], 
                                  columns=["opp_enc", "venue_enc", "is_home", "toss_csk", "toss_bat"])
        
        # Predict probability
        prob_csk_win = model.predict_proba(input_data)[0][1]
        
        # Form adjustments
        form_multiplier = {"Excellent": 0.08, "Good": 0.03, "Average": 0.0, "Poor": -0.07}
        prob_csk_win += form_multiplier.get(current_form, 0.0)
        
        # Normalize between 10% and 90% for realism
        prob_csk_win = max(0.12, min(0.88, prob_csk_win))
        
        confidence = 100 - abs(prob_csk_win - 0.5) * 100
        
        # Key Factors list based on venue / toss
        factors = []
        if venue == "Chepauk (Chennai)":
            factors.append("Chepauk home advantage: CSK's historical spin dominance makes it highly favorable.")
        else:
            factors.append("Away fixture requires robust middle-overs containment by spinners.")
            
        if toss_winner == "CSK":
            factors.append("Toss advantage secured: Ability to control match tempo by selecting first action.")
            
        if toss_decision == "field" and venue in ["Wankhede (Mumbai)", "Chinnaswamy (Bengaluru)"]:
            factors.append("Chasing at a high-scoring venue helps with dew and target pace calculations.")
        elif toss_decision == "bat" and venue == "Chepauk (Chennai)":
            factors.append("Batting first at Chepauk avoids facing degraded pitches in the second innings.")
            
        return round(prob_csk_win * 100, 1), round(confidence, 1), factors
        
    except Exception as e:
        # Fallback heuristic
        prob = 55.0
        if venue == "Chepauk (Chennai)":
            prob += 10.0
        if toss_winner == "CSK":
            prob += 3.0
        return prob, 75.0, ["Heuristic fallback applied: " + str(e)]

def generate_playing_xi(opponent, venue, pitch_type, weather):
    """
    Selects the optimal Playing XI and Impact Player with explanations.
    """
    # Base players
    xi = {}
    
    # Heuristics based on conditions
    is_spin_friendly = (pitch_type == "Spin Friendly" or venue == "Chepauk (Chennai)")
    is_flat_deck = (pitch_type == "Flat / Batting Friendly" or venue == "Chinnaswamy (Bengaluru)")
    is_green_deck = (pitch_type == "Green / Pace Friendly")
    
    # 1. Opening Pair
    xi["openers"] = [
        {"player": "Ruturaj Gaikwad", "reason": "Squad Captain. Anchors the innings and handles new ball swing with high technical competency."},
        {"player": "Devon Conway", "reason": "Left-hand balance. Outstanding player of spin and provides clean powerplay accumulation."}
    ]
    
    # 2. Middle Order
    middle = []
    middle.append({"player": "Rachin Ravindra", "reason": "Dynamic left-hander. Can counter-attack in the powerplay if wickets fall, and bowls orthodox spin."})
    middle.append({"player": "Shivam Dube", "reason": "Provides massive firepower against middle-overs spin, particularly at venues with short boundaries."})
    
    if is_flat_deck or opponent in ["RCB", "KKR"]:
        middle.append({"player": "Sameer Rizvi", "reason": "Young aggressive batsman selected to maintain scoring rate in middle-overs on flat decks."})
    else:
        middle.append({"player": "Moeen Ali", "reason": "Veteran presence. Offers valuable off-spin against opponent left-handers and solid batting stability."})
        
    xi["middle_order"] = middle
    
    # 3. Finishers
    xi["finishers"] = [
        {"player": "Ravindra Jadeja", "reason": "Premier Indian all-rounder. Controls the middle-overs bowling rate and provides elite finishing cameos."},
        {"player": "MS Dhoni", "reason": "Wicketkeeper and finisher. Mastermind at the death, unmatched experience, and supreme glovework."}
    ]
    
    # 4. Spinners
    spinners = []
    if is_spin_friendly:
        spinners.append({"player": "Maheesh Theekshana", "reason": "Mystery carrom bowler. Restricts runs in the powerplay and extracts sharp turn on dusty wickets."})
        spinners.append({"player": "Mitchell Santner", "reason": "Left-arm restriction specialist. Offers world-class economy and handles low-scoring tracks excellently."})
    else:
        spinners.append({"player": "Maheesh Theekshana", "reason": "Provides mystery spin depth and match-up advantages against top-order right-handers."})
        spinners.append({"player": "Shardul Thakur", "reason": "Medium pacer acting as bowling depth who can bat. (Spin-Pace balance adjusted)."})
        
    xi["spinners"] = spinners
    
    # 5. Fast Bowlers
    pacers = []
    # Pathirana is a lock
    pacers.append({"player": "Matheesha Pathirana", "reason": "World-class death bowler. Slingy action delivers accurate yorkers exceeding 145km/h."})
    
    if is_green_deck or weather == "Overcast":
        pacers.append({"player": "Deepak Chahar", "reason": "swing specialist. Excellent with the new ball under overcast skies or green pitches to take early wickets."})
    else:
        pacers.append({"player": "Tushar Deshpande", "reason": "Hit-the-deck bowler. Takes wickets in the middle overs and handles pressure situations."})
        
    xi["pacers"] = pacers
    
    # 6. Impact Player Selection
    if is_spin_friendly:
        xi["impact_player"] = {"player": "Prashant Solanki", "reason": "Leg-spinner used to exploit turning tracks when defending in the second innings."}
    elif is_green_deck:
        xi["impact_player"] = {"player": "Mukesh Choudhary", "reason": "Left-arm swing bowler to double down on new ball movement under lights."}
    else:
        xi["impact_player"] = {"player": "Sameer Rizvi", "reason": "Explosive batsman to be subbed in during chases to boost the run-rate."}
        
    # Captain and Vice
    xi["captain"] = "Ruturaj Gaikwad"
    xi["vice_captain"] = "Ravindra Jadeja"
    
    return xi

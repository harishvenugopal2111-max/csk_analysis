import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_directory_structure():
    directories = [
        "pages",
        "utils",
        "assets",
        "assets/images",
        "assets/logo",
        "assets/css",
        "database",
        "reports",
        "scripts"
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def generate_players_data():
    players_data = [
        # Batters
        {
            "Player": "Ruturaj Gaikwad", "Role": "Batter", "Age": 29, "Batting Style": "Right-hand bat",
            "Bowling Style": "Right-arm offbreak", "Nationality": "Indian", "Experience": 68,
            "Career Runs": 2380, "Career Wickets": 0, "Strike Rate": 135.5, "Economy": 7.5,
            "Catches": 40, "Fitness Status": "Fit", "Salary": 18.0,
            "Strengths": "Anchor Play, Spin Hitting, Powerplay Timing",
            "Weaknesses": "Left-arm Fast Inswing, Slow Starts"
        },
        {
            "Player": "Devon Conway", "Role": "Wicketkeeper-Batter", "Age": 34, "Batting Style": "Left-hand bat",
            "Bowling Style": "Right-arm medium", "Nationality": "Overseas", "Experience": 30,
            "Career Runs": 1050, "Career Wickets": 0, "Strike Rate": 131.2, "Economy": 0.0,
            "Catches": 18, "Fitness Status": "Fit", "Salary": 6.0,
            "Strengths": "Spin Domination, Powerplay Accumulator, Sweep Shots",
            "Weaknesses": "High Pace Seam, Left-arm Orthodoxy early on"
        },
        {
            "Player": "Sameer Rizvi", "Role": "Batter", "Age": 22, "Batting Style": "Right-hand bat",
            "Bowling Style": "Right-arm offbreak", "Nationality": "Indian", "Experience": 10,
            "Career Runs": 120, "Career Wickets": 0, "Strike Rate": 145.0, "Economy": 8.5,
            "Catches": 3, "Fitness Status": "Fit", "Salary": 8.4,
            "Strengths": "Aggressive Spin Hitting, Clearing Long Boundaries",
            "Weaknesses": "Express Pace Short Ball, Outswingers"
        },
        {
            "Player": "Shaik Rasheed", "Role": "Batter", "Age": 21, "Batting Style": "Right-hand bat",
            "Bowling Style": "Right-arm legbreak", "Nationality": "Indian", "Experience": 2,
            "Career Runs": 15, "Career Wickets": 0, "Strike Rate": 110.0, "Economy": 0.0,
            "Catches": 1, "Fitness Status": "Fit", "Salary": 0.5,
            "Strengths": "Solid Technique, Timing, Anchor Capability",
            "Weaknesses": "Accelerating against high-quality spin"
        },
        # All-rounders
        {
            "Player": "Ravindra Jadeja", "Role": "All-rounder", "Age": 37, "Batting Style": "Left-hand bat",
            "Bowling Style": "Left-arm orthodox", "Nationality": "Indian", "Experience": 240,
            "Career Runs": 2950, "Career Wickets": 160, "Strike Rate": 128.5, "Economy": 7.6,
            "Catches": 105, "Fitness Status": "Fit", "Salary": 18.0,
            "Strengths": "Elite Fielding, Accurate Line/Length Spin, Middle-Overs Control",
            "Weaknesses": "Express Pace Short Ball, Struggling to start fast against spin"
        },
        {
            "Player": "Shivam Dube", "Role": "All-rounder", "Age": 32, "Batting Style": "Left-hand bat",
            "Bowling Style": "Right-arm medium", "Nationality": "Indian", "Experience": 65,
            "Career Runs": 1610, "Career Wickets": 5, "Strike Rate": 141.2, "Economy": 8.9,
            "Catches": 12, "Fitness Status": "Fit", "Salary": 12.0,
            "Strengths": "Spin Destroyer, Massive Hit Power, Tall Reach",
            "Weaknesses": "Express Pace Rib-cage Bouncers, Hard Lengths"
        },
        {
            "Player": "Rachin Ravindra", "Role": "All-rounder", "Age": 26, "Batting Style": "Left-hand bat",
            "Bowling Style": "Left-arm orthodox", "Nationality": "Overseas", "Experience": 15,
            "Career Runs": 450, "Career Wickets": 5, "Strike Rate": 140.0, "Economy": 8.2,
            "Catches": 8, "Fitness Status": "Rest", "Salary": 4.0,
            "Strengths": "Powerplay Intent, Lofted Cover Drives, Useful Left-arm Spin",
            "Weaknesses": "Off-spin Matchup, Outswing outside off stump"
        },
        {
            "Player": "Mitchell Santner", "Role": "All-rounder", "Age": 34, "Batting Style": "Left-hand bat",
            "Bowling Style": "Left-arm orthodox", "Nationality": "Overseas", "Experience": 25,
            "Career Runs": 160, "Career Wickets": 20, "Strike Rate": 125.0, "Economy": 6.9,
            "Catches": 15, "Fitness Status": "Fit", "Salary": 2.0,
            "Strengths": "Impeccable Economy, Under-cutting Carrom Spin, Smart Running",
            "Weaknesses": "Power Hitting range against high-pace bowlers"
        },
        {
            "Player": "Shardul Thakur", "Role": "All-rounder", "Age": 34, "Batting Style": "Right-hand bat",
            "Bowling Style": "Right-arm fast-medium", "Nationality": "Indian", "Experience": 95,
            "Career Runs": 320, "Career Wickets": 96, "Strike Rate": 140.0, "Economy": 8.9,
            "Catches": 23, "Fitness Status": "Rehab", "Salary": 4.0,
            "Strengths": "Partnership Breaker, Golden Arm, Lower Order Cameos",
            "Weaknesses": "Leaking Boundary Runs, Consistency of Length"
        },
        {
            "Player": "Moeen Ali", "Role": "All-rounder", "Age": 38, "Batting Style": "Left-hand bat",
            "Bowling Style": "Right-arm offbreak", "Nationality": "Overseas", "Experience": 67,
            "Career Runs": 1100, "Career Wickets": 35, "Strike Rate": 138.0, "Economy": 7.1,
            "Catches": 21, "Fitness Status": "Fit", "Salary": 8.0,
            "Strengths": "Destroying Off-spin, Powerplay Bowling, Quick Hands",
            "Weaknesses": "High Pace Short Ball, Left-arm Orthodox matchups"
        },
        # Wicketkeepers
        {
            "Player": "MS Dhoni", "Role": "Wicketkeeper-Batter", "Age": 44, "Batting Style": "Right-hand bat",
            "Bowling Style": "Right-arm medium", "Nationality": "Indian", "Experience": 264,
            "Career Runs": 5240, "Career Wickets": 0, "Strike Rate": 137.5, "Economy": 0.0,
            "Catches": 148, "Fitness Status": "Fit", "Salary": 4.0,
            "Strengths": "Death Overs Power, Elite Gloves, Tactical Genius, Calmness",
            "Weaknesses": "Slow Pitch Leg Spin, High Dot Ball % early in innings"
        },
        # Bowlers
        {
            "Player": "Matheesha Pathirana", "Role": "Bowler", "Age": 23, "Batting Style": "Right-hand bat",
            "Bowling Style": "Right-arm fast", "Nationality": "Overseas", "Experience": 29,
            "Career Runs": 10, "Career Wickets": 45, "Strike Rate": 100.0, "Economy": 7.8,
            "Catches": 5, "Fitness Status": "Fit", "Salary": 13.0,
            "Strengths": "Slingy Release, Searing Death Overs Yorks, Hard-to-read Slower ball",
            "Weaknesses": "Early Control of Swing, Control over Extras"
        },
        {
            "Player": "Tushar Deshpande", "Role": "Bowler", "Age": 30, "Batting Style": "Right-hand bat",
            "Bowling Style": "Right-arm fast-medium", "Nationality": "Indian", "Experience": 36,
            "Career Runs": 30, "Career Wickets": 42, "Strike Rate": 90.0, "Economy": 8.8,
            "Catches": 9, "Fitness Status": "Fit", "Salary": 5.0,
            "Strengths": "Wicket-taking Ability, Hard Lengths, Inswing to right handers",
            "Weaknesses": "Predictable Slower balls, High Economy in Death Overs"
        },
        {
            "Player": "Deepak Chahar", "Role": "Bowler", "Age": 33, "Batting Style": "Right-hand bat",
            "Bowling Style": "Right-arm fast-medium", "Nationality": "Indian", "Experience": 80,
            "Career Runs": 120, "Career Wickets": 72, "Strike Rate": 135.0, "Economy": 7.9,
            "Catches": 19, "Fitness Status": "Rehab", "Salary": 6.0,
            "Strengths": "Powerplay Outswing, Early Breakthroughs, Handy Batting",
            "Weaknesses": "Injury Recovery, Bowling in the Death Overs"
        },
        {
            "Player": "Maheesh Theekshana", "Role": "Bowler", "Age": 25, "Batting Style": "Right-hand bat",
            "Bowling Style": "Right-arm offbreak", "Nationality": "Overseas", "Experience": 34,
            "Career Runs": 15, "Career Wickets": 35, "Strike Rate": 80.0, "Economy": 7.4,
            "Catches": 6, "Fitness Status": "Fit", "Salary": 5.5,
            "Strengths": "Mystery Carrom Ball, Powerplay Control, Off-spinner matchup",
            "Weaknesses": "Ground Fielding, Dropped Catches"
        },
        {
            "Player": "Mukesh Choudhary", "Role": "Bowler", "Age": 27, "Batting Style": "Left-hand bat",
            "Bowling Style": "Left-arm fast-medium", "Nationality": "Indian", "Experience": 18,
            "Career Runs": 5, "Career Wickets": 18, "Strike Rate": 60.0, "Economy": 8.5,
            "Catches": 3, "Fitness Status": "Fit", "Salary": 1.0,
            "Strengths": "Left-arm Powerplay Swing, Angling across right-hand batters",
            "Weaknesses": "Vulnerable at the Death, Injury prone"
        },
        {
            "Player": "Simarjeet Singh", "Role": "Bowler", "Age": 27, "Batting Style": "Right-hand bat",
            "Bowling Style": "Right-arm medium-fast", "Nationality": "Indian", "Experience": 12,
            "Career Runs": 10, "Career Wickets": 10, "Strike Rate": 80.0, "Economy": 8.6,
            "Catches": 2, "Fitness Status": "Fit", "Salary": 0.8,
            "Strengths": "Hit-the-deck Bowler, High Release Point",
            "Weaknesses": "Lack of variety in slow pitches"
        },
        {
            "Player": "Prashant Solanki", "Role": "Bowler", "Age": 26, "Batting Style": "Right-hand bat",
            "Bowling Style": "Right-arm legbreak", "Nationality": "Indian", "Experience": 4,
            "Career Runs": 0, "Career Wickets": 5, "Strike Rate": 0.0, "Economy": 8.1,
            "Catches": 1, "Fitness Status": "Fit", "Salary": 0.5,
            "Strengths": "Traditional Legbreak Loop, Flighting the ball",
            "Weaknesses": "Struggles with short boundary dimensions"
        }
    ]
    df = pd.DataFrame(players_data)
    df.to_csv("players.csv", index=False)
    print("players.csv updated with salary and catches telemetry.")

def generate_auction_targets():
    targets = [
        {
            "Player": "Rishabh Pant", "Role": "Wicketkeeper-Batter", "Age": 28, "Nationality": "Indian",
            "Batting Style": "Left-hand bat", "Bowling Style": "None", "Career Runs": 3200, "Career Wickets": 0,
            "Strike Rate": 148.5, "Economy": 0.0, "Expected Auction Price": 16.5, "Base Price": 2.0,
            "Recent Form": "Excellent", "Fitness Status": "Fit", "Fit Score": 95, "Availability": "100%",
            "Risk": "Low", "Value Rating": "Recommended Target",
            "Reason": "Explosive middle-order left-hander, elite glovework, and potential captaincy candidate to succeed Dhoni."
        },
        {
            "Player": "Trent Boult", "Role": "Bowler", "Age": 36, "Nationality": "Overseas",
            "Batting Style": "Right-hand bat", "Bowling Style": "Left-arm fast-medium", "Career Runs": 110, "Career Wickets": 121,
            "Strike Rate": 105.0, "Economy": 7.9, "Expected Auction Price": 8.5, "Base Price": 2.0,
            "Recent Form": "Excellent", "Fitness Status": "Fit", "Fit Score": 92, "Availability": "100%",
            "Risk": "Low", "Value Rating": "High Value Option",
            "Reason": "Elite left-arm powerplay swing specialist who addresses CSK's historical lack of a world-class left-arm pacer."
        },
        {
            "Player": "Mitchell Starc", "Role": "Bowler", "Age": 36, "Nationality": "Overseas",
            "Batting Style": "Left-hand bat", "Bowling Style": "Left-arm fast", "Career Runs": 180, "Career Wickets": 92,
            "Strike Rate": 115.0, "Economy": 8.6, "Expected Auction Price": 12.0, "Base Price": 2.0,
            "Recent Form": "Good", "Fitness Status": "Fit", "Fit Score": 88, "Availability": "90%",
            "Risk": "Medium", "Value Rating": "High Value Option",
            "Reason": "Express pace, steep bounce, and lethal death-overs yorkers, though comes with a high price tag and fitness risk."
        },
        {
            "Player": "Ravichandran Ashwin", "Role": "All-rounder", "Age": 39, "Nationality": "Indian",
            "Batting Style": "Right-hand bat", "Bowling Style": "Right-arm offbreak", "Career Runs": 820, "Career Wickets": 172,
            "Strike Rate": 118.0, "Economy": 7.1, "Expected Auction Price": 4.5, "Base Price": 1.5,
            "Recent Form": "Good", "Fitness Status": "Fit", "Fit Score": 94, "Availability": "100%",
            "Risk": "Low", "Value Rating": "Budget Option",
            "Reason": "CSK alumnus with exceptional tactical intelligence, defensive off-spin control, and lower-order batting stability at Chepauk."
        },
        {
            "Player": "Quinton de Kock", "Role": "Wicketkeeper-Batter", "Age": 33, "Nationality": "Overseas",
            "Batting Style": "Left-hand bat", "Bowling Style": "None", "Career Runs": 3150, "Career Wickets": 0,
            "Strike Rate": 134.2, "Economy": 0.0, "Expected Auction Price": 7.0, "Base Price": 2.0,
            "Recent Form": "Good", "Fitness Status": "Fit", "Fit Score": 85, "Availability": "100%",
            "Risk": "Low", "Value Rating": "Recommended Target",
            "Reason": "Aggressive overseas opener and solid keeper who can replicate Devon Conway's anchor-hitting profile."
        },
        {
            "Player": "Arshdeep Singh", "Role": "Bowler", "Age": 27, "Nationality": "Indian",
            "Batting Style": "Left-hand bat", "Bowling Style": "Left-arm fast-medium", "Career Runs": 45, "Career Wickets": 77,
            "Strike Rate": 80.0, "Economy": 8.7, "Expected Auction Price": 13.5, "Base Price": 2.0,
            "Recent Form": "Excellent", "Fitness Status": "Fit", "Fit Score": 93, "Availability": "100%",
            "Risk": "Low", "Value Rating": "Recommended Target",
            "Reason": "Premier Indian left-arm pacer, highly skilled in death overs bowling and new-ball swing. Long-term asset."
        },
        {
            "Player": "Jos Buttler", "Role": "Wicketkeeper-Batter", "Age": 35, "Nationality": "Overseas",
            "Batting Style": "Right-hand bat", "Bowling Style": "None", "Career Runs": 3580, "Career Wickets": 0,
            "Strike Rate": 147.5, "Economy": 0.0, "Expected Auction Price": 14.0, "Base Price": 2.0,
            "Recent Form": "Excellent", "Fitness Status": "Fit", "Fit Score": 89, "Availability": "100%",
            "Risk": "Medium", "Value Rating": "High Value Option",
            "Reason": "Match-winning opener, explosive scoring capability in the powerplay, and vast captaincy/leadership experience."
        },
        {
            "Player": "David Miller", "Role": "Batter", "Age": 36, "Nationality": "Overseas",
            "Batting Style": "Left-hand bat", "Bowling Style": "None", "Career Runs": 2850, "Career Wickets": 0,
            "Strike Rate": 139.2, "Economy": 0.0, "Expected Auction Price": 6.5, "Base Price": 1.5,
            "Recent Form": "Good", "Fitness Status": "Fit", "Fit Score": 84, "Availability": "100%",
            "Risk": "Low", "Value Rating": "Budget Option",
            "Reason": "Proven middle-order finisher under pressure; handles spin well and offers strong support to Dube/Dhoni."
        },
        {
            "Player": "Washington Sundar", "Role": "All-rounder", "Age": 26, "Nationality": "Indian",
            "Batting Style": "Left-hand bat", "Bowling Style": "Right-arm offbreak", "Career Runs": 420, "Career Wickets": 38,
            "Strike Rate": 120.5, "Economy": 7.4, "Expected Auction Price": 9.0, "Base Price": 2.0,
            "Recent Form": "Good", "Fitness Status": "Fit", "Fit Score": 91, "Availability": "100%",
            "Risk": "Low", "Value Rating": "Recommended Target",
            "Reason": "Local Chennai talent, provides defensive powerplay off-spin and handy left-handed batting utility in middle-overs."
        },
        {
            "Player": "Yuzvendra Chahal", "Role": "Bowler", "Age": 35, "Nationality": "Indian",
            "Batting Style": "Right-hand bat", "Bowling Style": "Right-arm legbreak", "Career Runs": 40, "Career Wickets": 205,
            "Strike Rate": 55.0, "Economy": 7.7, "Expected Auction Price": 8.0, "Base Price": 2.0,
            "Recent Form": "Good", "Fitness Status": "Fit", "Fit Score": 90, "Availability": "100%",
            "Risk": "Low", "Value Rating": "High Value Option",
            "Reason": "IPL's all-time leading wicket-taker. Solves CSK's missing wrist-spin puzzle and thrives in middle-overs wicket-taking."
        },
        {
            "Player": "T Natarajan", "Role": "Bowler", "Age": 34, "Nationality": "Indian",
            "Batting Style": "Left-hand bat", "Bowling Style": "Left-arm fast-medium", "Career Runs": 10, "Career Wickets": 65,
            "Strike Rate": 60.0, "Economy": 8.4, "Expected Auction Price": 7.5, "Base Price": 1.5,
            "Recent Form": "Good", "Fitness Status": "Fit", "Fit Score": 92, "Availability": "100%",
            "Risk": "Medium", "Value Rating": "Recommended Target",
            "Reason": "Tamil Nadu native, lethal yorker accuracy at the death. Complements Pathirana's slingy releases perfectly."
        },
        {
            "Player": "Khaleel Ahmed", "Role": "Bowler", "Age": 28, "Nationality": "Indian",
            "Batting Style": "Right-hand bat", "Bowling Style": "Left-arm fast-medium", "Career Runs": 5, "Career Wickets": 68,
            "Strike Rate": 50.0, "Economy": 8.5, "Expected Auction Price": 7.0, "Base Price": 1.5,
            "Recent Form": "Good", "Fitness Status": "Fit", "Fit Score": 90, "Availability": "100%",
            "Risk": "Low", "Value Rating": "Budget Option",
            "Reason": "Experienced Indian left-arm bowler who creates angles across right-handers in powerplay matches."
        }
    ]
    df = pd.DataFrame(targets)
    df.to_csv("auction_targets.csv", index=False)
    print("auction_targets.csv generated successfully with 12 prime candidates.")

def generate_matches_and_deliveries():
    venues = [
        "Chepauk (Chennai)",
        "Wankhede (Mumbai)",
        "Chinnaswamy (Bengaluru)",
        "Narendra Modi Stadium (Ahmedabad)",
        "Eden Gardens (Kolkata)",
        "Rajiv Gandhi Stadium (Hyderabad)",
        "Arun Jaitley Stadium (Delhi)",
        "Ekana Stadium (Lucknow)",
        "Sawai Mansingh Stadium (Jaipur)"
    ]
    
    opponents = ["MI", "RCB", "GT", "SRH", "KKR", "RR", "PBKS", "DC", "LSG"]
    csk_players = [
        "Ruturaj Gaikwad", "Devon Conway", "Shivam Dube", "Rachin Ravindra", 
        "Ravindra Jadeja", "MS Dhoni", "Sameer Rizvi", "Mitchell Santner", 
        "Shardul Thakur", "Deepak Chahar", "Tushar Deshpande", "Matheesha Pathirana",
        "Maheesh Theekshana", "Mukesh Choudhary"
    ]
    
    opponent_players = {
        "MI": ["Rohit Sharma", "Ishan Kishan", "Suryakumar Yadav", "Hardik Pandya", "Jasprit Bumrah"],
        "RCB": ["Virat Kohli", "Faf du Plessis", "Glenn Maxwell", "Rajat Patidar", "Mohammed Siraj"],
        "GT": ["Shubman Gill", "Sai Sudharsan", "David Miller", "Rashid Khan", "Mohit Sharma"],
        "SRH": ["Travis Head", "Abhishek Sharma", "Heinrich Klaasen", "Pat Cummins", "Bhuvneshwar Kumar"],
        "KKR": ["Sunil Narine", "Phil Salt", "Shreyas Iyer", "Rinku Singh", "Mitchell Starc"],
        "RR": ["Yashasvi Jaiswal", "Jos Buttler", "Sanju Samson", "Riyan Parag", "Yuzvendra Chahal"],
        "PBKS": ["Shikhar Dhawan", "Jonny Bairstow", "Liam Livingstone", "Sam Curran", "Arshdeep Singh"],
        "DC": ["David Warner", "Prithvi Shaw", "Rishabh Pant", "Axar Patel", "Kuldeep Yadav"],
        "LSG": ["KL Rahul", "Quinton de Kock", "Nicholas Pooran", "Marcus Stoinis", "Ravi Bishnoi"]
    }
    
    matches = []
    deliveries = []
    
    start_date = datetime(2021, 4, 9)
    match_id_counter = 1
    
    # Generate matches across seasons
    for year in [2021, 2022, 2023, 2024, 2025]:
        num_matches = 30
        season_date = start_date + timedelta(days=(year - 2021) * 365)
        
        for m_idx in range(num_matches):
            opponent = np.random.choice(opponents)
            venue = np.random.choice(venues)
            if np.random.rand() < 0.4:
                venue = "Chepauk (Chennai)"
                
            toss_winner = np.random.choice(["CSK", opponent])
            toss_decision = np.random.choice(["bat", "field"])
            
            # home ground vs away
            win_prob = 0.58
            if venue == "Chepauk (Chennai)":
                win_prob = 0.72
            if opponent in ["MI", "GT"]:
                win_prob -= 0.08
                
            winner = "CSK" if np.random.rand() < win_prob else opponent
            win_type = np.random.choice(["runs", "wickets"])
            
            if win_type == "runs":
                win_margin = max(1, int(np.random.normal(25, 15)))
            else:
                win_margin = max(1, min(10, int(np.random.normal(5, 2))))
                
            match_date = season_date + timedelta(days=m_idx * 3)
            
            avg_score = 175
            if venue == "Chepauk (Chennai)":
                avg_score = 168
            elif venue == "Chinnaswamy (Bengaluru)":
                avg_score = 192
            elif venue == "Ekana Stadium (Lucknow)":
                avg_score = 158  # Spin-friendly, slow
                
            csk_score = int(np.random.normal(avg_score, 20))
            opp_score = int(np.random.normal(avg_score, 20))
            
            if winner == "CSK":
                if win_type == "runs":
                    opp_score = csk_score - win_margin
                else:
                    csk_score = opp_score + int(np.random.randint(2, 8))
            else:
                if win_type == "runs":
                    csk_score = opp_score - win_margin
                else:
                    opp_score = csk_score + int(np.random.randint(2, 8))
            
            csk_wickets = np.random.randint(2, 10) if winner != "CSK" or win_type == "runs" else np.random.randint(2, 8)
            opp_wickets = np.random.randint(2, 10) if winner == "CSK" or win_type == "runs" else np.random.randint(2, 8)
            
            pom = np.random.choice(csk_players if winner == "CSK" else opponent_players[opponent])
            
            match_row = {
                "match_id": match_id_counter,
                "season": str(year),
                "date": match_date.strftime("%Y-%m-%d"),
                "venue": venue,
                "team1": "CSK",
                "team2": opponent,
                "toss_winner": toss_winner,
                "toss_decision": toss_decision,
                "winner": winner,
                "win_type": win_type,
                "win_margin": win_margin,
                "player_of_match": pom,
                "team1_score": csk_score,
                "team1_wickets": csk_wickets,
                "team2_score": opp_score,
                "team2_wickets": opp_wickets
            }
            matches.append(match_row)
            
            # Generate deliveries for 2024 and 2025 to keep sizes logical
            generate_delivs = (year >= 2024) or (m_idx % 3 == 0)
            if generate_delivs:
                for inning in [1, 2]:
                    batting_team = "CSK" if (inning == 1 and toss_decision == "bat" and toss_winner == "CSK") or \
                                           (inning == 1 and toss_decision == "field" and toss_winner != "CSK") or \
                                           (inning == 2 and toss_decision == "field" and toss_winner == "CSK") or \
                                           (inning == 2 and toss_decision == "bat" and toss_winner != "CSK") else opponent
                    bowling_team = opponent if batting_team == "CSK" else "CSK"
                    
                    batters = csk_players[:7] if batting_team == "CSK" else opponent_players[opponent][:5] + ["Tail 1", "Tail 2"]
                    bowlers = opponent_players[opponent][3:] + ["Op Bowler 1"] if bowling_team == "CSK" else csk_players[7:]
                    if len(bowlers) < 5:
                        bowlers = bowlers + csk_players[4:7]
                        
                    curr_bat_idx = 0
                    striker = batters[curr_bat_idx]
                    curr_bat_idx += 1
                    non_striker = batters[curr_bat_idx]
                    curr_bat_idx += 1
                    
                    wkts = 0
                    runs_cum = 0
                    target = opp_score if inning == 2 and batting_team == "CSK" else csk_score
                    if inning == 2:
                        target_runs = target
                    else:
                        target_runs = csk_score if batting_team == "CSK" else opp_score
                        
                    for over in range(20):
                        if wkts >= 10 or (inning == 2 and runs_cum > target_runs):
                            break
                        
                        # bowler rotation
                        if over < 6:
                            bowler = bowlers[over % 2]
                        elif over < 15:
                            bowler = bowlers[2 + (over % 3)]
                        else:
                            bowler = bowlers[-1] if over % 2 == 0 else bowlers[-2]
                            
                        for ball in range(1, 7):
                            if wkts >= 10 or (inning == 2 and runs_cum > target_runs):
                                break
                                
                            runs_off_bat = np.random.choice([0, 1, 2, 4, 6], p=[0.35, 0.40, 0.08, 0.12, 0.05])
                            wicket_prob = 0.04
                            
                            if "Dhoni" in striker or "Dube" in striker or "Pooran" in striker:
                                runs_off_bat = np.random.choice([0, 1, 2, 4, 6], p=[0.38, 0.30, 0.05, 0.12, 0.15])
                                wicket_prob = 0.05
                            elif "Ruturaj" in striker or "Kohli" in striker:
                                runs_off_bat = np.random.choice([0, 1, 2, 4, 6], p=[0.25, 0.48, 0.12, 0.12, 0.03])
                                wicket_prob = 0.02
                                
                            if "Bumrah" in bowler or "Pathirana" in bowler or "Jadeja" in bowler:
                                runs_off_bat = np.random.choice([0, 1, 2, 4], p=[0.45, 0.42, 0.08, 0.05])
                                wicket_prob = 0.045
                                
                            is_wkt = np.random.rand() < wicket_prob
                            wkt_type = None
                            pd_dismissed = None
                            
                            if is_wkt:
                                wkts += 1
                                pd_dismissed = striker
                                wkt_type = np.random.choice(["caught", "bowled", "lbw", "run out"], p=[0.6, 0.2, 0.15, 0.05])
                                runs_off_bat = 0
                                if curr_bat_idx < len(batters):
                                    striker = batters[curr_bat_idx]
                                    curr_bat_idx += 1
                                else:
                                    striker = f"Tail {curr_bat_idx}"
                                    curr_bat_idx += 1
                            else:
                                runs_cum += runs_off_bat
                                
                            if runs_off_bat in [1, 3, 5]:
                                striker, non_striker = non_striker, striker
                                
                            ex = 0
                            wd = 0
                            nb = 0
                            if np.random.rand() < 0.05:
                                ex = 1
                                wd = 1
                                runs_cum += 1
                                
                            speed = 0.0
                            if "Pathirana" in bowler or "Bumrah" in bowler:
                                speed = round(float(np.random.normal(143.5, 4.2)), 1)
                            elif "Chahar" in bowler or "Thakur" in bowler:
                                speed = round(float(np.random.normal(132.8, 3.1)), 1)
                                
                            delivery_row = {
                                "match_id": match_id_counter,
                                "inning": inning,
                                "batting_team": batting_team,
                                "bowling_team": bowling_team,
                                "over": over,
                                "ball": ball,
                                "batter": striker,
                                "non_striker": non_striker,
                                "bowler": bowler,
                                "runs_off_bat": runs_off_bat,
                                "extras": ex,
                                "wides": wd,
                                "noballs": nb,
                                "byes": 0,
                                "legbyes": 0,
                                "wicket_type": wkt_type if is_wkt else "",
                                "player_dismissed": pd_dismissed if is_wkt else "",
                                "ball_speed": speed
                            }
                            deliveries.append(delivery_row)
                            
            match_id_counter += 1
            
    df_matches = pd.DataFrame(matches)
    df_deliveries = pd.DataFrame(deliveries)
    
    df_matches.to_csv("matches.csv", index=False)
    df_deliveries.to_csv("deliveries.csv", index=False)
    print("matches and deliveries regenerated successfully.")

if __name__ == "__main__":
    print("Regenerating upgraded datasets for High Performance Strategy Lab...")
    create_directory_structure()
    generate_players_data()
    generate_auction_targets()
    generate_matches_and_deliveries()
    print("Done!")

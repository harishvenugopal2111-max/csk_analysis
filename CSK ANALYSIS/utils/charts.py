import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

CSK_YELLOW = "#FFD305"
CSK_NAVY = "#002B66"
ACCENT_BLUE = "#3B82F6"
BG_CARD = "rgba(13, 20, 38, 0.7)"

def get_plot_layout(is_dark=True):
    font_color = "#F3F4F6" if is_dark else "#09090b"
    grid_color = "rgba(255, 255, 255, 0.06)" if is_dark else "rgba(0, 0, 0, 0.06)"
    
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, -apple-system, sans-serif", color=font_color, size=11),
        margin=dict(l=40, r=20, t=30, b=40),
        xaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=grid_color,
            tickfont=dict(size=10, color="#9CA3AF" if is_dark else "#52525b"),
            showgrid=True,
        ),
        yaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=grid_color,
            tickfont=dict(size=10, color="#9CA3AF" if is_dark else "#52525b"),
            showgrid=True,
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=10, color=font_color)
        )
    )

def plot_season_performance(matches_df, is_dark=True):
    """Line + bar chart showing matches played vs wins per season."""
    csk_matches = matches_df[(matches_df["team1"] == "CSK") | (matches_df["team2"] == "CSK")]
    
    summary = []
    for season, group in csk_matches.groupby("season"):
        total = len(group)
        wins = len(group[group["winner"] == "CSK"])
        win_rate = (wins / total) * 100 if total > 0 else 0
        summary.append({"Season": season, "Total Matches": total, "Wins": wins, "Win Rate (%)": round(win_rate, 1)})
        
    df = pd.DataFrame(summary)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df["Season"],
        y=df["Total Matches"],
        name="Total Matches",
        marker_color="rgba(59, 130, 246, 0.35)",
        bordercolor=ACCENT_BLUE,
        borderwidth=1.5
    ))
    
    fig.add_trace(go.Bar(
        x=df["Season"],
        y=df["Wins"],
        name="Wins",
        marker_color="rgba(255, 211, 5, 0.45)",
        bordercolor=CSK_YELLOW,
        borderwidth=1.5
    ))
    
    fig.add_trace(go.Scatter(
        x=df["Season"],
        y=df["Win Rate (%)"],
        name="Win Rate (%)",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color="#10B981", width=3),
        marker=dict(size=8, symbol="diamond")
    ))
    
    layout = get_plot_layout(is_dark)
    layout.update(dict(
        title="",
        barmode="group",
        yaxis=dict(title="Matches", gridcolor="rgba(255, 255, 255, 0.06)", showgrid=True),
        yaxis2=dict(
            title="Win Rate (%)",
            overlaying="y",
            side="right",
            range=[0, 100],
            showgrid=False
        )
    ))
    
    fig.update_layout(layout)
    return fig

def plot_runs_trend(matches_df, is_dark=True):
    """Line chart representing run scoring trajectory over time."""
    # Let's filter matches where CSK played
    csk_m = matches_df[(matches_df["team1"] == "CSK") | (matches_df["team2"] == "CSK")].sort_values("date")
    
    # Calculate CSK's score
    scores = []
    for _, row in csk_m.iterrows():
        score = row["team1_score"] if row["team1"] == "CSK" else row["team2_score"]
        opponent = row["team2"] if row["team1"] == "CSK" else row["team1"]
        opp_score = row["team2_score"] if row["team1"] == "CSK" else row["team1_score"]
        scores.append({
            "Match": f"vs {opponent} ({row['season']})",
            "CSK Score": score,
            "Opponent Score": opp_score
        })
    df = pd.DataFrame(scores).tail(15) # Show last 15 matches for readability
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Match"],
        y=df["CSK Score"],
        name="CSK Score",
        mode="lines+markers",
        line=dict(color=CSK_YELLOW, width=2.5),
        marker=dict(size=6)
    ))
    fig.add_trace(go.Scatter(
        x=df["Match"],
        y=df["Opponent Score"],
        name="Opponent Score",
        mode="lines+markers",
        line=dict(color=ACCENT_BLUE, width=2, dash="dash"),
        marker=dict(size=6)
    ))
    
    layout = get_plot_layout(is_dark)
    layout.update(dict(
        xaxis=dict(tickangle=45, gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(title="Runs scored")
    ))
    fig.update_layout(layout)
    return fig

def plot_wickets_trend(deliveries_df, is_dark=True):
    """Trend chart showing bowler statistics (wickets and economy) for main squad."""
    csk_bowling = deliveries_df[deliveries_df["bowling_team"] == "CSK"]
    
    # Exclude runs that are wide/noball from bowling runs
    csk_bowling["is_wide"] = csk_bowling["wides"] > 0
    csk_bowling["is_noball"] = csk_bowling["noballs"] > 0
    csk_bowling["bowling_runs"] = csk_bowling["runs_off_bat"]
    # Wides and noballs are added to bowling runs
    csk_bowling.loc[csk_bowling["is_wide"] | csk_bowling["is_noball"], "bowling_runs"] += csk_bowling["extras"]
    
    # Calculate wickets (excluding run outs)
    valid_wickets = ["caught", "bowled", "lbw", "stumped", "caught and bowled", "hit wicket"]
    csk_bowling["is_bowler_wicket"] = csk_bowling["wicket_type"].isin(valid_wickets)
    
    bowler_stats = csk_bowling.groupby("bowler").agg(
        Balls=("ball", "count"),
        Runs=("bowling_runs", "sum"),
        Wickets=("is_bowler_wicket", "sum")
    ).reset_index()
    
    # Filter bowlers with meaningful volume
    bowler_stats = bowler_stats[bowler_stats["Balls"] >= 60]
    bowler_stats["Overs"] = bowler_stats["Balls"] / 6
    bowler_stats["Economy"] = round(bowler_stats["Runs"] / bowler_stats["Overs"], 2)
    bowler_stats = bowler_stats.sort_values(by="Wickets", ascending=False).head(8)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bowler_stats["bowler"],
        y=bowler_stats["Wickets"],
        name="Wickets",
        marker_color="rgba(16, 185, 129, 0.4)",
        bordercolor="#10B981",
        borderwidth=1.5
    ))
    
    fig.add_trace(go.Scatter(
        x=bowler_stats["bowler"],
        y=bowler_stats["Economy"],
        name="Economy",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color=CSK_YELLOW, width=2),
        marker=dict(size=8)
    ))
    
    layout = get_plot_layout(is_dark)
    layout.update(dict(
        yaxis=dict(title="Wickets", showgrid=True),
        yaxis2=dict(
            title="Economy Rate",
            overlaying="y",
            side="right",
            showgrid=False
        )
    ))
    fig.update_layout(layout)
    return fig

def plot_winning_percentage(matches_df, is_dark=True):
    """Donut chart for CSK's overall Win/Loss share."""
    csk_matches = matches_df[(matches_df["team1"] == "CSK") | (matches_df["team2"] == "CSK")]
    total = len(csk_matches)
    wins = len(csk_matches[csk_matches["winner"] == "CSK"])
    losses = total - wins
    
    labels = ["Wins", "Losses"]
    values = [wins, losses]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=[CSK_YELLOW, "rgba(59, 130, 246, 0.35)"], line=dict(color="#111827", width=2)),
        hoverinfo="label+percent+value",
        textinfo="percent"
    )])
    
    font_color = "#F3F4F6" if is_dark else "#09090b"
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5, font=dict(color=font_color)),
        font=dict(color=font_color)
    )
    return fig

def plot_team_comparison(matches_df, is_dark=True):
    """Bar chart comparing Head-to-Head win ratios against other teams."""
    opponents = ["RCB", "MI", "GT", "SRH", "KKR", "RR", "PBKS", "DC", "LSG"]
    h2h_data = []
    
    for opp in opponents:
        opp_matches = matches_df[((matches_df["team1"] == "CSK") & (matches_df["team2"] == opp)) |
                                 ((matches_df["team1"] == opp) & (matches_df["team2"] == "CSK"))]
        total = len(opp_matches)
        wins = len(opp_matches[opp_matches["winner"] == "CSK"])
        losses = total - wins
        win_rate = (wins / total) * 100 if total > 0 else 0
        h2h_data.append({"Opponent": opp, "Wins": wins, "Losses": losses, "WinRate": win_rate})
        
    df = pd.DataFrame(h2h_data).sort_values("WinRate", ascending=False)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["Opponent"],
        y=df["Wins"],
        name="CSK Wins",
        marker_color=CSK_YELLOW
    ))
    fig.add_trace(go.Bar(
        x=df["Opponent"],
        y=df["Losses"],
        name="CSK Losses",
        marker_color="rgba(59, 130, 246, 0.35)"
    ))
    
    layout = get_plot_layout(is_dark)
    layout.update(dict(
        barmode="stack",
        yaxis=dict(title="Matches Head-to-Head")
    ))
    fig.update_layout(layout)
    return fig

def plot_role_distribution(players_df, is_dark=True):
    """Bar chart of squad roles."""
    counts = players_df["Role"].value_counts().reset_index()
    counts.columns = ["Role", "Count"]
    
    fig = px.bar(
        counts,
        x="Role",
        y="Count",
        color="Role",
        color_discrete_sequence=[CSK_YELLOW, ACCENT_BLUE, "#10B981", "#F59E0B"]
    )
    
    layout = get_plot_layout(is_dark)
    layout.update(dict(showlegend=False))
    fig.update_layout(layout)
    return fig

def plot_age_distribution(players_df, is_dark=True):
    """Histogram of player age bins in the squad."""
    fig = px.histogram(
        players_df,
        x="Age",
        nbins=6,
        color_discrete_sequence=[CSK_YELLOW]
    )
    fig.update_traces(
        marker=dict(line=dict(color="#060B18", width=1.5)),
        opacity=0.85
    )
    
    layout = get_plot_layout(is_dark)
    layout.update(dict(
        xaxis=dict(title="Age Bins"),
        yaxis=dict(title="Number of Players")
    ))
    fig.update_layout(layout)
    return fig

def plot_boundary_dimension_chart(venue_meta, is_dark=True):
    """Polar/Radar chart displaying the stadium boundary dimensions in meters."""
    categories = ['Straight', 'Left Boundary', 'Off Boundary', 'Right Boundary', 'Leg Boundary']
    # Map from metadata
    straight = venue_meta.get("StraightBound", 70)
    left = venue_meta.get("OffBound", 65)  # Let's map Off/Leg/Straight
    right = venue_meta.get("LegBound", 65)
    
    values = [straight, left, left-2, right, right+2]
    # close the loop
    categories.append(categories[0])
    values.append(values[0])
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(255, 211, 5, 0.15)',
        line=dict(color=CSK_YELLOW, width=2),
        name='Boundary (m)'
    ))
    
    font_color = "#F3F4F6" if is_dark else "#09090b"
    grid_color = "rgba(255, 255, 255, 0.1)" if is_dark else "rgba(0, 0, 0, 0.1)"
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 90],
                gridcolor=grid_color,
                linecolor=grid_color,
                tickfont=dict(color="#9CA3AF")
            ),
            angularaxis=dict(
                gridcolor=grid_color,
                linecolor=grid_color,
                tickfont=dict(color=font_color)
            ),
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(family="DM Sans", color=font_color)
    )
    return fig

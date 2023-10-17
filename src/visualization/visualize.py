from espn_api.football import League
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add data folder to path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
# Add features folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'features')))
from import_league import import_league
from rosters import get_team, get_players, get_roster, get_top10

league_id = 201187
year = 2023
league = import_league(league_id, year)

def top10_players(league):
    """Returns a plotly figure of the top 10 players by total points for each owner

    Args:
        league (espn_api.football.League): ESPN Fantasy Football League
    Returns:
        fig (plotly.graph_objects.Figure): Plotly figure of the top 10 players by total points for each owner
    """
    
    df_teams = get_team(league)
    df_players = get_players(league)
    df_rosters = get_roster(df_players, df_teams)
    top10_df = get_top10(df_rosters)
        
    # 7 rows, 2 columns of subplots, plotly
    fig = make_subplots(rows=7, cols=2, subplot_titles=top10_df['owner'].unique())

    # iterate through each owner and row, column
    for i, owner in enumerate(top10_df['owner'].unique()):
        row = int(i/2) + 1
        col = i%2 + 1
        fig.add_trace(go.Bar(x=top10_df[top10_df['owner'] == owner]['name'],
                            y=top10_df[top10_df['owner'] == owner]['total_points'],
                            name=owner),
                    row=row, col=col)
    # Hide legend
    fig.update_layout(showlegend=False)
    # Update layout   
    fig.update_layout(height=2000, width=1000, title_text="Top 10 Players by Total Points")
    
    return fig 

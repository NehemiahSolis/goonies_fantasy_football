from espn_api.football import League
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Add data folder to path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
from import_league import import_league

league_id = 201187
year = 2023
league = import_league(league_id, year)

def get_team(league):
    """ 
    Returns a dataframe of team names, owners, and team ids
    
    Parameters
    ----------
    league : espn_api.football.League
        ESPN Fantasy Football League
        
    Returns
    -------
    df_teams : pandas.core.frame.DataFrame
        Dataframe of team names, owners, and team ids    
    """
    teams = []
    for team in league.teams:
        teams.append(team)
    df_teams = pd.DataFrame([team.__dict__ for team in teams])
    df_teams = df_teams[['team_name', 'owner', 'team_id' ]]
    
    return df_teams

def get_players(league):
    """Returns a dataframe of all players in the league

    Args:
        league (espn_api.football.League): ESPN Fantasy Football League

    Returns:
        df_players (pandas.core.frame.DataFrame): Dataframe of all players in the league
    """
    players = []
    for team in league.teams:
        for player in team.roster:
            players.append(player)
        df_team = pd.DataFrame([player.__dict__ for player in players])
        df_players = df_team.copy()
        
    return df_players

def get_roster(df_players, df_teams):
    """Returns a dataframe of all players in the league with their team names and owners

    Args:
        df_players (dataframe): Dataframe of all players in the league (from get_players)
        df_teams (dataframe): Dataframe of team names, owners, and team ids (from get_team)

    Returns:
        df_rosters (dataframe): Dataframe of all players in the league with their team names and owners
    """
    # Merge team dataframe with roster dataframe
    df_rosters = df_players.merge(df_teams, left_on='onTeamId', right_on='team_id', how='left')    
    
    return df_rosters

def get_top10(df_rosters):
    """Returns a dataframe of the top 10 players by total points for each owner
    
    Args:
        df_rosters (dataframe): Dataframe of all players in the league with their team names and owners (from get_roster)

    Returns:
        top10_df (dataframe): Dataframe of the top 10 players by total points for each owner
    """
    top10_df = df_rosters.groupby(['owner', 'name'])['total_points'].sum().reset_index()
    top10_df = top10_df.sort_values(by='total_points', ascending=False)
    top10_df = top10_df.groupby('owner').head(10)
    # Sort by owners then total_points
    top10_df = top10_df.sort_values(by=['owner', 'total_points'], ascending=[True, False])
    
    return top10_df

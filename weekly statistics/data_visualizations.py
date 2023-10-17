from espn_api.football import League
import pandas as pd
# add path to import_league.py and owners.py from src/data
import sys
sys.path.append("src/data")
sys.path.append("src/features")
sys.path.append("src/visualization")
import import_league as il
import owners as own
import visualize as vis
import rosters as ros
import plotly

league = il.import_league(league_id=201187, year=2023)
fig = vis.top10_players(league)

# Save figure to reports/figures
plotly.offline.plot(fig, filename='reports/figures/top10_players.html', auto_open=False)
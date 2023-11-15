from espn_api.football import League
import pandas as pd
import import_league as il

league = il.import_league(league_id=201187, year=2023)

""" 
Documentation of all variables for Team Class

team_id: int
team_abbrev: str
team_name: str
division_id: str
division_name: str
wins: int
losses: int
ties: int
points_for: int # total points for through out the season
points_against: int # total points against through out the season
acquisitions: int # number of acquisitions made by the team
acquisition_budget_spent: int # budget spent on acquisitions 
drops: int # number of drops made by the team
trades: int # number of trades made by the team 
owners: List[str] # array of owner ids
streak_type: str # string of either WIN or LOSS
streak_length: int # how long the streak is for streak type
standing: int # standing before playoffs
final_standing: int # final standing at end of season
draft_projected_rank: int # projected rank after draft
playoff_pct: int # teams projected chance to make playoffs
logo_url: str
roster: List[Player]

# These 3 variables will have the same index and match on those indexes
schedule: List[Team]
scores: List[int]
outcomes: List[str]

"""

def owners(league):
    """Returns a list of owners in the league
    Args:
        league (_type_): _description_

    Returns:
        dict: Dictionary of owners in the league
    """
    # Get the owners in the league and store them in a dictionary with the values being the team names
    owner_list = [team.owners for team in league.teams]
    team_list = [team.team_name for team in league.teams]
    owners = dict(zip(team_list, owner_list))
    
    return owners


def owner_schedule(league, owners, first_names=True):
    """Constructs a DataFrame of the schedule for each owner.

    Args:
        league (Object): ESPN league object.
        owners (list): List of owners in the league.

    Returns:
        pd.DataFrame: DataFrame of the schedule for each owner.
    """
    # Extract the owners from the dictionary and store them in a list
    owners = list(owners.keys())

    # Create a DataFrame for owners
    owners_df = pd.DataFrame(owners, columns=["Owner"])
    owners_df["Index"] = owners_df.index + 1

    # Add team names to owners_df
    owners_df["Team"] = owners_df["Index"].apply(
        lambda x: league.teams[x - 1].team_name
    )

    # Get the schedule for each owner
    schedule = [team.schedule for team in league.teams]

    # Add schedule to owners_df
    owners_df["Schedule"] = schedule

    # Explode the schedule into weeks
    owners_df = owners_df.explode("Schedule")

    # Drop unnecessary columns
    owners_df = owners_df.drop(columns=["Index", "Team"])

    # For each owner, assign a number 1 through 14 representing the week if there is a unique matchup
    owners_df["Week"] = owners_df.groupby("Owner").cumcount() + 1

    # Pivot the DataFrame so that each owner has a column for each week
    owners_df = owners_df.pivot(index="Owner", columns="Week", values="Schedule")

    # Rename the columns
    owners_df.columns = ["Week " + str(col) for col in owners_df.columns]

    # Reset the index
    owners_df = owners_df.reset_index()

    # In each week, replace the team name with the owner name
    for col in owners_df.columns[1:]:
        owners_df[col] = owners_df[col].apply(lambda x: x.owners)

    # For all names in the DataFrame, replace the first last name with the first name. Except if name is "Jacob Woodward", use "Woodward"
    if first_names:
        owners_df["Owner"] = owners_df["Owner"].apply(
            lambda x: x.split()[0] if x != "Jacob Woodward" else "Woodward"
        )
        # Capitalize the first letter of each name
        owners_df["Owner"] = owners_df["Owner"].apply(lambda x: x.capitalize())
        for col in owners_df.columns[1:]:
            owners_df[col] = owners_df[col].apply(
                lambda x: x.split()[0] if x != "Jacob Woodward" else "Woodward"
            )
            owners_df[col] = owners_df[col].apply(lambda x: x.capitalize())

    return owners_df

def save_schedule(owners_df, path):
    """Saves the owners_df to a csv file.

    Args:
        owners_df (pd.DataFrame): DataFrame of the schedule for each owner.
        path (str): Path to save the csv file.
    """
    owners_df.to_csv(path, index=False)

if __name__ == "__main__":
    owners = owners(league)
    owners_df = owner_schedule(league, owners)
    #save_schedule(owners_df, "reports/owner_schedule.csv")
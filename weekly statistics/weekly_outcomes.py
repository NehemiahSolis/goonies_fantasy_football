from espn_api.football import League
import pandas as pd
import import_league as il
import owners as own

league = il.import_league(league_id=201187, year=2023)
owners = own.owners(league)


def points_for(league, owners, first_names=True):
    """Returns a DataFrame of points for each team in each week

    Args:
        league (Object): ESPN league object.

    Returns:
        pd.DataFrame: DataFrame of points for each team in each week
    """
    # For each team, get the points scored each week
    points = [team.scores for team in league.teams]

    # Create a DataFrame for points
    points_df = pd.DataFrame(points)

    # Add team names to points_df
    points_df["Team"] = points_df.index + 1
    points_df["Team"] = points_df["Team"].apply(lambda x: league.teams[x - 1].team_name)

    # Replace the team names with the owner names. Flip the dictionary so that the team names are the keys
    owners = {v: k for k, v in owners.items()}
    points_df["Owner"] = points_df["Team"].apply(lambda x: owners[x])
    # Replace owner names with first names
    if first_names:
        points_df["Owner"] = points_df["Owner"].apply(
            lambda x: x.split()[0] if x != "Jacob Woodward" else "Woodward"
        )
        # Capitalize the first letter of each name
        points_df["Owner"] = points_df["Owner"].apply(lambda x: x.capitalize())

    # Drop unnecessary columns
    points_df = points_df.drop(columns=["Team"])

    # Set the index to the owner names
    points_df = points_df.set_index("Owner")

    # Flip dataframe so that index becomes columns and columns become index (weeks)
    points_df = points_df.transpose()
    
    # Re-order columns: Austin, Byron, Frankie, Gary, Grant, Jacob, Woodward, Jimmy, Jose, Kevin, Nehemiah, Rilee, Clark, Clay
    points_df = points_df[["Austin", "Byron", "Frankie", "Gary", "Grant", "Jacob", "Woodward", "Jimmy", "Jose", "Kevin", "Nehemiah", "Rilee", "Clark", "Clay"]]

    return points_df



if __name__ == "__main__":
    points_df = points_for(league, owners)
    # save to ../reports/weekly_outcomes.csv
    points_df.to_csv("reports/weekly_outcomes.csv")

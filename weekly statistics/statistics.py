def points_against(league, owners, first_names=True):
    """Returns a DataFrame of points against each team in each week

    Args:
        league (Object): ESPN league object.

    Returns:
        pd.DataFrame: DataFrame of points against each team in each week
    """
    points = [team.points_against for team in league.teams]

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

    return points_df
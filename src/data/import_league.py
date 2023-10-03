from espn_api.football import League

# Importing the league
def import_league(league_id, year) -> League:
    """Imports the league from ESPN API
    Args:
        league_id (int): ESPN league ID
        year (int): Year of the league
    Returns:
        League: ESPN league object
    """
    espn_s2 = """AEBo1xH%2Fb5bOjaZ%2FWHu81SGRj2zOwPB6DW4zVPwTOH42CoU0oKD05hhjZjpuwicz%2Fs6d1q73ZSMv8%2FrHpL9XrFL6La1GAyLgViGJ29bUTGsryg%2FbX6bHEm4IHdcLtpJ7fN53Y1%2BPXYOVAbv3LQTdYMMyfXCc9dCxgmgI36w%2BKav0KoPVDV0JyROcar75bJK7u3fX2w2%2BcBcOD05%2Fzx8zQvKmYrH7GTYrswYmoNTuHyefSquIpSrDWK2Wi2t16keGoUIwXmBkPR3WQK0M0kg9icOpi68LhtAxGd%2B9BJita%2FX3WdJ4zu7rCKgYw9PQ%2FMC%2BPjQ%3D"""
    swid = "D92738E9-FF51-4F91-B8A3-7AF454C9EE6D"
    league = League(league_id, year, espn_s2, swid)
    return league
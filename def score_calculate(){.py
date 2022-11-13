def score_calculate_home(team_name, x):
    score = 0
    for keys, values in x.items():
        if keys == "matches":
            for item in values:
                if item["homeTeam"]["name"] == team_name:
                    home_score = int(item['score']['fullTime']['home'])
                    away_score = int(item['score']['fullTime']['away'])
                    difference = home_score - away_score
                    return difference

                

 
def gd_tracker():
    gd = {}
    lst = []
    for keys, values in x.items():
        if keys == "matches":
            for item in values:
                if item["homeTeam"]["name"]not in gd:
                    goal_difference = score_calculate_home(item["homeTeam"]["name"])
                    gd[item["homeTeam"]["name"]] = [goal_difference]
                else:
                    goal_difference = score_calculate_home(item["homeTeam"]["name"])
                    gd[item["homeTeam"]["name"]].append(goal_difference)
    return gd
                    
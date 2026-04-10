import requests
# API info at https://developer.riotgames.com/docs/lol


all_game_data = requests.get("https://127.0.0.1:2999/liveclientdata/allgamedata", verify = False)       
#print(all_game_data.status_code)

player_score = requests.get("https://127.0.0.1:2999/liveclientdata/playerscores?riotId=", params = {"riotId": "Vasu#OC"}, verify = False)
#print(player_score.status_code)

game_stats = requests.get("https://127.0.0.1:2999/liveclientdata/gamestats", verify = False)
#print(game_stats.status_code)



game_mode = game_stats.json()["gameMode"]

game_time = game_stats.json()["gameTime"]

champion_name = all_game_data.json()["activePlayer"]["abilities"]["E"]["id"]
champion_name = champion_name[:-1]

kills = player_score.json()["kills"]

deaths = player_score.json()["deaths"]

assists = player_score.json()["assists"]

creep_score = player_score.json()["creepScore"]


print(game_mode)
print(game_time)
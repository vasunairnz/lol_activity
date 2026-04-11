import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
# API info at https://developer.riotgames.com/docs/lol

# 2 states  "in_game" and "out_of_game"
state = "out_of_game"

#overall Loop
while True:
    if state == "out_of_game":
        try:
            game_stats = requests.get("https://127.0.0.1:2999/liveclientdata/gamestats", verify = False)
            game_mode = game_stats.json()["gameMode"]
        except:
            print(f"[{time.ctime()}]  still out of game")
            time.sleep(10)
            continue
        state = "in_game"   # if exception didnt occur -> ingame -> change state

    
    elif state == "in_game":

        #initial call to get champion, gamemode data 
        try:
            all_game_data = requests.get("https://127.0.0.1:2999/liveclientdata/allgamedata", verify = False)       
            game_stats = requests.get("https://127.0.0.1:2999/liveclientdata/gamestats", verify = False)
        except:
            state = "out_of_game" # if fail to get data -> out of game -> continue back to waiting
            continue


        # extract gamemode and champ name from the response json
        game_mode = game_stats.json()["gameMode"]
        for player in all_game_data.json()["allPlayers"]:
            if player["riotId"] == "Vasu#OC":
                champion_name = player["championName"]
                break


        #repeated call for live kda, cs, time
        while True:       
            try:
                player_score = requests.get("https://127.0.0.1:2999/liveclientdata/playerscores?riotId=", params = {"riotId": "Vasu#OC"}, verify = False)

                game_stats = requests.get("https://127.0.0.1:2999/liveclientdata/gamestats", verify = False)
            except:
                state = "out_of_game" # if fail to get data -> out of game -> break the loop to return back to waiting
                print("game is over/quit")
                break


            game_time = game_stats.json()["gameTime"]

            kills = player_score.json()["kills"]

            deaths = player_score.json()["deaths"]

            assists = player_score.json()["assists"]

            creep_score = player_score.json()["creepScore"]
            

            print(f"{time.ctime()}  {kills}/{deaths}/{assists} | cs = {creep_score} | {champion_name} | {game_mode}")

            time.sleep(2)
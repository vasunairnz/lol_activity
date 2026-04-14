from dotenv import load_dotenv
import os
load_dotenv()
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
from pypresence import Presence
from pypresence.types import StatusDisplayType
# API info at https://developer.riotgames.com/docs/lol

riot_id = "Vasu#OC" # GLOBAL RIOT ID USED FOR APP
state = "out_of_game" # 2 states  "in_game" and "out_of_game"

# initialise discord rich presene connection
rpc = Presence(os.getenv("DISCORD_CLIENT_ID")) #id from discrd dev portal
rpc.connect()


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
            
            game_mode = game_stats.json()["gameMode"]
            
            champion_name = None
            for player in all_game_data.json()["allPlayers"]:
                if player["riotId"] == riot_id:
                    champion_name = player["championName"]
                    break
            
            if champion_name is None:
                state = "out_of_game"
                rpc.clear()
                continue

        except:
            state = "out_of_game" # if fail to get data -> out of game -> continue back to waiting
            rpc.clear()
            continue


        # extract gamemode and champ name from the response json
        

        #repeated call for live kda, cs, time
        while True:       
            try:
                player_score = requests.get("https://127.0.0.1:2999/liveclientdata/playerscores?riotId=", params = {"riotId": riot_id}, verify = False)
                player_score_data = player_score.json()

                kills = player_score_data["kills"]
                deaths = player_score_data["deaths"]
                assists = player_score_data["assists"]
                creep_score = player_score_data["creepScore"]
            
            except:
                state = "out_of_game" # if fail to get data -> out of game -> break the loop to return back to waiting
                print("game is over/quit")
                rpc.clear()
                break
            

            rpc.update(
                status_display_type=StatusDisplayType.STATE,
                state=f" {kills}/{deaths}/{assists}   |   cs = {creep_score}",
                details= f"{champion_name}",
                name= f"{game_mode}",
                # large_image = f"{champion_name}",  set up later!!!
                # large_text= f"{champion_name}",    set up later!!!
                )

            print(f"{time.ctime()}  {kills}/{deaths}/{assists} | cs = {creep_score} | {champion_name} | {game_mode}")

            time.sleep(2)
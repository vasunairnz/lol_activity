import requests

response = requests.get("https://127.0.0.1:2999/liveclientdata/allgamedata")

print(response.status_code)
print(response.text)
print(response.json())
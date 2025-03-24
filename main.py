import requests
import json

url = "http://localhost:8080"

game = input("Game number: ")
result_game = requests.get(f"{url}/partida/{game}")
print(json.dumps(result_game.json(), indent=2))

#result_jugadors = requests.get(f"{url}/jugadors")
#print(result_jugadors.json())
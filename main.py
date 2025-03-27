import requests
import json
import time

url = "http://localhost:8080"
eliminated = ""
points = {
    "Hans Muller": 0,
    "Mei Lin": 0,
    "Kenji Tanaka": 0,
    "Rahul Patel": 0,
    "John Smith": 0,
    "Ainhoa Ojeda": 0,
    "Sophie Dupont": 0,
    "Lee Min-ho": 0,
    "Olga Ivanova": 0,
    "Tariq Hassan": 0,
    "Carlos Carmona": 0,
    "Elena Viera": 0,
    "Giuseppe Rossi": 0,
    "Aisha Khan": 0,
    "Liam O'Connell": 0,
    "Isabella Dubois": 0,
    "Maria Silva": 0,
    "Fatima Diallo": 0,
    "Nadia Nkosi": 0,
    "Manaia Williams": 0
}

def participants():
    global eliminated
    result_jugadors = requests.get(f"{url}/jugadors")
    players = result_jugadors.json()
    
    print("\033[32mParticipants:\033[0m")
    time.sleep(0.6)
    for player in players:
        time.sleep(0.1)
        words = player.split()
        name = ""
        country = ""
        
        for i in range(len(words)):
            if words[i].lower() == "participant":
                name = " ".join(words[i+1:i+3]).replace(",", "").replace(".", "")
            elif words[i].lower() == "representa":
                country = words[i+2].replace(",", "").replace(".", "")
            elif words[i].lower() == "representant":
                country = words[i+2].replace(",", "").replace(".", "")
        
        if "desqualificada" in player.lower():
            eliminated = name

        print(f"{name} de {country}")

    print(f"eliminated: {eliminated}")

def guanyador():
    global eliminated
    print("\033[32mGuanyador:\033[0m")
    print("Carregant resultats...", end="", flush=True)
    for counter in range(1, 10001):

        print(f"\rCarregant resultats... Partida {counter}", end="", flush=True)
        
        result_game = requests.get(f"{url}/partida/{counter}")
        game = result_game.json()
        table = game["tauler"]

        def winner(player):
            winner_name = game[player]
            if winner_name not in eliminated:
                points[winner_name] += 1

        for row in table:
            if row == "OOO":
                winner('jugador1')
            elif row == "XXX":
                winner('jugador2')

        for col in range(3):
            if table[0][col] + table[1][col] + table[2][col] == "OOO":
                winner('jugador1')
            elif table[0][col] + table[1][col] + table[2][col] == "XXX":
                winner('jugador2')
            
        diag1 = table[0][0] + table[1][1] + table[2][2]
        diag2 = table[0][2] + table[1][1] + table[2][0]
        
        if diag1 == "OOO" or diag2 == "OOO":
            winner('jugador1')
        elif diag1 == "XXX" or diag2 == "XXX":
            winner('jugador2')
        else:
            pass
    
    highest = max(points.values())
    winners = [player for player, score in points.items() if score == highest]
    
    print("\n\033[32mGuanyador finals:\033[0m")
    for winner in winners:
        print(f"{winner}: {highest} victòries")

participants()
guanyador()
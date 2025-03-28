import requests
import json
import time

class Player:
    def __init__(self, name, country):
        self.name = name
        self.country = country
        self.points = 0
        self.is_eliminated = False

class Game:
    def __init__(self, game_data):
        self.board = game_data["tauler"]
        self.player1 = game_data["jugador1"]
        self.player2 = game_data["jugador2"]

    def check_winner(self):
        for row in self.board:
            if row == "OOO": return self.player1
            if row == "XXX": return self.player2

        for col in range(3):
            column = self.board[0][col] + self.board[1][col] + self.board[2][col]
            if column == "OOO": return self.player1
            if column == "XXX": return self.player2

        diag1 = self.board[0][0] + self.board[1][1] + self.board[2][2]
        diag2 = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag1 == "OOO" or diag2 == "OOO": return self.player1
        if diag1 == "XXX" or diag2 == "XXX": return self.player2

        return None

class Tournament:
    def __init__(self, url):
        self.url = url
        self.players = {}
        self.eliminated_player = None

    def load_players(self):
        response = requests.get(f"{self.url}/jugadors")
        players_data = response.json()
        
        print("\033[32mParticipants:\033[0m")
        time.sleep(0.6)
        
        for player_info in players_data:
            words = player_info.split()
            name = ""
            country = ""
            
            for i in range(len(words)):
                if words[i].lower() == "participant":
                    name = " ".join(words[i+1:i+3]).replace(",", "").replace(".", "")
                elif words[i].lower() in ["representa", "representant"]:
                    country = words[i+2].replace(",", "").replace(".", "")
            
            self.players[name] = Player(name, country)
            if "desqualificada" in player_info.lower():
                self.eliminated_player = name
                self.players[name].is_eliminated = True
            
            print(f"{name} de {country}")
        
        print(f"eliminated: {self.eliminated_player}")

    def play_tournament(self):
        print("\033[32mGuanyador:\033[0m")
        print("Carregant resultats...", end="", flush=True)
        
        for game_id in range(1, 10001):
            print(f"\rCarregant resultats... Partida {game_id}", end="", flush=True)
            response = requests.get(f"{self.url}/partida/{game_id}")
            game = Game(response.json())
            
            winner = game.check_winner()
            if winner and winner != self.eliminated_player:
                self.players[winner].points += 1

        self.show_results()

    def show_results(self):
        max_points = max(player.points for player in self.players.values())
        winners = [p for p in self.players.values() if p.points == max_points]
        
        print("\n\033[32mGuanyador finals:\033[0m")
        for winner in winners:
            print(f"{winner.name}: {winner.points} victòries")

def main():
    tournament = Tournament("http://localhost:8080")
    tournament.load_players()
    tournament.play_tournament()

if __name__ == "__main__":
    main()
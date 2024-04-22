import json

from models import Player
from typing import List


class PlayerService:
    def __init__(self):
        self.players: List[Player] = []


    def read_players_config(self):
        with open("config/player.json", "r") as players_file:
            players_data = json.load(players_file)
            for player in players_data["players"]:
                self.players.append(Player(
                    player_no=player["player_no"],
                    name=player["name"],
                    defence_set_length=player["defence_set_length"]
                ))
    

    def get_player_username(self, username: str):
        for player in self.players:
            if player.name == username:
                return player
        
        return None


    def get_player_id(self, id: int):
        for player in self.players:
            if player.id == id:
                return Player
            
        return None


player_service = PlayerService()
player_service.read_players_config()

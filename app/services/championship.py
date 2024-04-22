from enum import Enum
from typing import List
from random import shuffle

from models import Player

from services.game import GameService
from services.player import player_service


class ChampionshipStatus(str, Enum):
    PENDING = "PENDING"
    WAITING = "WAITING"
    STARTED = "STARTED"
    ENDED = "ENDED"
    INVALID = "INVALID"


class ChampionshipService:
    def __init__(self):
        self.status = ChampionshipStatus.PENDING
        self.enrolled_players: List[Player] = player_service.players
        self.current_players: List[Player] = []
        self.current_games: List[GameService] = []
        self.completed_games: List[GameService] = []
        self.current_game_id: int = 1


    def __check_enrolled_player(self, player: Player):
        return any(player.name == enrolled_payer.name for enrolled_payer in self.enrolled_players)


    def join_championship(self, player: Player):
        if self.__check_enrolled_player(player):
            self.current_players.append(player)
            return player
    
        else:
            return None

    def start_championship(self):
        if self.player_count < 2:
            self.status = ChampionshipStatus.INVALID
            return self.status

        if self.current_players < len(self.current_players):
            self.status = ChampionshipStatus.WAITING
            return self.status

        if self.current_players == len(self.current_players) and self.current_players == self.enrolled_players:
            self.status = ChampionshipStatus.STARTED
            return self.status

        return self.status


    def draw_games(self):
        num_players = len(self.players)
        num_games = num_players // 2
        players = shuffle(self.current_players.copy())
        for i in range(num_games):
            game_id = self.current_game_id
            player1 = players.pop(0)
            player2 = players.pop(0)
            game = GameService(id=game_id, player1=player1, player2=player2)
            self.current_games.append(game)
            self.current_game_id += 1


    def generate_report(self):
        if self.status == ChampionshipStatus.ENDED:
            raise ValueError("Championship is not ended yet")

        report = "Championship Report:\n"
        for game in self.games:
            report += f"Game {game.id}: {game.player1.username} vs {game.player2.username}, Winner: {game.winner.username}\n"
        return report


championship_service = ChampionshipService()

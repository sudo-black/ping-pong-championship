from enum import Enum
from typing import List
from random import shuffle

from models import Player

from services.game import GameService


class ChampionshipStatus(str, Enum):
    PENDING = "PENDING"
    WAITING = "WAITING"
    STARTED = "STARTED"
    ENDED = "ENDED"
    INVALID = "INVALID"


class ChampionshipService:
    def __init__(self):
        self.status = ChampionshipStatus.PENDING
        self.current_players: List[Player] = []
        self.current_games: List[GameService] = []
        self.completed_games: List[GameService] = []

    def join_championship(self, player: Player):
        self.current_players.append(player)
        return self.current_players

    def start_championship(self):
        if self.player_count < 2:
            self.status = ChampionshipStatus.INVALID
            return self.status

        if self.current_players < len(self.current_players):
            self.status = ChampionshipStatus.WAITING
            return self.status

        if self.current_players < len(self.current_players):
            self.status = ChampionshipStatus.STARTED
            return self.status

        return self.status

    def draw_games(self):
        num_players = len(self.players)
        num_games = num_players // 2
        players = self.current_players.copy()
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

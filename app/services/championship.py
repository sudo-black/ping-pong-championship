from uuid import UUID
from enum import Enum
from typing import List
from random import shuffle

from models import Player

from services.game import Turn
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
        self.current_players: List[Player] = (
            self.enrolled_players
        )  # TODO: change back to []
        self.current_games: List[GameService] = []
        self.completed_games: List[GameService] = []

    def __check_enrolled_player(self, player: Player):
        return any(
            player.name == enrolled_payer.name
            for enrolled_payer in self.enrolled_players
        )

    def join_championship(self, player: Player):
        if self.__check_enrolled_player(player):
            self.current_players.append(player)
            return player

        else:
            return None

    def start_championship(self):
        if len(self.enrolled_players) < 2:
            self.status = ChampionshipStatus.INVALID
            return self.status

        if len(self.current_players) < len(self.enrolled_players):
            self.status = ChampionshipStatus.WAITING
            return self.status

        if self.current_players == self.enrolled_players:
            self.status = ChampionshipStatus.STARTED
            return self.status

        return self.status

    def draw_games(self):
        num_players = len(self.current_players)
        num_games = num_players // 2
        players = self.current_players.copy()
        shuffle(players)
        for i in range(num_games):
            player1 = players.pop(0)
            player2 = players.pop(0)
            game = GameService(player1=player1, player2=player2, turn=Turn.PLAYER1)
            self.current_games.append(game)

    def get_game_by_player(self, player: Player):
        for game in self.current_games:
            if game.player1 == player or game.player2 == player:
                return game

        return None

    def get_game_by_id(self, id: UUID):
        for game in self.current_games:
            if game.id == id:
                return game

        return None

    def generate_report(self):
        if self.status == ChampionshipStatus.ENDED:
            raise ValueError("Championship is not ended yet")

        report = "Championship Report:\n"
        for game in self.completed_games:
            report += f"Game {game.id}: {game.player1.name} vs {game.player2.name}, Winner: {game.winner.name}\n"

        return report


championship_service = ChampionshipService()

from uuid import UUID
from uuid import uuid4
from enum import Enum
from typing import List
from typing import Tuple
from random import shuffle

from pydantic.dataclasses import dataclass

from models import Player

from services.game import Turn
from services.game import GameStatus
from services.game import GameService
from services.player import player_service


class RoundStatus(str, Enum):
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"


@dataclass
class Round:
    id: UUID = uuid4()
    games: List[GameService] = []
    winners: List[Player] = []
    status: RoundStatus = RoundStatus.READY

    def check_games_finished_status(self, update_status: bool = True) -> bool:
        check = all(game.status == GameStatus.FINISHED for game in self.games)
        if update_status and check:
            self.status == GameStatus.FINISHED

        return check

    def update_winners(self) -> List[Player]:
        if self.check_games_finished_status(update_status=False):
            for game in self.games:
                self.winners.append(game.winner)

        return self.winners


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
        self.current_round: Round | None = None
        self.completed_rounds: List[Round] = []
        self.winner: Player | None = None

    def __check_enrolled_player(self, player: Player) -> bool:
        return any(
            player.name == enrolled_payer.name
            for enrolled_payer in self.enrolled_players
        )

    def __check_current_player(self, player: Player) -> bool:
        return any(
            player.name == current_player.name
            for current_player in self.current_players
        )

    def check_championship_end(
        self, status_update: bool = True, winner_update: bool = True
    ):
        if len(self.completed_rounds) == len(self.enrolled_players) - 1:
            if status_update:
                self.status = ChampionshipStatus.ENDED

            if winner_update:
                self.winner = self.completed_rounds[-1].winners[0]

    def join_championship(self, player: Player) -> Player | None:
        if self.__check_enrolled_player(player):
            if not self.__check_current_player(player):
                self.current_players.append(player)

            return player

        else:
            return None

    def start_championship(self) -> ChampionshipStatus:
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

    def draw_games(self, bye_round: bool = True) -> List[GameService] | None:
        if self.status == ChampionshipStatus.STARTED and not self.current_round:
            self.current_round = Round()
            num_players = len(self.current_players)
            num_games = num_players // 2
            players = self.current_players.copy()
            shuffle(players)
            if num_players % 2 != 0 and bye_round:
                bye_player = players.pop(0)
                self.current_round.winners.append(bye_player)

            for i in range(num_games):
                player1 = players.pop(0)
                player2 = players.pop(0)
                game = GameService(player1=player1, player2=player2, turn=Turn.PLAYER1)
                self.current_round.games.append(game)

            return self.current_round.games

        else:
            return None

    def __get_not_none_game(
        game1: GameService, game2: GameService
    ) -> GameService | None:
        if game1:
            return game1

        elif game2:
            return game2

        else:
            return None

    def get_game_by_player_current_round(self, player: Player) -> GameService | None:
        for game in self.current_round.games:
            if game.player1 == player or game.player2 == player:
                return game

        return None

    def get_game_by_player_completed_rounds(self, player: Player) -> GameService | None:
        for round in self.completed_rounds:
            for game in round.games:
                if game.player1 == player or game.player2 == player:
                    return game

        return None

    def get_game_by_player(self, player: Player) -> GameService | None:
        game1 = self.get_game_by_player_current_round(player)
        game2 = self.get_game_by_player_completed_rounds(player)
        return self.__get_not_none_game(game1, game2)

    def get_game_by_id_current_round(self, id: UUID) -> GameService | None:
        for game in self.current_round.games:
            if game.id == id:
                return game

        return None

    def get_game_by_id_completed_rounds(self, id: UUID) -> GameService | None:
        for round in self.completed_rounds:
            for game in round.games:
                if game.id == id:
                    return game

        return None

    def get_game_by_id(self, id: UUID) -> GameService | None:
        game1 = self.get_game_by_id_current_round(id)
        game2 = self.get_game_by_id_completed_rounds(id)
        return self.__get_not_none_game(game1, game2)

    def execute_play_by_id(self, game_id: UUID) -> bool | None:
        game = self.get_game_by_id_current_round(game_id)
        if game:
            result = game.execute_play()
            if result:
                if game.status == GameStatus.FINISHED:
                    if self.current_round.check_games_finished_status():
                        self.current_players = self.current_round.update_winners()
                        self.completed_rounds.append(self.completed_rounds)
                        self.current_round = None
                        self.check_championship_end()

            return result

        return None

    def generate_report(self) -> str:
        if self.status == ChampionshipStatus.ENDED:
            raise ValueError("Championship is not ended yet")

        report = "Championship Report:\n"
        for round in self.completed_rounds:
            for game in round.games:
                report += f"Game {game.id}: {game.player1.name} vs {game.player2.name}, Winner: {game.winner.name}\n"

        report += f"Championship Winner: {self.winner.name}"

        return report


championship_service = ChampionshipService()

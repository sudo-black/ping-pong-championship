from uuid import UUID
from uuid import uuid4
from enum import Enum
from typing import List
from random import randint

from models import Player
from models import Game


class Turn(str, Enum):
    PLAYER1 = "PLAYER1"
    PLAYER2 = "PLAYER2"


class GameStatus(str, Enum):
    WAITING = "WAITING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"


class Play:
    def __init__(
        self, offensive_num: int | None = None, defensive_arr: List[int] | None = None
    ):
        self.offensive_num: int | None = offensive_num
        self.defensive_arr: List[int] | None = defensive_arr
        self.result: bool | None = None

    def __condition_execute(self):
        if self.offensive_num and isinstance(self.offensive_num, int):
            return True

        if self.defensive_arr and isinstance(self.defensive_arr, List[int]):
            return True

        return False

    def execute(self):
        if self.__condition_execute():
            if self.offensive_num in self.defensive_arr:
                self.result = True

            else:
                self.result = False

            self.offensive_num = None
            self.defensive_arr = None

        else:
            self.result = None

        return self.result


class GameService:
    def __init__(self, player1: Player, player2: Player, turn: Turn = Turn.PLAYER1):
        self.id: UUID = uuid4()
        self.player1: Player = player1
        self.player2: Player = player2
        self.turn: Turn = turn
        self.score1: int = 0
        self.score2: int = 0
        self.play: Play = Play()
        self.player1_joined: bool = False
        self.player2_joined: bool = False
        self.status: GameStatus = GameStatus.WAITING
        self.winner: Player | None = None
        # self.stats: dict = {}

    def __get_offensive_player(self):
        if self.turn == Turn.PLAYER1:
            return self.player1

        elif self.turn == Turn.PLAYER2:
            return self.player2

    def __get_defensive_player(self):
        if self.turn == Turn.PLAYER1:
            return self.player2

        elif self.turn == Turn.PLAYER2:
            return self.player1

    def __switch_turn(self):
        if self.turn == Turn.PLAYER1:
            self.turn = Turn.PLAYER2

        elif self.turn == Turn.PLAYER2:
            self.turn = Turn.PLAYER1

        return self.turn

    def __check_both_players_joined(self):
        if self.player1_joined and self.player2_joined:
            return True

    def join_game_player1(self, player: Player):
        if player == self.player1:
            self.player1_joined = True
            if self.__check_both_players_joined():
                self.status = GameStatus.RUNNING

    def join_game_player1(self, player: Player):
        if player == self.player2:
            self.player2_joined = True
            if self.__check_both_players_joined():
                self.status = GameStatus.RUNNING

    def join_game(self, player: Player):
        if player == self.player1:
            self.player1_joined = True

        elif player == self.player2:
            self.player2_joined = True

        else:
            return False

        if self.__check_both_players_joined():
            self.status = GameStatus.RUNNING

        return True

    def __create_defense_set(self, player):
        return set(randint(1, 10) for _ in range(player.defence_set_length))

    def get_offence(self) -> int | None:
        return self.play.offensive_num

    def __condition_update_offence(self, num: int) -> bool:
        if num >= 1 and num <= 10:
            return True

        else:
            return False

    def update_offence(self, num: int) -> int | None:
        if self.__condition_update_offence(num):
            self.play.offensive_num = num
            return True

        else:
            return False

    def get_defence(self) -> List[int] | None:
        return self.play.get_defensive_arr

    def __check_integers_in_range(arr: List[int]) -> bool:
        return all(isinstance(num, int) and 1 <= num <= 10 for num in arr)

    def __condition_update_defence(self, arr: List[int]) -> bool:
        player = self.__get_defensive_player()
        if len(arr) == player.defence_set_length:
            if self.__check_integers_in_range(arr):
                self.play.defensive_arr = arr
                return True

            else:
                return False

        else:
            return False

    def update_defence(self, arr: List[int] | None) -> List[int] | None:
        if self.__condition_update_defence(arr):
            self.play.defensive_arr = arr
            return self.play.defensive_arr

        else:
            return None

    def __condition_update_score(self) -> bool:
        if self.play.result is not None:
            return True

        else:
            return False

    def __update_score(self, result: bool | None) -> bool | None:
        if self.__condition_update_score():
            match result:
                case True:
                    match self.turn:
                        case Turn.PLAYER1:
                            self.score1 += 1

                        case Turn.PLAYER2:
                            self.score2 += 1

                case False:
                    match self.turn:
                        case Turn.PLAYER1:
                            self.score2 += 1

                        case Turn.PLAYER2:
                            self.score1 += 1

                    self.__switch_turn()

        else:
            return None

    def __condition_execute_play(self) -> bool:
        if self.score1 <= 5 and self.score2 <= 5:
            if self.status == GameStatus.RUNNING:
                return True

            else:
                return False

        else:
            return False

    def execute_play(self) -> bool:
        if self.__condition_execute_play():
            result = self.play.execute()
            if result:
                self.__update_score(result)
                if self.status == GameStatus.WAITING:
                    self.status = GameStatus.RUNNING
                    return True

        else:
            if self.status == GameStatus.RUNNING:
                self.status = GameStatus.FINISHED
                if self.score1 > self.score2:
                    self.winner = self.player1

                elif self.score1 < self.score2:
                    self.winner = self.player2

        return False

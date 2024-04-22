from typing import List
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass
class Referee:
    name: str
    ROLE: str = "referee"


@dataclass
class Player:
    player_no: int
    name: str
    defence_set_length: int
    ROLE: str = "player"

    def __eq__(self, other):
        if isinstance(other, Player):
            are_equal = True
            if self.player_no != other.player_no:
                are_equal = False

            if self.name != other.name:
                are_equal = False

            if self.defence_set_length != other.defence_set_length:
                are_equal = False

            return are_equal

        elif isinstance(other, List[Player]):
            return frozenset(self.__dict__.items()) == frozenset(other.__dict__.items())

        return False


@dataclass
class Game:
    id: int
    player_1: Player
    player_2: Player
    winner: Player


@dataclass
class LoginRequest:
    username: str
    password: str


@dataclass
class ApiResponse:
    status: int
    message: str | None
    data: object | None

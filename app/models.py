from pydantic import BaseModel
from pydantic.dataclasses import dataclass

@dataclass
class Referee:
    name: str

@dataclass
class Player:
    player_no: int
    name: str
    defence_set_length: int

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
    # token: dict | None

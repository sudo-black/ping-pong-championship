import json
from datetime import datetime, timedelta, timezone
from jwt import encode, decode, PyJWTError
from models import Player, Referee

# Secret key for signing JWT tokens
SECRET_KEY = "6/jotiCilCcoGf5VzODJIuEwccsTp26D7zxIiaspnVM="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Load referee data from JSON file
# with open("app/config/referee.json", "r") as referee_file:
with open("config/referee.json", "r") as referee_file:
    referee_data = json.load(referee_file)

# Load players data from JSON file
# with open("app/config/player.json", "r") as players_file:
with open("config/player.json", "r") as players_file:
    players_data = json.load(players_file)


def get_player(name: str, password: str) -> Player | None:
    for player in players_data["players"]:
        if player["name"] == name and player["password"] == password:
            player_obj = Player(
                player_no=player["player_no"],
                name=player["name"],
                defence_set_length=player["defence_set_length"]
            )
            return player_obj

    return None


def get_referee(username: str, password: str) -> Referee | None:
    if username == referee_data["referee"]["username"] and password == referee_data["referee"]["password"]:
        referee = Referee(username)
        return referee

    else:
        return None


def get_user(username: str, password: str) -> Player | Referee | None:
    referee = get_referee(username, password)
    player = get_player(username, password)
    if referee:
        return referee

    elif player:
        return player

    else:
        return None


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    try:
        encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return {
            "token": encoded_jwt,
            "exp": expire
        }

    except PyJWTError as exception:
        raise exception



def decode_token(token: str):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except PyJWTError as exception:
        raise exception

class Player:
    def __init__(self, username: str):
        self.username = username
        self.picked_number = None

class PlayerService:
    def __init__(self):
        self.players = []

    def add_player(self, username: str):
        if any(player.username == username for player in self.players):
            return 400  # Bad Request - Player already exists

        player = Player(username)
        self.players.append(player)
        return 201  # Created - Player added successfully

    def get_player(self, username: str):
        for player in self.players:
            if player.username == username:
                return player
        return 404  # Not Found - Player not found

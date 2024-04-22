from services.championship import ChampionshipService
from services.championship import championship_service


class RefereeService:
    def __init__(self):
        self.championship_service: ChampionshipService = championship_service


referee_service = RefereeService()

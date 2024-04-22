from services.championship import ChampionshipService
from services.championship import championship_service


class RefereeService:
    def __init__(self):
        self.championship_service: ChampionshipService = championship_service


    def start_championship(self):
        status = self.championship_service.start_championship()
        return status

referee_service = RefereeService()

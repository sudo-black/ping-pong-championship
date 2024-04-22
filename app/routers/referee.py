from uuid import UUID
from typing import Annotated
from dataclasses import asdict

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi import Response

from models import Referee
from models import ApiResponse

from routers.auth import get_current_user
from services.referee import referee_service
from services.championship import championship_service
from services.championship import ChampionshipStatus


router = APIRouter()


@router.get("/referee/championship", status_code=status.HTTP_200_OK)
async def get_championship(
    referee: Annotated[Referee, Depends(get_current_user)], response: Response
):
    response.status_code = status.HTTP_200_OK
    return vars(championship_service)


@router.post("/referee/championship")
async def start_championship(
    referee: Annotated[Referee, Depends(get_current_user)], response: Response
):
    championship_status: ChampionshipStatus = championship_service.start_championship()
    if championship_status == ChampionshipStatus.STARTED:
        return vars(championship_service)

    elif championship_status == ChampionshipStatus.WAITING:
        response.status_code = status.HTTP_202_ACCEPTED
        # message="Championship cant start, waiting for all players to join"
        return vars(championship_service)

    elif championship_status == ChampionshipStatus.INVALID:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        # message="Championship can't have less then 2 enrolled players"
        return vars(championship_service)

    elif championship_status == ChampionshipStatus.ENDED:
        response.status_code = status.HTTP_226_IM_USED
        # message="Championship finished, youcan generate repoet now"
        return vars(championship_service)


@router.post("/referee/games")
async def draw_games(
    referee: Annotated[Referee, Depends(get_current_user)], response: Response
):
    championship_status: ChampionshipStatus = championship_service.status
    if championship_status == ChampionshipStatus.STARTED:
        championship_service.draw_games()
        response.status_code = status.HTTP_200_OK
        return championship_service.current_games

    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Championship not in state to draw games, status: {championship_status}",
        )


@router.post("referee/game/{id}/run")
async def run_game(id: UUID):
    game = championship_service.get_game_by_id(id)
    result = game.execute_play()
    if result:
        return game

    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Unable tp run game, status: {game.status}",
        )


@router.get("/referee/export-report")
async def export_report(referee: Annotated[Referee, Depends(get_current_user)]):
    report = championship_service.generate_report()
    return report

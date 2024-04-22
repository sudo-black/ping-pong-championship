from typing import Annotated
from dataclasses import asdict

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi import Response

from models import Referee, Player
from models import ApiResponse

from routers.auth import get_current_user
from services.referee import referee_service
from services.championship import championship_service
from services.championship import ChampionshipStatus


router = APIRouter()


@router.get("/referee/championship", status_code=status.HTTP_200_OK)
async def get_championship(referee: Annotated[Referee | Player, Depends(get_current_user)], response: Response) -> ApiResponse:
    response.status_code = status.HTTP_200_OK
    return asdict(championship_service)


@router.post("/referee/championship")
async def start_championship(referee: Annotated[Referee, Depends(get_current_user)]) -> ApiResponse:
    championship_status: ChampionshipStatus = championship_service.start_championship()
    if championship_status == ChampionshipStatus.STARTED:
        return ApiResponse(
            status=status.HTTP_200_OK,
            message="Championship started",
            data=asdict(championship_service)
        )
    
    elif championship_status == ChampionshipStatus.WAITING:
        return ApiResponse(
            status=status.HTTP_202_ACCEPTED,
            message="Championship cant start, waiting for all players to join",
            data=asdict(championship_service)
        )
    
    elif championship_status == ChampionshipStatus.INVALID:
        return ApiResponse(
            status=status.HTTP_406_NOT_ACCEPTABLE,
            message="Championship cant start, waiting for all players to join",
            data=asdict(championship_service)
        )

    elif championship_status == ChampionshipStatus.ENDED:
        return ApiResponse(
            status=status.HTTP_226_IM_USED,
            message="Championship finished, youcan generate repoet now",
            data=asdict(championship_service)
        )
    

@router.get("/referee/draw-games")
async def draw_games(referee: Annotated[Referee, Depends(get_current_user)]):
    championship_status: ChampionshipStatus = championship_service.status
    if championship_status == ChampionshipStatus.STARTED:
        championship_service.draw_games()
        return ApiResponse(
            status=status.HTTP_200_OK,
            message="All games of this round",
            data=asdict(championship_service.current_games)
        )
    
    else:
        return ApiResponse(
            status=status.htt,
            message="Championship not in state to genrate report",
            data=asdict(championship_service)
        )


@router.get("/referee/export-report")
async def export_report(referee: Annotated[Referee, Depends(get_current_user)]):
    pass

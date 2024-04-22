from uuid import UUID
from typing import Annotated
from typing import List

from pydantic import BaseModel

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status
from fastapi import HTTPException

from models import Player
from models import Referee
from models import ApiResponse

from routers.auth import get_current_user
from services.championship import championship_service
from services.game import Turn
from services.game import GameStatus


router = APIRouter()


@router.get("/player/championship")
async def get_championship(
    current_user: Annotated[Player, Depends(get_current_user)], response: Response
):
    return {
        "championship": {
            "status": championship_service.status,
            "game": championship_service.get_game_by_player(current_user),
        }
    }


@router.post("/player/championship")
async def join_championship(
    current_user: Annotated[Player, Depends(get_current_user)], response: Response
):
    if championship_service.join_championship(current_user):
        response.status_code = status.HTTP_200_OK
        return {"message": "accepted"}

    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Player cant join championship, alread joined",
        )


@router.get("/player/game/{id}")
async def get_game(
    id: UUID, current_user: Annotated[Player, Depends(get_current_user)]
):
    game = championship_service.get_game_by_id(id)
    return game


@router.post("/player/game/{id}")
async def join_game(
    id: UUID, current_user: Annotated[Player, Depends(get_current_user)]
):
    game = championship_service.get_game_by_id(id)
    if game:
        if game.join_game(current_user):
            return game

        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Failed to join game"
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Player cant join championship, game not found",
        )


class OffensivePickBody(BaseModel):
    num: int


@router.put("/player/game/{id}/offence")
async def offensive_pick_number(
    id: UUID,
    body: OffensivePickBody,
    current_user: Annotated[Player, Depends(get_current_user)],
):
    game = championship_service.get_game_by_id(id)
    if game.status != GameStatus.RUNNING:
        raise HTTPException(status_code=status)

    if (game.turn == Turn.PLAYER1 and current_user == game.player1) or (
        game.turn == Turn.PLAYER2 and current_user == game.player2
    ):
        game.update_offence(body.num)

    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Player doesnt have turn",
        )


class DefensiveArrayBody(BaseModel):
    arr: List[int]


@router.put("/player/game/{id}/defence")
async def defensive_array(
    id: UUID,
    body: DefensiveArrayBody,
    current_user: Annotated[Player, Depends(get_current_user)],
):
    game = championship_service.get_game_by_id(id)
    if game.status != GameStatus.RUNNING:
        raise HTTPException(status_code=status)

    if (game.turn == Turn.PLAYER2 and current_user == game.player1) or (
        game.turn == Turn.PLAYER1 and current_user == game.player2
    ):
        game.update_offence(body.defensive_array)

    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Player doesnt have turn",
        )

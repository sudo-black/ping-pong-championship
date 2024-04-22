from typing import Annotated
from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends


from models import Player
from models import Referee
from models import ApiResponse

from routers.auth import get_current_user
from services.player import PlayerService


router = APIRouter()

@router.post("/player/championship")
async def join_championship(current_user: Annotated[Player, Depends(get_current_user)]) -> ApiResponse:
    return {"message": "Player added successfully"}

@router.get("/player/championship")
async def get_championship(current_user: Annotated[Player, Depends(get_current_user)]) -> ApiResponse:
    pass

@router.get("/player/game/{id}")
async def get_game(id: int, current_user: Annotated[Player, Depends(get_current_user)]) -> ApiResponse:
    pass

@router.post("/player/game/{id}")
async def join_game(id: int, current_user: Annotated[Player, Depends(get_current_user)]) -> ApiResponse:
    pass


@router.put("/player/game/{id}/pick")
async def offensive_pick_number(id: int, num: int, current_user: Annotated[Player, Depends(get_current_user)]) -> ApiResponse:
    pass

@router.put("/player/game/{id}/array")
async def defensive_array(id: int, defensive_array: List[int], current_user: Annotated[Player, Depends(get_current_user)]) -> ApiResponse:
    pass

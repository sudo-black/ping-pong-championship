# app/routers/game_router.py

from fastapi import APIRouter
from services.game import GameService

router = APIRouter()
game_service = GameService()

@router.post("/game/play")
async def play_game(offensive_number: int, defensive_array: list):
    result = game_service.play_game(offensive_number, defensive_array)
    return {"result": result}

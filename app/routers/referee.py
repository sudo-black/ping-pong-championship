# app/routers/referee_router.py

from fastapi import APIRouter, HTTPException
from services.referee import referee_service

router = APIRouter()


@router.get("/referee/championship-start")
async def championship_start():
    pass


@router.get("/referee/draw-games")
async def draw_games():
    pass


@router.get("/referee/export-report")
async def export_report():
    pass

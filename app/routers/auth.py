from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from services.auth import create_access_token, decode_token, get_user
from models import ApiResponse, Player, Referee
from dataclasses import asdict


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.post("/login")
async def login(login_data: OAuth2PasswordRequestForm = Depends()) -> ApiResponse:
    user = get_user(login_data.username, login_data.password)
    if user:
        access_token = create_access_token(data=asdict(user))
        return ApiResponse(
            status=status.HTTP_200_OK,
            message="ok",
            data=access_token
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )


@router.get("/verify-token")
async def verify_token(authorization: str = Header(...)) -> ApiResponse:
    try:
        token = authorization.split("bearer ")[1]
        token_data = decode_token(token)
        return ApiResponse(
            status=status.HTTP_200_OK,
            message="ok",
            data=token_data
        )

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

@router.get("/user")
async def this_user(current_user: Annotated[Player | Referee, Depends(get_current_user)]) -> ApiResponse:
    return ApiResponse(
        status=status.HTTP_200_OK,
        message="ok",
        data=current_user
    )

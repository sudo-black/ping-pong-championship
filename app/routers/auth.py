from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter
from fastapi import status
from fastapi import Header
from fastapi import Depends
from fastapi import Response
from fastapi import HTTPException

from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from services.auth import get_user
from services.auth import decode_token
from services.auth import create_access_token

from models import Player
from models import Referee
from models import ApiResponse


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> Player | Referee:
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "bearer"},
        )

    else:
        if "ROLE" not in user.keys():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="",
                headers={"WWW-Authenticate": "bearer"},
            )

        else:
            if user["ROLE"] == "referee":
                return Referee(**user)

            elif user["ROLE"] == "player":
                return Player(**user)

            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="",
                    headers={"WWW-Authenticate": "bearer"},
                )


@router.post("/login")
async def login(response: Response, login_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(login_data.username, login_data.password)
    if user:
        access_token = create_access_token(data=asdict(user))
        response.status_code = status.HTTP_200_OK
        return access_token

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
        return ApiResponse(status=status.HTTP_200_OK, message="ok", data=token_data)

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )


@router.get("/user")
async def this_user(
    current_user: Annotated[Player | Referee, Depends(get_current_user)]
) -> ApiResponse:
    return ApiResponse(status=status.HTTP_200_OK, message="ok", data=current_user)

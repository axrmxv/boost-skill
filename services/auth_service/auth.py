import jwt

from datetime import timedelta, datetime, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from common.config import settings

from jwt.exceptions import (
    ExpiredSignatureError, InvalidSignatureError
)

from typing import Dict


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


fake_db = {
    "c45fdceb-b991-4a0b-b268-20c8b2383592": {
        "client_id": "c45fdceb-b991-4a0b-b268-20c8b2383592",
        "client_secret": "61c908f9-61e3-4565-961f-efc016e5971c",
        "client_name": "market_approach",
    }
}


async def get_fake_clietnt(client_id, fake_db):
    if client_id in fake_db:
        client_dict = fake_db[client_id]
        return client_dict


async def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings["secret_key"],
        algorithm=settings["algorithm"],
    )
    return encoded_jwt


async def get_current_client(
        token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    try:
        payload = jwt.decode(
            token,
            settings["secret_key"],
            algorithms=[settings["algorithm"]]
        )
        client_id: str | None = payload.get("sub")
        client = await get_fake_clietnt(client_id, fake_db)
        if client_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token: client_id not found"
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    client = await get_fake_clietnt(client_id, fake_db)
    return client

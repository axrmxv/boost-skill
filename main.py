import re
import uuid
import uvicorn
import settings

from fastapi import FastAPI, HTTPException
from fastapi.routing import APIRouter

from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID

from pydantic import BaseModel, EmailStr, field_validator


# interaction with the database
# create an async engine to interact with the database
engine = create_async_engine(settings.PROD_DB_URL, future=True, echo=True)

# create a session to interact with the database
async_session = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession
    )


# Database model
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)


class UserDAL:
    """
    Data access layer for "User".
    """
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_user(self, name: str, surname: str, email: str) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user


# block with api models
MATCHING_LETTERS = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr

    @field_validator("name")
    def validator_name(cls, value):
        if not MATCHING_LETTERS.match(value):
            return HTTPException(
                status_code=422, detail="Field 'name' must contai only letters"
            )
        return value

    @field_validator("surname")
    def validator_surname(cls, value):
        if not MATCHING_LETTERS.match(value):
            raise HTTPException(
                status_code=422,
                detail="Field 'surname' must contai only letters"
            )
        return value


# API Routers

app = FastAPI(title="Boost Skill")

user_router = APIRouter()


async def _create_new_user(body: UserCreate) -> ShowUser:
    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
            )
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate) -> ShowUser:
    return await _create_new_user(body)


main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8027)

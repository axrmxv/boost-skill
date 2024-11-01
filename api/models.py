import re
import uuid

from fastapi import HTTPException

from pydantic import BaseModel, EmailStr, field_validator


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

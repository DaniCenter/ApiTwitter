from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, validator
from fastapi import FastAPI

app = FastAPI()


class UserBase(BaseModel):
    user_id: UUID = Field()
    email: EmailStr = Field()
    firts_name: str = Field(min_length=1, max_length=20)
    last_name: str = Field(min_length=1, max_length=20)
    birth_date: Optional[date] = Field(default=None)

    @validator(birth_date)
    def older_than_legal_age(cls, v):
        todays_date = datetime.date.today()
        delta = todays_date - v
        if delta.days / 365 <= 18:
            raise ValueError("The age must be over 18")
        else:
            return v


class UserLogin(UserBase):
    password: str = Field(min_length=7)


class Tweet(BaseModel):
    pass


@app.get("/")
def home():
    return {"Twiter API": "Working"}

from datetime import date, datetime
from email.policy import default
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

    @validator("birth_date")
    def older_than_legal_age(cls, v):
        today = datetime.today()
        delta = today.year - v.year
        if delta <= 18:
            raise ValueError("The age must be over 18")
        else:
            return v


class UserLogin(UserBase):
    password: str = Field(min_length=7)


class Tweet(BaseModel):
    tweet_id: UUID = Field()
    content: str = Field(max_length=256)
    create_at: datetime = Field(default=datetime.now())
    update_at: Optional[datetime] = Field()
    by: UserBase = Field()


@app.get("/")
def home():
    return {"Twiter API": "Working"}

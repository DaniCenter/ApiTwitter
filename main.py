import json
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, validator
from fastapi import FastAPI, status, Body

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
    update_at: Optional[datetime] = Field(default=None)
    by: UserBase = Field()


@app.get("/")
def home():
    return {"Twiter API": "Working"}


# Users
@app.post(
    "/singup",
    response_model=UserBase,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["Users"],
)
def signup(user: UserLogin = Body()):
    """This paht operation register a user in the database

    Returns:
        UserBase.json: Returns a User object without its password information
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        result = json.load(f)
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        result.append(user_dict)
        f.seek(0)
        json.dump(result, f)
    return user


@app.post(
    "/login",
    response_model=UserBase,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags=["Users"],
)
def login():
    pass


@app.get(
    "/users",
    response_model=List[UserBase],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"],
)
def show_users():
    """
    This path operation shows all users in the app

    Parameters:
    -

    Returns a json list with all users in the app
    """
    with open("users.json", "r", encoding="utf-8") as f:
        result = json.load(f)
        return result


@app.get(
    "/users/{user_id}",
    response_model=UserBase,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"],
)
def show_a_user():
    pass


@app.delete(
    "/users/{user_id}/delete",
    response_model=UserBase,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"],
)
def delete_a_user():
    pass


@app.put(
    "/users/{user_id}/update",
    response_model=UserBase,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"],
)
def update_a_user():
    pass


# Tweets
@app.get(
    "/",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"],
)
def show_tweets():
    return {"Twiter API": "Working"}


@app.post(
    "/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"],
)
def post(tweet: Tweet = Body()):
    with open("tweets.json", "r+", encoding="utf-8") as f:
        result = json.load(f)
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["create_at"] = str(tweet_dict["create_at"])
        if tweet_dict["update_at"]:
            tweet_dict["update_at"] = str(tweet_dict["update_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        result.append(tweet_dict)
        f.seek(0)
        json.dump(result, f)
    return tweet


@app.get(
    "/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"],
)
def get():
    pass


@app.delete(
    "/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"],
)
def delete():
    pass


@app.put(
    "/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"],
)
def update():
    pass

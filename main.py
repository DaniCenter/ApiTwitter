import json
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, validator
from fastapi import FastAPI, status, Body, Path, HTTPException

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


class UserAuthLogin(BaseModel):
    email: EmailStr = Field()
    password: str = Field(min_length=7)


class Tweet(BaseModel):
    tweet_id: UUID = Field()
    content: str = Field(max_length=256)
    create_at: datetime = Field(default=datetime.now())
    update_at: Optional[datetime] = Field(default=None)
    by: UserBase = Field()


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
    "/login", status_code=status.HTTP_200_OK, summary="Login a user", tags=["Users"],
)
def login(userlogin: UserAuthLogin = Body()):
    with open("users.json", "r", encoding="utf-8") as f:
        result = json.load(f)
    for i in result:
        if userlogin.email == i["email"] and userlogin.password == i["password"]:
            return "Successful logging"
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="This person doesnot exist")


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
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"],
)
def show_a_user(user_id: str = Path(example="3fa85f64-5717-4562-b3fc-2c963f66afa6")):
    with open("users.json", "r", encoding="utf-8") as f:
        result = json.load(f)
        for i in result:
            if i["user_id"] == user_id:
                return i
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This person doesnot exist")


@app.delete(
    "/users/{user_id}/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"],
)
def delete_a_user(user_id: str = Path(example="3fa85f64-5717-4562-b3fc-2c963f66afa6")):
    with open("users.json", "r+", encoding="utf-8") as f:
        result = json.load(f)
        for idx, obj in enumerate(result):
            if obj["user_id"] == user_id:
                result.pop(idx)
                with open("users.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(result))
                    return "Eliminated"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This person doesnot exist")


@app.put(
    "/users/{user_id}/update",
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"],
)
def update_a_user(
    user_id: str = Path(example="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
    user: UserBase = Body(),
):
    with open("users.json", "r+", encoding="utf-8") as f:
        result = json.load(f)
        for idx, obj in enumerate(result):
            if obj["user_id"] == user_id:
                result.pop(idx)
                temp = user.dict()
                temp["user_id"] = str(temp["user_id"])
                temp["birth_date"] = str(temp["birth_date"])
                result.append(temp)
                with open("users.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(result))
                    return "Updated"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This person doesnot exist")

# Tweets
@app.get(
    "/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"],
)
def show_tweets():
    with open("tweets.json", "r", encoding="utf-8") as f:
        result = json.load(f)
        return result


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
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"],
)
def get(tweet_id: str = Path()):
    with open("tweets.json", "r", encoding="utf-8") as f:
        result = json.load(f)
        for i in result:
            if i["tweet_id"] == tweet_id:
                return i
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This tweet doesnot exist")


@app.delete(
    "/tweets/{tweet_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"],
)
def delete(tweet_id: str = Path()):
    with open("tweets.json", "r+", encoding="utf-8") as f:
        result = json.load(f)
        for idx, obj in enumerate(result):
            if obj["tweet_id"] == tweet_id:
                result.pop(idx)
                with open("tweets.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(result))
                    return "Eliminated"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This tweet doesnot exist")


@app.put(
    "/tweets/{tweet_id}/update",
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"],
)
def update(tweet_id: str = Path(), tweet: Tweet = Body(),):
    with open("tweets.json", "r+", encoding="utf-8") as f:
        result = json.load(f)
        for idx, obj in enumerate(result):
            if obj["tweet_id"] == tweet_id:
                result.pop(idx)
                temp = tweet.dict()
                temp["tweet_id"] = str(temp["tweet_id"])
                temp["create_at"] = str(temp["create_at"])
                if temp["update_at"]:
                    temp["update_at"] = str(temp["update_at"])
                temp["by"]["user_id"] = str(temp["by"]["user_id"])
                temp["by"]["birth_date"] = str(temp["by"]["birth_date"])
                result.append(temp)
                with open("tweets.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(result))
                    return "Updated"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This person doesnot exist")

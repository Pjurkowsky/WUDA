from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from flask import session
import requests
from settings import BACKEND_URL


class Login(BaseModel):
    username: str
    password: str


class RegisterUser(Login):
    email: EmailStr
    repeat_pwd: str


class User(BaseModel):
    id: int
    username: str


class Comment(BaseModel):
    id: int
    content: str
    created_at: datetime
    author: User


class GameSelectBox(BaseModel):
    id: int
    title: str


class Post(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
    author: User
    game: Optional[GameSelectBox] = None
    comments: List[Comment] = []


class NewPost(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    body: str = Field(min_length=5)
    game_id: int


class NewComment(BaseModel):
    content: str


class NewGame(BaseModel):
    title: str
    players: str
    playtime: int
    short_description: str
    description: str
    image_url: str


def fetch_posts():
    response = requests.get(
        url=f"{BACKEND_URL}/posts",
    )
    response.raise_for_status()
    return [Post.model_validate(p) for p in response.json()]


def fetch_post(post_id: int):
    response = requests.get(
        url=f"{BACKEND_URL}/posts/{post_id}",
        # params={"post_id": post_id}
    )
    response.raise_for_status()
    return Post.model_validate(response.json())


def add_post(post: NewPost) -> bool:

    if post.game_id == -1:
        data = post.model_dump(exclude=set("game_id"))
    else:
        data = post.model_dump()

    response = requests.post(
        headers={"Authorization": f"Bearer {session['access-token']}"},
        url=f"{BACKEND_URL}/posts",
        json=data,
    )
    if response.status_code == 201:
        return True
    else:
        return False


def add_comment(post_id: int, comment_content: NewComment) -> bool:
    data = comment_content.model_dump()

    response = requests.post(
        headers={"Authorization": f"Bearer {session['access-token']}"},
        url=f"{BACKEND_URL}/posts/{post_id}/comments",
        json=data,
    )
    response.raise_for_status()

    return True


def login_user(user: Login) -> dict[str, str] | None:
    payload = user.model_dump()
    response = requests.post(f"{BACKEND_URL}/auth/login", json=payload)
    if response.status_code == 200:
        return response.json()
    return None


def register_user(user: RegisterUser) -> dict[str, str] | None:
    payload = user.model_dump(exclude=set("repeat_pwd"))
    response = requests.post(f"{BACKEND_URL}/auth/register", json=payload)
    if response.status_code == 201:
        return response.json()
    return None


def add_game_req(new_game: dict):
    response = requests.post(
        headers={"Authorization": f"Bearer {session['access-token']}"},
        url=f"{BACKEND_URL}/games",
        json=new_game,
    )
    response.raise_for_status()
    return True


def get_games_req(game_id=None):
    if game_id:
        part = f"/games/{game_id}"
    else:
        part = "/games"

    response = requests.get(url=f"{BACKEND_URL}{part}")
    response.raise_for_status()
    print(response.json())
    return response.json()

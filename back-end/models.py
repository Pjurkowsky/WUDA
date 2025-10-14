from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(Text, nullable=False)
    email = Column(String(200), nullable=False)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    players = Column(String(8), nullable=False)
    playtime = Column(Integer, nullable=False)
    short_description = Column(String(200), nullable=False)
    description = Column(String(400), nullable=False)
    image_url = Column(String(1000), nullable=True)

    posts = relationship("Post", back_populates="game")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    created_at = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=True)
    body = Column(String(400), nullable=False)

    author = relationship("User", back_populates="posts")
    game = relationship("Game", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    created_at = Column(Date, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")

from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"

    accountid = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    passwordhash = Column(Text, nullable=False)
    createdat = Column(TIMESTAMP, server_default=func.now(), index=True)

    posts = relationship("Post", back_populates="account", passive_deletes=True)
    likes = relationship("Like", back_populates="account", passive_deletes=True)

    followers = relationship(
        "Follower",
        foreign_keys="[Follower.followingid]",
        backref="followed_account",
        passive_deletes=True
    )
    following = relationship(
        "Follower",
        foreign_keys="[Follower.followerid]",
        backref="follower_account",
        passive_deletes=True
    )

class Follower(Base):
    __tablename__ = "followers"

    followerid = Column(Integer, ForeignKey("accounts.accountid", ondelete="CASCADE"), primary_key=True)
    followingid = Column(Integer, ForeignKey("accounts.accountid", ondelete="CASCADE"), primary_key=True)

class Post(Base):
    __tablename__ = "posts"

    postid = Column(Integer, primary_key=True, index=True)
    accountid = Column(Integer, ForeignKey("accounts.accountid", ondelete="CASCADE"), nullable=False)
    parentpostid = Column(Integer, ForeignKey("posts.postid", ondelete="SET NULL"), nullable=True)
    content = Column(String(240), nullable=False)
    createdat = Column(TIMESTAMP, server_default=func.now(), index=True)
    lastedited = Column(TIMESTAMP, nullable=True)

    account = relationship("Account", back_populates="posts", passive_deletes=True)
    parent_post = relationship("Post", remote_side=[postid], backref="replies", cascade="all, delete")

class Like(Base):
    __tablename__ = "likes"

    accountid = Column(Integer, ForeignKey("accounts.accountid", ondelete="CASCADE"), primary_key=True)
    postid = Column(Integer, ForeignKey("posts.postid", ondelete="CASCADE"), primary_key=True)

    account = relationship("Account", back_populates="likes", passive_deletes=True)

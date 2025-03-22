from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"

    AccountID = Column(Integer, primary_key=True, index=True)
    Email = Column(String(255), unique=True, nullable=False)
    Username = Column(String(50), unique=True, nullable=False)
    PasswordHash = Column(Text, nullable=False)
    CreatedAt = Column(TIMESTAMP, server_default=func.now(), index=True)

    posts = relationship("post", back_populates="account", passive_deletes=True)
    likes = relationship("like", back_populates="account", passive_deletes=True)

    followers = relationship(
        "follower",
        foreign_keys="[follower.FollowingID]",
        backref="followed_account",
        passive_deletes=True
    )
    following = relationship(
        "follower",
        foreign_keys="[follower.followerID]",
        backref="follower_account",
        passive_deletes=True
    )

class follower(Base):
    __tablename__ = "followers"

    followerID = Column(Integer, ForeignKey("accounts.AccountID", ondelete="CASCADE"), primary_key=True)
    FollowingID = Column(Integer, ForeignKey("accounts.AccountID", ondelete="CASCADE"), primary_key=True)

class post(Base):
    __tablename__ = "posts"

    postID = Column(Integer, primary_key=True, index=True)
    AccountID = Column(Integer, ForeignKey("accounts.AccountID", ondelete="CASCADE"), nullable=False)
    ParentpostID = Column(Integer, ForeignKey("posts.postID", ondelete="SET NULL"), nullable=True)
    Content = Column(String(240), nullable=False)
    CreatedAt = Column(TIMESTAMP, server_default=func.now(), index=True)
    LastEdited = Column(TIMESTAMP, nullable=True)

    account = relationship("Account", back_populates="posts", passive_deletes=True)
    parent_post = relationship("post", remote_side=[postID], backref="replies", cascade="all, delete")

class Like(Base):
    __tablename__ = "Likes"

    AccountID = Column(Integer, ForeignKey("accounts.AccountID", ondelete="CASCADE"), primary_key=True)
    postID = Column(Integer, ForeignKey("posts.postID", ondelete="CASCADE"), primary_key=True)

    account = relationship("Account", back_populates="likes", passive_deletes=True)
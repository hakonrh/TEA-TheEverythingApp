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

    posts = relationship("Post", back_populates="account", passive_deletes=True)
    likes = relationship("Like", back_populates="account", passive_deletes=True)

    followers = relationship(
        "Follower",
        foreign_keys="[Follower.FollowingID]",
        backref="followed_account",
        passive_deletes=True
    )
    following = relationship(
        "Follower",
        foreign_keys="[Follower.FollowerID]",
        backref="follower_account",
        passive_deletes=True
    )

class Follower(Base):
    __tablename__ = "followers"

    FollowerID = Column(Integer, ForeignKey("accounts.AccountID", ondelete="CASCADE"), primary_key=True)
    FollowingID = Column(Integer, ForeignKey("accounts.AccountID", ondelete="CASCADE"), primary_key=True)

class Post(Base):
    __tablename__ = "posts"

    PostID = Column(Integer, primary_key=True, index=True)
    AccountID = Column(Integer, ForeignKey("accounts.AccountID", ondelete="CASCADE"), nullable=False)
    ParentPostID = Column(Integer, ForeignKey("posts.PostID", ondelete="SET NULL"), nullable=True)
    Content = Column(String(240), nullable=False)
    CreatedAt = Column(TIMESTAMP, server_default=func.now(), index=True)
    LastEdited = Column(TIMESTAMP, nullable=True)

    account = relationship("Account", back_populates="posts", passive_deletes=True)
    parent_post = relationship("Post", remote_side=[PostID], backref="replies", cascade="all, delete")

class Like(Base):
    __tablename__ = "likes"

    AccountID = Column(Integer, ForeignKey("accounts.AccountID", ondelete="CASCADE"), primary_key=True)
    PostID = Column(Integer, ForeignKey("posts.PostID", ondelete="CASCADE"), primary_key=True)

    account = relationship("Account", back_populates="likes", passive_deletes=True)

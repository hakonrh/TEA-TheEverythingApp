from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = "Accounts"

    AccountID = Column(Integer, primary_key=True, index=True)
    Email = Column(String(255), unique=True, nullable=False)
    Username = Column(String(50), unique=True, nullable=False)
    PasswordHash = Column(Text, nullable=False)
    CreatedAt = Column(TIMESTAMP, server_default=func.now())

    posts = relationship("Post", back_populates="account")
    followers = relationship("Follower", back_populates="following")
    likes = relationship("Like", back_populates="account")


class Follower(Base):
    __tablename__ = "Followers"

    FollowerID = Column(Integer, ForeignKey("Accounts.AccountID"), primary_key=True)
    FollowingID = Column(Integer, ForeignKey("Accounts.AccountID"), primary_key=True)

    following = relationship("Account", foreign_keys=[FollowingID], back_populates="followers")


class Post(Base):
    __tablename__ = "Posts"

    PostID = Column(Integer, primary_key=True, index=True)
    AccountID = Column(Integer, ForeignKey("Accounts.AccountID"), nullable=False)
    ParentPostID = Column(Integer, ForeignKey("Posts.PostID"), nullable=True)
    Content = Column(String(240), nullable=False)
    CreatedAt = Column(TIMESTAMP, server_default=func.now())
    LastEdited = Column(TIMESTAMP, nullable=True)

    account = relationship("Account", back_populates="posts")
    parent_post = relationship("Post", remote_side=[PostID])


class Like(Base):
    __tablename__ = "Likes"

    AccountID = Column(Integer, ForeignKey("Accounts.AccountID"), primary_key=True)
    PostID = Column(Integer, ForeignKey("Posts.PostID"), primary_key=True)

    account = relationship("Account", back_populates="likes")

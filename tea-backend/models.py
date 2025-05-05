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

class Post(Base):
    __tablename__ = "posts"

    postid = Column(Integer, primary_key=True, index=True)
    accountid = Column(Integer, ForeignKey("accounts.accountid", ondelete="CASCADE"), nullable=False)
    content = Column(String(240), nullable=False)
    likes = Column(Integer, nullable=True)
    createdat = Column(TIMESTAMP, server_default=func.now(), index=True)
    lastedited = Column(TIMESTAMP, nullable=True)

    account = relationship("Account", back_populates="posts", passive_deletes=True)
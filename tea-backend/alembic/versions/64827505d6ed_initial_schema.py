"""Initial schema

Revision ID: 64827505d6ed
Revises: 
Create Date: 2025-03-21 17:00:51.189517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64827505d6ed'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.execute("""
        CREATE TABLE Accounts (
            AccountID SERIAL PRIMARY KEY,
            Email VARCHAR(255) UNIQUE NOT NULL,
            Username VARCHAR(50) UNIQUE NOT NULL,
            PasswordHash TEXT NOT NULL,
            CreatedAt TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE Posts (
            PostID SERIAL PRIMARY KEY, 
            AccountID INT NOT NULL,
            Content VARCHAR(240) NOT NULL,
            Likes INT NULL,
            CreatedAt TIMESTAMP DEFAULT NOW(),
            LastEdited TIMESTAMP NULL,
            FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID) ON DELETE CASCADE
        );
    """)

def downgrade():
    op.execute("""
        DROP TABLE Likes;
        DROP TABLE Posts;
        DROP TABLE Followers;
        DROP TABLE Accounts;
    """)

import uuid

from fastapi import Depends
from fastapi_users.db import (SQLAlchemyBaseUserTableUUID,
                              SQLAlchemyUserDatabase)
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import BINARY, UUID, Boolean, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from main.db import get_async_session

UUID_ID = uuid.UUID


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    Models User:
    Attributes:
        - id: pk, type UUID
        - email: unique email
        - hashed password: str
        - is_active: boolean
        - is_superuser: boolean
        - is_verified: boolean
    """
    id: Mapped[UUID_ID] = mapped_column(
        GUID, primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(length=128), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=128), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )


class AudioFile(Base):
    """
    Models AudioFile:
    Attributes:
        - id: pk, type UUID
        - user: ForeignKey, type UUID
        - filename: str
        - file_path: str
        - data: Binary (возможно скачивание на прямую из базы)
    """
    __tablename__ = 'audio_file'

    id: Mapped[UUID_ID] = mapped_column(
        GUID, primary_key=True, default=uuid.uuid4
    )
    user: Mapped[UUID_ID] = mapped_column(
        UUID, ForeignKey('user.id', ondelete='CASCADE')
    )
    filename: Mapped[str] = mapped_column(
        String, nullable=False, unique=True,
    )
    file_path: Mapped[str] = mapped_column(
        String, nullable=False, unique=True,
    )
    data = mapped_column(
        BINARY, nullable=False,
    )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

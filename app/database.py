"""Database configuration, SQLAlchemy engine, and session management."""

from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_prefix="VINUM_", extra="ignore")

    database_url: str = "sqlite:///./vinum_pulse.db"


class Base(DeclarativeBase):
    """Base declarative class for SQLAlchemy ORM models."""


def create_db_engine(database_url: str) -> Engine:
    """Create a SQLAlchemy engine configured for SQLite or relational backends."""
    kwargs: dict[str, Any] = {}
    if database_url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
        if ":memory:" in database_url:
            kwargs["poolclass"] = StaticPool
    return create_engine(database_url, **kwargs)


settings = Settings()
engine = create_db_engine(settings.database_url)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False, class_=Session
)

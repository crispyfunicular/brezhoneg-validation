"""SQLAlchemy models — mirrors the schema defined in PRD §7.3."""

from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Segment(Base):
    __tablename__ = "segments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    breton: Mapped[str] = mapped_column(Text, nullable=False)
    francais: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow
    )

    annotations: Mapped[list["Annotation"]] = relationship(back_populates="segment")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pseudonyme: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    niveau_breton: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint("niveau_breton IN ('debutant', 'moyen', 'confirme')"),
        nullable=False,
    )
    nom: Mapped[str | None] = mapped_column(String(100), nullable=True)
    prenom: Mapped[str | None] = mapped_column(String(100), nullable=True)
    genre: Mapped[str | None] = mapped_column(String(20), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow
    )

    annotations: Mapped[list["Annotation"]] = relationship(back_populates="user")


class Annotation(Base):
    __tablename__ = "annotations"
    __table_args__ = (
        UniqueConstraint("user_id", "segment_id", name="uq_user_segment"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    segment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("segments.id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    label: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint("label IN ('correct', 'incorrect', 'incertain')"),
        nullable=False,
    )
    confidence: Mapped[int | None] = mapped_column(
        Integer,
        CheckConstraint("confidence BETWEEN 1 AND 5"),
        nullable=True,
    )
    corrected_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow
    )

    segment: Mapped["Segment"] = relationship(back_populates="annotations")
    user: Mapped["User"] = relationship(back_populates="annotations")

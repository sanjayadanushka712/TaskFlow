from sqlalchemy import Boolean, Integer, String,JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )


class IdempotencyRecord(Base):
    __tablename__ = "idempotency_records"

    key: Mapped[str] = mapped_column(
        String(255),
        primary_key=True
    )
    request_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )
    response_body: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )
    status_code: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

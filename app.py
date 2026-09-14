import os
from datetime import datetime, timezone

from flask import Flask, request
from sqlalchemy import DateTime, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


app = Flask(__name__)


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "visits_db")
DB_USER = os.getenv("DB_USER", "app")
DB_PASSWORD = os.getenv("DB_PASSWORD", "changeme")


DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    visited_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    ip_address: Mapped[str] = mapped_column(
        String(45),
        nullable=False
    )


Base.metadata.create_all(engine)


@app.get("/hello")
def hello():
    visited_at = datetime.now(timezone.utc)
    ip_address = request.remote_addr or "unknown"

    with SessionLocal() as session:
        visit = Visit(
            visited_at=visited_at,
            ip_address=ip_address
        )

        session.add(visit)
        session.commit()

    return "Hello", 200
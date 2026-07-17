from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///invoice.db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(bind=engine)


def init_db() -> None:
    from app.db.seed import seed
    from app.db.seed_registry import SEED_SPECS

    with SessionLocal() as session:
        seed(session, SEED_SPECS)
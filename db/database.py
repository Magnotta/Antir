from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URL = "sqlite:///game.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Session = scoped_session(SessionFactory)
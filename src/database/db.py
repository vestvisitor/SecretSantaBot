from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base
from src.config import settings


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False}
)

Session = sessionmaker(engine)


def db_session():
    with Session.begin() as session:
        yield session


def init_db():
    Base.metadata.create_all(engine)


def destroy_db():
    Base.metadata.drop_all(engine)

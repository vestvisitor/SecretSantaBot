from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from collections import namedtuple

from src.database.crud import *
from src.database.models import Base
from src.utils import get_random_number
from src.config import settings

engine = create_engine(
            "sqlite:///app/tests/testing.db",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

Base.metadata.create_all(engine)


def db_testing_session():
    with Session(engine) as session:
        yield session


user_manager = UserManager(next(db_testing_session()))

UserTest = namedtuple("UserTest", ["name", "vk_id"])
user_test = UserTest("RandomUser", 111111111)

class TestClassUser:

    def test_create_users(self):
        random_numbers = [get_random_number() for _ in range(len(settings.PARTICIPANTS))]
        for name, vk_id, number in zip(settings.PARTICIPANTS.keys(), settings.PARTICIPANTS.values(), random_numbers):
            user_manager.create_user(
                name = name,
                vk_id = vk_id,
                number = number
            )

        assert random_numbers == user_manager.read_users_numbers()
        assert list(settings.PARTICIPANTS.keys()) == user_manager.read_users_names()
        assert list(settings.PARTICIPANTS.values()) == user_manager.read_users_vk_ids()

    def test_read_user(self):
        user = user_manager.read_user(user_test.vk_id)

        assert type(user) is User
        assert user.name == user_test.name
        assert user.vk_id == user_test.vk_id

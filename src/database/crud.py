from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from src.database.db import db_session
from src.database.models import User, Decision, Wish


class BaseManager:
    def __init__(self, session: Session | None = next(db_session())):
        self.session = session


class UserManager(BaseManager):

    def create_user(
            self,
            name: str,
            vk_id: int,
            number: int,
            wishlist: str,
            state: int | None = 0,
            active: int | None = 0
    ):
        user = User(
            name = name,
            vk_id = vk_id,
            number = number,
            wishlist = wishlist,
            state = state,
            active = active
        )
        self.session.add(user)
        self.session.commit()

    def read_user(self, vk_id: int) -> User:
        return self.session.scalar(select(User).where(User.vk_id == vk_id))

    def read_user_state(self, vk_id: int) -> int:
        return self.session.scalar(select(User.state).where(User.vk_id == vk_id))

    def read_user_number(self, vk_id: int) -> int:
        return self.session.scalar(select(User.number).where(User.vk_id == vk_id))

    def read_user_active(self, vk_id: int) -> int:
        return self.session.scalar(select(User.active).where(User.vk_id == vk_id))

    def read_user_wishlist(self, vk_id: int) -> str:
        return self.session.scalar(select(User.wishlist).where(User.vk_id == vk_id))

    def read_active_users(self) -> list[User]:
        return [user for user in self.session.scalars(select(User).where(User.active == 1)).all()]

    def read_all_users(self) -> list[User]:
        return [user for user in self.session.scalars(select(User)).all()]

    def read_users_numbers(self) -> list[int]:
        return [number for number in self.session.scalars(select(User.number)).all()]

    def read_users_names(self) -> list[str]:
        return [name for name in self.session.scalars(select(User.name)).all()]

    def read_users_vk_ids(self) -> list[int]:
        return [vk_id for vk_id in self.session.scalars(select(User.vk_id)).all()]

    def update_user_state(self, vk_id: int, state: int):
        user = self.session.scalar(select(User).where(User.vk_id == vk_id))
        user.state = state
        self.session.add(user)
        self.session.commit()

    def update_user_active(self, vk_id: int):
        user = self.session.scalar(select(User).where(User.vk_id == vk_id))
        user.active = 1
        self.session.add(user)
        self.session.commit()

    def update_user_number(self, vk_id: int, number: int):
        user = self.session.scalar(select(User).where(User.vk_id == vk_id))
        user.number = number
        self.session.add(user)
        self.session.commit()

    def update_user_wishlist(self, vk_id: int, wishlist: str):
        user = self.session.scalar(select(User).where(User.vk_id == vk_id))
        user.wishlist = wishlist
        self.session.add(user)
        self.session.commit()

    def delete_user(self, user_id: int):
        user = self.session.scalar(select(User).where(User.id == user_id))
        self.session.delete(user)
        self.session.commit()


class DecisionManager(BaseManager):

    def create_pair(self, giver: str, receiver: str):
        pair = Decision(
            giver = giver,
            receiver = receiver
        )
        self.session.add(pair)
        self.session.commit()

    def read_pairs(self):
        return [pair for pair in self.session.scalars(select(Decision)).all()]


class WishManager(BaseManager):

    def create_wish(self, name: str, link: str, code: int, priority: int, user_id: int):
        wish = Wish(
            name = name,
            link = link,
            code = code,
            priority = priority,
            owner = user_id
        )
        self.session.add(wish)
        self.session.commit()

    def read_wish(self, user_id: int, wish_id: int) -> Wish:
        return self.session.scalar(select(Wish).where(and_(Wish.id == wish_id, Wish.owner == user_id)))

    def read_wishes(self, user_id: int) -> list[Wish]:
        return [wish for wish in self.session.scalars(select(Wish).where(Wish.owner == user_id))]

    def update_wish_priority(self, user_id: int, wish_id: int, priority: int):
        wish = self.session.scalar(select(Wish).where(and_(Wish.id == wish_id, Wish.owner == user_id)))
        wish.priority = priority
        self.session.add(wish)
        self.session.commit()

    def delete_wish(self, user_id: int, wish_id: int):
        wish = self.session.scalar(select(Wish).where(and_(Wish.id == wish_id, Wish.owner == user_id)))
        self.session.delete(wish)
        self.session.commit()

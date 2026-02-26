from sqlalchemy.orm import Session
from persistencia.models import User
from domain.schemas.user import UserCreate
from core.security import get_password_hash

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str):
        return self.session.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def create(self, user_in: UserCreate) -> User:
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password)
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def update_password(self, user: User, new_password: str):
        user.hashed_password = get_password_hash(new_password)
        self.session.commit()
        self.session.refresh(user)
        return user

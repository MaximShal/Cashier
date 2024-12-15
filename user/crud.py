from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, login: str, password: str):
    user = db.query(User).filter(User.login == login).first()
    if not user:
        return None
    if not pwd_context.verify(password, user.password):
        return None
    return user


def create_user(db_session: Session, login: str, password: str, name: str = None):
    hashed_password = pwd_context.hash(password)
    new_user = User(login=login, password=hashed_password, name=name)
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user

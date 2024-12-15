from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from core.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    disabled = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, login={self.login})>"

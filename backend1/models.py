from typing import Optional
from sqlalchemy import UUID, Column, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from database import Base

# https://docs.sqlalchemy.org/en/20/orm/quickstart.html
class User(Base):
    __tablename__ = "user_account"
    
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
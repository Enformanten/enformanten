from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import declarative_base

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    __abstract__ = True
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    pass

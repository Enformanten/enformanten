from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.ext.declarative import declarative_base


DeclarativeBase = declarative_base()


class UserBase(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, UserBase):
    pass

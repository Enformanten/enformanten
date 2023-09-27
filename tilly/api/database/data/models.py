from sqlalchemy import Boolean, Column, Date, Float, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base

from tilly.api.config import TRAINING_TABLE_NAME, UNSCORED_TABLE_NAME, SCORED_TABLE_NAME

DeclarativeBase = declarative_base()


class TrainingTimeslots(DeclarativeBase):
    __tablename__ = TRAINING_TABLE_NAME

    id = Column(Integer, primary_key=True)
    room_id = Column("ID", Integer, nullable=False)
    municipality = Column("KOMMUNE", String, nullable=False)
    school = Column("SKOLE", String, nullable=False)
    date = Column("DATE", Date, nullable=False)
    time = Column("TIME", Time, nullable=False)
    dayname = Column("DAYNAME", String, nullable=False)
    time_type = Column("TIDSPUNKT_TYPE", String, nullable=False)
    scheduled = Column("SKEMALAGT", Boolean, nullable=False)
    type = Column("TYPE", String, nullable=False)
    name = Column("NAVN", String, nullable=False)
    co2 = Column("CO2", Float, nullable=True)
    temp = Column("TEMP", Float, nullable=True)
    motion = Column("MOTION", Float, nullable=True)
    iaq = Column("IAQ", Float, nullable=True)
    booked = Column("BOOKET", Boolean, nullable=True)

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}


class UnscoredTimeslots(DeclarativeBase):
    __tablename__ = UNSCORED_TABLE_NAME

    id = Column(Integer, primary_key=True)
    room_id = Column("ID", Integer, nullable=False)
    municipality = Column("KOMMUNE", String, nullable=False)
    school = Column("SKOLE", String, nullable=False)
    date = Column("DATE", Date, nullable=False)
    time = Column("TIME", Time, nullable=False)
    dayname = Column("DAYNAME", String, nullable=False)
    time_type = Column("TIDSPUNKT_TYPE", String, nullable=False)
    scheduled = Column("SKEMALAGT", Boolean, nullable=False)
    type = Column("TYPE", String, nullable=False)
    name = Column("NAVN", String, nullable=False)
    co2 = Column("CO2", Float, nullable=True)
    temp = Column("TEMP", Float, nullable=True)
    motion = Column("MOTION", Float, nullable=True)
    iaq = Column("IAQ", Float, nullable=True)
    booked = Column("BOOKET", Boolean, nullable=True)

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}


class ScoredTimeslots(DeclarativeBase):
    __tablename__ = SCORED_TABLE_NAME

    id = Column(Integer, primary_key=True)
    room_id = Column("ID", Integer, nullable=False)
    municipality = Column("KOMMUNE", String, nullable=False)
    school = Column("SKOLE", String, nullable=False)
    date = Column("DATE", Date, nullable=False)
    time = Column("TIME", Time, nullable=False)
    score = Column("ANOMALY_SCORE", Float, nullable=True)
    IN_USE = Column("IN_USE", Boolean, nullable=True)

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

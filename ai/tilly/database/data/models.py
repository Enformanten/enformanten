"""
Database Tables Definition

This script defines SQLAlchemy database tables for training,
unscored, and scored timeslots data.
"""

from sqlalchemy import Boolean, Column, Date, Float, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base

from tilly.config import TRAINING_TABLE_NAME, UNSCORED_TABLE_NAME, SCORED_TABLE_NAME

DeclarativeBase = declarative_base()


class TrainingTimeslots(DeclarativeBase):
    """
    SQLAlchemy table definition for training timeslots data.

    Args:
        DeclarativeBase: Base class for declarative SQLAlchemy
            table definitions.

    Example:
    ```python
    # Create a new TrainingTimeslots object
    new_training_entry = TrainingTimeslots(
        room_id=123,
        municipality="Example Municipality",
        school="Example School",
        date="2023-10-17",
        time="08:00 AM",
        dayname="Monday",
        time_type="Regular",
        scheduled=True,
        type="Classroom",
        name="Room 101",
        co2=400.0,
        temp=22.5,
        motion=1.0,
        iaq=0.95,
        booked=True
    )
    ```
    """

    __tablename__ = TRAINING_TABLE_NAME

    id = Column(Integer, primary_key=True)
    room_id = Column("ID", Integer, nullable=False)
    municipality = Column("KOMMUNE", String, nullable=False)
    school = Column("SKOLE", String, nullable=False)
    date = Column("DATE", String, nullable=False)
    time = Column("TIME", String, nullable=False)
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

    def as_dict(self) -> dict:
        """
        Convert the table row to a dictionary.

        Returns:
            dict: A dictionary representing the table row.
        """
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}


class UnscoredTimeslots(DeclarativeBase):
    """
    SQLAlchemy table definition for unscored timeslots data.

    Args:
        DeclarativeBase: Base class for declarative SQLAlchemy
            table definitions.

    Example:
    ```python
    # Create a new UnscoredTimeslots object
    new_unscored_entry = UnscoredTimeslots(
        room_id="Room101",
        municipality="Example Municipality",
        school="Example School",
        date="2023-10-17",
        time="08:00 AM",
        dayname="Monday",
        time_type="Regular",
        scheduled=True,
        type="Classroom",
        name="Room 101",
        co2=400.0,
        temp=22.5,
        motion=1.0,
        iaq=0.95,
        booked=True
    )
    ```
    """

    __tablename__ = UNSCORED_TABLE_NAME

    id = Column(Integer, primary_key=True)
    room_id = Column("ID", String, nullable=False)
    municipality = Column("KOMMUNE", String, nullable=False)
    school = Column("SKOLE", String, nullable=False)
    date = Column("DATE", String, nullable=False)
    time = Column("TIME", String, nullable=False)
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

    def as_dict(self) -> dict:
        """
        Convert the table row to a dictionary.

        Returns:
            dict: A dictionary representing the table row.
        """
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}


class ScoredTimeslots(DeclarativeBase):
    """
    SQLAlchemy table definition for scored timeslots data.

    Args:
        DeclarativeBase: Base class for declarative SQLAlchemy
            table definitions.
    """

    __tablename__ = SCORED_TABLE_NAME

    id = Column(Integer, primary_key=True)
    ID = Column("ID", String, nullable=False)
    KOMMUNE = Column("KOMMUNE", String, nullable=False)
    DATE = Column("DATE", Date, nullable=False)
    TIME = Column("TIME", Time, nullable=False)
    ANOMALY_SCORE = Column("ANOMALY_SCORE", Float, nullable=True)
    IN_USE = Column("IN_USE", Boolean, nullable=True)

    def as_dict(self) -> dict:
        """
        Convert the table row to a dictionary.

        Returns:
            dict: A dictionary representing the table row.
        """
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

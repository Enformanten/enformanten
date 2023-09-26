from datetime import datetime
from pydantic import BaseModel, Field
from pandas import DataFrame


class Timeslots(BaseModel):

    """Pydantic model for Timeslots table"""

    room_id: int = Field(alias="ID")
    municipality: str = Field(alias="KOMMUNE")
    school: str = Field(alias="SKOLE")
    date: datetime = Field(alias="DATE")
    time: datetime = Field(alias="TIME")
    dayname: str = Field(alias="DAYNAME")
    time_type: str = Field(alias="TIDSPUNKT_TYPE")
    scheduled: bool = Field(alias="SKEMALAGT")
    type: str = Field(alias="TYPE")
    name: str = Field(alias="NAVN")
    co2: float = Field(alias="CO2")
    temp: float = Field(alias="TEMP")
    motion: float = Field(alias="MOTION")
    iaq: float = Field(alias="IAQ")
    booked: bool = Field(alias="BOOKET")

    class Config:
        """This is to allow the model to be populated by field name.
        Put simply: Timeslots(**dict) will work"""

        allow_population_by_field_name = True

    def to_frame(self):
        """Convert to pandas dataframe"""
        return DataFrame([dict(self)])


class Rooms(BaseModel):

    """Pydantic model for Timeslots table"""

    room_id: int = Field(alias="ID")
    municipality: str = Field(alias="KOMMUNE")
    school: str = Field(alias="SKOLE")
    date: datetime = Field(alias="DATE")
    time: datetime = Field(alias="TIME")
    dayname: str = Field(alias="DAYNAME")
    time_type: str = Field(alias="TIDSPUNKT_TYPE")
    scheduled: bool = Field(alias="SKEMALAGT")
    type: str = Field(alias="TYPE")
    name: str = Field(alias="NAVN")
    co2: float = Field(alias="CO2")
    temp: float = Field(alias="TEMP")
    motion: float = Field(alias="MOTION")
    iaq: float = Field(alias="IAQ")
    booked: bool = Field(alias="BOOKET")

    class Config:
        """This is to allow the model to be populated by field name.
        Put simply: Timeslots(**dict) will work"""

        allow_population_by_field_name = True

    def to_frame(self):
        """Convert to pandas dataframe"""
        return DataFrame([dict(self)])

    def group_by_school_room(self):
        """Group by school and room"""
        return self.groupby(["SKOLE", "ID"])


class Room(BaseModel):

    """Pydantic model for Timeslots table"""

    def to_frame(self):
        """Convert to pandas dataframe"""
        return DataFrame([dict(self)])


class Predictions(BaseModel):

    """Pydantic model for Timeslots table"""

    labels: list[int]
    scores: list[float]

    class Config:
        """This is to allow the model to be populated by field name.
        Put simply: Timeslots(**dict) will work"""

        allow_population_by_field_name = True


class IsOK(BaseModel):
    ok: bool

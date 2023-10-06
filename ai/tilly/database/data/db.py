from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from tilly.config import SNOWFLAKE_CREDENTIALS, DB_ECHO


# Define your Snowflake connection parameters
SNOWFLAKE_URL = (
    "snowflake://{user}:{password}@{account}"
    "/{database}/{schema}?warehouse={warehouse}&role={role}"
).format(**SNOWFLAKE_CREDENTIALS)

# Create a synchronous engine
engine = create_engine(SNOWFLAKE_URL, echo=DB_ECHO, future=True)
Session = sessionmaker(bind=engine)


def get_session() -> Generator[Session, None, None]:
    with Session() as session:
        yield session

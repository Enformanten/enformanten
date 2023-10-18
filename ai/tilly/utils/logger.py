import time
import logging
from rich.logging import RichHandler
from typing import Callable
from functools import wraps
import pandas as pd

from tilly.config import DEBUG


# setting for stdout and file logging
logger = logging.getLogger(__name__)
stdout_handler = RichHandler()

# logging levels
logger.setLevel(logging.DEBUG)

stdout_handler.setFormatter(logging.Formatter("%(message)s"))
# add handlers
logger.addHandler(stdout_handler)


# pipeline logger
def log_pipeline(function: Callable, verbose=DEBUG) -> Callable:
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not verbose:
            return function(*args, **kwargs)

        start_time = time.perf_counter()
        result = function(*args, **kwargs)
        time_taken = time.perf_counter() - start_time
        logger.debug(
            f"{function.__name__} completed | "
            + f"shape = {result.shape:} | "
            + f"time {time_taken:.3f}s"
        )
        return result

    return wrapper


def log_size(df, unique="SKOLE_ID") -> pd.DataFrame:
    """
    Pandas pipe function to log:
    - The size of the dataframe.
    - The number of uniques in column 'unique'.

    Args:
        df (pd.DataFrame): The dataframe to log.

    Returns:
        pd.DataFrame: The dataframe.

    Example:
    ```python
    # Apply the log_size function to a DataFrame
    df = df.pipe(log_size)
    ```
    """
    logger.info(f"Shape {df.shape} | " + f"Unique '{unique}': {df[unique].nunique()}")
    return df

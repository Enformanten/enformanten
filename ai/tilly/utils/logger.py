"""
This script contains utilities for logging within the Tilly application.
It is designed to provide both console and file-based logging functionalities
for the entire application. The script uses the RichHandler from the Rich
library for enhanced console outputs and the built-in logging module for
creating logs.

Main Components:
    - Configuration of the logger with different handlers and formatters.
    - `log_pipeline` function: A decorator for logging various details about 
        functions. It wraps around any callable and logs its execution time, 
        the shape of its output (assuming it returns a Pandas DataFrame), and
        the function name.
    - `log_size` function: A Pandas pipe function that logs the size of the
        DataFrame and the number of unique values in a specified column.

Usage:
    - For logging details about a function, use the `@log_pipeline` decorator:
        ```python
        @log_pipeline
        def some_function(arg1, arg2):
            # function logic here
        ```
    - For logging the size of a DataFrame within a Pandas pipeline:
        ```python
        df = df.pipe(log_size)
        ```

The `log_pipeline` function uses the `DEBUG` setting from `tilly.config` 
to decide whether to display verbose logs or not.

Example:
    >>> from tilly.logging_utils import log_pipeline, log_size
    >>> @log_pipeline
    ... def my_function(data):
    ...     # some code
    ...     return data
    >>> df = df.pipe(log_size)
"""


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

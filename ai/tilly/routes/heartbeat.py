"""
Heartbeat Endpoint for Tilly Service

This module contains a FastAPI router for serving a heartbeat endpoint.
The endpoint returns the current version of the service based on the GIT metadata.
"""

from fastapi import APIRouter, Request

from tilly.config import (
    GIT_METADATA,
)  # Environment variable set during GitHub Actions job

# Initialize FastAPI router
router = APIRouter()


@router.get("/heartbeat/")
def heartbeat(_: Request) -> dict:
    """
    Heartbeat Endpoint for Health Check and Versioning.

    This route returns a JSON object containing the current version of the service.
    The version information is retrieved from an environment variable, `GIT_METADATA`,
    which is set during a GitHub Actions job.

    Args:

        request (Request): The FastAPI request object. This argument is ignored but
            included for potential future use.

    Returns:

        dict: A dictionary containing the version information, with key "version" and
            value as the short version of the git hash of the last commit.


    Examples:

        ```bash
        curl http://localhost:8000/heartbeat/
        ```

    Output:

        ```json
        {
            "version": "abc123"  # The git hash short version
        }
        ```

    Note:

        The `GIT_METADATA` environment variable must be set, usually during a
        GitHub Actions job, for this endpoint to return accurate version information.
        If run locally, the version will be set to "local".
    """
    return {"version": GIT_METADATA}

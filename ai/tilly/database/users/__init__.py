"""
The database.users module is responsible for all communication
with the in-memory sqllite database that stores user credentials.

The module is organized as follows:

- `/database/users/crud.py`: Contains the functions that are used
to interact with the database.
- `/database/users/models.py`: Contains the SQLAlchemy schemas 
that are used to interact with the database.

**NOTE**: This project uses `fastapi-users` to automate parts of 
the user management. The `fastapi-users` configuration can be 
found in `/users/`.
"""

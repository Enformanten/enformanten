from decouple import config

LOGIN_NAME = (config("LOGIN_NAME", "datax_admin@tilly.dk"),)
LOGIN_PASSWORD = config("LOGIN_PASSWORD", "password")
URL = config("URL", "http://localhost:8001")

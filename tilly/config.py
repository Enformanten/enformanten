from configparser import ConfigParser

config = ConfigParser()
config.read("config.cfg")

DATA_PATH: str = config["DATA"]["DATA_PATH"]
OUTPUT_COLUMNS: list = config["FORMAT"]["OUTPUT_COLUMNS"]

FEATURES: list = config["MODELLING"]["FEATURES"]

USAGE_COEFF = float(config["MODELLING"]["USAGE_COEFF"])
USAGE_LIMIT = float(config["MODELLING"]["USAGE_LIMIT"])
RANDOM_STATE = int(config["MODELLING"]["RANDOM_STATE"])
APPLY_RULES = bool(config["MODELLING"]["APPLY_RULES"])

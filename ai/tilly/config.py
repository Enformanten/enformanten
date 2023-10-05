from ast import literal_eval
from decouple import config
from pathlib import Path


GIT_METADATA = config("GIT_METADATA", default="local")

##################
# USERS AND USERS DB
##################

SECRET = config("SECRET")
USERS = config("USERS", cast=literal_eval)
USER_DATABASE_URL = config("DATABASE_URL")

################
# API
################

TITLE = "Tilly API"
DEBUG = True
DESCRIPTION = "Unsupervised anomaly detection for room usage"
PLOTS_DIR = Path("tilly/dashboard/plots")


################
# DATA FACTORY TABLES
################

# Table to load training data from
TRAINING_TABLE_NAME = config("TRAINING_TABLE")
# Table to load data to predict on from
UNSCORED_TABLE_NAME = config("PREDICT_TABLE")
# Table to append predictions in
SCORED_TABLE_NAME = config("SCORED_TABLE")

OUTPUT_COLUMNS = ["ID", "KOMMUNE", "DATE", "TIME", "ANOMALY_SCORE", "IN_USE"]


################
# snowflake credentials
################

SNOWFLAKE_CREDENTIALS = config("SNOWFLAKE_CREDENTIALS", cast=literal_eval)

################
# MODEL
################
MODEL_PARAMS = {"n_estimators": 300, "random_state": 42}

FEATURES = ["CO2_ACC", "CO2"]

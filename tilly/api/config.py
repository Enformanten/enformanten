from ast import literal_eval
from decouple import config


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
PLOT_DIR = "dashboard/plots"


################
# DATA FACTORY DB
################

# Table to load training data from
TRAINING_TABLE_NAME = "4_FEATURIZ_DRIFTOPTIMERING_TRAINING_TEST"

# Table to load data to predict on from
UNSCORED_TABLE_NAME = "4_FEATURIZ_DRIFTOPTIMERING_PREDICT_TEST"

# Table to append predictions in
SCORED_TABLE_NAME = "1_RAW_DRIFTOPTIMERINGSMODEL_TEST"

# snowflake credentials
SNOWFLAKE_CREDENTIALS = config("SNOWFLAKE_CREDENTIALS", cast=literal_eval)


################
# MODEL
################
MODEL_PARAMS = {
    "n_estimators": 100,
}

FEATURES = [
    "CO2_ACC",
]
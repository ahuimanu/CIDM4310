# Using the Azure AutoML SDK in Python
"""
Design assumptions: 
+ You have an Azure subscription
+ You have an Azure Machine Learning workspace
+ You have an Azure Machine Learning compute target
+ You have an Azure Machine Learning dataset
+ You have an Azure Machine Learning experiment
+ You have an Azure Machine Learning model
+ You have an Azure Machine Learning deployment
+ You have an Azure Machine Learning endpoint
+ You have an Azure Machine Learning API key
+ You have an Azure Machine Learning API URL
+ You want to use the Azure AutoML SDK in Python
+ You want to use the Azure AutoML SDK in Python to make predictions
+ You want to use the Azure AutoML SDK in Python to make predictions reading to and from sqlite
+ you will then plug Power BI into the sqlite database to visualize the data
"""

from azure.ai.ml import automl, Input, MLClient
from azure.ai.ml.automl import ColumnTransformer
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Data
from azure.identity import DefaultAzureCredential
import mltable
from mltable import DataType
from decimal import Decimal
import pandas as pd
import os
import pickle
import time

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

AZ_COMPUTE_NAME = os.getenv("AZ_COMPUTE_NAME")
AZ_EXPERIMENT_NAME = os.getenv("AZ_EXPERIMENT_NAME")
AZ_RESOURCE_GROUP = os.getenv("AZ_RESOURCE_GROUP")
AZ_SUBSCRIPTION_ID = os.getenv("AZ_SUBSCRIPTION_ID")
AZ_WORKSPACE_NAME = os.getenv("AZ_WORKSPACE_NAME")

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

VERSION = time.strftime("%Y.%m.%d.%H%M%S", time.localtime())

TRAIN_CSV_FILE = "./train_data/bts_results.csv"
TRAIN_CSV_FILE_MOD = "./train_data/bts_results_mod.csv"


def transform_decimal_to_period_decimal(csv_file):
    """Transform the decimal delimiter to a period decimal."""
    dataset_for_training = pd.read_csv(
        csv_file,
        delimiter=".",
        decimal=",",
        header="infer",
    )
    dataset_for_training.to_csv(csv_file, sep=",", decimal=".", index=False)


# we first will rely on pandas for some data cleaning as there is no built-in data cleaning in the SDK
# with respect to transforming the comma decimal to a period decimal. Pandas makes quick work of this
# doing this everytime is not needed as once we've run this, the data will be transformed
# SO, this could be commented out for subsequent runs
# transform_decimal_to_period_decimal(TRAIN_CSV_FILE)


# create client
ml_client = MLClient(
    DefaultAzureCredential(), AZ_SUBSCRIPTION_ID, AZ_RESOURCE_GROUP, AZ_WORKSPACE_NAME
)

# Get the training data
paths = [{"file": TRAIN_CSV_FILE}]

train_table = mltable.from_delimited_files(
    paths, header="from_first_file", delimiter=",", infer_column_types=True
)

# keep only the columns of interest
train_table = train_table.keep_columns(
    [
        "OP_CARRIER",
        "DEP_TIME",
        "DEP_DELAY",
        "ORIGIN",
        "DEST",
        "DISTANCE",
        "CARRIER_DELAY",
        "WEATHER_DELAY",
        "NAS_DELAY",
        "SECURITY_DELAY",
        "LATE_AIRCRAFT_DELAY",
        "FLIGHT_RULES",
    ]
)

# raise Exception(f"Stop here to check the Train table: {train_table.show(1)}")

# https://learn.microsoft.com/en-us/azure/machine-learning/how-to-mltable?view=azureml-api-2&tabs=cli#delimited-files

#   - OP_CARRIER
#   - DEP_TIME
#   - DEP_DELAY
#   - DEP_DELAY_GROUP
#   - ORIGIN
#   - DEST
#   - DISTANCE
#   - CARRIER_DELAY
#   - WEATHER_DELAY
#   - NAS_DELAY
#   - SECURITY_DELAY
#   - LATE_AIRCRAFT_DELAY
#   - FLIGHT_RULES

column_types = {
    "OP_CARRIER": DataType.to_string(),
    "DEP_TIME": DataType.to_string(),
    "DEP_DELAY": DataType.to_float(),
    "ORIGIN": DataType.to_string(),
    "DEST": DataType.to_string(),
    "DISTANCE": DataType.to_float(),
    "CARRIER_DELAY": DataType.to_float(),
    "WEATHER_DELAY": DataType.to_float(),
    "NAS_DELAY": DataType.to_float(),
    "SECURITY_DELAY": DataType.to_float(),
    "LATE_AIRCRAFT_DELAY": DataType.to_float(),
    "FLIGHT_RULES": DataType.to_string(),
}

# convert the column types - Tobias uses a different decimal delimiter for instance
train_table = train_table.convert_column_types(column_types)

# raise Exception(f"Stop here to check the Train table: {train_table}")
train_table.save("./train_data")

# setup the data object
train_data = Data(
    path="./train_data",
    type=AssetTypes.MLTABLE,
    description="Training data for the AUS flights ontime model",
    name="AUS_FLIGHTS_SUMMER_2023",
    version=VERSION,
)

# create the data asset in the workspace
result = ml_client.data.create_or_update(train_data)

print(f"Data asset created: {result}")

# Training Day
# make an Input object for the training data
aus_ontime_training_data_input = Input(type=AssetTypes.MLTABLE, path="./train_data")


# configure the regression job
aus_ontime_regression_job = automl.regression(
    compute=AZ_COMPUTE_NAME,
    experiment_name=AZ_EXPERIMENT_NAME,
    training_data=aus_ontime_training_data_input,
    target_column_name="CARRIER_DELAY",
    primary_metric="normalized_root_mean_squared_error",
    enable_model_explainability=True,
    tags={"bts": "aus ontime flight data"},
)

# Limits are all optional
aus_ontime_regression_job.set_limits(
    timeout_minutes=60,
    trial_timeout_minutes=20,
    max_trials=5,
    enable_early_termination=True,
)


# configure the classification job
# aa_ontime_classification_job = automl.classification(
#     compute=AZ_COMPUTE_NAME,
#     experiment_name=AZ_EXPERIMENT_NAME,
#     training_data=aa_ontime_training_data_input,
#     target_column_name="ArrDel15",
#     primary_metric="precision_score_weighted",
#     n_cross_validations=5,
#     enable_model_explainability=True,
#     tags={"bts": "ontime flight data"},
# )

# Limits are all optional
# aa_ontime_classification_job.set_limits(
#     timeout_minutes=60,
#     trial_timeout_minutes=20,
#     max_trials=5,
#     enable_early_termination=True,
# )

# Submit the AutoML job
returned_job = ml_client.jobs.create_or_update(
    aus_ontime_regression_job
)  # submit the job to the backend

print(f"Created job: {returned_job}")

# Get a URL for the status of the job
url = returned_job.services["Studio"].endpoint

print(f"Job URL: {url}")

# its not straighforward to get monitor the job, so you can use the URL to monitor the job
# we'll want a separate script to use the model locally
# we still need to monitor the model at azure
# however, we can use the model locally and make predictions here - no endnpoint needed
# also, since we read the file locally, BLOB storage became unnecessary

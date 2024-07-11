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
import os
import pickle
import time
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

AZ_COMPUTE_NAME = os.getenv("COMPUTE_NAME")
AZ_EXPERIMENT_NAME = os.getenv("AZ_EXPERIMENT_NAME")
AZ_RESOURCE_GROUP = os.getenv("AZ_RESOURCE_GROUP")
AZ_SUBSCRIPTION_ID = os.getenv("AZ_SUBSCRIPTION_ID")
AZ_WORKSPACE_NAME = os.getenv("AZ_WORKSPACE_NAME")

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

VERSION = time.strftime("%Y.%m.%d.%H%M%S", time.localtime())

# create client
ml_client = MLClient(
    DefaultAzureCredential(), AZ_SUBSCRIPTION_ID, AZ_RESOURCE_GROUP, AZ_WORKSPACE_NAME
)

# Get the training data
paths = [{"file": "./train_data/AA_Flights_2021_01.csv"}]

train_table = mltable.from_delimited_files(paths, header="from_first_file", delimiter=";")

column_types = {
    "DepDeplay": DataType.to_float(),
}

train_table.save("./train_data")

# raise Exception(f"Stop here to check the Train table: {train_table}")
train_table.save("./train_data")

# setup the data object
train_data = Data(
    path="./train_data",
    type=AssetTypes.MLTABLE,
    description="Training data for the AA flights ontime model",
    name="AA_Flights_2021_01",
    version=VERSION,
)

# create the data asset in the workspace
result = ml_client.data.create_or_update(train_data)

print(f"Data asset created: {result}")

# Training Day
# make an Input object for the training data
aa_ontime_training_data_input = Input(type=AssetTypes.MLTABLE, path="./train_data")

# configure the classification job
aa_ontime_classification_job = automl.classification(
    compute=AZ_COMPUTE_NAME,
    experiment_name=AZ_EXPERIMENT_NAME,
    training_data=aa_ontime_training_data_input,
    target_column_name="y",
    primary_metric="precision_score_weighted",
    n_cross_validations=5,
    enable_model_explainability=True,
    tags={"bts": "ontime flight data"},
)

# Limits are all optional
aa_ontime_classification_job.set_limits(
    timeout_minutes=60,
    trial_timeout_minutes=20,
    max_trials=5,
    enable_early_termination=True,
)

# Submit the AutoML job
returned_job = ml_client.jobs.create_or_update(
    aa_ontime_classification_job
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

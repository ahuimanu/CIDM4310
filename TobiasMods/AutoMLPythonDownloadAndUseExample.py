# Using the Azure AutoML SDK in Python
"""
Design assumptions: 
+ we want to download the model directly from the Azure AutoML SDK
+ we want to use the model in a separate script
+ we want to use the model in a to produce the predictions
"""

# NOTE: it is be neccessary to download and install the Azure CLI to access credential tokens

from azure.ai.ml import automl, Input, MLClient
from azure.ai.ml.automl import ColumnTransformer
from azure.ai.ml.constants import AssetTypes
from azure.identity import DefaultAzureCredential
import mltable
import os
import pickle
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

AZ_COMPUTE_NAME = os.getenv("COMPUTE_NAME")
AZ_EXPERIMENT_NAME = os.getenv("AZ_EXPERIMENT_NAME")
AZ_RESOURCE_GROUP = os.getenv("AZ_RESOURCE_GROUP")
AZ_SUBSCRIPTION_ID = os.getenv("AZ_SUBSCRIPTION_ID")
AZ_WORKSPACE_NAME = os.getenv("AZ_WORKSPACE_NAME")


API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

# create client
ml_client = MLClient(
    DefaultAzureCredential(exclude_interactive_browser_credential=False), AZ_SUBSCRIPTION_ID, AZ_RESOURCE_GROUP, AZ_WORKSPACE_NAME
)

print(f"Client created {ml_client}")

# Get the training data
paths = [{"file": "./AA_Flights_2021_01.csv"}]

train_table = mltable.from_delimited_files(paths)
raise Exception("Stop here to check the Train table: {train_table}")
print(f"Train table: {train_table}")
train_table.save("./train_data")


# Training Day
# make an Input object for the training data
aa_ontime_training_data_input = Input(
    type=AssetTypes.MLTABLE, path="./data/training-mltable-folder"
)

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

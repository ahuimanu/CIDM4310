# SECTION 0: Setup and Variables ----

# An actual example of the endpoint call!
# https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-mlflow-models-online-endpoints?view=azureml-api-2&tabs=sdk

# Make sure these packages are installed
import pandas as pd
import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

API_KEY = ""
API_URL = (os.getenv("API_URL"))


# SECTION 1: API Request Function ----

def inference_request(
    DayOfWeek,
    Origin,
    Dest,
    DepDelay,
    DepDelayMinutes,
    DepDel15,
    DepartureDelayGroups,
    DepTimeBlk,
    TaxiOut,
    ArrTimeBlk,
    Distance,
    DistanceGroup,
):

    input_data = {
        "DayOfWeek": [DayOfWeek],
        "Origin": [Origin],
        "Dest": [Dest],
        "DepDelay": [DepDelay],
        "DepDelayMinutes": [DepDelayMinutes],
        "DepDel15": [DepDel15],
        "DepartureDelayGroups": [DepartureDelayGroups],
        "DepTimeBlk": [DepTimeBlk],
        "TaxiOut": [TaxiOut],
        "ArrTimeBlk": [ArrTimeBlk],
        "Distance" : [Distance],
        "DistanceGroup": [DistanceGroup],
    }

    # Bind columns to dataframe
    request_df = pd.DataFrame(input_data)
    df_array = list(request_df.to_dict(orient="records"))

    req = {
        "input_data": 
        {
            "columns": request_df.columns.tolist(),
            "index": [0],
            "data": df_array,
        }
    }

    # POST request - send JSON to API
    headers = {
        "Authorization": ("Bearer " + API_KEY),
        "Content-Type": "application/json",
    }

    raise Exception(json.dumps(req))

    # result = requests.post(url=API_URL, data=str.encode(json.dumps(req)), headers=headers)
    result = requests.post(API_URL, json=req, headers=headers)
    return result


# SECTION 2: Data preprocessing ----

# Fetch data from Power Query workflow

df = dataset

# SECTION 3: Get Predictions ----
for index, row in df.iterrows():
    # to prevent bombarding the API
    time.sleep(1)
    result = inference_request(
        row["DayOfWeek"],
        row["Origin"],
        row["Dest"],
        row["DepDelay"],
        row["DepDelayMinutes"],
        row["DepDel15"],
        row["DepartureDelayGroups"],
        row["DepTimeBlk"],
        row["TaxiOut"],
        row["ArrTimeBlk"],
        row["Distance"],
        row["DistanceGroup"],
    )

    # SECTION 4: Data postprocessing ----
    result = pd.DataFrame(json.loads(result.content))
    # raising an excpetion seems to be the only path for debugging purposes in Power BI
    # raise Exception(result.values[0])
    row["ArrDel15_Prediction"] = result.values[0]


# SECTION 5: Format output for Power BI ----
output = df

"""
This is Tobias' script modified to simply read a csv file and return the predictions.
We'll also output the predictions to a csv file.
"""

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

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")


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
        "Distance": [Distance],
        "DistanceGroup": [DistanceGroup],
    }

    # Bind columns to dataframe
    request_df = pd.DataFrame(input_data)
    df_array = list(request_df.to_dict(orient="records"))

    # extract just the values from the dictionary
    # helpful: https://stackoverflow.com/questions/7271482/getting-a-list-of-values-from-a-list-of-dicts-in-python
    values_list = []
    for x in df_array[0].items():
        values_list.append(x[1])

    # create the json structure for the request
    req = {
        "input_data": 
        {
            "columns": request_df.columns.tolist(),
            "index": [0],
            "data": [values_list],
        }
    }

    # POST request - send JSON to API
    headers = {
        "Authorization": ("Bearer " + API_KEY),
        "Content-Type": "application/json",
    }

    # quick test of the results
    # raise Exception(json.dumps(req))

    # result = requests.post(url=API_URL, data=str.encode(json.dumps(req)), headers=headers)
    result = requests.post(API_URL, json=req, headers=headers)
    return result


# SECTION 2: Data preprocessing ----

# read from CSV file
df = pd.read_csv("AA_Hourly_Batches_2021-02-07_08000-859.csv")

dfo_structure = {"ArrDel15_Prediction": []}
dfo = pd.DataFrame(dfo_structure)

# raise Exception(dfo)

# SECTION 3: Get Predictions ----
for index, row in df.iterrows():
    # to prevent bombarding the API
    time.sleep(0.1)
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
    print(result)
    result = pd.DataFrame(json.loads(result.content))
    print(f"model result for {index}: {result.values[0]}")
    dfo.loc[index] = result.values[0]

# SECTION 5: Write output to csv ----

# shows the last row of the dataframe
# raise Exception(df.values[len(df) - 1])
dfoutput = pd.concat([df, dfo], axis="columns")

# write to csv
dfoutput.to_csv("AA_Hourly_Batches_2021-02-07_08000-859_output.csv", index=False)

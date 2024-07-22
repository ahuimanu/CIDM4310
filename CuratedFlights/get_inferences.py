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
from random import randint
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")


# SECTION 1: API Request Function ----

def inference_request(
    OP_CARRIER,
    DEP_TIME,
    DEP_DELAY,
    ORIGIN,
    DEST,
    DISTANCE,
):
    
    # "OP_CARRIER": DataType.to_string(),
    # "DEP_TIME": DataType.to_string(),
    # "DEP_DELAY": DataType.to_float(),
    # "ORIGIN": DataType.to_string(),
    # "DEST": DataType.to_string(),
    # "DISTANCE": DataType.to_float(),
    # "CARRIER_DELAY": DataType.to_float(),
    # "WEATHER_DELAY": DataType.to_float(),
    # "NAS_DELAY": DataType.to_float(),
    # "SECURITY_DELAY": DataType.to_float(),
    # "LATE_AIRCRAFT_DELAY": DataType.to_float(),
    # "FLIGHT_RULES": DataType.to_string(),

    # randomize the flight rules
    frlist = ["VFR", "IFR", "MVFR", "LIFR"]

    if DEP_DELAY is None:
        DEP_DELAY = 0
    if DEP_TIME is None:
        DEP_TIME = "0000"
    if DISTANCE is None:
        DISTANCE = 0

    ddelay = float(DEP_DELAY) / 15
    fr = frlist[randint(0, 3)]
    origin = ORIGIN[1:]
    dest = DEST[1:]

    input_data = {
        "OP_CARRIER": [OP_CARRIER],
        "DEP_TIME": [DEP_TIME],
        "DEP_DELAY": [DEP_DELAY],
        "DEP_DELAY_GROUP": [str(ddelay)],        
        "ORIGIN": [origin],
        "DEST": [dest],
        "DISTANCE": [DISTANCE],
        "WEATHER_DELAY": [0],
        "NAS_DELAY": [0],        
        "SECURITY_DELAY": [0],
        "LATE_AIRCRAFT_DELAY": [0],
        "FLIGHT_RULES": [fr],
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
df = pd.read_csv("KAUS_inferencing_inputs.csv")

dfo_structure = {"CARRIER_DELAY_Prediction": []}
dfo = pd.DataFrame(dfo_structure)

# raise Exception(df)

# SECTION 3: Get Predictions ----
for index, row in df.iterrows():
    # to prevent bombarding the API
    time.sleep(0.1)
    # "OP_CARRIER","DEP_TIME","DEP_DELAY","ORIGIN","DEST","DISTANCE"
    result = inference_request(
        row["OP_CARRIER"],
        row["DEP_TIME"],
        row["DEP_DELAY"],
        row["ORIGIN"],
        row["DEST"],
        row["DISTANCE"],
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
dfoutput.to_csv("KAUS_inferencing_outputs.csv", index=False)

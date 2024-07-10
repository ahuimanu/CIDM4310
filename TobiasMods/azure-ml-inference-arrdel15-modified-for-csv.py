"""
This is Tobias' script modified to simply read a csv file and return the predictions.
We'll also output the predictions to a csv file.
"""

# SECTION 0: Setup and Variables ----

# Make sure these packages are installed
import pandas as pd
import requests
import json
import time

API_KEY = ""
API_URL = (
    "http://ee983424-4dea-47ec-a14b-e3f847c262f5.westcentralus.azurecontainer.io/score"
)


# SECTION 1: API Request Function ----

# This function stays because we still need to map dissimilarities between the trained data and the 
# data we're sending to the API
def create_full_model_record(
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
        "Year": [0],
        "Quarter": [0],
        "Month": [0],
        "DayofMonth": [0],
        "DayOfWeek": DayOfWeek,
        "FlightDate": ["2000-01-01T00:00:00.000Z"],
        "Reporting_Airline": ["example_value"],
        "DOT_ID_Reporting_Airline": [0],
        "IATA_CODE_Reporting_Airline": ["example_value"],
        "Tail_Number": ["example_value"],
        "Flight_Number_Reporting_Airline": [0],
        "OriginAirportID": [0],
        "OriginAirportSeqID": [0],
        "OriginCityMarketID": [0],
        # "Origin": "example_value",
        "Origin": Origin,
        "OriginCityName": ["example_value"],
        "OriginState": ["example_value"],
        "OriginStateFips": [0],
        "OriginStateName": ["example_value"],
        "OriginWac": [0],
        "DestAirportID": [0],
        "DestAirportSeqID": [0],
        "DestCityMarketID": [0],
        # "Dest": "example_value",
        "Dest": Dest,
        "DestCityName": ["example_value"],
        "DestState": ["example_value"],
        "DestStateFips": [0],
        "DestStateName": ["example_value"],
        "DestWac": [0],
        "CRSDepTime": [0],
        "DepTime": [0],
        # "DepDelay": "example_value",
        "DepDelay": DepDelay,
        # "DepDelayMinutes": "example_value",
        "DepDelayMinutes": DepDelayMinutes,
        # "DepDel15": "example_value",
        "DepDel15": DepDel15,
        # "DepartureDelayGroups": 0,
        "DepartureDelayGroups": DepartureDelayGroups,
        # "DepTimeBlk": "example_value",
        "DepTimeBlk": DepTimeBlk,
        # "TaxiOut": "example_value",
        "TaxiOut": TaxiOut,
        "WheelsOff": [0],
        "WheelsOn": [0],
        "TaxiIn": ["example_value"],
        "CRSArrTime": [0],
        "ArrTime": [0],
        "ArrDelay": ["example_value"],
        "ArrDelayMinutes": ["example_value"],
        "ArrivalDelayGroups": [0],
        #  "ArrTimeBlk": "example_value",
        "ArrTimeBlk": ArrTimeBlk,
        "Cancelled": [0],
        "CancellationCode": ["example_value"],
        "Diverted": [0],
        "CRSElapsedTime": ["example_value"],
        "ActualElapsedTime": ["example_value"],
        "AirTime": ["example_value"],
        "Flights": [0],
        # "Distance": "example_value",
        "Distance": Distance,
        # "DistanceGroup": 0,
        "DistanceGroup": DistanceGroup,
        "CarrierDelay": [0],
        "WeatherDelay": [0],
        "NASDelay": [0],
        "SecurityDelay": [0],
        "LateAircraftDelay": [0],
        "PREDICTED_BASELINE": ["example_value"],
        "DIFF_ELAPSED_ACTUAL": ["example_value"],
        "REGRESSION_ELAPSED_TIME": [0],
    }

    return input_data


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

    input_data = create_full_model_record(
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
    )

    # input_data = {
    #     "DayOfWeek": [DayOfWeek],
    #     "Origin": [Origin],
    #     "Dest": [Dest],
    #     "DepDelay": [DepDelay],
    #     "DepDelayMinutes": [DepDelayMinutes],
    #     "DepDel15": [DepDel15],
    #     "DepartureDelayGroups": [DepartureDelayGroups],
    #     "DepTimeBlk": [DepTimeBlk],
    #     "TaxiOut": [TaxiOut],
    #     "ArrTimeBlk": [ArrTimeBlk],
    #     "Distance" : [Distance],
    #     "DistanceGroup": [DistanceGroup],
    # }

    # Bind columns to dataframe
    request_df = pd.DataFrame(input_data)
    df_array = list(request_df.to_dict(orient="records"))

    req = {
        "Inputs": {"data": df_array},
        "GlobalParameters": {"method": "predict"},
    }

    # POST request - send JSON to API
    headers = {
        "Authorization": ("Bearer " + API_KEY),
        "Content-Type": "application/json",
    }

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
    result = pd.DataFrame(json.loads(result.content))
    print(f"model result for {index}: {result.values[0]}")
    dfo.loc[index] = result.values[0]
    # print(dfo.values[index])
    # row["ArrDel15_Prediction"] = result.values[0]

# SECTION 5: Write output to csv ----

# shows the last row of the dataframe
# raise Exception(df.values[len(df) - 1])
dfoutput = pd.concat([df, dfo], axis=1)

# write to csv
dfoutput.to_csv("AA_Hourly_Batches_2021-02-07_08000-859_output.csv", index=False)

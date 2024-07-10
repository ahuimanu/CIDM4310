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

    # Bind columns to dataframe
    request_df = pd.DataFrame(input_data)
    df_array = list(request_df.to_dict(orient="records"))

    req = {
        "Inputs": {"data": df_array},
        # "Inputs": {"data": list(request_df.to_dict(orient="records"))},
        # "Inputs": {"data": request_df.to_json(orient="records")},
        # "Inputs": {"data": list(request_df.to_dict("records"))},
        # "Inputs": {"data": request_df.to_dict("records")},
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

# temporary dataset

# 7	LAX	JFK	-6	0	0	-1	0800-0859	28	1600-1659	2475	10
# dataset = {
#     "Year": [0],
#     "Quarter": [0],
#     "Month": [0],
#     "DayofMonth": [0],
#     "DayOfWeek": [7],
#     "FlightDate": ["2000-01-01T00:00:00.000Z"],
#     "Reporting_Airline": ["example_value"],
#     "DOT_ID_Reporting_Airline": [0],
#     "IATA_CODE_Reporting_Airline": ["example_value"],
#     "Tail_Number": ["example_value"],
#     "Flight_Number_Reporting_Airline": [0],
#     "OriginAirportID": [0],
#     "OriginAirportSeqID": [0],
#     "OriginCityMarketID": [0],
#     # "Origin": "example_value",
#     "Origin": ["LAX"],
#     "OriginCityName": ["example_value"],
#     "OriginState": ["example_value"],
#     "OriginStateFips": [0],
#     "OriginStateName": ["example_value"],
#     "OriginWac": [0],
#     "DestAirportID": [0],
#     "DestAirportSeqID": [0],
#     "DestCityMarketID": [0],
#     # "Dest": "example_value",
#     "Dest": ["JFK"],
#     "DestCityName": ["example_value"],
#     "DestState": ["example_value"],
#     "DestStateFips": [0],
#     "DestStateName": ["example_value"],
#     "DestWac": [0],
#     "CRSDepTime": [0],
#     "DepTime": [0],
#     # "DepDelay": "example_value",
#     "DepDelay": [-6],
#     # "DepDelayMinutes": "example_value",
#     "DepDelayMinutes": [0],
#     # "DepDel15": "example_value",
#     "DepDel15": [0],
#     # "DepartureDelayGroups": 0,
#     "DepartureDelayGroups": [-1],
#     # "DepTimeBlk": "example_value",
#     "DepTimeBlk": ["0800-0859"],
#     # "TaxiOut": "example_value",
#     "TaxiOut": [28],
#     "WheelsOff": [0],
#     "WheelsOn": [0],
#     "TaxiIn": ["example_value"],
#     "CRSArrTime": [0],
#     "ArrTime": [0],
#     "ArrDelay": ["example_value"],
#     "ArrDelayMinutes": ["example_value"],
#     "ArrivalDelayGroups": [0],
#     #  "ArrTimeBlk": "example_value",
#     "ArrTimeBlk":  ["1600-1659"],
#     "Cancelled": [0],
#     "CancellationCode": ["example_value"],
#     "Diverted": [0],
#     "CRSElapsedTime": ["example_value"],
#     "ActualElapsedTime": ["example_value"],
#     "AirTime": ["example_value"],
#     "Flights": 0,
#     # "Distance": "example_value",
#     "Distance": [2475],
#     # "DistanceGroup": 0,
#     "DistanceGroup": [10],
#     "CarrierDelay": [0],
#     "WeatherDelay": [0],
#     "NASDelay": [0],
#     "SecurityDelay": [0],
#     "LateAircraftDelay": [0],
#     "PREDICTED_BASELINE": ["example_value"],
#     "DIFF_ELAPSED_ACTUAL": ["example_value"],
#     "REGRESSION_ELAPSED_TIME": [0],
# }

# 7	LAX	JFK	-6	0	0	-1	0800-0859	28	1600-1659	2475	10
# comment this out before using with Power BI
# dataset = {
#     "DayOfWeek": [7],
#     "Origin": ["LAX"],
#     "Dest": ["JFK"],
#     "DepDelay": [-6],
#     "DepDelayMinutes": [0],
#     "DepDel15": [0],
#     "DepartureDelayGroups": [-1],
#     "DepTimeBlk": ["0800-0859"],
#     "TaxiOut": [28],
#     "ArrTimeBlk": ["1600-1659"],
#     "Distance": [2475],
#     "DistanceGroup": [10],
# }

# comment this out before using with Power BI
# df = pd.DataFrame(dataset)


# Fetch data from Power Query workflow

# uncomment before using with Power BI

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

# result = inference_request(
#     df["DayOfWeek"],
#     df["Origin"],
#     df["Dest"],
#     df["DepDelay"],
#     df["DepDelayMinutes"],
#     df["DepDel15"],
#     df["DepartureDelayGroups"],
#     df["DepTimeBlk"],
#     df["TaxiOut"],
#     df["ArrTimeBlk"],
#     df["Distance"],
#     df["DistanceGroup"],
# )

# print(result.content)

# SECTION 4: Data postprocessing ----
# result = pd.DataFrame(json.loads(result.content))
# df["ArrDel15_Prediction"] = result

# SECTION 5: Format output for Power BI ----
output = df

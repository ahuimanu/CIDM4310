import argparse
import os

import pandas as pd
import requests

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

AEROAPI_BASE_URL = "https://aeroapi.flightaware.com/aeroapi"
AEROAPI_KEY = os.getenv("AEROAPI_KEY")
AEROAPI = requests.Session()
AEROAPI.headers.update({"x-apikey": AEROAPI_KEY})


def configargs():
    parser = argparse.ArgumentParser()

    # stations argument
    parser.add_argument("--station", help="four-letter ICAO airport code")
    args = parser.parse_args()
    return args


def validateargs(args):
    if args.station is None:
        print("Please provide a four-letter ICAO airport code")
        exit(1)


def main():
    """Main loop."""
    args = configargs()
    validateargs(args)
    station_id = args.station

    """
    "ident",
    "ident_icao",
    "ident_iata",
    "actual_runway_off",
    "actual_runway_on",
    "fa_flight_id",
    "operator",
    "operator_icao",
    "operator_iata",
    "flight_number",
    "registration",
    "atc_ident",
    "inbound_fa_flight_id",
    "blocked",
    "diverted",
    "cancelled",
    "position_only",
    "origin_code",
    "origin_code_icao",
    "origin_code_iata",
    "origin_code_lid",
    "origin_timezone",
    "origin_name",
    "origin_city",
    "origin_airport_info_url",
    "destination_code",
    "destination_code_icao",
    "destination_code_iata",
    "destination_code_lid",
    "destination_timezone",
    "destination_name",
    "destination_city",
    "destination_airport_info_url",
    "departure_delay",
    "arrival_delay",
    "filed_ete",
    "progress_percent",
    "status",
    "aircraft_type",
    "route_distance",
    "filed_airspeed",
    "filed_altitude",
    "route",
    "baggage_claim",
    "seats_cabin_business",
    "seats_cabin_coach",
    "seats_cabin_first",
    "gate_origin",
    "gate_destination",
    "terminal_origin",
    "terminal_destination",
    "type",
    "scheduled_out",
    "estimated_out",
    "actual_out",
    "scheduled_off",
    "estimated_off",
    "actual_off",
    "scheduled_on",
    "estimated_on",
    "actual_on",
    "scheduled_in",
    "estimated_in",
    "actual_in",   
    """
    # prepare pandas dataframe to store the data
    df = pd.DataFrame(
        columns=[
            "ident",
            "ident_icao",
            "ident_iata",
            "actual_runway_off",
            "actual_runway_on",
            "fa_flight_id",
            "operator",
            "operator_icao",
            "operator_iata",
            "flight_number",
            "registration",
            "atc_ident",
            "inbound_fa_flight_id",
            "blocked",
            "diverted",
            "cancelled",
            "position_only",
            "origin_code",
            "origin_code_icao",
            "origin_code_iata",
            "origin_code_lid",
            "origin_timezone",
            "origin_name",
            "origin_city",
            "origin_airport_info_url",
            "destination_code",
            "destination_code_icao",
            "destination_code_iata",
            "destination_code_lid",
            "destination_timezone",
            "destination_name",
            "destination_city",
            "destination_airport_info_url",
            "departure_delay",
            "arrival_delay",
            "filed_ete",
            "progress_percent",
            "status",
            "aircraft_type",
            "route_distance",
            "filed_airspeed",
            "filed_altitude",
            "route",
            "baggage_claim",
            "seats_cabin_business",
            "seats_cabin_coach",
            "seats_cabin_first",
            "gate_origin",
            "gate_destination",
            "terminal_origin",
            "terminal_destination",
            "type",
            "scheduled_out",
            "estimated_out",
            "actual_out",
            "scheduled_off",
            "estimated_off",
            "actual_off",
            "scheduled_on",
            "estimated_on",
            "actual_on",
            "scheduled_in",
            "estimated_in",
            "actual_in",
        ]
    )

    # call scheduled arrivals
    api_resource = f"/airports/{station_id}/flights/scheduled_arrivals"
    print(f"Making AeroAPI request to GET {api_resource}")
    result = AEROAPI.get(f"{AEROAPI_BASE_URL}{api_resource}?type=Airline&max_pages=10")
    scheduled = result.json()

    # check for rate limit - if rate limit exceeded, exit
    # if scheduled["reason"] == "RATE_LIMIT_ERROR":
    #     print("Rate limit exceeded. Please wait and try again.")
    #     exit(1)

    for flight in scheduled["scheduled_arrivals"]:
        print(
            f"Processing... Flight {flight["ident"]} from {flight["origin"]["code"]} ({flight["origin"]["name"]}) to "
            f"{flight["destination"]["code"]} ({flight["destination"]["name"]}) operated by "
            f"{flight["operator"]} is scheduled to arrive at {flight["scheduled_in"]}"
        )

        # "ident": "string",
        # "ident_icao": "string",
        # "ident_iata": "string",
        # "actual_runway_off": "string",
        # "actual_runway_on": "string",
        # "fa_flight_id": "string",
        # "operator": "string",
        # "operator_icao": "string",
        # "operator_iata": "string",
        # "flight_number": "string",
        # "registration": "string",
        # "atc_ident": "string",
        # "inbound_fa_flight_id": "string",
        # "codeshares": [
        # "string"
        # ],
        # "codeshares_iata": [
        # "string"
        # ],
        # "blocked": false,
        # "diverted": false,
        # "cancelled": false,
        # "position_only": false,
        # "origin": {
        # "code": "string",
        # "code_icao": "string",
        # "code_iata": "string",
        # "code_lid": "string",
        # "timezone": "America/New_York",
        # "name": "LaGuardia",
        # "city": "New York",
        # "airport_info_url": ""
        # },
        # "destination": {
        # "code": "string",
        # "code_icao": "string",
        # "code_iata": "string",
        # "code_lid": "string",
        # "timezone": "America/New_York",
        # "name": "LaGuardia",
        # "city": "New York",
        # "airport_info_url": ""
        # },
        # "departure_delay": 0,
        # "arrival_delay": 0,
        # "filed_ete": 0,
        # "progress_percent": 0,
        # "status": "string",
        # "aircraft_type": "string",
        # "route_distance": 0,
        # "filed_airspeed": 0,
        # "filed_altitude": 0,
        # "route": "string",
        # "baggage_claim": "string",
        # "seats_cabin_business": 0,
        # "seats_cabin_coach": 0,
        # "seats_cabin_first": 0,
        # "gate_origin": "string",
        # "gate_destination": "string",
        # "terminal_origin": "string",
        # "terminal_destination": "string",
        # "type": "General_Aviation",
        # "scheduled_out": "2021-12-31T19:59:59Z",
        # "estimated_out": "2021-12-31T19:59:59Z",
        # "actual_out": "2021-12-31T19:59:59Z",
        # "scheduled_off": "2021-12-31T19:59:59Z",
        # "estimated_off": "2021-12-31T19:59:59Z",
        # "actual_off": "2021-12-31T19:59:59Z",
        # "scheduled_on": "2021-12-31T19:59:59Z",
        # "estimated_on": "2021-12-31T19:59:59Z",
        # "actual_on": "2021-12-31T19:59:59Z",
        # "scheduled_in": "2021-12-31T19:59:59Z",
        # "estimated_in": "2021-12-31T19:59:59Z",
        # "actual_in": "2021-12-31T19:59:59Z"                

        record = [
            flight["ident"],
            flight["ident_icao"],
            flight["ident_iata"],
            flight["actual_runway_off"],
            flight["actual_runway_on"],
            flight["fa_flight_id"],
            flight["operator"],
            flight["operator_icao"],
            flight["operator_iata"],
            flight["flight_number"],
            flight["registration"],
            flight["atc_ident"],
            flight["inbound_fa_flight_id"],
            flight["blocked"],
            flight["diverted"],
            flight["cancelled"],
            flight["position_only"],
            flight["origin"]["code"],
            flight["origin"]["code_icao"],
            flight["origin"]["code_iata"],
            flight["origin"]["code_lid"],
            flight["origin"]["timezone"],
            flight["origin"]["name"],
            flight["origin"]["city"],
            flight["origin"]["airport_info_url"],
            flight["destination"]["code"],
            flight["destination"]["code_icao"],
            flight["destination"]["code_iata"],
            flight["destination"]["code_lid"],
            flight["destination"]["timezone"],
            flight["destination"]["name"],
            flight["destination"]["city"],
            flight["destination"]["airport_info_url"],
            flight["departure_delay"],
            flight["arrival_delay"],
            flight["filed_ete"],
            flight["progress_percent"],
            flight["status"],
            flight["aircraft_type"],
            flight["route_distance"],
            flight["filed_airspeed"],
            flight["filed_altitude"],
            flight["route"],
            flight["baggage_claim"],
            flight["seats_cabin_business"],
            flight["seats_cabin_coach"],
            flight["seats_cabin_first"],
            flight["gate_origin"],
            flight["gate_destination"],
            flight["terminal_origin"],
            flight["terminal_destination"],
            flight["type"],
            flight["scheduled_out"],
            flight["estimated_out"],
            flight["actual_out"],
            flight["scheduled_off"],
            flight["estimated_off"],
            flight["actual_off"],
            flight["scheduled_on"],
            flight["estimated_on"],
            flight["actual_on"],
            flight["scheduled_in"],
            flight["estimated_in"],
            flight["actual_in"],
        ]

        df.loc[len(df)] = record

    # print dataframe
    print(df.head(5))   

    # save to csv
    df.to_csv(f"{station_id}_scheduled_arrivals.csv", index=False)


if __name__ == "__main__":
    main()

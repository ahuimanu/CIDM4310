# credit: https://github.com/akrherz/iem/blob/main/scripts/asos/iem_scraper_example2.py

"""
An example script to sequentially download data from a bunch of long term
ASOS sites, for only a few specific variables, and save the result to
individual CSV files.

You are free to use this however you want.

Author: daryl herzmann akrherz@iastate.edu
"""

import os
from datetime import date, datetime, timedelta

import argparse
import requests

def configargs():
    parser = argparse.ArgumentParser()

    # stations argument
    parser.add_argument("--station", help="IEM ASOS station to download")
    parser.add_argument("--start", help="Start date YYYYMMDD")
    parser.add_argument("--end", help="End date YYYYMMDD")
    args = parser.parse_args()
    return args

def validateargs(args):
    if args.station is None:
        print("Please provide a three-letter IEM ASOS station to download")
        exit(1)

    if args.start is None:
        print("Please provide a Start date YYYYMMDD")
        exit(1)        

    if args.end is None:
        print("Please provide an End date YYYYMMDD")
        exit(1)          


def fetch(station_id, start_date, end_date):
    """Download data we are interested in!"""
    print(f"Downloading for {station_id} between {start_date} and {end_date}")
    station_output_file = f"{station_id}.csv"
    if os.path.isfile(station_output_file):
        print(f"- Unable to over-write existing file: {station_output_file}")
        return
    print(f"+ Downloading for {station_id}")
    # end_date = date.today() + timedelta(days=2)
    uri = (
        "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"
        f"station={station_id}&data=metar&"
        f"year1={start_date.year}&month1={start_date.month}&day1={start_date.day}&"
        f"year2={end_date.year}&month2={end_date.month}&day2={end_date.day}&"
        "tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=M&trace=T&"
        "direct=yes&report_type=3"
    )
    res = requests.get(uri, timeout=300)
    with open(station_output_file, "w", encoding="utf-8") as fh:
        fh.write(res.text)


def main():
    """Main loop."""
    args = configargs()
    validateargs(args)
    station_id = args.station
    start_date = datetime.strptime(args.start, "%Y%m%d")
    end_date = datetime.strptime(args.end, "%Y%m%d")

    # raise Exception(f"station_id: {station_id}, start_date: {start_date}, end_date: {end_date}")


    # Step 1: Fetch global METAR geojson metadata
    # https://mesonet.agron.iastate.edu/sites/networks.php
    req = requests.get(
        "http://mesonet.agron.iastate.edu/geojson/network/AZOS.geojson",
        timeout=60,
    )
    geojson = req.json()
    for feature in geojson["features"]:
        if station_id == feature["id"]:
            print(f"Found {station_id} in metadata")
            props = feature["properties"]
            # We want stations with data to today (archive_end is null)
            if props["archive_end"] is None:
                print(f"Station {station_id} has no archive_end")
                fetch(station_id, start_date, end_date)

if __name__ == "__main__":
    main()
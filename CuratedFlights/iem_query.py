# credit: https://github.com/akrherz/iem/blob/main/scripts/asos/iem_scraper_example2.py

"""
An example script to sequentially download data from a bunch of long term
ASOS sites, for only a few specific variables, and save the result to
individual CSV files.

You are free to use this however you want.

Author: daryl herzmann akrherz@iastate.edu

our query parameters are as follows:
station,valid,vsby,skyl1,metar
"""

import os
from datetime import date, datetime, timedelta

import argparse
import requests

OUTPUT_FOLDER = f"IEM_Outputs/"
REQUEST_TIMEOUT = 300


def configargs():
    parser = argparse.ArgumentParser()

    # stations argument
    parser.add_argument("--infile", help="Input file of IEM ASOS stations to download")
    parser.add_argument("--station", help="IEM ASOS station to download")
    parser.add_argument("--start", help="Start date YYYYMMDD")
    parser.add_argument("--end", help="End date YYYYMMDD")
    args = parser.parse_args()
    return args


def validateargs(args):

    if args.start is None:
        print("Please provide a Start date YYYYMMDD")
        exit(1)

    if args.end is None:
        print("Please provide an End date YYYYMMDD")
        exit(1)

    # we can take an infile or a station, but not both
    if args.infile is not None:
        if args.station is not None:
            print("Cannot specify both --infile and --station")
            exit(1)

        if not os.path.exists(args.infile):
            print(f"Cannot find infile: {args.infile}")
            exit(1)

    if args.station is not None:
        if args.infile is not None:
            print("Cannot specify both --infile and --station")
            exit(1)

        if args.infile is None and args.station is None:
            print("Please provide either --infile or --station")
            exit(1)

    if args.infile is None and args.station is None:
        print("Please provide either --infile or --station")
        exit(1)


def fetch(station_id, start_date, end_date):
    """Download data we are interested in!"""
    print(f"Downloading for {station_id} between {start_date} and {end_date}")
    station_output_file = f"{OUTPUT_FOLDER}{station_id}.csv"

    # get rid of current file if it exist
    if os.path.exists(station_output_file):
        os.remove(station_output_file)

    print(f"+ Downloading for {station_id}")
    # end_date = date.today() + timedelta(days=2)

    # our query parameters are as follows:
    # station,valid,vsby,skyl1,metar

    uri = (
        "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"
        f"station={station_id}&data=vsby&data=skyl1&data=metar&"
        f"year1={start_date.year}&month1={start_date.month}&day1={start_date.day}&"
        f"year2={end_date.year}&month2={end_date.month}&day2={end_date.day}&"
        "tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=M&trace=T&"
        "direct=yes&report_type=3"
    )
    res = requests.get(uri, timeout=REQUEST_TIMEOUT)
    # then write the data
    with open(station_output_file, "w", encoding="utf-8") as fh:
        fh.write(res.text)


def station_has_valid_metar_data(geojson, station_id):
    """Check if station has valid METAR data."""
    for feature in geojson["features"]:
        if station_id == feature["id"]:
            print(f"Found {station_id} in metadata")
            props = feature["properties"]
            # We want stations with data to today (archive_end is null)
            if props["archive_end"] is None:
                print(f"Station {station_id} has no archive_end")
                return True
    return False


def fetch_for_infile(infile, start_date, end_date, geojson):
    """Download data we are interested in!"""
    with open(infile) as fh:
        for line in fh:
            line = line.replace('"', "")
            station = line.strip()
            if station_has_valid_metar_data(geojson, station):
                fetch(station, start_date, end_date)
            else:
                print(f"Station {station} has no valid METAR data")


def main():
    """Main loop."""
    args = configargs()
    validateargs(args)
    stations_infile = args.infile
    station_id = args.station
    start_date = datetime.strptime(args.start, "%Y%m%d")
    end_date = datetime.strptime(args.end, "%Y%m%d")

    # raise Exception(f"station_id: {station_id}, start_date: {start_date}, end_date: {end_date}")

    # Step 1: Fetch global METAR geojson metadata
    # https://mesonet.agron.iastate.edu/sites/networks.php
    req = requests.get(
        "http://mesonet.agron.iastate.edu/geojson/network/AZOS.geojson",
        timeout=REQUEST_TIMEOUT,
    )
    geojson = req.json()
    if stations_infile is not None:
        fetch_for_infile(stations_infile, start_date, end_date, geojson)
    elif station_has_valid_metar_data(geojson, station_id):
        fetch(station_id, start_date, end_date)
    else:
        print(f"Station {station_id} has no valid METAR data")


if __name__ == "__main__":
    main()

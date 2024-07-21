import sqlite3
import csv
import os
import pandas as pd
from metar import Metar


OUTPUT_FOLDER = f"IEM_Outputs/"

# create table for Iowa Environmental Mesonet (IEM) data
iem_statement = """
CREATE TABLE IF NOT EXISTS iem_weather (
    station TEXT,
    valid TEXT,
    tmpf REAL,
    dwpf REAL,
    relh REAL,
    drct REAL,
    sknt REAL,
    p01i REAL,
    alti REAL,
    mslp REAL,
    vsby REAL,
    gust REAL,
    skyc1 TEXT,
    skyc2 TEXT,
    skyc3 TEXT,
    skyc4 TEXT,
    skyl1 REAL,
    skyl2 REAL,
    skyl3 REAL,
    skyl4 REAL,
    wxcodes TEXT,
    ice_accretion_1hr REAL,
    ice_accretion_3hr REAL,
    ice_accretion_6hr REAL,
    peak_wind_gust REAL,
    peak_wind_drct REAL,
    peak_wind_time TEXT,
    feel REAL,
    metar TEXT
)
"""

# create table for raw metar from IEM stations

iem_metar_drop_statement = """
DROP TABLE iem_metar
"""

# our query parameters are as follows:
# station,valid,vsby,skyl1,metar

iem_metar_create_statement = """
CREATE TABLE IF NOT EXISTS iem_metar (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    station TEXT NOT NULL,
    valid_time TEXT NOT NULL,
    visibility REAL,
    ceiling REAL,
    metar TEXT NOT NULL,
    flight_rules TEXT
)
"""


def prepare_db():
    conn = sqlite3.connect("bts.db")
    cursor = conn.cursor()

    # drop if exists
    exec_result = cursor.execute(iem_metar_drop_statement)
    print(f"Table dropped: {exec_result}")
    conn.commit()

    # then create table
    exec_result = cursor.execute(iem_metar_create_statement)
    print(f"Table created: {exec_result}")
    conn.commit()

    return conn, cursor


def set_flight_rules(ceiling, visibility):
    """Set flight rules based on METAR object."""

    # https://en.wikipedia.org/wiki/Flight_categories
    # based on visibility and ceiling
    # uses python-metar: https://github.com/python-metar/python-metar/tree/main

    # VFR: Visual Flight Rules - null values from IEM are M
    if visibility >= 5 and ceiling == "M":
        return "VFR"
    # Also VFR: Visual Flight Rules
    elif visibility >= 5 and ceiling >= 3000:
        return "VFR"
    # MVFR: Marginal Visual Flight Rules
    elif visibility >= 3 and ceiling >= 1000:
        return "MVFR"
    # IFR: Instrument Flight Rules
    elif visibility >= 1 and ceiling >= 500:
        return "IFR"
    # LIFR: Low Instrument Flight Rules
    elif visibility < 1 or ceiling < 500:
        return "LIFR"
    else:
        return "UNKNOWN"


def main():
    """Main loop."""
    cursor, conn = prepare_db()

    """Download data we are interested in!"""
    infile = "stations_input.csv"
    with open(infile) as fh:
        for line in fh:
            line = line.replace('"', "")
            station = line.strip()
            if station == "ORIGIN":
                continue
            else:
                # read the csv file into a pandas dataframe to write to the database
                station_obs = pd.read_csv(f"{OUTPUT_FOLDER}{station}.csv")

                top_count = 0
                for index, row in station_obs.iterrows():
                    top_count = index

                    # determine flight rules from raw metar

                    # False argument prevents strict parsing
                    flight_rules = set_flight_rules(row["visibility"], row["ceiling"])

                    # headings for pandas: station,valid,vsby,skyl1,metar
                    cursor.execute(
                        "INSERT INTO iem_metar (station, valid_time, visibility, ceiling, metar, flight_rules) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            row["station"],
                            row["valid"],
                            row["vsby"],
                            row["skyl1"],
                            row["metar"],
                            flight_rules,
                        ),
                    )

                    result = conn.commit()
                    print(f"{top_count + 1} rows inserted into iem_stations: {result}")

    conn.close()


if __name__ == "__main__":
    main()

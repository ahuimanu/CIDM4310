import sqlite3
import csv
import pandas as pd
from metar import Metar


conn = sqlite3.connect("bts.db")

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
iem_metar_statement = """
CREATE TABLE IF NOT EXISTS iem_metar (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    station TEXT NOT NULL,
    valid_time TEXT NOT NULL,
    metar TEXT NOT NULL
)
"""

cursor = conn.cursor()

dude = cursor.execute(iem_metar_statement)
print(f"Table iem_stations created: {dude}")
conn.commit()

# read the csv file into a pandas dataframe to write to the database
station_obs = pd.read_csv("DAL.csv")

top_count = 0
for index, row in station_obs.iterrows():
    top_count = index
    cursor.execute(
        "INSERT INTO iem_metar (station, valid_time, metar) VALUES (?, ?, ?)",
        (row["station"], row["valid"], row["metar"]),
    )

result = conn.commit()
print(f"{top_count + 1} rows inserted into iem_stations: {result}")

# get all flights and convert metar string to metar object


def view_via_sql(cursor):
    cursor.execute("SELECT metar FROM iem_metar")
    metar_rows = cursor.fetchall()

    iterator = iter(metar_rows)
    for raw in iterator:
        print(raw[0])
        try:
            report = Metar.Metar(raw[0])
            print(f"{report.wind_dir} at {report.wind_speed} kts")
        except Exception as e:
            print(f"Error: {e}")

    # report = Metar.Metar(raw[0])
    # print(report.time)


# we can also read straight into a dataframe
def view_via_dataframe(conn):
    metar_rows = pd.read_sql_query("SELECT metar FROM iem_metar", conn)

    for index, row in metar_rows.iterrows():
        print(row["metar"])
        try:
            report = Metar.Metar(row["metar"])
            print(f"{report.wind_dir} at {report.wind_speed} kts")
        except Exception as e:
            print(f"Error: {e}")


# Call the method
view_via_dataframe(conn)
view_via_sql(cursor)

conn.close()

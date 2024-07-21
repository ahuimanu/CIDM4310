import sqlite3
import csv
import os
import pandas as pd
from metar import Metar
import argparse


def prepare_db():
    conn = sqlite3.connect("bts.db")
    cursor = conn.cursor()
    return conn, cursor


def view_via_sql(cursor, station_id):

    query = f"SELECT metar FROM iem_metar WHERE station = {station_id}"

    cursor.execute(query)
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
def view_via_dataframe(conn, station_id):

    query = f"SELECT metar FROM iem_metar WHERE station = {station_id}"

    metar_rows = pd.read_sql_query(query, conn)

    for index, row in metar_rows.iterrows():
        print(row["metar"])
        try:
            report = Metar.Metar(row["metar"])
            print(f"{report.wind_dir} at {report.wind_speed} kts")
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main loop."""
    cursor, conn = prepare_db()

    # These methods would allow for the review of all observations for a given station
    view_via_dataframe(conn, "AUS")
    view_via_sql(cursor, "AUS")

    conn.close()


if __name__ == "__main__":
    main()

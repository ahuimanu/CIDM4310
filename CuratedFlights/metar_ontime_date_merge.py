import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

"""
The final training set is put together in this script by merging the weather data with the on-time flight data.
"""


def prepare_db():
    conn = sqlite3.connect("bts.db")
    cursor = conn.cursor()
    return conn, cursor


def get_time_from_parts(dep_date, dep_time):
    dt = datetime.strptime(dep_date, "%m/%d/%Y %I:%M:%S %p")
    str_dep_time = str(dep_time)
    str_dep_time = str_dep_time.replace(".0", "")
    for i in range(4 - len(str_dep_time)):
        str_dep_time = "0" + str_dep_time
    combined_dep_time = datetime.strptime(str_dep_time, "%H%M").time()
    new_time = dt.combine(dt, combined_dep_time)
    return new_time


def get_timezone_for_city(conn, city_name):
    query = f"SELECT tz_name FROM city_tz WHERE city_name = '{city_name}'"
    tz_rows = pd.read_sql_query(query, conn)
    timezone_str = tz_rows.values[0][0]
    return pytz.timezone(timezone_str)


def get_weather_information(conn, station_id, dep_time):
    metar_query = (
        f"SELECT valid_time, flight_rules FROM iem_metar WHERE station = '{station_id}'"
    )

    metar_rows = pd.read_sql_query(
        metar_query,
        conn,
    )

    delta = timedelta(days=365)
    flight_rules = "INVALID"
    report_time = None

    for index, row in metar_rows.iterrows():
        nreport_time = datetime.strptime(row["valid_time"], "%Y-%m-%d %H:%M")
        nreport_time = pytz.utc.localize(nreport_time)
        ndelta = abs(dep_time - nreport_time)
        if ndelta < delta:
            delta = ndelta
            flight_rules = row["flight_rules"]
            report_time = nreport_time

    return flight_rules, report_time


# we can also read straight into a dataframe
def get_depature_time_information(conn, station_id):
    # query for times for weather
    """
    SELECT T_ONTIME_REPORTING.FL_DATE,
    T_ONTIME_REPORTING.OP_CARRIER,
    T_ONTIME_REPORTING.DEP_TIME,
    T_ONTIME_REPORTING.DEP_DELAY,
    T_ONTIME_REPORTING.DEP_DELAY_GROUP,
    T_ONTIME_REPORTING.ORIGIN,
    T_ONTIME_REPORTING.ORIGIN_CITY_NAME,
    T_ONTIME_REPORTING.DEST,
    T_ONTIME_REPORTING.DEST_CITY_NAME,
    T_ONTIME_REPORTING.DISTANCE,
    T_ONTIME_REPORTING.CARRIER_DELAY,
    T_ONTIME_REPORTING.WEATHER_DELAY,
    T_ONTIME_REPORTING.NAS_DELAY,
    T_ONTIME_REPORTING.SECURITY_DELAY,
    T_ONTIME_REPORTING.LATE_AIRCRAFT_DELAY
    FROM
    T_ONTIME_REPORTING
    WHERE
    T_ONTIME_REPORTING.DEST = 'AUS'
    AND
    T_ONTIME_REPORTING.CANCELLED = '0'
    AND
    T_ONTIME_REPORTING.DIVERTED = '0'
    """

    # query for times
    flight_times_query = (
        f"SELECT T_ONTIME_REPORTING.FL_DATE, "
        f"T_ONTIME_REPORTING.OP_CARRIER, "
        f"T_ONTIME_REPORTING.DEP_TIME, "
        f"T_ONTIME_REPORTING.DEP_DELAY, "
        f"T_ONTIME_REPORTING.DEP_DELAY_GROUP, "
        f"T_ONTIME_REPORTING.ORIGIN, "
        f"T_ONTIME_REPORTING.ORIGIN_CITY_NAME, "
        f"T_ONTIME_REPORTING.DEST, "
        f"T_ONTIME_REPORTING.DEST_CITY_NAME, "
        f"T_ONTIME_REPORTING.DISTANCE, "
        f"T_ONTIME_REPORTING.CARRIER_DELAY, "
        f"T_ONTIME_REPORTING.WEATHER_DELAY, "
        f"T_ONTIME_REPORTING.NAS_DELAY, "
        f"T_ONTIME_REPORTING.SECURITY_DELAY, "
        f"T_ONTIME_REPORTING.LATE_AIRCRAFT_DELAY "
        f"FROM T_ONTIME_REPORTING "
        f"WHERE T_ONTIME_REPORTING.DEST = '{station_id}' AND "
        f"T_ONTIME_REPORTING.CANCELLED = '0' AND "
        f"T_ONTIME_REPORTING.DIVERTED = '0'"
    )
    bts_result_set = pd.read_sql_query(flight_times_query, conn)

    flight_rules_list = []

    for index, row in bts_result_set.iterrows():
        origin = row["ORIGIN"]
        origin_city = row["ORIGIN_CITY_NAME"]
        fl_date = row["FL_DATE"]
        dep_time = row["DEP_TIME"]
        origin_timezone = get_timezone_for_city(conn, origin_city)
        new_time = get_time_from_parts(fl_date, dep_time)
        utc_time = origin_timezone.localize(new_time).astimezone(pytz.utc)
        flight_rules, report_time = get_weather_information(conn, origin, utc_time)
        flight_rules_list.append(flight_rules)
        print(f"From {origin_city}-{utc_time} was {flight_rules} at {report_time}")

    bts_result_set["FLIGHT_RULES"] = flight_rules_list
    return bts_result_set


def main():
    """Main loop."""

    conn, cursor = prepare_db()  # prepare the database
    bts_results = get_depature_time_information(conn, "AUS")  # view the data
    bts_results.to_csv("bts_results.csv", index=False)  # save the data for training


if __name__ == "__main__":
    main()

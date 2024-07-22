import pandas as pd
import sqlite3
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz


# create table for raw metar from IEM stations

iem_metar_drop_statement = """
DROP TABLE IF EXISTS city_tz
"""

# our query parameters are as follows:
# station,valid,vsby,skyl1,metar

iem_metar_create_statement = """
CREATE TABLE IF NOT EXISTS city_tz (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    station TEXT NOT NULL,
    city_name TEXT NOT NULL,
    tz_name TEXT NOT NULL
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


# we can also read straight into a dataframe
def view_via_dataframe(conn, station_id):
    pass


def get_timezone_for_city(city):
    geolocator = Nominatim(user_agent="curatedflights")
    location = geolocator.geocode(city)
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    return pytz.timezone(timezone_str)


def main():
    """Main loop."""
    conn, cursor = prepare_db()

    """
    select DISTINCT ORIGIN, ORIGIN_CITY_NAME from T_ONTIME_REPORTING where DEST = 'AUS' ORDER BY ORIGIN;
    """
    station_id = "AUS"

    query = f"select DISTINCT ORIGIN, ORIGIN_CITY_NAME from T_ONTIME_REPORTING where DEST = '{station_id}' ORDER BY ORIGIN;"
    metar_rows = pd.read_sql_query(query, conn)
    for index, row in metar_rows.iterrows():
        origin = row["ORIGIN"]
        city = row["ORIGIN_CITY_NAME"]
        timezone = get_timezone_for_city(city)
        cursor.execute(
            "INSERT INTO city_tz (station, city_name, tz_name) VALUES (?, ?, ?)",
            (origin, city, f"{timezone}"),
        )
        conn.commit()
        print(f"{index + 1} rows inserted into city_tz for {city}")

    conn.close()


if __name__ == "__main__":
    main()

# CuratedFlights

These are files and scripts to support OPTION A for the project.

This is what is here:

- Python scripts:
    - `iem_query.py` - used to grab historical weather data
    - `weather_csv_to_db.py` - takes historical weather data and saves it to a sqlite database
    - `flightaware.py` - uses the (NOT FREE) Flightaware API to grab future flights for an airport.
- Data:
    - DL_SelectFields (june to august 2023) - BTS data from these months
    - L_ CSV files - lookup tables for the BTS data
    - `bts.db` - this is too large to post, but this is the database I am working with in the example(s) above
- Links
    - Links to sources of the data
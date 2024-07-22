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

# STEPS TAKEN

1. Downloaded ontime data for June, July and August 2023 and loaded these records into a SQLite database (a dump of this data can be made vailable, but the number of records is staggering)
2. Filtered for Austin as a destination to obtain 74 unique origins (remove Hawaii)
3. Obtained historical Weather data (from IEM) for these stations
4. Classified flight categories with Python script
5. Developed new training set based on merge between the above
6. Train AutoML Regression
7. Use inferencing dataset from Flightaware for July 21 to 23 2024
import datetime as dt
import pandas as pd
import requests

yesterday = dt.date.today() - dt.timedelta(days=1)

api_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'

api_args = {
    'format': 'geojson',
    'starttime': yesterday - dt.timedelta(days=30),
    'endtime' : yesterday
}

response = requests.get(api_url, params=api_args)

earthquake_json = response.json()
print(earthquake_json['metadata'])

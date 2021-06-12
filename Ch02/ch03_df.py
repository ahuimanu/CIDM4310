import numpy as np
import pandas as pd
df = pd.read_csv('data/earthquakes.csv')

# print(df.empty)
# print(df.shape)
# print(df.head())
# print(df.tail(3))

# print(df.info())

# print(df.describe(include=object))

#uses list slicing: https://www.w3schools.com/python/python_lists_access.asp
# print(df[['mag', 'title']][100:105])

subset = df.loc[ 
    (df.place.str.contains('Alaska')) & (df.alert.notnull()), # rows
    ['alert', 'mag', 'magType', 'title', 'tsunami', 'type'] # columns
]


print(subset)
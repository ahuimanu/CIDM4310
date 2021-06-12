import numpy as np

# numpy data
data = np.genfromtxt(
    'data/example_data.csv', delimiter=';',
    names=True, dtype=None, encoding='UTF',
)

# print (data)
# print (f"the shape of the data: {data.shape}")0
print (f"the data types of the data: {data.dtype}")

for row in data:
    print(f"Place: {row}")
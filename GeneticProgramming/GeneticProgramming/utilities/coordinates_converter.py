import numpy as np


def convert_to_cartesian(lat_f, lon_f, lat_s, lon_s):

    R = 6371
    lat1 = np.radians(lat_f)
    lon1 = np.radians(lon_f)
    lat2 = np.radians(lat_s)
    lon2 = np.radians(lon_s)

    x = R * np.cos(lat2) * np.sin(lon2 - lon1)
    y = R * (np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(lon2 - lon1))
    return x, y


lat_factory, lon_factory = 20 + 34 / 60 + 8 / 3600, -(101 + 10 / 60 + 15 / 3600)

stations = [
    (20 + 34 / 60 + 37 / 3600, -(101 + 11 / 60 + 46 / 3600)),
    (20 + 33 / 60 + 57 / 3600, -(101 + 11 / 60 + 23 / 3600))
]

coordinates = [convert_to_cartesian(lat_factory, lon_factory, lat, lon) for lat, lon in stations]

print(coordinates[0])
print(coordinates[1])
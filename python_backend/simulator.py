import csv
import random
import time

with open("python_backend/data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["lat", "lon", "theft"])

    lat = 18.52
    lon = 73.85

    for i in range(50):
        lat += random.uniform(-0.002, 0.002)
        lon += random.uniform(-0.002, 0.002)

        theft = 1 if lat > 18.525 else 0

        writer.writerow([lat, lon, theft])
        print(lat, lon, theft)

        time.sleep(1)
import requests
import random
import time
import os

API_KEY = os.getenv("THINGSPEAK_API_KEY")
URL = "https://api.thingspeak.com/update"

# -----------------------
# THINGSPEAK CONFIG
# -----------------------

# -----------------------
# INITIAL VALUES
# -----------------------
lat = 18.5204
lon = 73.8567

print("🚗 IoT Vehicle Tracking with Gauge Field Started...")

while True:

    # -----------------------
    # SIMULATED MOVEMENT
    # -----------------------
    lat += random.uniform(-0.001, 0.001)
    lon += random.uniform(-0.001, 0.001)

    # -----------------------
    # THEFT LOGIC
    # -----------------------
    theft = 1 if lat > 18.525 else 0

    # -----------------------
    # GAUGE VALUE (IMPORTANT)
    # -----------------------
    if theft == 1:
        gauge = random.randint(70, 100)   # danger zone
    else:
        gauge = random.randint(10, 40)    # safe zone

    # -----------------------
    # DATA PACKET
    # -----------------------
    data = {
        "api_key": API_KEY,
        "field1": lat,
        "field2": lon,
        "field3": theft,
        "field4": gauge
    }

    # -----------------------
    # SEND TO THINGSPEAK
    # -----------------------
    response = requests.get(URL, params=data)

    print("Sent Data:", data)
    print("Response:", response.text)

    time.sleep(15)  # IMPORTANT limit
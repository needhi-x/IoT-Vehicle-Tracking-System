from flask import Flask, render_template_string
import pandas as pd
import random
import time
import threading

app = Flask(__name__)

# -------------------------------
# SIMULATE IoT DATA STREAM
# -------------------------------
data_file = "data.csv"

def generate_data():
    lat = 18.5204 + random.uniform(-0.01, 0.01)
    lon = 73.8567 + random.uniform(-0.01, 0.01)
    theft = 1 if lat > 18.525 else 0

    df = pd.DataFrame([[lat, lon, theft]],
                      columns=["lat", "lon", "theft"])

    try:
        old = pd.read_csv(data_file)
        df = pd.concat([old, df])
    except:
        pass

    df.to_csv(data_file, index=False)

# run continuously (SIMULATED IoT STREAM)
def background_simulation():
    while True:
        generate_data()
        time.sleep(2)

threading.Thread(target=background_simulation, daemon=True).start()

# -------------------------------
# DASHBOARD UI
# -------------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>IoT Vehicle Tracking Dashboard</title>
    <style>
        body { font-family: Arial; background: #0f172a; color: white; text-align:center; }
        h1 { color: #38bdf8; }

        table {
            margin:auto;
            width:80%;
            border-collapse: collapse;
            margin-top:20px;
        }

        th, td {
            padding:10px;
            border:1px solid #334155;
        }

        th { background:#1e293b; }

        .safe { color: #22c55e; font-weight:bold; }
        .danger { color: #ef4444; font-weight:bold; }

        .card {
            display:inline-block;
            padding:15px;
            margin:10px;
            background:#1e293b;
            border-radius:10px;
            width:200px;
        }
    </style>
</head>

<body>

<h1>🚗 IoT Vehicle Tracking & Theft Prevention</h1>

<div class="card">📍 Live Tracking System</div>
<div class="card">☁ Cloud Simulation Active</div>
<div class="card">🚨 Theft Detection Enabled</div>

<table>
<tr>
<th>Latitude</th>
<th>Longitude</th>
<th>Status</th>
</tr>

{% for row in data %}
<tr>
<td>{{row.lat}}</td>
<td>{{row.lon}}</td>
<td class="{{ 'danger' if row.theft==1 else 'safe' }}">
    {{ '🚨 THEFT ALERT' if row.theft==1 else '🟢 SAFE' }}
</td>
</tr>
{% endfor %}

</table>

</body>
</html>
"""

@app.route("/")
def home():
    try:
        df = pd.read_csv(data_file)
    except:
        df = pd.DataFrame(columns=["lat","lon","theft"])

    return render_template_string(HTML,
                                  data=df.tail(20).to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
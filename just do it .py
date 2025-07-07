from flask import Flask, request, jsonify, render_template, redirect
import json
import os

app = Flask(__name__)
DATA_FILE = "locations.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        locations = json.load(f)
else:
    locations = {}

@app.route("/")
def home():
    return redirect("/track")

@app.route("/track")
def track_page():
    return render_template("track.html")

@app.route("/map")
def map_page():
    return render_template("map.html")

@app.route("/update_location", methods=["POST"])
def update_location():
    data = request.get_json()
    name = data.get("name")
    lat = data.get("latitude")
    lng = data.get("longitude")
    locations[name] = {"lat": lat, "lng": lng}
    with open(DATA_FILE, "w") as f:
        json.dump(locations, f)
    return jsonify({"status": "تم تحديث موقعك بنجاح"})

@app.route("/locations")
def get_locations():
    return jsonify(locations)

@app.route("/clear")
def clear_locations():
    locations.clear()
    with open(DATA_FILE, "w") as f:
        json.dump(locations, f)
    return "تم مسح كل المواقع."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
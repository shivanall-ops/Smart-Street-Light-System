"""
Smart Street Light System - Web Dashboard Application
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import random

from database import (
    create_database,
    add_street_light,
    get_all_lights,
    get_light_by_id,
    update_light_status,
    update_ambient_light,
    get_summary_stats,
    get_energy_waste_alerts,
    get_faulty_lights,
    check_database_status
)

app = Flask(__name__)

# --------------------------
# INIT DATABASE
# --------------------------
create_database()

print("MY APP.PY IS RUNNING")


# --------------------------
# HOME DASHBOARD
# --------------------------
@app.route('/')
def dashboard():
    return render_template('dashboard.html')


# --------------------------
# SUMMARY API (FIXED - CLEAN VERSION)
# --------------------------
@app.route('/api/summary', methods=['GET'])
def summary():
    return jsonify(get_summary_stats())


# --------------------------
# GET + ADD LIGHTS
# --------------------------
@app.route('/api/lights', methods=['GET', 'POST'])
def lights():
    if request.method == 'GET':
        return jsonify(get_all_lights())

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = [
        'light_id', 'area_name', 'pole_number',
        'latitude', 'longitude', 'installation_date', 'status'
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    status = data['status'].upper()
    if status not in ['ON', 'OFF']:
        return jsonify({"error": "Status must be ON or OFF"}), 400

    try:
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        ambient_light = float(data.get('ambient_light', 0))
    except:
        return jsonify({"error": "Invalid numeric values"}), 400

    add_street_light(
        data['light_id'],
        data['area_name'],
        data['pole_number'],
        latitude,
        longitude,
        data['installation_date'],
        status,
        ambient_light
    )

    return jsonify({"success": True, "message": "Street light added"})


# --------------------------
# SINGLE LIGHT
# --------------------------
@app.route('/api/lights/<light_id>', methods=['GET'])
def get_light(light_id):
    light = get_light_by_id(light_id)
    if light:
        return jsonify(light)
    return jsonify({"error": "Light not found"}), 404


# --------------------------
# UPDATE STATUS
# --------------------------
@app.route('/api/lights/<light_id>/status', methods=['POST'])
def update_status(light_id):
    data = request.get_json()

    if not data or 'status' not in data:
        return jsonify({"error": "Status required"}), 400

    status = data['status'].upper()
    if status not in ['ON', 'OFF']:
        return jsonify({"error": "Status must be ON or OFF"}), 400

    success = update_light_status(light_id, status)

    if success:
        return jsonify({"success": True, "message": "Status updated"})
    return jsonify({"error": "Light not found"}), 404


# --------------------------
# UPDATE AMBIENT LIGHT
# --------------------------
@app.route('/api/lights/<light_id>/ambient', methods=['POST'])
def update_ambient(light_id):
    data = request.get_json()

    if not data or 'ambient_light' not in data:
        return jsonify({"error": "Ambient light required"}), 400

    try:
        ambient = float(data['ambient_light'])
    except:
        return jsonify({"error": "Invalid ambient value"}), 400

    success = update_ambient_light(light_id, ambient)

    if success:
        return jsonify({"success": True, "message": "Ambient updated"})
    return jsonify({"error": "Light not found"}), 404


# --------------------------
# ENERGY ALERTS
# --------------------------
@app.route('/api/alerts', methods=['GET'])
def alerts():
    return jsonify(get_energy_waste_alerts())


# --------------------------
# FAULTY LIGHTS
# --------------------------
@app.route('/api/faulty-lights', methods=['GET'])
def faulty_lights():
    return jsonify(get_faulty_lights())


# --------------------------
# DEBUG ROUTE
# --------------------------
@app.route('/debug')
def debug():
    return jsonify(get_faulty_lights())


# --------------------------
# SYSTEM HEALTH
# --------------------------
@app.route('/api/system-health', methods=['GET'])
def system_health():
    return jsonify({
        "database_status": "Connected" if check_database_status() else "Disconnected",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


# --------------------------
# SIMULATION
# --------------------------
@app.route('/api/simulate-ambient', methods=['POST'])
def simulate_ambient():
    lights = get_all_lights()

    for light in lights:
        ambient = random.randint(0, 500)
        update_ambient_light(light['light_id'], ambient)

    return jsonify({
        "success": True,
        "message": f"Updated {len(lights)} lights"
    })


# --------------------------
# RUN APP
# --------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
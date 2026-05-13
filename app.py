from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_connection, init_db

app = Flask(__name__)
CORS(app)

# HOME ROUTE
@app.route("/")
def home():
    return "Flask API is running!"

# INITIALIZE DATABASE
@app.route("/init")
def initialize_database():
    init_db()
    return "Database initialized!"

# =========================
# DRIVER ROUTES
# =========================

# GET ALL DRIVERS
@app.route("/drivers", methods=["GET"])
def get_drivers():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM driver")

    drivers = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(drivers)

# CREATE DRIVER
@app.route("/drivers", methods=["POST"])
def create_driver():

    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO driver (name, license_type)
        VALUES (%s, %s)
        """,
        (data["name"], data["license_type"])
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Driver added successfully!"})

# DELETE DRIVER
@app.route("/drivers/<int:id>", methods=["DELETE"])
def delete_driver(id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM driver WHERE driver_id = %s",
        (id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Driver deleted!"})

# =========================
# VEHICLE ROUTES
# =========================

# GET ALL VEHICLES
@app.route("/vehicles", methods=["GET"])
def get_vehicles():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM vehicle")

    vehicles = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(vehicles)

# CREATE VEHICLE
@app.route("/vehicles", methods=["POST"])
def create_vehicle():

    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO vehicle (license_plate, model)
        VALUES (%s, %s)
        """,
        (data["license_plate"], data["model"])
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Vehicle added successfully!"})

# RUN APP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
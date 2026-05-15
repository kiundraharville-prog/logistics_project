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

# ====================================
# DRIVER ROUTES
# ====================================

# GET DRIVERS
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

    return jsonify({"message": "Driver created"}), 201

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

    return jsonify({"message": "Driver deleted"})

# ====================================
# VEHICLE ROUTES
# ====================================

# GET VEHICLES
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

    return jsonify({"message": "Vehicle created"}), 201

# ====================================
# ROUTE ROUTES
# ====================================

# GET ROUTES
@app.route("/routes", methods=["GET"])
def get_routes():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM route")

    routes = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(routes)

# CREATE ROUTE
@app.route("/routes", methods=["POST"])
def create_route():

    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO route (service_zone, route_date)
        VALUES (%s, %s)
        """,
        (
            data["service_zone"],
            data["route_date"]
        )
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Route created"}), 201

# ====================================
# PACKAGE ROUTES
# ====================================

# GET PACKAGES
@app.route("/packages", methods=["GET"])
def get_packages():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM package")

    packages = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(packages)

# CREATE PACKAGE
@app.route("/packages", methods=["POST"])
def create_package():

    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO package
        (description, weight, route_id)
        VALUES (%s, %s, %s)
        """,
        (
            data["description"],
            data["weight"],
            data["route_id"]
        )
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Package created"}), 201

# ROUTE DETAILS VIEW
@app.route("/routes/<int:id>/packages", methods=["GET"])
def get_route_packages(id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM package
        WHERE route_id = %s
        """,
        (id,)
    )

    packages = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(packages)

# RUN APP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
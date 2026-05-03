from flask import Flask, request, jsonify
from database import get_connection, init_db

app = Flask(__name__)

@app.route("/")
def home():
    return "API is running!"

@app.route("/init")
def initialize():
    init_db()
    return "Database initialized!"

@app.route("/drivers", methods=["POST"])
def create_driver():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO driver (name, license_type, vehicle_id) VALUES (%s, %s, %s)",
        (data["name"], data["license_type"], data["vehicle_id"])
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Driver created"}), 201

@app.route("/drivers", methods=["GET"])
def get_drivers():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM driver")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS vehicle (
        vehicle_id SERIAL PRIMARY KEY,
        license_plate VARCHAR(50),
        model VARCHAR(50)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS driver (
        driver_id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        license_type VARCHAR(50),
        vehicle_id INTEGER UNIQUE,
        FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS route (
        route_id SERIAL PRIMARY KEY,
        date DATE,
        service_zone VARCHAR(100),
        driver_id INTEGER,
        FOREIGN KEY (driver_id) REFERENCES driver(driver_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS package (
        package_id SERIAL PRIMARY KEY,
        description TEXT,
        weight FLOAT,
        route_id INTEGER,
        FOREIGN KEY (route_id) REFERENCES route(route_id)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
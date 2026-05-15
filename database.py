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

    # DRIVER TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS driver (
        driver_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        license_type VARCHAR(50) NOT NULL
    );
    """)

    # VEHICLE TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vehicle (
        vehicle_id SERIAL PRIMARY KEY,
        license_plate VARCHAR(50) NOT NULL,
        model VARCHAR(100) NOT NULL
    );
    """)

    # ROUTE TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS route (
        route_id SERIAL PRIMARY KEY,
        service_zone VARCHAR(100) NOT NULL,
        route_date DATE NOT NULL
    );
    """)

    # PACKAGE TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS package (
        package_id SERIAL PRIMARY KEY,
        description VARCHAR(255) NOT NULL,
        weight DECIMAL(10,2) NOT NULL,
        route_id INTEGER NOT NULL,
        FOREIGN KEY (route_id)
        REFERENCES route(route_id)
    );
    """)

    conn.commit()

    cur.close()
    conn.close()
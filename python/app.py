from flask import Flask, jsonify
from flask_cors import CORS 
import psycopg2
import os
import time

app = Flask(__name__)
CORS(app)

# Database connection parameters
db_params = {
    "dbname": os.getenv("DB_NAME", "yourdb"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "prodigy"),
    "host": os.getenv("DB_HOST", "db"),
    "port": "5432"
}

# Function to create the "pressed" table
def create_pressed_table():
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Check if a row exists in the "pressed" table
        cur.execute("CREATE TABLE IF NOT EXISTS pressed (count INTEGER);")

        cur.execute("SELECT 1 FROM pressed LIMIT 1;")

        if cur.fetchone() is None:
            # If no row exists, insert an initial row with count = 1
            cur.execute("INSERT INTO pressed (count) VALUES (1);")
        else:
            # If a row exists, increment the count
            cur.execute("UPDATE pressed SET count = count + 1;")

        conn.commit()
    except Exception as e:
        print(str(e))
    finally:
        if conn:
            conn.close()

# Function to get the count from the "pressed" table
def get_pressed_count():
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Retrieve the count from the "pressed" table
        cur.execute("SELECT count FROM pressed;")
        count = cur.fetchone()[0] if cur.rowcount > 0 else 0
        return count
    except Exception as e:
        print(str(e))
        return 0
    finally:
        if conn:
            conn.close()

# Define a route to get the status
@app.route('/api/get-status', methods=['GET'])
def get_status():
    # Get the count from the "pressed" table
    count = get_pressed_count()

    return jsonify({'count': count})

# Define a route to increment the "pressed" table
@app.route('/api/pressed', methods=['GET'])
def increment_pressed():
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Increment the "pressed" table
        cur.execute("UPDATE pressed SET count = count + 1;")
        conn.commit()

        # Get the updated count
        count = get_pressed_count()

        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        if conn:
            conn.close()

def wait_for_db(max_retries=30, delay_seconds=1):
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**db_params)
            conn.close()
            print("Successfully connected to the database")
            return True
        except psycopg2.OperationalError as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Database not ready. Retrying in {delay_seconds} seconds...")
            time.sleep(delay_seconds)
    return False



if __name__ == '__main__':
    if not wait_for_db():
        print("Could not connect to the database. Exiting.")
        exit(1)
    try:
        test_conn = psycopg2.connect(
            "dbname='yourdb' user='postgres' host='localhost' password='prodigy'"
        )
        print("Test connection successful!")
        test_conn.close()
    except Exception as e:
        print(f"Test connection failed: {e}")

    create_pressed_table()
    app.run(host='0.0.0.0', port=5000)
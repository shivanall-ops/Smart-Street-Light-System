import sqlite3
import os

# -----------------------------
# FIX: Absolute database path
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "streetlight.db")


def create_database():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS street_light (
                light_id TEXT PRIMARY KEY,
                area_name TEXT,
                pole_number TEXT,
                latitude REAL,
                longitude REAL,
                installation_date TEXT,
                status TEXT,
                ambient_light REAL DEFAULT 0
            )
        """)

        conn.commit()
        conn.close()

        print("Database and table created successfully.")

    except sqlite3.Error as e:
        print(f"Error creating database: {e}")


def add_street_light(light_id, area_name, pole_number,
                     latitude, longitude,
                     installation_date, status,
                     ambient_light=0):

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO street_light (
                light_id,
                area_name,
                pole_number,
                latitude,
                longitude,
                installation_date,
                status,
                ambient_light
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            light_id,
            area_name,
            pole_number,
            latitude,
            longitude,
            installation_date,
            status,
            ambient_light
        ))

        conn.commit()

    except sqlite3.IntegrityError:
        print("Street Light ID already exists.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        conn.close()


def get_all_lights():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM street_light")
        records = cursor.fetchall()

        return [dict(record) for record in records]

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

    finally:
        conn.close()


def get_light_by_id(light_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM street_light WHERE light_id = ?",
            (light_id,)
        )

        record = cursor.fetchone()

        if record:
            return dict(record)

        return None

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        conn.close()


def update_light_status(light_id, status):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE street_light SET status=? WHERE light_id=?",
            (status, light_id)
        )

        conn.commit()

        return cursor.rowcount > 0

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

    finally:
        conn.close()


def update_ambient_light(light_id, ambient_light):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE street_light SET ambient_light=? WHERE light_id=?",
            (ambient_light, light_id)
        )

        conn.commit()

        return cursor.rowcount > 0

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

    finally:
        conn.close()


def get_energy_waste_alerts():
    """
    Light ON when ambient light is high.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM street_light
            WHERE status='ON'
            AND ambient_light > 200
        """)

        records = cursor.fetchall()

        return [dict(record) for record in records]

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

    finally:
        conn.close()


def get_faulty_lights():
    """
    Returns lights that are OFF during dark conditions.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM street_light
            WHERE status = 'OFF'
            AND ambient_light < 100
        """)

        records = cursor.fetchall()
        conn.close()

        return [dict(record) for record in records]

    except Exception as e:
        print(f"Error: {e}")
        return []


def get_summary_stats():
    lights = get_all_lights()

    total = len(lights)
    on = 0
    off = 0
    faulty = 0

    for l in lights:
        status = l["status"].upper().strip()
        ambient = l["ambient_light"]

        if status == "ON":
            on += 1
        elif status == "OFF":
            off += 1

        if status == "OFF" and ambient < 100:
            faulty += 1

    return {
        "total": total,
        "on": on,
        "off": off,
        "faulty": faulty
    }


def check_database_status():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT 1")

        conn.close()

        return True

    except sqlite3.Error:
        return False


if __name__ == "__main__":
    create_database()
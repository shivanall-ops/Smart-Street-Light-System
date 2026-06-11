import sqlite3

DB_NAME = "streetlight.db"


def create_database():
    """
    Creates the SQLite database and the street_lights table if they do not exist.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Create the street_lights table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS street_light (
                light_id TEXT PRIMARY KEY,
                area_name TEXT,
                pole_number TEXT,
                latitude REAL,
                longitude REAL,
                installation_date TEXT,
                status TEXT
            )
        """)

        # Save changes
        conn.commit()
        conn.close()

        print("Database and table created successfully.")

    except sqlite3.Error as e:
        print(f"Error creating database: {e}")


def add_street_light(light_id, area_name, pole_number,
                      latitude, longitude,
                      installation_date, status):
    """
    Adds a new street light record to the database.
    """

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
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            light_id,
            area_name,
            pole_number,
            latitude,
            longitude,
            installation_date,
            status
        ))

        conn.commit()
        print("Street Light Registered Successfully.")

    except sqlite3.IntegrityError:
        print("Street Light ID already exists.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    create_database()
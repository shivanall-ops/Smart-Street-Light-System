import sqlite3

# Database file name
DB_NAME = "street_lights.db"


def create_database():
    """
    Creates the SQLite database and the street_lights table if they do not exist.
    This function ensures the database schema is set up correctly for the
    smart street light energy waste detection system.
    """
    try:
        # Connect to the database (creates it if it doesn't exist)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Create the street_lights table with the specified columns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS street_lights (
                light_id TEXT PRIMARY KEY,
                area_name TEXT,
                pole_number TEXT,
                latitude REAL,
                longitude REAL,
                installation_date TEXT,
                status TEXT
            )
        """)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print(f"Database '{DB_NAME}' and table 'street_lights' created successfully.")

    except sqlite3.Error as e:
        print(f"Error creating database: {e}")


if __name__ == "__main__":
    # Call the function to create the database when the script is run directly
    create_database()

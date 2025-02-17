import sqlite3

def connect_db():
    try:
        conn = sqlite3.connect("data.db")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table():
    conn = connect_db()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    property_name TEXT,
                    location TEXT,
                    type TEXT,
                    price REAL,
                    status TEXT,
                    image_url TEXT
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()
    else:
        print("Failed to create database connection.")

def add_property(property_name, location, type, price, status, image_url=None):
    conn = connect_db()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO properties (property_name, location, type, price, status, image_url)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (property_name, location, type, price, status, image_url))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding property: {e}")
        finally:
            conn.close()

def update_property(property_id, property_name, location, type, price, status, image_url=None):
    conn = connect_db()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE properties
                SET property_name = ?, location = ?, type = ?, price = ?, status = ?, image_url = ?
                WHERE id = ?
            ''', (property_name, location, type, price, status, image_url, property_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating property: {e}")
        finally:
            conn.close()

def delete_property(property_id):
    conn = connect_db()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM properties
                WHERE id = ?
            ''', (property_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting property: {e}")
        finally:
            conn.close()

def list_properties():
    conn = connect_db()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM properties')
            properties = cursor.fetchall()
            return properties
        except sqlite3.Error as e:
            print(f"Error listing properties: {e}")
            return []
        finally:
            conn.close()

def search_properties(search_term):
    conn = connect_db()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM properties
                WHERE property_name LIKE ? OR location LIKE ?
            ''', ('%' + search_term + '%', '%' + search_term + '%'))
            properties = cursor.fetchall()
            return properties
        except sqlite3.Error as e:
            print(f"Error searching properties: {e}")
            return []
        finally:
            conn.close()

if __name__ == "__main__":
    create_table()
import sqlite3
class PropertiesModel:
    def connect_db(self):
        return sqlite3.connect(self.db_path)
    def __init__(self, db_path="data.db"):
        self.db_path = db_path


    def add_property(self, property_name, location, type, price, status):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO properties (property_name, location, type, price, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (property_name, location, type, price, status))
        conn.commit()
        conn.close()

    def update_property(self, property_id, property_name, location, type, price, status):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE properties
            SET property_name = ?, location = ?, type = ?, price = ?, status = ?
            WHERE id = ?
        ''', (property_name, location, type, price, status, property_id))
        conn.commit()
        conn.close()

    def delete_property(self, property_id):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM properties
            WHERE id = ?
        ''', (property_id,))
        conn.commit()
        conn.close()

    def list_properties(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM properties')
        properties = cursor.fetchall()
        conn.close()
        return properties

    def search_properties(self, keyword):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM properties
            WHERE property_name LIKE ? OR location LIKE ? OR type LIKE ? OR status LIKE ?
        ''', (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        results = cursor.fetchall()
        conn.close()
        return results
import sqlite3
from manage_sql import connect_db

def add_property(property_name, location, type, price, status, image, description, specs, area, bathrooms, bedrooms, direction):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO properties (property_name, location, type, price, status, image, description, specs, area, bathrooms, bedrooms, direction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (property_name, location, type, price, status, image, description, specs, area, bathrooms, bedrooms, direction))
    conn.commit()
    conn.close()

def update_property(property_id, property_name, location, type, price, status, image, description, specs, area, bathrooms, bedrooms, direction):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE properties
        SET property_name = ?, location = ?, type = ?, price = ?, status = ?, image = ?, description = ?, specs = ?, area = ?, bathrooms = ?, bedrooms = ?, direction = ?
        WHERE id = ?
    ''', (property_name, location, type, price, status, image, description, specs, area, bathrooms, bedrooms, direction, property_id))
    conn.commit()
    conn.close()

def delete_property(property_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM properties WHERE id = ?', (property_id,))
    conn.commit()
    conn.close()

def get_properties():
    conn = connect_db()
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM properties')
    rows = cursor.fetchall()
    conn.close()
    # Convert rows to list of dictionaries
    results = [dict(row) for row in rows]
    return results

def search_properties(search_type, property_type, location, street, price_range, area, bathrooms, bedrooms, direction):
    conn = connect_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM properties WHERE 1=1"
    params = []

    if search_type:
        query += " AND type = ?"
        params.append(search_type)
    if property_type:
        query += " AND property_type = ?"
        params.append(property_type)
    if location:
        query += " AND location LIKE ?"
        params.append(f'%{location}%')
    if street:
        query += " AND street LIKE ?"
        params.append(f'%{street}%')
    if price_range:
        query += " AND price_range = ?"
        params.append(price_range)
    if area:
        query += " AND area = ?"
        params.append(area)
    if bathrooms:
        query += " AND bathrooms = ?"
        params.append(bathrooms)
    if bedrooms:
        query += " AND bedrooms = ?"
        params.append(bedrooms)
    if direction:
        query += " AND direction = ?"
        params.append(direction)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results
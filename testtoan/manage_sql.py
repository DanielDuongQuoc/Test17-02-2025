import sqlite3

def connect_db():
    return sqlite3.connect('data.db')

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Tạo bảng properties
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_name TEXT NOT NULL,
        property_type TEXT NOT NULL,
        location TEXT NOT NULL,
        type TEXT NOT NULL,
        price REAL,
        status TEXT NOT NULL,
        image TEXT,
        image_url TEXT,
        description TEXT,
        specs TEXT,
        area REAL,
        bathrooms INTEGER,
        bedrooms INTEGER,
        direction TEXT
    )
    ''')
    
    
    conn.commit()
    conn.close()

# Gọi hàm create_table để tạo bảng khi khởi động ứng dụng
create_table()
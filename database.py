import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_name="stok_takip.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Veritabanı tablolarını oluştur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Kategoriler tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Ürünler tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                barcode TEXT UNIQUE,
                category_id INTEGER,
                unit_price REAL DEFAULT 0,
                current_stock INTEGER DEFAULT 0,
                min_stock INTEGER DEFAULT 5,
                description TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        # Stok hareketleri tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                movement_type TEXT CHECK(movement_type IN ('IN', 'OUT')),
                quantity INTEGER,
                unit_price REAL,
                total_price REAL,
                note TEXT,
                movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Tedarikçiler tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact_person TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Örnek veriler ekle
        self.insert_sample_data()
    
    def insert_sample_data(self):
        """İlk çalıştırmada örnek veriler ekle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Kategori var mı kontrol et
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            # Örnek kategoriler
            categories = [
                ("Elektronik", "Elektronik ürünler"),
                ("Kırtasiye", "Ofis malzemeleri"),
                ("Gıda", "Gıda ürünleri"),
                ("Temizlik", "Temizlik malzemeleri")
            ]
            
            cursor.executemany(
                "INSERT INTO categories (name, description) VALUES (?, ?)",
                categories
            )
            
            # Örnek ürünler
            products = [
                ("Laptop", "8690123456789", 1, 15000, 10, 2, "Gaming Laptop"),
                ("Wireless Mouse", "8690123456790", 1, 250, 25, 5, "Kablosuz mouse"),
                ("A4 Kağıt", "8690123456791", 2, 15, 100, 20, "500 sayfa A4"),
                ("Kalem Seti", "8690123456792", 2, 45, 50, 10, "Tükenmez kalem seti"),
                ("Çay", "8690123456793", 3, 25, 200, 50, "Bergamot çayı"),
                ("Deterjan", "8690123456794", 4, 35, 30, 10, "Çamaşır deterjanı")
            ]
            
            cursor.executemany(
                "INSERT INTO products (name, barcode, category_id, unit_price, current_stock, min_stock, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                products
            )
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, params=None):
        """SQL sorgusu çalıştır"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.rowcount
        
        conn.close()
        return result
    
    def get_all_products(self):
        """Tüm ürünleri getir (ID'ye göre sıralı)"""
        query = '''
            SELECT p.id, p.name, p.barcode, c.name as category, 
                   p.unit_price, p.current_stock, p.min_stock, p.description
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            ORDER BY p.id ASC
        '''
        return self.execute_query(query)
    
    def get_all_categories(self):
        """Tüm kategorileri getir"""
        return self.execute_query("SELECT id, name FROM categories ORDER BY name")
    
    def add_product(self, name, barcode, category_id, unit_price, min_stock, description):
        """Yeni ürün ekle"""
        query = '''
            INSERT INTO products (name, barcode, category_id, unit_price, min_stock, description)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        return self.execute_query(query, (name, barcode, category_id, unit_price, min_stock, description))
    
    def update_product_stock(self, product_id, new_stock):
        """Ürün stok miktarını güncelle"""
        query = "UPDATE products SET current_stock = ? WHERE id = ?"
        return self.execute_query(query, (new_stock, product_id))
    
    def add_stock_movement(self, product_id, movement_type, quantity, unit_price, note):
        """Stok hareketi ekle"""
        total_price = quantity * unit_price
        query = '''
            INSERT INTO stock_movements (product_id, movement_type, quantity, unit_price, total_price, note)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        return self.execute_query(query, (product_id, movement_type, quantity, unit_price, total_price, note))
    
    def get_low_stock_products(self):
        """Düşük stoklu ürünleri getir"""
        query = '''
            SELECT p.id, p.name, p.current_stock, p.min_stock, c.name as category
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.current_stock <= p.min_stock
            ORDER BY p.current_stock ASC
        '''
        return self.execute_query(query)
import sqlite3

def init_db():
    conn = sqlite3.connect("receipts.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor TEXT,
            date TEXT,
            amount REAL,
            category TEXT,
            currency TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_receipt(receipt):
    conn = sqlite3.connect("receipts.db")
    c = conn.cursor()
    c.execute("INSERT INTO receipts (vendor, date, amount, category, currency) VALUES (?, ?, ?, ?, ?)",
              (receipt.vendor, receipt.date, receipt.amount, receipt.category, receipt.currency))
    conn.commit()
    conn.close()

def fetch_all():
    conn = sqlite3.connect("receipts.db")
    return conn.execute("SELECT * FROM receipts").fetchall()

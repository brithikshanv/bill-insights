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

def add_currency_column():
    conn = sqlite3.connect("receipts.db")
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE receipts ADD COLUMN currency TEXT")
        print("Currency column added.")
    except sqlite3.OperationalError as e:
        print(f"Skipped: {e}")
    conn.commit()
    conn.close()

add_currency_column()

def insert_receipt(receipt):
    conn = sqlite3.connect("receipts.db")
    c = conn.cursor()
    c.execute("INSERT INTO receipts (vendor, date, amount, category, currency) VALUES (?, ?, ?, ?, ?)",
              (receipt.vendor, receipt.date, receipt.amount, receipt.category, receipt.currency))
    conn.commit()
    conn.close()

def fetch_all():
    conn = sqlite3.connect("receipts.db")
    c = conn.cursor()
    rows = c.execute("SELECT * FROM receipts").fetchall()
    conn.close()
    return rows




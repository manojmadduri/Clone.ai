import sqlite3

DB_FILE = "personal_data.db"

def init_db():
    """
    Create 'personal_data' table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personal_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_personal_text(title: str, content: str) -> bool:
    """
    Insert new personal data. If 'title' already exists, returns False.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO personal_data (title, content) VALUES (?, ?)",
            (title, content)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Title already exists
        return False
    finally:
        conn.close()

def get_all_personal_texts():
    """
    Fetch all rows from personal_data table.
    Returns a list of (id, title, content).
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM personal_data")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Initialize database on import
init_db()

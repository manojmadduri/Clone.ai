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

def add_personal_text(title: str, content: str) -> str:
    """
    Insert or update personal data. If 'title' exists, updates content.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO personal_data (title, content) VALUES (?, ?) ON CONFLICT(title) DO UPDATE SET content = ?",
            (title, content, content)
        )
        conn.commit()
        return "Data successfully stored."
    except sqlite3.Error as e:
        return f"Database Error: {str(e)}"
    finally:
        conn.close()

def get_all_personal_texts():
    """
    Fetch all rows from personal_data table.
    Returns a list of (id, title, content).
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM personal_data ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_most_relevant_data(query: str):
    """
    Fetch the most relevant response for a given query.
    Uses SQL LIKE matching for initial retrieval before FAISS ranking.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM personal_data WHERE title LIKE ? ORDER BY id DESC LIMIT 1", ('%' + query + '%',))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# Initialize database on import
init_db()

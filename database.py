import sqlite3
from datetime import datetime

# The name of your local database file
DB_NAME = "mindful.db"

def get_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    # This allows us to access columns by name (like row['note'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initializes the database by creating the necessary tables 
    if they don't already exist.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table for storing mood entries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            mood_value INTEGER NOT NULL,
            note TEXT,
            emoji TEXT
        )
    ''')
    
    # Table for storing chat history (Optional, for future memory)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            role TEXT,
            content TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

def save_mood(value: int, note: str):
    """
    Saves a new mood entry into the database.
    """
    # Mapping values back to emojis if you want to store them
    emojis = {1: '😢', 2: '😔', 3: '😐', 4: '🙂', 5: '😄'}
    emoji = emojis.get(value, '😐')

    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO mood_logs (timestamp, mood_value, note, emoji)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), value, note, emoji))
        
        conn.commit()
    except Exception as e:
        print(f"❌ Error saving mood: {e}")
    finally:
        conn.close()

def get_mood_history(limit: int = 10):
    """
    Retrieves the last 'n' mood entries to show on the UI.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM mood_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    
    # Convert rows to a list of dictionaries for FastAPI to return as JSON
    history = [dict(row) for row in rows]
    
    conn.close()
    return history
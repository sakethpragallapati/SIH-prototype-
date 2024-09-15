import sqlite3

DATABASE = 'users.db'

def get_db_connection():
    """Establish and return a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows you to access columns by name
    return conn

def init_db():
    """Create the `users` and `topics` tables if they don't exist and insert initial data."""
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            name TEXT NOT NULL
                        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS topics (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            content TEXT NOT NULL
                        )''')
        conn.commit()

        # Insert initial data into the `topics` table (if not already present)
        conn.execute('''INSERT OR IGNORE INTO topics (title, content) VALUES 
                        ('Executive', 'The Executive branch enforces laws and is responsible for implementing government policies and administering public services.'),
                        ('Article 52', 'Article 52 of the Indian Constitution states: "There shall be a President of India." This article establishes the office of the President as the formal Head of the State of India. The President represents the unity and integrity of the country and is the highest constitutional authority in the country.')''')
        conn.commit()

def get_topic_content(title):
    """Fetch content of a specific topic based on its title."""
    conn = get_db_connection()
    try:
        topic = conn.execute('SELECT content FROM topics WHERE title = ?', (title,)).fetchone()
        if topic:
            return topic['content']
        return 'Content not found.'
    finally:
        conn.close()

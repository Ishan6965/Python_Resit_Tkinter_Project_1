import sqlite3

DB_NAME = "movies.db"

# --- DB Connection ---
def connect():
    return sqlite3.connect(DB_NAME)

# --- Create Tables ---
def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Movies table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        seats INTEGER NOT NULL
    )
    """)

    # Bookings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(movie_id) REFERENCES movies(id)
    )
    """)

    conn.commit()
    conn.close()

# --- User Functions ---
def register_user(username, password):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# --- Movie Functions ---
def add_movie(title, seats):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO movies (title, seats) VALUES (?, ?)", (title, seats))
    conn.commit()
    conn.close()

def get_movies():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    conn.close()
    return movies

# --- Booking Functions ---
def book_seat(user_id, movie_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT seats FROM movies WHERE id=?", (movie_id,))
    seats = cursor.fetchone()

    if seats and seats[0] > 0:
        cursor.execute("UPDATE movies SET seats = seats - 1 WHERE id=?", (movie_id,))
        cursor.execute("INSERT INTO bookings (user_id, movie_id) VALUES (?, ?)", (user_id, movie_id))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False
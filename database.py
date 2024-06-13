import sqlite3
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash

def generate_random_password():
    # Generate a random password
    password_length = 12
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_characters) for _ in range(password_length))
    return password

def create_connection():
    conn = sqlite3.connect('users.db')
    create_tables(conn)  # Call create_tables function here
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            google_id TEXT UNIQUE,
            facebook_id TEXT UNIQUE
        )
    ''')
    conn.commit()

def register_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        password_hash = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user is not None:
        password_hash = user[0]
        return check_password_hash(password_hash, password)
    return False

def register_google_user(google_id, username, name):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Check if the user already exists based on the username
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            # Update the existing user with the Google ID
            cursor.execute("UPDATE users SET google_id = ? WHERE username = ?", (google_id, username))
        else:
            # Generate a random password hash
            password = generate_random_password()
            password_hash = generate_password_hash(password)
            
            # Create a new user with the Google ID, username, and password hash
            cursor.execute("INSERT INTO users (google_id, username, password_hash) VALUES (?, ?, ?)",
                           (google_id, username, password_hash))
        conn.commit()
        print(f"User registered: {google_id}, {username}")  # Logging statement
        return get_user_by_username(username)
    except sqlite3.IntegrityError as e:
        print(f"Error registering user: {str(e)}")  # Logging statement
        return None
    finally:
        conn.close()

def get_google_user(google_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        user = {
            'id': row[0],
            'username': row[1],
            'password_hash': row[2],
            'google_id': row[3]
        }
        return user
    return None

def get_facebook_user(facebook_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE facebook_id = ?", (facebook_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        user = {
            'id': row[0],
            'username': row[1],
            'password_hash': row[2],
            'google_id': row[3],
            'facebook_id': row[4]
        }
        return user
    return None

def register_facebook_user(facebook_id, username, name):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Check if the user already exists based on the username
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            # Update the existing user with the Facebook ID
            cursor.execute("UPDATE users SET facebook_id = ? WHERE username = ?", (facebook_id, username))
        else:
            # Generate a random password hash
            password = generate_random_password()
            password_hash = generate_password_hash(password)
            
            # Create a new user with the Facebook ID, username, and password hash
            cursor.execute("INSERT INTO users (facebook_id, username, password_hash) VALUES (?, ?, ?)",
                           (facebook_id, username, password_hash))
        conn.commit()
        print(f"User registered: {facebook_id}, {username}")  # Logging statement
        return get_user_by_username(username)
    except sqlite3.IntegrityError as e:
        print(f"Error registering user: {str(e)}")  # Logging statement
        return None
    finally:
        conn.close()

def get_user_by_username(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        user = {
            'id': row[0],
            'username': row[1],
            'password_hash': row[2],
            'google_id': row[3],
            'facebook_id': row[4]
        }
        return user
    return None
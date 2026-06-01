import sqlite3
from datetime import datetime
import bcrypt

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def user_exists(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT 1 FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

def get_user(username):
    if not user_exists(username):
        return None
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, password, created_at FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"username": row[0], "password": row[1], "created_at": row[2]}
    return None

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register_user(username, password):
    if user_exists(username):
        return {"error": "Username already taken"}
    
    hashed_password = hash_password(password)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)',
              (username, hashed_password, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    return {"message": "Account created!", "username": username}

def login_user(username, password):
    user = get_user(username)
    if not user:
        return {"error": "Username not found"}
    
    if not verify_password(password, user["password"]):
        return {"error": "Password incorrect"}
    
    return {"message": "Logged in!", "username": username}

init_db()
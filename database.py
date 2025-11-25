import sqlite3
DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, name TEXT, language TEXT DEFAULT 'ru')''')
    conn.commit()
    conn.close()

def get_user(uid): 
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    r = c.fetchone(); conn.close()
    return {"user_id": r[0], "name": r[1], "language": r[2]} if r else None

def create_user(uid, name): 
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, name, language) VALUES (?, ?, 'ru')", (uid, name))
    conn.commit(); conn.close()

def update_user(uid, **kw): 
    conn = sqlite3.connect(DB); c = conn.cursor()
    for k, v in kw.items():
        c.execute(f"UPDATE users SET {k}=? WHERE user_id=?", (v, uid))
    conn.commit(); conn.close()

def get_all_users():
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT user_id, name, language FROM users")
    rows = c.fetchall(); conn.close()
    return [{"user_id": r[0], "name": r[1], "language": r[2]} for r in rows]

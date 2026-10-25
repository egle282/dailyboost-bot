"""Database operations for DailyBoost bot.
Handles user profiles, subscriptions, and referral bonus tracking.
"""
import sqlite3
from typing import Optional, Dict, Any, List

DB_PATH = "users.db"
ALLOWED_UPDATE_FIELDS = {"name", "language", "premium_until"}


def get_connection() -> sqlite3.Connection:
    """Creates a database connection with row factory support."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initializes tables and applies backward-compatible column migrations."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                language TEXT DEFAULT 'ru',
                premium_until INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )

        # Migration check: if premium_until is missing in legacy schema
        cursor.execute("PRAGMA table_info(users)")
        columns = [row["name"] for row in cursor.fetchall()]
        if "premium_until" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN premium_until INTEGER DEFAULT 0")
        if "created_at" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        conn.commit()


def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a single user by Telegram user ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, name, language, premium_until, created_at FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return dict(row)


def create_user(user_id: int, name: str, language: str = "ru") -> None:
    """Registers a new user if not already present."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO users (user_id, name, language, premium_until)
               VALUES (?, ?, ?, 0)""",
            (user_id, name, language),
        )
        conn.commit()


def update_user(user_id: int, **fields: Any) -> None:
    """Safely updates specified fields for a user with whitelist validation."""
    valid_fields = {k: v for k, v in fields.items() if k in ALLOWED_UPDATE_FIELDS}
    if not valid_fields:
        return

    set_clause = ", ".join(f"{k} = ?" for k in valid_fields.keys())
    values = list(valid_fields.values()) + [user_id]

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET {set_clause} WHERE user_id = ?", values)
        conn.commit()


def get_all_users() -> List[Dict[str, Any]]:
    """Returns a list of all registered users."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, language, premium_until FROM users")
        return [dict(row) for row in cursor.fetchall()]

"""User authentication: register, login, password hashing, profile, sessions, password reset."""

import random
import secrets
from datetime import datetime, timedelta
import bcrypt
from .db import get_connection


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def register_user(email: str, name: str, password: str) -> dict | None:
    """Register a new user. Returns user dict or None if email exists."""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (email, name, password) VALUES (?, ?, ?)",
            (email.lower().strip(), name.strip(), _hash_password(password)),
        )
        conn.commit()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),)).fetchone()
        return dict(user) if user else None
    except Exception:
        return None
    finally:
        conn.close()


def authenticate_user(email: str, password: str) -> dict | None:
    """Authenticate user by email and password. Returns user dict or None."""
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),)).fetchone()
        if row and _check_password(password, row["password"]):
            return dict(row)
        return None
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> dict | None:
    conn = get_connection()
    try:
        row = conn.execute("SELECT id, email, name, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


# ── Profile updates ──────────────────────────────────────────────────────

def update_user_profile(user_id: int, name: str, email: str) -> dict | None:
    """Update name and email. Returns refreshed user dict or None on conflict."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (name.strip(), email.lower().strip(), user_id),
        )
        conn.commit()
        return get_user_by_id(user_id)
    except Exception:
        return None
    finally:
        conn.close()


def change_password(user_id: int, current: str, new: str) -> bool:
    """Change password after verifying the current one."""
    conn = get_connection()
    try:
        row = conn.execute("SELECT password FROM users WHERE id = ?", (user_id,)).fetchone()
        if not row or not _check_password(current, row["password"]):
            return False
        conn.execute("UPDATE users SET password = ? WHERE id = ?", (_hash_password(new), user_id))
        conn.commit()
        return True
    finally:
        conn.close()


# ── Persistent sessions ─────────────────────────────────────────────────

def create_session(user_id: int) -> str:
    """Create a session token for the user, returning the token string."""
    token = secrets.token_urlsafe(48)
    conn = get_connection()
    try:
        conn.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, user_id))
        conn.commit()
        return token
    finally:
        conn.close()


def validate_session(token: str) -> dict | None:
    """Look up a session token. Returns user dict or None."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT u.id, u.email, u.name, u.created_at "
            "FROM sessions s JOIN users u ON u.id = s.user_id "
            "WHERE s.token = ?", (token,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def destroy_session(token: str) -> None:
    conn = get_connection()
    try:
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()
    finally:
        conn.close()


# ── Password reset ───────────────────────────────────────────────────────

def create_reset_code(email: str) -> str | None:
    """Generate a 6-digit reset code valid for 15 minutes. Returns code or None if email not found."""
    conn = get_connection()
    try:
        row = conn.execute("SELECT id FROM users WHERE email = ?", (email.lower().strip(),)).fetchone()
        if not row:
            return None
        code = f"{random.randint(0, 999999):06d}"
        expires = (datetime.utcnow() + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            "INSERT INTO password_resets (email, code, expires_at) VALUES (?, ?, ?)",
            (email.lower().strip(), code, expires),
        )
        conn.commit()
        return code
    finally:
        conn.close()


def verify_reset_code(email: str, code: str) -> bool:
    """Check whether a reset code is valid and not expired."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id FROM password_resets "
            "WHERE email = ? AND code = ? AND used = 0 AND expires_at > datetime('now') "
            "ORDER BY created_at DESC LIMIT 1",
            (email.lower().strip(), code.strip()),
        ).fetchone()
        return row is not None
    finally:
        conn.close()


def reset_password(email: str, code: str, new_password: str) -> bool:
    """Reset password using a valid code. Marks code as used."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id FROM password_resets "
            "WHERE email = ? AND code = ? AND used = 0 AND expires_at > datetime('now') "
            "ORDER BY created_at DESC LIMIT 1",
            (email.lower().strip(), code.strip()),
        ).fetchone()
        if not row:
            return False
        conn.execute("UPDATE users SET password = ? WHERE email = ?",
                     (_hash_password(new_password), email.lower().strip()))
        conn.execute("UPDATE password_resets SET used = 1 WHERE id = ?", (row["id"],))
        conn.commit()
        return True
    finally:
        conn.close()

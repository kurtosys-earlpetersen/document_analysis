"""Database: SQLite storage for users and analysis history."""

from .db import init_db, get_connection
from .auth import (
    register_user, authenticate_user, get_user_by_id,
    update_user_profile, change_password,
    create_session, validate_session, destroy_session,
    create_reset_code, verify_reset_code, reset_password,
)
from .library import save_analysis, get_user_analyses, delete_analysis

__all__ = [
    "init_db", "get_connection",
    "register_user", "authenticate_user", "get_user_by_id",
    "update_user_profile", "change_password",
    "create_session", "validate_session", "destroy_session",
    "create_reset_code", "verify_reset_code", "reset_password",
    "save_analysis", "get_user_analyses", "delete_analysis",
]

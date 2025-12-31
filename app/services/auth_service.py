import os
import secrets

def check_admin(user: str, password: str) -> bool:
    admin_user = os.getenv("ADMIN_USER", "admin")
    admin_pass = os.getenv("ADMIN_PASS", "admin123")
    return secrets.compare_digest(user, admin_user) and secrets.compare_digest(password, admin_pass)

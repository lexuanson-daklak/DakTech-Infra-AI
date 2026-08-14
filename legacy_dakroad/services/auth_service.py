from database.repository import connect
from services.password_utils import verify_password

def authenticate(username: str, password: str):
    with connect() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND is_active=1",
            (username,),
        ).fetchone()
    if not user:
        return None
    return dict(user) if verify_password(password, user["password_hash"]) else None

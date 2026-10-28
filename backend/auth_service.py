import os
import json
import hashlib
import hmac
from datetime import datetime

USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "users.json")
AUTH_SECRET_SALT = b"JUDICIAL_FORENSIC_AUTH_SALT_2026_TAMILNADU"

def hash_password(password: str) -> str:
    """Computes salted HMAC-SHA256 of the password."""
    return hmac.new(AUTH_SECRET_SALT, password.encode("utf-8"), hashlib.sha256).hexdigest()

def get_all_users() -> list:
    """Reads users from users.json, seeds defaults if file does not exist."""
    if not os.path.exists(USERS_FILE):
        return seed_default_users()
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return seed_default_users()

def save_all_users(users: list):
    """Saves updated user list to users.json."""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def seed_default_users() -> list:
    """Seeds initial administrative, police, lawyer, and judicial accounts."""
    default_users = [
        {
            "user_id": "USR-ADMIN-01",
            "username": "admin",
            "full_name": "Chief Forensic Registrar",
            "role": "admin",
            "identifier": "SYS-ADMIN-01",
            "department": "State Forensic Directorate",
            "password_hash": hash_password("admin123"),
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "is_active": True
        },
        {
            "user_id": "USR-POL-01",
            "username": "CB-TN-4091",
            "full_name": "Inspector R. Vikram",
            "role": "police",
            "identifier": "CB-TN-4091",
            "department": "Cyber Crime Investigation Wing",
            "password_hash": hash_password("police123"),
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "is_active": True
        },
        {
            "user_id": "USR-LAW-01",
            "username": "advocate_kavin",
            "full_name": "Advocate Kavin R., B.Tech, LL.B",
            "role": "lawyer",
            "identifier": "BAR-TN-8092/2024",
            "department": "High Court Bar Association",
            "password_hash": hash_password("lawyer123"),
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "is_active": True
        },
        {
            "user_id": "USR-JUD-01",
            "username": "justice_sharma",
            "full_name": "Hon. Justice S. Sharma",
            "role": "judge",
            "identifier": "BENCH-SPE-04",
            "department": "Special Court for Cyber & Financial Crimes",
            "password_hash": hash_password("judge123"),
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "is_active": True
        }
    ]
    save_all_users(default_users)
    return default_users

def authenticate_user(username_or_id: str, password: str, expected_role: str = None) -> tuple[bool, dict, str]:
    """
    Authenticates a user by username/unique ID and password.
    Optionally validates that the user matches the expected role.
    Returns: (is_success, user_dict, message)
    """
    if not username_or_id or not password:
        return False, {}, "Please provide both credentials."

    users = get_all_users()
    pwd_hash = hash_password(password.strip())
    clean_id = username_or_id.strip()

    for u in users:
        # Match either username or unique badge/bar identifier
        if (u.get("username", "").lower() == clean_id.lower() or u.get("identifier", "").lower() == clean_id.lower()):
            if not u.get("is_active", True):
                return False, {}, "Account has been deactivated by the System Administrator."

            if expected_role and u.get("role") != expected_role:
                return False, {}, f"Access Denied: This account is registered as '{u.get('role').upper()}', not '{expected_role.upper()}'."

            if u.get("password_hash") == pwd_hash:
                return True, u, f"Welcome, {u.get('full_name')}!"
            else:
                return False, {}, "Incorrect password. Please verify your credentials."

    return False, {}, "Account not found. Registration must be performed by the System Administrator."

def register_new_user(admin_user: dict, full_name: str, username: str, role: str, identifier: str, department: str, initial_password: str) -> tuple[bool, str]:
    """
    Admin-only user creation function.
    """
    if not admin_user or admin_user.get("role") != "admin":
        return False, "Unauthorized: Only the System Administrator can register new users."

    if not full_name or not username or not role or not identifier or not initial_password:
        return False, "All user fields are required."

    if role not in ["police", "lawyer", "judge", "admin"]:
        return False, f"Invalid role '{role}'. Must be police, lawyer, judge, or admin."

    users = get_all_users()
    clean_uname = username.strip().lower()
    clean_ident = identifier.strip().lower()

    for u in users:
        if u.get("username", "").lower() == clean_uname:
            return False, f"Username '{username}' already exists. Choose a different username."
        if u.get("identifier", "").lower() == clean_ident:
            return False, f"Identifier / Badge '{identifier}' is already assigned to {u.get('full_name')}."

    new_id = f"USR-{role.upper()[:3]}-{len(users) + 1:02d}"
    new_user = {
        "user_id": new_id,
        "username": username.strip(),
        "full_name": full_name.strip(),
        "role": role,
        "identifier": identifier.strip(),
        "department": department.strip() if department else "Department of Forensics",
        "password_hash": hash_password(initial_password.strip()),
        "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "created_by": admin_user.get("full_name", "Administrator"),
        "is_active": True
    }

    users.append(new_user)
    save_all_users(users)
    return True, f"Successfully registered {role.upper()} user '{full_name}' with ID {new_id}."

def get_user_by_identifier(identifier_or_username: str) -> dict:
    """Finds a user by username, user_id, or unique identifier."""
    if not identifier_or_username:
        return {}
    clean_id = identifier_or_username.strip().lower()
    for u in get_all_users():
        if (u.get("username", "").lower() == clean_id or 
            u.get("identifier", "").lower() == clean_id or 
            u.get("user_id", "").lower() == clean_id):
            return u
    return {}

def delete_user(admin_user: dict, user_id: str) -> tuple[bool, str]:
    """Allows admin to remove a user (except the root admin)."""
    if not admin_user or admin_user.get("role") != "admin":
        return False, "Unauthorized."
    users = get_all_users()
    target = None
    for u in users:
        if u.get("user_id") == user_id:
            target = u
            break
    if not target:
        return False, "User not found."
    if target.get("username") == "admin":
        return False, "Cannot delete primary root administrator account."

    users = [u for u in users if u.get("user_id") != user_id]
    save_all_users(users)
    return True, f"User {target.get('full_name')} deleted."

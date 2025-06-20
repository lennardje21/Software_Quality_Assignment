# Logic/user_logic.py

from DataModels.user import User
from DataAccess.insert_data import InsertData
from DataAccess.get_data import GetData
from DataAccess.delete_data import DeleteData
import uuid, time, re, hashlib


class UserLogic:

    # === COMMON: System Admin & Super Admin ===

    @staticmethod
    def check_users(user: User):
        if user.is_authorized("system_admin"):
            getData = GetData()
            return getData.get_all_users()
        else:
            return False

    @staticmethod
    def create_service_engineer_object(user: User, username, password, first_name, last_name):
        if user.is_authorized("system_admin"):
            new_engineer = User(str(uuid.uuid4()), 
                                username, password, 
                                first_name, last_name, 
                                "service_engineer", 
                                time.strftime("%Y-%m-%d"))
            return new_engineer 
        else:
            return False

    @staticmethod
    def add_service_engineer(user: User, engineer: User):
        if user.is_authorized("system_admin"):
            insertData = InsertData()
            insertData.insert_user(engineer)
            return True
        else:
            return False

    @staticmethod
    def modify_service_engineer(user: User, engineer: User):
        if user.is_authorized("system_admin"):
            insertData = InsertData()
            insertData.insert_user(engineer)
            return True
        else:
            return False

    @staticmethod
    def delete_service_engineer(user: User, engineer_id: str):
        if user.is_authorized("system_admin"):
            deleteData = DeleteData()
            deleteData.delete_user(engineer_id)
            return True
        else:
            return False

    @staticmethod
    def get_service_engineer_by_id(user: User, engineer_id: str):
        if user.is_authorized("system_admin"):
            getData = GetData()
            return getData.get_user_by_id(engineer_id)
        else:
            return None

    @staticmethod
    def search_service_engineers(user: User, search_key: str = None):
        if user.is_authorized("system_admin"):
            getData = GetData()
            all_users = getData.get_user_by_partial(search_key)
            engineers = [user for user in all_users if user.role == "service_engineer"]
            return engineers
        else:
            return None

    @staticmethod
    def reset_service_engineer_password(user: User, engineer_id: int):
        if user.is_authorized("system_admin"):
            print(f"[UserLogic] Resetting service_engineer {engineer_id} password...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def update_own_profile(user: User):
        if user.is_authorized("system_admin"):
            print(f"[UserLogic] Updating own profile for user {user.id}...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def delete_own_account(user: User):
        if user.is_authorized("system_admin"):
            print(f"[UserLogic] Deleting own account for user {user.id}...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def restore_backup(user: User):
        if user.is_authorized("system_admin"):
            print("[UserLogic] Restoring backup (System Admin)...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def view_logs(user: User):
        if user.is_authorized("system_admin"):
            print("[UserLogic] Viewing logs...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def update_own_password(user: User, new_password: str):
        #NOTE Misschien try and except?
        insertData = InsertData()
        user.password_hash = new_password
        insertData.insert_user(user)
        return True
    
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def check_password_requirements(password: str):
    
        if len(password) < 12:
            return False, "Password must be at least 12 characters long."
        
        if len(password) > 30:
            return False, "Password must be no longer than 30 characters."
        
        lowercase_chars = r'[a-z]'
        uppercase_chars = r'[A-Z]'
        digit_chars = r'[0-9]'
        special_chars = r'[~!@#$%&_+=`|\\(){}\[\]:;\'<>,.?/]'
        
        allowed_chars = r'^[a-zA-Z0-9~!@#$%&_+=`|\\(){}\[\]:;\'<>,.?/]*$'
        
        if not re.match(allowed_chars, password):
            return False, "Password contains forbidden characters. Only letters, numbers, and these special characters are allowed: ~!@#$%&_+=`|\\(){}[]:;'<>,.?/"
        
        has_lowercase = bool(re.search(lowercase_chars, password))
        has_uppercase = bool(re.search(uppercase_chars, password))
        has_digit = bool(re.search(digit_chars, password))
        has_special = bool(re.search(special_chars, password))
        
        if not has_lowercase:
            return False, "Password must contain at least one lowercase letter (a-z)."
        
        if not has_uppercase:
            return False, "Password must contain at least one uppercase letter (A-Z)."
        
        if not has_digit:
            return False, "Password must contain at least one digit (0-9)."
        
        if not has_special:
            return False, "Password must contain at least one special character (~!@#$%&_+=`|\\(){}[]:;'<>,.?/)."
        
        return True, None
    
    def verify_password(user_password, entered_password: str) -> bool:
        return user_password == hashlib.sha256(entered_password.encode()).hexdigest()

    @staticmethod
    def check_username_requirements(username: str) -> tuple[bool, str]:
        # 1) Length: 8–10 chars
        if len(username) < 8:
            return False, "Username must be at least 8 characters long."
        if len(username) > 10:
            return False, "Username must be no more than 10 characters long."

        # 2) Must start with letter or underscore
        if not re.match(r'^[A-Za-z_]', username):
            return False, "Username must start with a letter or underscore (_)."

        # 3) Only allowed characters: letters, digits, underscore, apostrophe, period
        if not re.match(r"^[A-Za-z0-9_\.\\']+$", username):
            return False, (
                "Username can only contain letters, numbers, underscores (_), apostrophes ('), and periods (.)"
            )

        # 4) All good
        return True, ""


    @staticmethod
    def authenticate_user(username, password_hash):
        try:
            getData = GetData()
            # Get all users, which will be decrypted by GetData
            users = getData.get_all_users()
            
            # Compare case-insensitive with decrypted usernames
            for user in users:
                if user.username.lower() == username.lower() and user.password_hash == password_hash:
                    return user
                    
            return None
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
        
    # === SUPER ADMIN ONLY ===

    @staticmethod
    def create_system_admin_object(user: User, username, password, first_name, last_name):
        if user.is_authorized("super_admin"):
            import uuid, time
            user_id = str(uuid.uuid4())
            registration_date = time.strftime("%Y-%m-%d")
            #NOTE HASH PASSWORD
            new_admin = User(user_id, username, password, first_name, last_name, "system_admin", registration_date)
            return new_admin
        else:
            return False

    @staticmethod
    def add_system_admin(user: User, admin: User):
        if user.is_authorized("super_admin"):
            insertData = InsertData()
            insertData.insert_user(admin)
            return True
        else:
            return False

    @staticmethod
    def modify_system_admin(user: User, admin: User):
        if user.is_authorized("super_admin"):
            insertData = InsertData()
            insertData.insert_user(admin)
            return True
        else:
            return False

    @staticmethod
    def delete_system_admin(user: User, admin_id: str):
        if user.is_authorized("super_admin"):
            deleteData = DeleteData()
            deleteData.delete_user(admin_id)
            return True
        else:
            return False

    @staticmethod
    def search_system_admins(user: User, search_key: str = None):
        if user.is_authorized("super_admin"):
            getData = GetData()
            all_users = getData.get_user_by_partial(search_key)
            admins = [user for user in all_users if user.role == "system_admin"]
            return admins
        else:
            return None

    @staticmethod
    def reset_system_admin_password(user: User, admin_id: int):
        if user.is_authorized("super_admin"):
            print(f"[UserLogic] Resetting system_admin {admin_id} password...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def make_backup(user: User):
        if user.is_authorized("super_admin"):
            print("[UserLogic] Making backup...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def restore_backup_super_admin(user: User):
        if user.is_authorized("super_admin"):
            print("[UserLogic] Restoring backup (Super Admin)...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def generate_restore_code(user: User, target_admin_id: int):
        if user.is_authorized("super_admin"):
            print(f"[UserLogic] Generating restore code for System Admin {target_admin_id}...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def revoke_restore_code(user: User, target_admin_id: int):
        if user.is_authorized("super_admin"):
            print(f"[UserLogic] Revoking restore code for System Admin {target_admin_id}...")
        else:
            print("Unauthorized action.")
    
    # check
    @staticmethod
    def username_exists(user: User, username: str) -> bool:
        if user.is_authorized("super_admin"):
            getData = GetData()
            all_users = getData.get_all_users()
            return any(user.username.lower() == username.strip().lower() for user in all_users)
        else:
            return False

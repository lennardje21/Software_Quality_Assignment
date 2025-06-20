# Logic/user_logic.py

from DataModels.user import User
from DataAccess.insert_data import InsertData
from DataAccess.get_data import GetData
from DataAccess.delete_data import DeleteData
import uuid, time, re, hashlib, string, random



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
            user_id = str(uuid.uuid4())
            registration_date = time.strftime("%Y-%m-%d")
            #NOTE HASH PASSWORD
            new_engineer = User(user_id, username, password, first_name, last_name, "service_engineer", registration_date)
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
    
    @staticmethod
    def verify_password(user_password, entered_password: str) -> bool:
        return user_password == hashlib.sha256(entered_password.encode()).hexdigest()
    
    @staticmethod
    def check_username_requirements(username: str):
        if len(username) < 8:
            return False, "Username must be at least 8 characters long."
        
        if len(username) > 10:
            return False, "Username must be no longer than 10 characters."
        
        # Check if username starts with a letter or underscore
        if not re.match(r'^[a-zA-Z_]', username):
            return False, "Username must start with a letter or underscore."
        
        # Check if username contains only allowed characters
        # Using a whitelist approach with ^ and $ to ensure the entire string matches
        allowed_chars = r'^[a-zA-Z0-9_\'\.]+$'
        if not re.match(allowed_chars, username):
            return False, "Username can only contain letters, numbers, underscores, apostrophes, and periods."
        
        # All checks passed
        return True, None
    
    @staticmethod
    def generate_temporary_password(length=12):

        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        special = "~!@#$%&_-+=`|\\(){}[]:;'<>,.?/"

        # Ensure at least one of each
        password_chars = [
            random.choice(lower),
            random.choice(upper),
            random.choice(digits),
            random.choice(special),
        ]

        # Fill the rest
        all_chars = lower + upper + digits + special
        password_chars += random.choices(all_chars, k=length - 4)

        # Shuffle to avoid predictable sequences
        random.shuffle(password_chars)

        return ''.join(password_chars)

    @staticmethod
    def set_temporary_password(user: User, target_user: User, new_password: str):
        if user.is_authorized("system_admin") or user.is_authorized("super_admin"):
            target_user.password_hash = new_password
            target_user.must_change_password = 1
            insertData = InsertData()
            insertData.insert_user(target_user)
            return True
        else:
            return False
    
    @staticmethod
    def reset_password_upon_login_successful(user: User):
        if user.must_change_password == 1:
            user.must_change_password = 0
            insertData = InsertData()
            insertData.insert_user(user)
            return True
        else:
            return False


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
    def modify_system_admin(user: User, admin: User, own_account: bool = False):
        if user.is_authorized("super_admin") or own_account:
            insertData = InsertData()
            insertData.insert_user(admin)
            return True
        else:
            return False

    @staticmethod
    def delete_system_admin(user: User, admin_id: str, own_account: bool = False):
        if user.is_authorized("super_admin") or own_account:
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
    
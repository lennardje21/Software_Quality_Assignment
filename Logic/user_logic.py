# Logic/user_logic.py

from DataModels.user import User
from DataAccess.insert_data import InsertData
from DataAccess.get_data import GetData
from DataAccess.delete_data import DeleteData
import uuid, time

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
    def update_own_password(user: User):
        if user.is_authorized("service_engineer"):
            insertData = InsertData()
            return True
        else:
            return False

    # === SUPER ADMIN ONLY ===

    @staticmethod
    def add_system_admin(user: User):
        if user.is_authorized("super_admin"):
            print("[UserLogic] Adding system_admin...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def modify_system_admin(user: User, admin_id: int):
        if user.is_authorized("super_admin"):
            print(f"[UserLogic] Modifying system_admin {admin_id}...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def delete_system_admin(user: User, admin_id: int):
        if user.is_authorized("super_admin"):
            print(f"[UserLogic] Deleting system_admin {admin_id}...")
        else:
            print("Unauthorized action.")

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

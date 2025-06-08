# Logic/user_logic.py

from DataModels.user import User

class UserLogic:

    # === COMMON: System Admin & Super Admin ===

    @staticmethod
    def check_users(user: User):
        if user.is_authorized("system_admin"):
            print("[UserLogic] Checking list of users and roles...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def add_service_engineer(user: User):
        if user.is_authorized("system_admin"):
            print("[UserLogic] Adding service_engineer...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def modify_service_engineer(user: User, engineer_id: int):
        if user.is_authorized("system_admin"):
            print(f"[UserLogic] Modifying service_engineer {engineer_id}...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def delete_service_engineer(user: User, engineer_id: int):
        if user.is_authorized("system_admin"):
            print(f"[UserLogic] Deleting service_engineer {engineer_id}...")
        else:
            print("Unauthorized action.")

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
            print(f"[UserLogic] Updating own password for user {user.id}...")
        else:
            print("Unauthorized action.")

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

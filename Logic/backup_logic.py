# Logic/backup_logic.py

from DataModels.user import User

class BackupLogic:

    @staticmethod
    def make_backup(user: User):
        if user.is_authorized("super_admin"):
            print("[BackupLogic] Making backup...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def restore_backup(user: User):
        if user.is_authorized("system_admin"):
            print("[BackupLogic] Restoring backup (System Admin, with restore code)...")
        elif user.is_authorized("super_admin"):
            print("[BackupLogic] Restoring backup (Super Admin)...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def generate_restore_code(user: User, target_admin_id: int):
        if user.is_authorized("super_admin"):
            print(f"[BackupLogic] Generating restore code for System Admin {target_admin_id}...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def revoke_restore_code(user: User, target_admin_id: int):
        if user.is_authorized("super_admin"):
            print(f"[BackupLogic] Revoking restore code for System Admin {target_admin_id}...")
        else:
            print("Unauthorized action.")

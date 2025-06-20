import os, shutil, uuid
from datetime import datetime
from DataAccess.get_data import GetData
from DataAccess.insert_data import InsertData
from DataAccess.delete_data import DeleteData
from DataModels.user import User

DB_PATH = 'Database/urbanmobility.db'
BACKUP_DIR = 'Backups'

os.makedirs(BACKUP_DIR, exist_ok=True)

class BackupLogic:

    @staticmethod
    def make_backup(user: User) -> str | None:
        if not user.is_authorized("system_admin"):
            return None
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            zip_name = f"backup_{timestamp}.zip"
            zip_path = os.path.join(BACKUP_DIR, zip_name)
            shutil.make_archive(zip_path[:-4], 'zip', root_dir=os.path.dirname(DB_PATH), base_dir=os.path.basename(DB_PATH))
            return zip_name
        except Exception as e:
            print(f"Backup creation failed: {e}")
            return None


    @staticmethod
    def restore_backup(user: User, backup_file: str = None, restore_code: str = None) -> bool:
        if user.role == "super_admin" and backup_file:
            return BackupLogic._unpack_backup(backup_file)
        elif user.role == "system_admin" and restore_code:
            get = GetData()
            restore_data = get.get_restore_code_entry(restore_code, user.id)
            if not restore_data or restore_data["used"]:
                return False
            success = BackupLogic._unpack_backup(restore_data["backup_file"])
            if success:
                insert = InsertData()
                insert.mark_restore_code_as_used(restore_code)
            return success
        return False

    @staticmethod
    def generate_restore_code(user: User, target_admin_id: str, backup_file: str) -> bool:
        if not user.is_authorized("super_admin"):
            return False
        code = str(uuid.uuid4())
        insert = InsertData()
        return insert.insert_restore_code(code, target_admin_id, backup_file)

    @staticmethod
    def revoke_restore_code_by_code(user: User, code: str) -> bool:
        if not user.is_authorized("super_admin"):
            return False
        delete = DeleteData()
        return delete.revoke_restore_code_by_code(code)


    @staticmethod
    def get_backup_list() -> list[str]:
        return sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith(".zip")], reverse=True)

    @staticmethod
    def user_still_exists(user_id: str) -> bool:
        get = GetData()
        return get.get_user_by_id(user_id) is not None

    @staticmethod
    def _unpack_backup(filename: str) -> bool:
        try:
            shutil.unpack_archive(os.path.join(BACKUP_DIR, filename), os.path.dirname(DB_PATH))
            return True
        except Exception as e:
            print(f"Unpack failed: {e}")
            return False

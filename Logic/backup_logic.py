# Logic/backup_logic.py

# Logic/backup_logic.py

import os
import shutil
import sqlite3
import uuid
from datetime import datetime
from DataModels.user import User

DB_PATH = 'Database/urbanmobility.db'
BACKUP_DIR = 'Backups'

# Ensure backup folder exists
os.makedirs(BACKUP_DIR, exist_ok=True)

class BackupLogic:

    @staticmethod
    def make_backup(user: User):
        if user.is_authorized("system_admin"):
            try:
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                zip_name = f"backup_{timestamp}"
                zip_path = os.path.join(BACKUP_DIR, zip_name)

                shutil.make_archive(zip_path, 'zip', root_dir=os.path.dirname(DB_PATH), base_dir=os.path.basename(DB_PATH))
                print(f"[BackupLogic] ✅ Backup created successfully: {zip_name}.zip")
            except Exception as e:
                print(f"[BackupLogic] ❌ Failed to create backup: {e}")
        else:
            print("🚫 You are not authorized to make backups.")

        BackupLogic.pause()

    @staticmethod
    def restore_backup(user: User):
        if user.role == "super_admin":
            backups = BackupLogic._get_backup_list()
            if not backups:
                print("No backups found.")
                BackupLogic.pause()
                return

            print("\nAvailable backups:")
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup}")

            while True:
                try:
                    choice = int(input("Select a backup to restore: "))
                    if 1 <= choice <= len(backups):
                        selected = backups[choice - 1]
                        break
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Enter a number.")

            try:
                shutil.unpack_archive(os.path.join(BACKUP_DIR, selected), os.path.dirname(DB_PATH))
                print(f"✅ Backup '{selected}' restored successfully.")
                BackupLogic.pause()
            except Exception as e:
                print(f"❌ Failed to restore backup: {e}")
        elif user.role == "system_admin":
            code = input("Enter restore code: ").strip()
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT backup_file, used FROM restore_codes WHERE code = ? AND target_admin_id = ?", (code, user.id))
            row = cur.fetchone()

            if not row:
                print("❌ Invalid or unauthorized restore code.")
                conn.close()
                BackupLogic.pause()
                return

            backup_file, used = row
            if used:
                print("⚠️ This code has already been used.")
                conn.close()
                BackupLogic.pause()
                return

            try:
                backup_path = os.path.join(BACKUP_DIR, backup_file)
                shutil.unpack_archive(backup_path, os.path.dirname(DB_PATH))
                cur.execute("UPDATE restore_codes SET used = 1 WHERE code = ?", (code,))
                conn.commit()
                print(f"✅ Backup '{backup_file}' restored successfully.")
                BackupLogic.pause()
            except Exception as e:
                print(f"❌ Restore failed: {e}")
            finally:
                conn.close()
        else:
            print("🚫 Unauthorized to restore backups.")
            BackupLogic.pause()
            return

        # Check if restoring user still exists after the restore
        if not BackupLogic._user_still_exists(user.id):
            print("⚠️ Your user account no longer exists in the restored backup.")
            print("You will now be logged out for safety.")
            input("\nPress Enter to exit...")
            exit()

        BackupLogic.pause()

    @staticmethod
    def generate_restore_code(user: User, target_admin_id: str):
        if user.is_authorized("super_admin"):
            backups = BackupLogic._get_backup_list()
            if not backups:
                print("No backups available.")
                BackupLogic.pause()
                return

            print("\nAvailable backups:")
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup}")

            while True:
                try:
                    choice = int(input("Select a backup to assign: "))
                    if 1 <= choice <= len(backups):
                        selected = backups[choice - 1]
                        break
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Enter a number.")

            code = str(uuid.uuid4())
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO restore_codes (code, target_admin_id, backup_file, used)
                VALUES (?, ?, ?, 0)
            """, (code, target_admin_id, selected))
            conn.commit()
            conn.close()

            print(f"Restore code generated: {code} (for backup: {selected})")
        else:
            print("🚫 Unauthorized to generate restore codes.")

        BackupLogic.pause()

    @staticmethod
    def revoke_restore_code(user: User, target_admin_id: str):
        if user.is_authorized("super_admin"):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("DELETE FROM restore_codes WHERE target_admin_id = ? AND used = 0", (target_admin_id,))
            deleted = cur.rowcount
            conn.commit()
            conn.close()
            print(f"Revoked {deleted} restore code(s).")
            BackupLogic.pause()
        else:
            print("🚫 Unauthorized to revoke restore codes.")

        BackupLogic.pause()

    @staticmethod
    def _get_backup_list():
        return sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith(".zip")], reverse=True)

    @staticmethod
    def _user_still_exists(user_id: str) -> bool:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE UserID = ?", (user_id,))
        exists = cur.fetchone() is not None
        conn.close()
        return exists

    
    @staticmethod
    def pause():
        input("\nPress Enter to return to the menu...\n")

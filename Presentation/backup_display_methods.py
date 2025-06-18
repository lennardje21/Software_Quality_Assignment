# Presentation/backup_display_methods.py

from Logic.backup_logic import BackupLogic
from Presentation.general_shared_methods import general_shared_methods
import time


class backup_display_methods:

    @staticmethod
    def display_create_backup(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Create Backup".center(75) + "|")
        print("----------------------------------------------------------------------------")

        backup_name = BackupLogic.make_backup(user)
        if backup_name:
            print(f"\nBackup successfully created: {backup_name}")
            print("----------------------------------------------------------------------------")
            input("Press any key to continue...")
            general_shared_methods.clear_console()
        else:
            print("\nFailed to create backup.")
            time.sleep(2)

    @staticmethod
    def display_restore_backup(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Restore Backup".center(75) + "|")
        print("----------------------------------------------------------------------------")

        if user.role == "super_admin":
            backups = BackupLogic.get_backup_list()
            if not backups:
                print("No backups available.")
                input("\nPress any key to continue...")
                return

            print("\nAvailable backups:")
            for i, b in enumerate(backups, 1):
                print(f"{i}. {b}")
            try:
                choice = int(input("\nChoose a backup number: "))
                if 1 <= choice <= len(backups):
                    selected_backup = backups[choice - 1]
                    result = BackupLogic.restore_backup(user, selected_backup)
                    if result:
                        print(f"\nRestore successful from backup: {selected_backup}")
                    else:
                        print("\nRestore failed.")
                else:
                    print("Invalid number.")
            except ValueError:
                print("Invalid input.")

        elif user.role == "system_admin":
            from DataAccess.get_data import GetData
            get = GetData()
            codes = get.get_restore_codes_for_admin(user.id)

            if not codes:
                print("No active restore codes found.")
                input("\nPress any key to continue...")
                return

            print("\nAvailable Restore Codes:")
            for idx, (code, backup_file) in enumerate(codes, 1):
                print(f"{idx}. Code: {code} | Backup: {backup_file}")

            try:
                choice = int(input("\nSelect a restore code to use (0 to cancel): "))
                if choice == 0:
                    return
                if 1 <= choice <= len(codes):
                    selected_code = codes[choice - 1][0]
                    result = BackupLogic.restore_backup(user, restore_code=selected_code)
                    if result:
                        print("\nRestore successful.")
                    else:
                        print("\nRestore failed.")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input.")
        else:
            print("\nYou are not authorized to restore backups.")

    print("----------------------------------------------------------------------------")
    input("Press any key to continue...")
    general_shared_methods.clear_console()


    @staticmethod
    def display_generate_restore_code(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Generate Restore Code".center(75) + "|")
        print("----------------------------------------------------------------------------")

        from DataAccess.get_data import GetData
        get = GetData()
        admins = get.get_all_system_admins()

        if not admins:
            print("No system administrators found.")
            input("\nPress any key to continue...")
            return

        print("\nSystem Administrators:")
        for idx, (admin_id, first, last, username) in enumerate(admins, 1):
            print(f"{idx}. {first} {last} ({username})")

        try:
            choice = int(input("\nSelect a System Admin to assign code to: "))
            if not (1 <= choice <= len(admins)):
                print("Invalid choice.")
                time.sleep(1.5)
                return
            target_admin_id = admins[choice - 1][0]
        except ValueError:
            print("Invalid input.")
            time.sleep(1.5)
            return

        backups = BackupLogic.get_backup_list()
        if not backups:
            print("No backups found.")
            input("\nPress any key to return...")
            return

        print("\nAvailable Backups:")
        for idx, b in enumerate(backups, 1):
            print(f"{idx}. {b}")

        try:
            choice = int(input("\nSelect backup to assign for restore: "))
            if not (1 <= choice <= len(backups)):
                print("Invalid backup choice.")
                time.sleep(1.5)
                return
            selected_backup = backups[choice - 1]
        except ValueError:
            print("Invalid input.")
            time.sleep(1.5)
            return

        result = BackupLogic.generate_restore_code(user, target_admin_id, selected_backup)
        if result:
            print(f"\nRestore code created for admin and backup: {selected_backup}")
        else:
            print("\nFailed to generate restore code.")
        print("----------------------------------------------------------------------------")
        input("Press any key to continue...")
        general_shared_methods.clear_console()



    @staticmethod
    def display_revoke_restore_code(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Revoke Restore Code".center(75) + "|")
        print("----------------------------------------------------------------------------")

        target_admin_id = input("Enter target system admin ID: ").strip()
        result = BackupLogic.revoke_restore_code(user, target_admin_id)
        if result:
            print(f"\nRestore codes revoked for admin ID: {target_admin_id}")
        else:
            print("\nFailed to revoke restore codes.")
        print("----------------------------------------------------------------------------")
        input("Press any key to continue...")
        general_shared_methods.clear_console()

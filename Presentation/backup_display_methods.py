from Logic.backup_logic import BackupLogic
from Logic.log_logic import LogLogic
from Presentation.general_shared_methods import general_shared_methods
import time


class backup_display_methods:

    @staticmethod
    def display_create_backup(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Create Backup".center(75) + "|")
        print("----------------------------------------------------------------------------")

        print("Creating backup...")
        time.sleep(1)

        backup_name = BackupLogic.make_backup(user)

        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Backup Result".center(75) + "|")
        print("----------------------------------------------------------------------------")

        if backup_name:
            print(f"Backup successfully created: {backup_name}")
            LogLogic.add_log_to_database(
                user.username,
                "Backup Created",
                f"Backup '{backup_name}' created successfully.",
                suspicious="No"
            )
            print("----------------------------------------------------------------------------")
            input("Press any key to continue...")
        else:
            print("Failed to create backup. Please check your permissions or system status.")
            LogLogic.add_log_to_database(
                user.username,
                "Backup Failed",
                "Attempted to create a backup but failed.",
                suspicious="Yes"
            )
            time.sleep(2)

        general_shared_methods.clear_console()

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
                LogLogic.add_log_to_database(
                    user.username,
                    "Backup Restore Attempt",
                    "No backups found during restore attempt.",
                    suspicious="No"
                )
                input("\nPress any key to continue...")
                general_shared_methods.clear_console()
                return

            print("\nAvailable Backups:")
            for i, b in enumerate(backups, 1):
                print(f"{i}. {b}")

            try:
                choice = int(input("\nChoose a backup number (or 0 to cancel): "))
                if choice == 0:
                    print("Restore cancelled.")
                    LogLogic.add_log_to_database(
                        user.username,
                        "Backup Restore Cancelled",
                        "Restore operation was cancelled by super admin.",
                        suspicious="No"
                    )
                elif 1 <= choice <= len(backups):
                    selected_backup = backups[choice - 1]
                    print("Restoring from backup...")
                    time.sleep(1)
                    result = BackupLogic.restore_backup(user, selected_backup)
                    if result:
                        print(f"\nRestore successful from backup: {selected_backup}")
                        LogLogic.add_log_to_database(
                            user.username,
                            "Backup Restored",
                            f"Restored system from backup '{selected_backup}'.",
                            suspicious="No"
                        )
                    else:
                        print("\nRestore failed. Please check logs or permissions.")
                        LogLogic.add_log_to_database(
                            user.username,
                            "Backup Restore Failed",
                            f"Attempted restore from backup '{selected_backup}' failed.",
                            suspicious="Yes"
                        )
                else:
                    print("Invalid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                LogLogic.add_log_to_database(
                    user.username,
                    "Backup Restore Failed",
                    "Invalid input during backup selection.",
                    suspicious="No"
                )

        elif user.role == "system_admin":
            from DataAccess.get_data import GetData
            get = GetData()
            codes = get.get_restore_codes_for_admin(user.id)

            if not codes:
                print("No active restore codes found.")
                LogLogic.add_log_to_database(
                    user.username,
                    "Restore Code Access",
                    "No restore codes available during attempt.",
                    suspicious="No"
                )
                input("\nPress any key to continue...")
                general_shared_methods.clear_console()
                return

            print("\nAvailable Restore Codes:")
            for idx, (code, backup_file) in enumerate(codes, 1):
                print(f"{idx}. Code: {code} | Backup: {backup_file}")

            try:
                choice = int(input("\nSelect a restore code to use (0 to cancel): "))
                if choice == 0:
                    print("Restore cancelled.")
                    LogLogic.add_log_to_database(
                        user.username,
                        "Restore Code Cancelled",
                        "Restore operation via restore code was cancelled.",
                        suspicious="No"
                    )
                elif 1 <= choice <= len(codes):
                    selected_code = codes[choice - 1][0]
                    print("Restoring using selected code...")
                    time.sleep(1)
                    result = BackupLogic.restore_backup(user, restore_code=selected_code)
                    if result:
                        print("\nRestore successful.")
                        LogLogic.add_log_to_database(
                            user.username,
                            "Backup Restored via Code",
                            f"Restored backup using restore code: {selected_code}",
                            suspicious="No"
                        )
                    else:
                        print("\nRestore failed. Please verify the restore code.")
                        LogLogic.add_log_to_database(
                            user.username,
                            "Restore Failed via Code",
                            f"Failed attempt to restore using restore code: {selected_code}",
                            suspicious="Yes"
                        )
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                LogLogic.add_log_to_database(
                    user.username,
                    "Restore Code Input Error",
                    "Invalid input during restore code selection.",
                    suspicious="No"
                )
        else:
            print("\nYou are not authorized to restore backups.")
            LogLogic.add_log_to_database(
                user.username,
                "Unauthorized Restore Attempt",
                "User without permission attempted a restore operation.",
                suspicious="Yes"
            )

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
            LogLogic.add_log_to_database(
                user.username,
                "Generate Restore Code",
                "Attempted to generate restore code but no system administrators found.",
                suspicious="Yes"
            )
            input("\nPress any key to continue...")
            general_shared_methods.clear_console()
            return

        print("\nSystem Administrators:")
        for idx, (admin_id, first, last, username) in enumerate(admins, 1):
            print(f"{idx}. {first} {last} ({username})")

        try:
            choice = int(input("\nSelect a System Admin to assign code to (0 to cancel): "))
            if choice == 0:
                print("Operation cancelled.")
                LogLogic.add_log_to_database(
                    user.username,
                    "Generate Restore Code",
                    "Restore code generation cancelled by user.",
                    suspicious="No"
                )
                time.sleep(1.5)
                general_shared_methods.clear_console()
                return
            if not (1 <= choice <= len(admins)):
                print("Invalid choice.")
                LogLogic.add_log_to_database(
                    user.username,
                    "Generate Restore Code",
                    f"Invalid admin selection: {choice}",
                    suspicious="No"
                )
                time.sleep(1.5)
                return
            target_admin_id = admins[choice - 1][0]
            target_admin_username = admins[choice - 1][3]
        except ValueError:
            print("Invalid input. Please enter a number.")
            LogLogic.add_log_to_database(
                user.username,
                "Generate Restore Code",
                "Non-integer input while selecting system admin.",
                suspicious="No"
            )
            time.sleep(1.5)
            return

        backups = BackupLogic.get_backup_list()
        if not backups:
            print("No backups found.")
            LogLogic.add_log_to_database(
                user.username,
                "Generate Restore Code",
                "Attempted to generate restore code but no backups available.",
                suspicious="Yes"
            )
            input("\nPress any key to return...")
            general_shared_methods.clear_console()
            return

        print("\nAvailable Backups:")
        for idx, b in enumerate(backups, 1):
            print(f"{idx}. {b}")

        try:
            choice = int(input("\nSelect a backup to assign (0 to cancel): "))
            if choice == 0:
                print("Operation cancelled.")
                LogLogic.add_log_to_database(
                    user.username,
                    "Generate Restore Code",
                    "Restore code generation cancelled at backup selection.",
                    suspicious="No"
                )
                time.sleep(1.5)
                general_shared_methods.clear_console()
                return
            if not (1 <= choice <= len(backups)):
                print("Invalid backup choice.")
                LogLogic.add_log_to_database(
                    user.username,
                    "Generate Restore Code",
                    f"Invalid backup selection: {choice}",
                    suspicious="No"
                )
                time.sleep(1.5)
                return
            selected_backup = backups[choice - 1]
        except ValueError:
            print("Invalid input. Please enter a number.")
            LogLogic.add_log_to_database(
                user.username,
                "Generate Restore Code",
                "Non-integer input while selecting backup.",
                suspicious="No"
            )
            time.sleep(1.5)
            return

        result = BackupLogic.generate_restore_code(user, target_admin_id, selected_backup)
        if result:
            print(f"\nRestore code successfully generated for backup: {selected_backup}")
            LogLogic.add_log_to_database(
                user.username,
                "Restore Code Generated",
                f"Restore code created for admin '{target_admin_username}' for backup '{selected_backup}'.",
                suspicious="No"
            )
        else:
            print("\nFailed to generate restore code.")
            LogLogic.add_log_to_database(
                user.username,
                "Restore Code Generation Failed",
                f"Attempt to generate restore code for backup '{selected_backup}' failed.",
                suspicious="Yes"
            )

        print("----------------------------------------------------------------------------")
        general_shared_methods.input_password("Press any key to continue...")
        general_shared_methods.clear_console()


    @staticmethod
    def display_revoke_restore_code(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Revoke Restore Code".center(75) + "|")
        print("----------------------------------------------------------------------------")

        from DataAccess.get_data import GetData
        get = GetData()
        admins = get.get_all_system_admins()

        if not admins:
            print("No system administrators found.")
            input("\nPress any key to continue...")
            general_shared_methods.clear_console()
            return

        print("\nSystem Administrators:")
        for idx, (admin_id, first, last, username) in enumerate(admins, 1):
            print(f"{idx}. {first} {last} ({username})")

        try:
            choice = int(input("\nSelect an admin to revoke a restore code from (0 to cancel): "))
            if choice == 0:
                print("Operation cancelled.")
                time.sleep(1.5)
                general_shared_methods.clear_console()
                return
            if not (1 <= choice <= len(admins)):
                print("Invalid selection.")
                time.sleep(1.5)
                return

            target_admin_id = admins[choice - 1][0]
        except ValueError:
            print("Invalid input. Please enter a number.")
            time.sleep(1.5)
            return

        codes = get.get_unused_restore_codes_for_admin(target_admin_id)
        if not codes:
            print("No unused restore codes found for this admin.")
            time.sleep(2)
            return

        print("\nAvailable Restore Codes:")
        for idx, (code, backup_file) in enumerate(codes, 1):
            print(f"{idx}. Code: {code} | Backup File: {backup_file}")

        try:
            code_choice = int(input("\nSelect a restore code to revoke (0 to cancel): "))
            if code_choice == 0:
                print("Operation cancelled.")
                return
            if 1 <= code_choice <= len(codes):
                selected_code = codes[code_choice - 1][0]
                from Logic.backup_logic import BackupLogic
                success = BackupLogic.revoke_restore_code_by_code(user, selected_code)
                if success:
                    print(f"Restore code '{selected_code}' has been successfully revoked.")
                else:
                    print("Failed to revoke restore code.")
            else:
                print("Invalid code selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")

        print("----------------------------------------------------------------------------")
        input("Press any key to continue...")
        general_shared_methods.clear_console()


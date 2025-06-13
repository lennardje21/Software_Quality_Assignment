# Presentation/super_admin_screen.py

from Logic.user_logic import UserLogic
from Logic.scooter_logic import ScooterLogic
from Logic.traveller_logic import TravellerLogic
from Logic.backup_logic import BackupLogic
from Logic.log_logic import LogLogic

class SuperAdminScreen:

    @staticmethod
    def display(user):
        while True:
            print("\nSuper Administrator Menu")
            print("[1] Check Users and Roles")
            print("[2] Add System Administrator")
            print("[3] Modify System Administrator")
            print("[4] Delete System Administrator")
            print("[5] Reset System Administrator Password")
            print("[6] Add Service Engineer")
            print("[7] Modify Service Engineer")
            print("[8] Delete Service Engineer")
            print("[9] Reset Service Engineer Password")
            print("[10] Generate Restore Code")
            print("[11] Revoke Restore Code")
            print("[12] Make Backup")
            print("[13] Restore Backup")
            print("[14] View Logs")
            print("[15] Add Traveller")
            print("[16] Modify Traveller")
            print("[17] Delete Traveller")
            print("[18] Search Traveller")
            print("[19] Add Scooter")
            print("[20] Modify Scooter")
            print("[21] Delete Scooter")
            print("[22] Search Scooter")
            print("[23] Logout")

            choice = input("Choose an option: ")

            if choice == "1":
                UserLogic.check_users(user)

            elif choice == "2":
                UserLogic.add_system_admin(user)

            elif choice == "3":
                admin_id = int(input("Enter System Admin ID to modify: "))
                UserLogic.modify_system_admin(user, admin_id)

            elif choice == "4":
                admin_id = int(input("Enter System Admin ID to delete: "))
                UserLogic.delete_system_admin(user, admin_id)

            elif choice == "5":
                admin_id = int(input("Enter System Admin ID to reset password: "))
                UserLogic.reset_system_admin_password(user, admin_id)

            elif choice == "6":
                UserLogic.add_service_engineer(user)

            elif choice == "7":
                engineer_id = int(input("Enter Service Engineer ID to modify: "))
                UserLogic.modify_service_engineer(user, engineer_id)

            elif choice == "8":
                engineer_id = int(input("Enter Service Engineer ID to delete: "))
                UserLogic.delete_service_engineer(user, engineer_id)

            elif choice == "9":
                engineer_id = int(input("Enter Service Engineer ID to reset password: "))
                UserLogic.reset_service_engineer_password(user, engineer_id)

            elif choice == "10":
                target_admin_id = str(input("Enter System Admin ID to generate restore code for: "))
                BackupLogic.generate_restore_code(user, target_admin_id)

            elif choice == "11":
                target_admin_id = str(input("Enter System Admin ID to revoke restore code for: "))
                BackupLogic.revoke_restore_code(user, target_admin_id)

            elif choice == "12":
                BackupLogic.make_backup(user)

            elif choice == "13":
                BackupLogic.restore_backup(user)

            elif choice == "14":
                LogLogic.view_logs(user)

            elif choice == "15":
                TravellerLogic.add_traveller(user)

            elif choice == "16":
                traveller_id = int(input("Enter Traveller ID to modify: "))
                TravellerLogic.modify_traveller(user, traveller_id)

            elif choice == "17":
                traveller_id = int(input("Enter Traveller ID to delete: "))
                TravellerLogic.delete_traveller(user, traveller_id)

            elif choice == "18":
                TravellerLogic.search_traveller(user)

            elif choice == "19":
                ScooterLogic.add_scooter(user)

            elif choice == "20":
                scooter_id = int(input("Enter Scooter ID to modify: "))
                ScooterLogic.modify_scooter(user, scooter_id)

            elif choice == "21":
                scooter_id = int(input("Enter Scooter ID to delete: "))
                ScooterLogic.delete_scooter(user, scooter_id)

            elif choice == "22":
                ScooterLogic.search_scooter(user)

            elif choice == "23":
                print("\nLogging out...")
                break

            else:
                print("Invalid option, please try again.")

# Presentation/system_admin_screen.py

from Logic.user_logic import UserLogic
from Logic.scooter_logic import ScooterLogic
from Logic.traveller_logic import TravellerLogic
from Logic.backup_logic import BackupLogic
from Logic.log_logic import LogLogic

class SystemAdminScreen:

    @staticmethod
    def display(user):
        while True:
            print("\nSystem Administrator Menu")
            print("[1] Check Users and Roles")
            print("[2] Add Service Engineer")
            print("[3] Modify Service Engineer")
            print("[4] Delete Service Engineer")
            print("[5] Reset Service Engineer Password")
            print("[6] Update My Profile")
            print("[7] Delete My Account")
            print("[8] Make Backup (not allowed!)")
            print("[9] Restore Backup (with restore code)")
            print("[10] View Logs")
            print("[11] Add Traveller")
            print("[12] Modify Traveller")
            print("[13] Delete Traveller")
            print("[14] Search Traveller")
            print("[15] Add Scooter")
            print("[16] Modify Scooter")
            print("[17] Delete Scooter")
            print("[18] Search Scooter")
            print("[19] Change My Password")
            print("[20] Logout")

            choice = input("Choose an option: ")

            if choice == "1":
                UserLogic.check_users(user)

            elif choice == "2":
                UserLogic.add_service_engineer(user)

            elif choice == "3":
                engineer_id = int(input("Enter Service Engineer ID to modify: "))
                UserLogic.modify_service_engineer(user, engineer_id)

            elif choice == "4":
                engineer_id = int(input("Enter Service Engineer ID to delete: "))
                UserLogic.delete_service_engineer(user, engineer_id)

            elif choice == "5":
                engineer_id = int(input("Enter Service Engineer ID to reset password: "))
                UserLogic.reset_service_engineer_password(user, engineer_id)

            elif choice == "6":
                UserLogic.update_own_profile(user)

            elif choice == "7":
                UserLogic.delete_own_account(user)

            elif choice == "9":
                BackupLogic.restore_backup(user)

            elif choice == "10":
                LogLogic.view_logs(user)

            elif choice == "11":
                TravellerLogic.add_traveller(user)

            elif choice == "12":
                traveller_id = int(input("Enter Traveller ID to modify: "))
                TravellerLogic.modify_traveller(user, traveller_id)

            elif choice == "13":
                traveller_id = int(input("Enter Traveller ID to delete: "))
                TravellerLogic.delete_traveller(user, traveller_id)

            elif choice == "14":
                TravellerLogic.search_traveller(user)

            elif choice == "15":
                ScooterLogic.add_scooter(user)

            elif choice == "16":
                scooter_id = int(input("Enter Scooter ID to modify: "))
                ScooterLogic.modify_scooter(user, scooter_id)

            elif choice == "17":
                scooter_id = int(input("Enter Scooter ID to delete: "))
                ScooterLogic.delete_scooter(user, scooter_id)

            elif choice == "18":
                ScooterLogic.search_scooter(user)

            elif choice == "19":
                UserLogic.update_own_password(user)

            elif choice == "20":
                print("\nLogging out...")
                break

            else:
                print("Invalid option, please try again.")

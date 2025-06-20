# Presentation/system_admin_screen.py

from Logic.user_logic import UserLogic
from Logic.traveller_logic import TravellerLogic
from Logic.backup_logic import BackupLogic
from Logic.log_logic import LogLogic
from Presentation.scooter_display_methods import scooter_display_methods
from Presentation.general_shared_methods import general_shared_methods
from Presentation.user_display_methods import user_display_methods
from Presentation.engineer_display_methods import engineer_display_methods
from Presentation.admin_display_methods import admin_display_methods
import time

class SystemAdminScreen:

    @staticmethod
    def display(user):
        if user.must_change_password == 1:
            if user_display_methods.display_necessary_password_update(user) is False:
                return
        while True:
            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "System Admin Menu".center(75) + "|")
            print("----------------------------------------------------------------------------")
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
            print("----------------------------------------------------------------------------")

            #NOTE INPUT FIELD
            choice = input("Choose an option: ")

            exit = False

            if choice == "1":
                exit = user_display_methods.display_check_users(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1)

            elif choice == "2":
                exit = engineer_display_methods.display_add_engineer(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "3":
                exit = engineer_display_methods.display_update_engineer(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "4":
                exit = engineer_display_methods.display_delete_engineer(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "5":
                exit = user_display_methods.display_reset_password(user, "Service Engineer")
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "6":
                exit = admin_display_methods.display_update_own_profile(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)
                
            elif choice == "7":
                exit = admin_display_methods.display_delete_my_account(user)
                general_shared_methods.clear_console()
                if exit:
                    print("Your account has been deleted. Logging out...")
                    time.sleep(1)
                    general_shared_methods.clear_console()
                    break

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
                exit = scooter_display_methods.display_add_scooter(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "16":
                exit = scooter_display_methods.display_update_scooter(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "17":
                exit = scooter_display_methods.display_delete_scooter(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "18":
                while True:
                    exit = scooter_display_methods.search_scooter_display(user)
                    if exit is True:
                        break
                    elif exit is None:
                        input("\nPress Enter to continue...")
                        break
                
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "19":
                user_display_methods.display_update_password(user)

            elif choice == "20":
                general_shared_methods.clear_console()
                print("\nLogging out...")
                time.sleep(1)
                break

            else:
                print("Invalid option, please try again.")

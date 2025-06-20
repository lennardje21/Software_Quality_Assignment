# Presentation/super_admin_screen.py

from Presentation.admin_display_methods import admin_display_methods
from Presentation.traveller_display_methods import traveller_display_methods
from Presentation.backup_display_methods import backup_display_methods
from Presentation.log_display_methods import log_display_methods
from Presentation.scooter_display_methods import scooter_display_methods
from Presentation.general_shared_methods import general_shared_methods
from Presentation.user_display_methods import user_display_methods
from Presentation.engineer_display_methods import engineer_display_methods
import time

class SuperAdminScreen:

    @staticmethod
    def display(user):
        while True:
            general_shared_methods.clear_console()

            print("----------------------------------------------------------------------------")
            print("|" + "Super Admin Menu".center(75) + "|")
            print("----------------------------------------------------------------------------")
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
                exit = admin_display_methods.display_add_admin(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "3":
                exit = admin_display_methods.display_update_admin(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "4":
                exit = admin_display_methods.display_delete_admin(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "5":
                exit = user_display_methods.display_reset_password(user, "System Admin")
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "6":
                exit = engineer_display_methods.display_add_engineer(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "7":
                exit = engineer_display_methods.display_update_engineer(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "8":
                exit = engineer_display_methods.display_delete_engineer(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "9":
                exit = user_display_methods.display_reset_password(user, "Service Engineer")
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "10":
                exit = backup_display_methods.display_generate_restore_code(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "11":
                exit = backup_display_methods.display_revoke_restore_code(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "12":
                exit = backup_display_methods.display_create_backup(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "13":
                exit = backup_display_methods.display_restore_backup(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "14":
                exit = log_display_methods.display_all_logs(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "15":
                exit = traveller_display_methods.display_add_traveller(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "16":
                exit = traveller_display_methods.display_update_traveller(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "17":
                exit = traveller_display_methods.display_delete_traveller(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "18":
                exit = traveller_display_methods.display_search_traveller(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "19":
                exit = scooter_display_methods.display_add_scooter(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "20":
                exit = scooter_display_methods.display_update_scooter(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "21":
                exit = scooter_display_methods.display_delete_scooter(user)
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "22":
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

            elif choice == "23":
                general_shared_methods.clear_console()
                print("Logging out...")
                time.sleep(1)
                break

            else:
                print("Invalid option, please try again.")
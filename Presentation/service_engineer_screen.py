# Presentation/service_engineer_screen.py

from Presentation.general_shared_methods import general_shared_methods
from Presentation.scooter_display_methods import scooter_display_methods
from Presentation.user_display_methods import user_display_methods
import time

class ServiceEngineerScreen:

    @staticmethod
    def home_display(user):
        if user.must_change_password == 1:
            if user_display_methods.display_necessary_password_update(user) is False:
                return

        while True:
            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "Service Engineer Menu".center(75) + "|")
            print("----------------------------------------------------------------------------")

            print("[1] Update Scooter Information")
            print("[2] Search for Scooter")
            print("[3] Change My Password")
            print("[4] Logout")
            print("----------------------------------------------------------------------------")

            #NOTE INPUT FIELD
            choice = input("Choose an option: ")
            general_shared_methods.clear_console()
            exit = False

            if choice == "1":
                exit = scooter_display_methods.display_update_scooter(user)
                general_shared_methods.clear_console()
                if exit is True:
                    break
                elif exit is False:
                    print("Returning to menu...")
                    time.sleep(1.5)

            elif choice == "2":
                while True:
                    exit = scooter_display_methods.search_scooter_display(user)
                    if exit is True:
                        break
                    elif exit is None:
                        #NOTE INPUT FIELD
                        print("----------------------------------------------------------------------------")
                        general_shared_methods.input_password("Press any key to continue...")
                        break
                
                general_shared_methods.clear_console()
                print("Returning to menu...")
                time.sleep(1.5)

            elif choice == "3":
                user_display_methods.display_update_password(user)
            elif choice == "4":
                general_shared_methods.clear_console()
                print("\nLogging out...")
                time.sleep(1)
                break

            else:
                print("Invalid option, please try again.")


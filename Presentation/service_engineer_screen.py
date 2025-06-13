# Presentation/service_engineer_screen.py

from Logic.user_logic import UserLogic
from Logic.scooter_logic import ScooterLogic
from Presentation.shared_methods import shared_methods
import time

class ServiceEngineerScreen:

    @staticmethod
    def home_display(user):
        from main import clear_console
        clear_console()
        while True:
            print("----------------------------------------------------------------------------")
            print("|" + "Service Engineer Menu".center(75) + "|")
            print("----------------------------------------------------------------------------")

            print("[1] Update Scooter Information")
            print("[2] Search for Scooter")
            print("[3] Change My Password")
            print("[4] Logout")
            #NOTE INPUT FIELD
            choice = input("Choose an option: ")
            clear_console()

            if choice == "1":
                shared_methods.display_update_scooter(user)
                clear_console()

            elif choice == "2":
                exit = False
                while exit is False:
                    exit = shared_methods.search_scooter_display(user)
                    if exit is None:
                        #NOTE INPUT FIELD
                        print("----------------------------------------------------------------------------")
                        input("Press any key to continue...")
                        clear_console()
                        print("Returning to menu...")
                        time.sleep(1.5)
                        clear_console()
                        break
                    if exit:
                        break

            elif choice == "3":
                UserLogic.update_own_password(user)

            elif choice == "4":
                print("\nLogging out...")
                break

            else:
                print("Invalid option, please try again.")

    @staticmethod
    def partial_update_scooter_display(scooter, user):
        from main import clear_console
        editable_fields = [
            "state_of_charge",
            "target_soc_min",
            "target_soc_max",
            "latitude",
            "longitude",
            "out_of_service_status",
            "mileage",
            "last_maintenance",
        ]
        clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Update Scooter Data".center(75) + "|")
        print("----------------------------------------------------------------------------")

        shared_methods.display_scooter(scooter, user=user)
        print("----------------------------------------------------------------------------")
        print("Enter the field you want to update (e.g., state_of_charge, etc.) or type 'exit' to cancel. Use '_' for spaces.")
        #NOTE INPUT FIELD
        field = input("Field to update: ").strip().lower()
        clear_console()

        if field == 'exit':
            print("Exiting update...")
            time.sleep(1)
            clear_console()
            return True
        elif field not in editable_fields:
            print(f"Invalid field '{field}'. Please choose from one of the editable fields.")
            time.sleep(3)
            clear_console()
            return False
        else:
            print(shared_methods.display_singular_scooter_field(scooter, field))            
            print("----------------------------------------------------------------------------")
            #NOTE INPUT FIELD
            new_value = input(f"Enter new value for {field}: ").strip()
            clear_console()
            shared_methods.update_scooter(scooter, field, new_value, user)
            time.sleep(2)
            clear_console()



        
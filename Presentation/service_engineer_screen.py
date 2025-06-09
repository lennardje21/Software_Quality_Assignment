# Presentation/service_engineer_screen.py

from Logic.user_logic import UserLogic
from Logic.scooter_logic import ScooterLogic

class ServiceEngineerScreen:

    @staticmethod
    def display(user):
        while True:
            print("\nService Engineer Menu")
            print("[1] Update Scooter Information (partial)")
            print("[2] Search for Scooter")
            print("[3] Change My Password")
            print("[4] Logout")
            
            choice = input("Choose an option: ")

            if choice == "1":
                scooter_id = int(input("Enter scooter ID to update: "))
                ScooterLogic.update_scooter_partial(user, scooter_id)

            elif choice == "2":
                ScooterLogic.search_scooter(user)

            elif choice == "3":
                UserLogic.update_own_password(user)

            elif choice == "4":
                print("\nLogging out...")
                break

            else:
                print("Invalid option, please try again.")

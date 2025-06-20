# Presentation/home_screen.py

import sqlite3, time
from Presentation.service_engineer_screen import ServiceEngineerScreen
from Presentation.system_admin_screen import SystemAdminScreen
from Presentation.super_admin_screen import SuperAdminScreen
from Logic.user_logic import UserLogic
from Presentation.general_shared_methods import general_shared_methods

db_path = 'Database/urbanmobility.db'

class HomeScreen:
    MAX_ATTEMPTS = 3

    @staticmethod
    def display():
        user = ""
        failed_attempts = 0
        while True:
            general_shared_methods.clear_console()
            print("\nWelcome to the Urban Mobility Backend System!\n")

            if failed_attempts >= HomeScreen.MAX_ATTEMPTS:
                print("\nToo many failed login attempts. The program is locked.")
                break

            print("\nMain Menu:")
            print("[1] Login")
            print("[2] Exit program")
            userInput = input("Choose an option: ")

            if userInput == "1":
                username = input("\nUsername: ")
                password = general_shared_methods.input_password("Password: ")
                password_hash = UserLogic.hash_password(password)
                
                # This now returns the whole user object or None
                user = UserLogic.authenticate_user(username, password_hash)
                
                if user:
                    print(f"\nLogin successful! Logged in as {user.role}.\n")
                    failed_attempts = 0  # reset attempts
                    
                    if user.role == "service_engineer":
                        ServiceEngineerScreen.home_display(user)
                    elif user.role == "system_admin":
                        SystemAdminScreen.display(user)
                    elif user.role == "super_admin":
                        SuperAdminScreen.display(user)
                    else:
                        print(f"Unknown role: {user.role}")
                else:
                    failed_attempts += 1
                    remaining = HomeScreen.MAX_ATTEMPTS - failed_attempts
                    print(f"\nInvalid username or password. Attempts left: {remaining}")
                    time.sleep(1.5)

            elif userInput == "2":
                print("\nGoodbye!")
                time.sleep(0.5)
                break

            else:
                print("\nInvalid option, please try again.")
                time.sleep(0.5)
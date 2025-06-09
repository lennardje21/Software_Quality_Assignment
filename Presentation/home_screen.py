# Presentation/home_screen.py

import sqlite3
from DataModels.user import User
from Presentation.service_engineer_screen import ServiceEngineerScreen
from Presentation.system_admin_screen import SystemAdminScreen
from Presentation.super_admin_screen import SuperAdminScreen

db_path = 'Database/urbanmobility.db'

class HomeScreen:
    MAX_ATTEMPTS = 3

    @staticmethod
    def display():
        failed_attempts = 0
        print("\nWelcome to the Urban Mobility Backend System!\n")
        
        while True:
            if failed_attempts >= HomeScreen.MAX_ATTEMPTS:
                print("\nToo many failed login attempts. The program is locked.")
                break

            print("\nMain Menu:")
            print("[1] Login")
            print("[2] Exit program")
            userInput = input("Choose an option: ")

            if userInput == "1":
                username = input("\nUsername: ")
                password = input("Password: ")

                role = HomeScreen.simulate_authentication(username, password)

                if role:
                    print(f"\nLogin successful! Logged in as {role}.\n")
                    failed_attempts = 0  # reset attempts

                    # Build User object
                    user = HomeScreen.get_user_object(username, password)

                    if user:
                        if user.role == "service_engineer":
                            ServiceEngineerScreen.display(user)

                        elif user.role == "system_admin":
                            SystemAdminScreen.display(user)

                        elif user.role == "super_admin":
                            SuperAdminScreen.display(user)

                        else:
                            print(f"Unknown role: {user.role}")
                    else:
                        print("Error loading user data.")

                else:
                    failed_attempts += 1
                    remaining = HomeScreen.MAX_ATTEMPTS - failed_attempts
                    print(f"\nInvalid username or password. Attempts left: {remaining}")

            elif userInput == "2":
                print("\nGoodbye!")
                break

            else:
                print("\nInvalid option, please try again.")

    # temp function
    @staticmethod
    def simulate_authentication(username, password):

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        query = '''
        SELECT Role
        FROM users
        WHERE UserName = ? AND PasswordHash = ?
        '''

        cursor.execute(query, (username, password))
        row = cursor.fetchone()

        connection.close()

        if row:
            # row[0] is Role
            return row[0]
        else:
            return None

    # temp function
    @staticmethod
    def get_user_object(username, password):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        query = '''
        SELECT UserID, UserName, PasswordHash, FirstName, LastName, Role, RegistrationDate
        FROM users
        WHERE UserName = ? AND PasswordHash = ?
        '''

        cursor.execute(query, (username, password))
        row = cursor.fetchone()

        connection.close()

        if row:
            return User(
                id=row[0],
                username=row[1],
                password_hash=row[2],
                first_name=row[3],
                last_name=row[4],
                role=row[5],
                registration_date=row[6]
            )
        else:
            return None

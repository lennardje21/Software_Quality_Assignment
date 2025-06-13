# Presentation/home_screen.py

from DataModels.user import User
from Presentation.service_engineer_screen import ServiceEngineerScreen
from Presentation.system_admin_screen import SystemAdminScreen
from Presentation.super_admin_screen import SuperAdminScreen

from Logic.login_logic import LoginLogic
from Logic.log_logic import LogLogic

class HomeScreen:
    MAX_ATTEMPTS = 3

    @staticmethod
    def display():
        failed_attempts = 0
        failed_usernames = []

        print("\n=== Welcome to the Urban Mobility Backend System ===\n")

        while True:
            if failed_attempts >= HomeScreen.MAX_ATTEMPTS:
                print("\n❌ Too many failed login attempts. The system is now locked.")
                attempted_users = ", ".join(set(failed_usernames)) or "unknown"
                LogLogic.add_log_to_database(
                    username=attempted_users,
                    action="Login Lockout",
                    description=f"Too many failed login attempts. Usernames tried: {attempted_users}",
                    suspicious="Yes"
                )
                break

            print("\nMain Menu:")
            print("[1] Login")
            print("[2] Exit program")
            userInput = input("Choose an option: ").strip()

            if userInput == "1":
                username = input("\nUsername: ").strip()
                password = input("Password: ").strip()

                user = LoginLogic.get_user_object(username, password)

                if user:
                    print(f"\n✅ Login successful! Logged in as {user.role}.\n")
                    failed_attempts = 0
                    failed_usernames.clear()

                    LogLogic.add_log_to_database(
                        username=user.username,
                        action="Login",
                        description="Successful login",
                        suspicious="No"
                    )

                    if user.role == "service_engineer":
                        ServiceEngineerScreen.display(user)
                    elif user.role == "system_admin":
                        SystemAdminScreen.display(user)
                    elif user.role == "super_admin":
                        SuperAdminScreen.display(user)
                    else:
                        print(f"⚠️ Unknown role: {user.role}")

                else:
                    failed_attempts += 1
                    failed_usernames.append(username)
                    remaining = HomeScreen.MAX_ATTEMPTS - failed_attempts
                    print(f"\n❌ Invalid username or password. Attempts left: {remaining}")

            elif userInput == "2":
                print("\n👋 Goodbye!")
                break
            else:
                print("\nInvalid option. Please try again.")

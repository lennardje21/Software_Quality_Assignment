import time
from Helpers.input_prompters import InputPrompters
from Helpers.input_validators import InputValidators
from Logic.log_logic import LogLogic
from Logic.user_logic import UserLogic
from Presentation.general_shared_methods import general_shared_methods
from Presentation.user_display_methods import user_display_methods
from Logic.log_logic import LogLogic

class engineer_display_methods:
    

    @staticmethod
    def search_engineer_display(user, update_call=False):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Search for Service Engineer".center(75) + "|")
        print("----------------------------------------------------------------------------")

        search_key = InputPrompters.prompt_until_valid(
            "Enter a search key (id, name, username, etc.) or type 'exit' to go back: ",
            InputValidators.validate_search_key,
            "Invalid search input. Only letters, numbers, and basic symbols allowed."
        )

        if search_key is None:
            print("Exiting search...")
            time.sleep(1)
            general_shared_methods.clear_console()
            return True

        general_shared_methods.clear_console()
        engineers = UserLogic.search_service_engineers(user, search_key)

        if engineers and len(engineers) > 0:
            LogLogic.add_log_to_database(
                username=user.username,
                action="Search Engineer",
                description=f"User searched for engineers using key '{search_key}' and found {len(engineers)} result(s).",
                suspicious="No"
            )
            print(f"\nFound {len(engineers)} service engineer(s) matching '{general_shared_methods.highlight(search_key, search_key)}':")
            time.sleep(1)
            for count, engineer in enumerate(engineers, 1):
                print("----------------------------------------------------------------------------")
                print("|" + f"Search Result #{count}".center(75) + "|")
                print("----------------------------------------------------------------------------")
                user_display_methods.display_user(engineer, search_key)
            if update_call:
                return engineers
            input("Press any key to continue...")
            general_shared_methods.clear_console()
            return None
        else:
            LogLogic.add_log_to_database(
                username=user.username,
                action="Search Engineer",
                description=f"User searched for engineers using key '{search_key}' but found no matches.",
                suspicious="No"
            )
            print("No service engineers found matching the search criteria.")
            time.sleep(2)
            general_shared_methods.clear_console()
            return False

    @staticmethod
    def display_add_engineer(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Add New Service Engineer".center(75) + "|")
        print("----------------------------------------------------------------------------")
        
        engineer = engineer_display_methods.prompt_for_new_engineer_details(user)
        
        if engineer is None:
            LogLogic.add_log_to_database(
                username=user.username,
                action="Add Service Engineer",
                description="Engineer creation was cancelled by user.",
                suspicious="No"
            )
            print("Engineer creation cancelled.")
            time.sleep(1.5)
            return False

        if UserLogic.add_service_engineer(user, engineer):
            LogLogic.add_log_to_database(
                username=user.username,
                action="Add Service Engineer",
                description=f"Service engineer '{engineer.username}' was added successfully.",
                suspicious="No"
            )
            general_shared_methods.clear_console()
            print(f"Service Engineer {engineer.username} has been added successfully.")
            time.sleep(2)
            general_shared_methods.clear_console()
            user_display_methods.display_user(engineer, search_key='', current_user=user)
            print("----------------------------------------------------------------------------")
            general_shared_methods.input_password("Press any key to continue...")
            general_shared_methods.clear_console()
            return True
        else:
            LogLogic.add_log_to_database(
                username=user.username,
                action="Add Service Engineer",
                description=f"Attempt to add service engineer '{engineer.username}' failed.",
                suspicious="Yes" 
            )
            print("Failed to add service engineer. Please check your permissions.")
            time.sleep(2)
            return False

    @staticmethod
    def prompt_for_new_engineer_details(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Enter Service Engineer Details".center(75) + "|")
        print("----------------------------------------------------------------------------")

        while True:
            username = InputPrompters.prompt_until_valid(
                "Enter Username: ",
                InputValidators.validate_username,
                "Invalid username. Use 3-30 characters, only letters, numbers, and underscores."
            )
            if username is None:
                return None

            if UserLogic.username_exists(user, username):
                print("This username is already taken. Please choose another one.")
                time.sleep(1.5)
                continue
            break

        while True:
            password = general_shared_methods.input_password("Enter Password: ").strip()
            if password.lower() == 'exit':
                return None

            passed, error_msg = UserLogic.check_password_requirements(password)
            if not passed:
                print(error_msg)
                time.sleep(2)
                continue

            password_confirm = general_shared_methods.input_password("Confirm Password: ").strip()
            if password != password_confirm:
                print("Passwords do not match. Please try again.")
                time.sleep(2)
                continue

            password = UserLogic.hash_password(password)
            break

        first_name = InputPrompters.prompt_until_valid(
            "Enter First Name: ",
            InputValidators.validate_name,
            "Invalid first name. Use alphabetic characters only."
        )
        if first_name is None:
            return None

        last_name = InputPrompters.prompt_until_valid(
            "Enter Last Name: ",
            InputValidators.validate_name,
            "Invalid last name. Use alphabetic characters only."
        )
        if last_name is None:
            return None

        engineer = UserLogic.create_service_engineer_object(
            user,
            username,
            password,
            first_name,
            last_name
        )
        return engineer
    
    @staticmethod
    def display_update_engineer(user):
        while True:
            engineers = engineer_display_methods.search_engineer_display(user, update_call=True)
            if engineers is True:
                return
            if engineers is False:
                continue
            
            print("----------------------------------------------------------------------------")
            engineer_id = input("Enter service engineer ID to update (or type 'exit' to cancel): ").strip()
            general_shared_methods.clear_console()

            if engineer_id.lower() == 'exit':
                print("Exiting update...")
                time.sleep(1)
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Update Engineer",
                    description="Engineer update was cancelled by user.",
                    suspicious="No"
                )
                return

            if not engineer_id:
                print("Engineer ID cannot be empty. Please try again.")
                time.sleep(1.5)
                continue

            engineer = next((eng for eng in engineers if eng.id == engineer_id), None)

            if engineer is None:
                print(f"No service engineer found with ID {engineer_id}. Please try again.")
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Update Engineer",
                    description=f"Failed attempt to update: No engineer found with ID '{engineer_id}'.",
                    suspicious="No"
                )
                time.sleep(2)
                continue

            update_success = engineer_display_methods.update_engineer_fully(engineer, user)
            if update_success:
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Update Engineer",
                    description=f"Updated profile for service engineer '{engineer.username}'.",
                    suspicious="No"
                )
                print("Exiting update...")
                time.sleep(1)
                return
            else:
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Update Engineer",
                    description=f"Update process for engineer '{engineer.username}' was not completed.",
                    suspicious="No"
                )
  
    @staticmethod
    def update_engineer_fully(engineer, user):
        editable_fields = ["username", "first_name", "last_name"]
        
        if user.role == "super_admin":
            editable_fields.append("role")

        validators = {
            "username": lambda val: (
                InputValidators.validate_safe_string(val) and not UserLogic.username_exists(user, val)
            ),
            "first_name": InputValidators.validate_name,
            "last_name": InputValidators.validate_name,
        }

        if "role" in editable_fields:
            validators["role"] = lambda val: val in ["service_engineer", "system_admin"]

        error_messages = {
            "username": "Invalid or already taken username. Only letters, numbers, and underscores allowed.",
            "first_name": "Invalid first name. Only letters and spaces allowed.",
            "last_name": "Invalid last name. Only letters and spaces allowed.",
            "role": "Invalid role. Choose from: service_engineer, system_admin.",
        }

        while True:
            field = engineer_display_methods.prompt_for_engineer_field(engineer, user, editable_fields)
            if field is None:
                return True 

            validator = validators.get(field)
            error_msg = error_messages.get(field, "Invalid input.")

            current_value = getattr(engineer, field, "")
            prompt_msg = f"Enter new value for {field.replace('_', ' ')} [Current: {current_value}]: "

            new_value = InputPrompters.prompt_until_valid(prompt_msg, validator, error_msg)

            if new_value is None:
                print("Update cancelled.")
                time.sleep(1.5)
                return False

            setattr(engineer, field, new_value.strip())
            if UserLogic.modify_service_engineer(user, engineer):
                print(f"Updated {field.replace('_', ' ').title()} for engineer {engineer.username}.")
                time.sleep(2)
                general_shared_methods.clear_console()
            else:
                print("Failed to update engineer. Please check your permissions.")
                time.sleep(2)
                general_shared_methods.clear_console()

    @staticmethod
    def prompt_for_engineer_field(engineer, user, editable_fields):
        while True:
            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "Update User Data".center(75) + "|")
            print("----------------------------------------------------------------------------")
            user_display_methods.display_user(engineer, current_user=user)
            print("----------------------------------------------------------------------------")
            print("Editable fields: " + ", ".join(editable_fields))
            print("Enter the field you want to update or type 'exit' to cancel:")

            field = input("Field to update: ").strip().lower()
            general_shared_methods.clear_console()

            if field == 'exit':
                print("Exiting update...")
                time.sleep(1)
                general_shared_methods.clear_console()
                return None

            if field not in editable_fields:
                print(f"Invalid field '{field}'. Please choose from one of the editable fields.")
                time.sleep(2)
                continue

            return field

    @staticmethod
    def display_delete_engineer(user):
        while True:
            engineers = engineer_display_methods.search_engineer_display(user, update_call=True)
            if engineers is True:
                return
            if not engineers:
                continue

            print("----------------------------------------------------------------------------")
            engineer_id = input("Enter service engineer ID to delete (or type 'exit' to cancel): ").strip()
            general_shared_methods.clear_console()

            if engineer_id.lower() == 'exit':
                print("Exiting deletion...")
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Delete Engineer",
                    description="Engineer deletion cancelled by user.",
                    suspicious="No"
                )
                time.sleep(1)
                return

            if not engineer_id:
                print("Engineer ID cannot be empty. Please try again.")
                time.sleep(1.5)
                continue

            engineer = next((eng for eng in engineers if eng.id == engineer_id), None)
            if engineer is None:
                print(f"No service engineer found with ID {engineer_id}. Please try again.")
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Delete Engineer",
                    description=f"Attempted to delete non-existent engineer with ID: {engineer_id}",
                    suspicious="No"
                )
                time.sleep(2)
                continue

            confirmed = engineer_display_methods.display_delete_engineer_confirm(engineer, user)
            if confirmed:
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Delete Engineer",
                    description=f"Deleted service engineer: {engineer.username}",
                    suspicious="No"
                )
                break
            else:
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Delete Engineer",
                    description=f"Deletion aborted for service engineer: {engineer.username}",
                    suspicious="No"
                )

    @staticmethod
    def display_delete_engineer_confirm(engineer, user):
        while True:
            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "Delete Service Engineer".center(75) + "|")
            print("----------------------------------------------------------------------------")
            user_display_methods.display_user(engineer)
            print("----------------------------------------------------------------------------")

            confirm = input(f"Are you sure you want to delete service engineer {engineer.username}? (yes/no): ").strip().lower()

            if confirm == 'yes':
                if UserLogic.delete_service_engineer(user, engineer.id):
                    general_shared_methods.clear_console()
                    print(f"Service Engineer {engineer.username} has been deleted successfully.")
                    time.sleep(2)
                    return True
                else:
                    print("Failed to delete service engineer. Please check your permissions.")
                    time.sleep(2)
                    return True
            elif confirm == 'no':
                general_shared_methods.clear_console()
                print("Deletion cancelled.")
                time.sleep(1)
                return True
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                time.sleep(1.5)

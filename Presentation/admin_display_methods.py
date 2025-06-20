import time
from Helpers.input_prompters import InputPrompters
from Helpers.input_validators import InputValidators
from Logic.user_logic import UserLogic
from Presentation.general_shared_methods import general_shared_methods
from Presentation.user_display_methods import user_display_methods

class admin_display_methods:
    
    @staticmethod
    def search_admin_display(user, update_call=False):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Search for System Administrator".center(75) + "|")
        print("----------------------------------------------------------------------------")

        search_key = InputPrompters.prompt_until_valid(
            prompt_msg="Enter a search key (id, name, username, etc.) or type 'exit' to go back: ",
            validate_func=InputValidators.validate_search_key,
            error_msg="Invalid search input. Please use letters, numbers, and common symbols only."
        )
        
        if search_key is None:
            print("Exiting search...")
            time.sleep(1)
            general_shared_methods.clear_console()
            return True
        
        general_shared_methods.clear_console()
        admins = UserLogic.search_system_admins(user, search_key)

        if admins is None:
            print("Failed to search for system administrators. Please check your permissions.")
            time.sleep(2)
            return False

        if admins and len(admins) > 0:
            print(f"\nFound {len(admins)} system administrator(s) matching '{general_shared_methods.highlight(search_key, search_key)}':")
            time.sleep(1)
            for count, admin in enumerate(admins, 1):
                print("----------------------------------------------------------------------------")
                print("|" + f"Search Result #{count}".center(75) + "|")
                print("----------------------------------------------------------------------------")
                user_display_methods.display_user(admin, search_key)
            if update_call:
                return admins
            input("Press any key to continue...")
            general_shared_methods.clear_console()
            return None
        else:
            print("No system administrators found matching the search criteria.")
            time.sleep(2)
            general_shared_methods.clear_console()
            return False

    @staticmethod
    def display_add_admin(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Add New System Administrator".center(75) + "|")
        print("----------------------------------------------------------------------------")
        
        admin = admin_display_methods.prompt_for_new_admin_details(user)
        if admin is None:
            print("Administrator creation cancelled.")
            time.sleep(1.5)
            return False
        
        if UserLogic.add_system_admin(user, admin):
            general_shared_methods.clear_console()
            print(f"System Administrator {admin.username} has been added successfully.")
            time.sleep(2)
            general_shared_methods.clear_console()
            user_display_methods.display_user(admin, search_key='', current_user=user)
            print("----------------------------------------------------------------------------")
            input("Press any key to continue...")
            general_shared_methods.clear_console()
            return True
        else:
            print("Failed to add system administrator. Please check your permissions.")
            time.sleep(2)
            return False
    
    @staticmethod
    def prompt_for_new_admin_details(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Enter System Administrator Details".center(75) + "|")
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
            password = input("Enter Password: ").strip()
            if password.lower() == 'exit':
                return None
            passed, error_msg = UserLogic.check_password_requirements(password)
            if passed:
                password = UserLogic.hash_password(password)
                break
            else:
                general_shared_methods.clear_console()
                print(error_msg)
                time.sleep(2)
                general_shared_methods.clear_console()
                return None
        
        # # Add confirmation password check
        # password_confirm = general_shared_methods.input_password("Confirm Password: ").strip()
        # if password != password_confirm:
        #     general_shared_methods.clear_console()
        #     print("Passwords do not match. Please try again.")
        #     time.sleep(2)
        #     general_shared_methods.clear_console()

        
        password = UserLogic.hash_password(password)

        first_name = InputPrompters.prompt_until_valid(
            prompt_msg="Enter First Name: ",
            validate_func=InputValidators.validate_name,
            error_msg="Invalid first name. Use alphabetic characters only."
        )
        if first_name is None:
            return None
        
        last_name = InputPrompters.prompt_until_valid(
            prompt_msg="Enter Last Name: ",
            validate_func=InputValidators.validate_name,
            error_msg="Invalid last name. Use alphabetic characters only."
        )
        if last_name is None:
            return None

        
        admin = UserLogic.create_system_admin_object(
            user,
            username,
            password,
            first_name,
            last_name
        )
        
        return admin

    @staticmethod
    def display_update_admin(user):
        while True:
            admins = admin_display_methods.search_admin_display(user, update_call=True)
            if admins is True:
                return
            if admins is False:
                continue
        
            print("----------------------------------------------------------------------------")
            #NOTE INPUT FIELD
            admin_id = input("Enter system administrator ID to update (or type 'exit' to cancel): ").strip()
            general_shared_methods.clear_console()
            
            admin_id = InputPrompters.prompt_until_valid(
                "Enter system administrator ID to update (or type 'exit' to cancel): ",
                InputValidators.validate_id,
                "Invalid ID. Use letters, numbers, dashes or underscores."
            )
            if admin_id is None:
                print("Exiting update...")
                time.sleep(1)
                general_shared_methods.clear_console()
                return
            
            general_shared_methods.clear_console()
            
            admin = next((adm for adm in admins if adm.id == admin_id), None)
            if admin is None:
                print(f"No system administrator found with ID {admin_id}. Please try again.")
                time.sleep(2)
                continue
            
            exit_update = admin_display_methods.update_admin_fully(admin, user)
            if exit_update:
                print("Exiting update...")
                time.sleep(1)
                break
    
    @staticmethod
    def update_admin_fully(admin, user):
        editable_fields = ["username", "first_name", "last_name"]
        
        validators = {
            "username": lambda val: InputValidators.validate_safe_string(val) and not UserLogic.username_exists(user, val),
            "first_name": InputValidators.validate_name,
            "last_name": InputValidators.validate_name,
        }
        
        while True:
            field = admin_display_methods.prompt_for_admin_field(admin, user, editable_fields)
            if field is None:
                return True
            
            validator = validators.get(field)
            error_msg = {
                "username": "Invalid or already taken username. Only letters, numbers, and underscores allowed.",
                "first_name": "Invalid first name. Only letters and spaces allowed.",
                "last_name": "Invalid last name. Only letters and spaces allowed.",
            }.get(field, "Invalid input.")

            new_value = InputPrompters.prompt_until_valid(
                f"Enter new value for {field} (or type 'exit' to cancel): ",
                validator,
                error_msg
            )

            if new_value is None:
                continue
            
            general_shared_methods.clear_console()
            setattr(admin, field, new_value)
            
            if UserLogic.modify_system_admin(user, admin):
                print(f"Updated {field.replace('_', ' ').title()} for administrator {admin.username}.")
                time.sleep(2)
                general_shared_methods.clear_console()
            else:
                print("Failed to update administrator. Please check your permissions.")
                time.sleep(2)
                general_shared_methods.clear_console()
            
            continue
    
    @staticmethod
    def prompt_for_admin_field(admin, user, editable_fields):
        while True:
            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "Update User Data".center(75) + "|")
            print("----------------------------------------------------------------------------")
            user_display_methods.display_user(admin, current_user=user)
            print("----------------------------------------------------------------------------")
            print("Editable fields: " + ", ".join(editable_fields))
            print("Enter the field you want to update or type 'exit' to cancel:")
            
            #NOTE INPUT FIELD
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
    def display_delete_admin(user):
        while True:
            admins = admin_display_methods.search_admin_display(user, update_call=True)
            if admins is True:
                return
            if admins is False:
                continue
            
            print("----------------------------------------------------------------------------")

            admin_id = InputPrompters.prompt_until_valid(
                "Enter system administrator ID to delete (or type 'exit' to cancel): ",
                InputValidators.validate_id,
                "Invalid administrator ID format. Only letters, numbers, dashes, and underscores are allowed."
            )

            general_shared_methods.clear_console()
            
            if admin_id is None:
                print("Exiting deletion...")
                time.sleep(1)
                return
            
            admin = next((adm for adm in admins if adm.id == admin_id), None)
            
            if admin is None:
                print(f"No system administrator found with ID {admin_id}. Please try again.")
                time.sleep(2)
                continue
            
            exit_delete = admin_display_methods.display_delete_admin_confirm(admin, user)
            if exit_delete:
                break
    
    @staticmethod
    def display_delete_admin_confirm(admin, user):
        while True:
            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "Delete System Administrator".center(75) + "|")
            print("----------------------------------------------------------------------------")
            user_display_methods.display_user(admin)
            print("----------------------------------------------------------------------------")
            
            confirm = InputPrompters.prompt_until_valid(
                f"Are you sure you want to delete system administrator {admin.username}? (yes/no): ",
                InputValidators.validate_yes_no,
                "Invalid input. Please enter 'yes' or 'no'."
            )

            general_shared_methods.clear_console()

            if confirm is None or confirm == 'no':
                print("Deletion cancelled.")
                time.sleep(1)
                return True
            
            if confirm == 'yes':
                if UserLogic.delete_system_admin(user, admin.id):
                    general_shared_methods.clear_console()
                    print(f"System Administrator {admin.username} has been deleted successfully.")
                    time.sleep(2)
                    return True
                else:
                    print("Failed to delete system administrator. Please check your permissions.")
                    time.sleep(2)
                    return True
            elif confirm == 'no':
                general_shared_methods.clear_console()
                print("Deletion cancelled.")
                time.sleep(1)
                return True
            else:
                general_shared_methods.clear_console()
                print("Invalid input. Please enter 'yes' or 'no'.")
                time.sleep(1.5)

    @staticmethod
    def display_delete_my_account(user):
        general_shared_methods.clear_console()
        if user_display_methods.verify_identity(user, "delete your account") is None:
                return False
        while True:
            general_shared_methods.clear_console()
            
            print("----------------------------------------------------------------------------")
            print("|" + "Delete My Account".center(75) + "|")
            print("----------------------------------------------------------------------------")
            confirm = input(f"Are you sure you want to delete your account {user.username}? (yes/no): ").strip().lower()
            general_shared_methods.clear_console()
            
            if confirm == 'yes':
                if UserLogic.delete_system_admin(user, user.id, delete_own_account=True):
                    print("Your account has been deleted successfully.")
                    time.sleep(2)
                    return True
                else:
                    print("Failed to delete your account. Please try again later.")
                    time.sleep(2)
                    return False
            elif confirm == 'no':
                print("Account deletion cancelled.")
                time.sleep(1.5)
                return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                time.sleep(1.5)
                continue
    
    @staticmethod
    def display_update_own_profile(user):
        general_shared_methods.clear_console()
        if user_display_methods.verify_identity(user, "update your profile") is None:
                return False
        
        while True:
            general_shared_methods.clear_console()
            updated = admin_display_methods.update_admin_fully(user, user, update_own_account=True)
            if updated is True:
                return False
            else:
                print("Your profile has been updated successfully.")
                time.sleep(1)
                return True
            
 

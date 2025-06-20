import time
from Logic.user_logic import UserLogic
from Presentation.general_shared_methods import general_shared_methods
from Presentation.user_display_methods import user_display_methods

class engineer_display_methods:
    
    @staticmethod
    def search_engineer_display(user, update_call=False):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Search for Service Engineer".center(75) + "|")
        print("----------------------------------------------------------------------------")

        #NOTE INPUT FIELD
        search_key = input("Enter a search key (id, name, username, etc.) or type 'exit' to go back: ")
        search_key = search_key.strip()
        general_shared_methods.clear_console()
        
        if search_key.lower() == 'exit':
            print("Exiting search...")
            time.sleep(1)
            general_shared_methods.clear_console()
            return True
        
        engineers = UserLogic.search_service_engineers(user, search_key)
        if engineers and len(engineers) > 0:
            print(f"\nFound {len(engineers)} service engineer(s) matching '{general_shared_methods.highlight(search_key, search_key)}':")
            time.sleep(1)
            for count, engineer in enumerate(engineers, 1):
                print("----------------------------------------------------------------------------")
                print("|" + f"search result #{count}".center(75) + "|")
                print("----------------------------------------------------------------------------")
                user_display_methods.display_user(engineer, search_key)
            if update_call:
                return engineers
            return None
        else:
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
            print("Engineer creation cancelled.")
            time.sleep(1.5)
            return False
        
        if UserLogic.add_service_engineer(user, engineer):
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
            print("Failed to add service engineer. Please check your permissions.")
            time.sleep(2)
            return False
    
    @staticmethod
    def prompt_for_new_engineer_details(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Enter Service Engineer Details".center(75) + "|")
        print("----------------------------------------------------------------------------")
        
        #NOTE INPUT FIELDS (no type exit and space checking)
        username = input("Enter Username: ").strip()
        username_passed, error_msg_username = UserLogic.check_username_requirements(username)
        if not username_passed:
            general_shared_methods.clear_console()
            print(error_msg_username)
            time.sleep(2)
            general_shared_methods.clear_console()
            return None
        
        #NOTE PASSWORD MOET GEHASHT WORDEN EN AAN VOORWAARDEN VOLDOEN
        password = general_shared_methods.input_password("Enter Password: ").strip()
        passed, error_msg = UserLogic.check_password_requirements(password)
        if not passed:
            general_shared_methods.clear_console()
            print(error_msg)
            time.sleep(2)
            general_shared_methods.clear_console()
            return None
        
        # Add confirmation password check
        password_confirm = general_shared_methods.input_password("Confirm Password: ").strip()
        if password != password_confirm:
            general_shared_methods.clear_console()
            print("Passwords do not match. Please try again.")
            time.sleep(2)
            general_shared_methods.clear_console()
            return None
        
        password = UserLogic.hash_password(password)
        first_name = input("Enter First Name: ").strip()
        last_name = input("Enter Last Name: ").strip()
        
        if not username or not password or not first_name or not last_name:
            print("All fields are required. Please try again.")
            time.sleep(2)
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
            #NOTE INPUT FIELD
            engineer_id = input("Enter service engineer ID to update (or type 'exit' to cancel): ").strip()
            general_shared_methods.clear_console()
            
            if engineer_id.lower() == 'exit':
                print("Exiting update...")
                time.sleep(1)
                return
            
            if engineer_id == '':
                print("Engineer ID cannot be empty. Please try again.")
                time.sleep(1.5)
                continue
            
            engineer = None
            for eng in engineers:
                if eng.id == engineer_id:
                    engineer = eng
                    break
            
            if engineer is None:
                print(f"No service engineer found with ID {engineer_id}. Please try again.")
                time.sleep(2)
                continue
            
            exit_update = engineer_display_methods.update_engineer_fully(engineer, user)
            if exit_update:
                print("Exiting update...")
                time.sleep(1)
                break
    
    @staticmethod
    def update_engineer_fully(engineer, user):
        editable_fields = [
            "username",
            "first_name",
            "last_name"
        ]
        
        # Add role field if the current user is a Super Admin
        if user.role == "super_admin":
            editable_fields.append("role")
        
        while True:
            field = engineer_display_methods.prompt_for_engineer_field(engineer, user, editable_fields)
            if field is None:
                return True
            
            new_value = engineer_display_methods.prompt_for_engineer_value(field, engineer)
            if new_value is None:
                continue
            
            general_shared_methods.clear_console()
            if field == "username":
                # Add username validation using existing method
                username_passed, error_msg = UserLogic.check_username_requirements(new_value)
                if not username_passed:
                    print(error_msg)
                    time.sleep(2)
                    general_shared_methods.clear_console()
                    continue
                
                engineer.username = new_value
            elif field == "first_name":
                engineer.first_name = new_value
            elif field == "last_name":
                engineer.last_name = new_value
            elif field == "role" and user.role == "super_admin":
                # Validate the role value
                valid_roles = ["service_engineer", "system_admin"]
                if new_value not in valid_roles:
                    print(f"Invalid role '{new_value}'. Valid roles are: {', '.join(valid_roles)}")
                    time.sleep(2)
                    general_shared_methods.clear_console()
                    continue
                engineer.role = new_value
            
            if UserLogic.modify_service_engineer(user, engineer):
                print(f"Updated {field.replace('_', ' ').title()} for engineer {engineer.username}.")
                time.sleep(2)
                general_shared_methods.clear_console()
            else:
                print(f"Failed to update engineer. Please check your permissions.")
                time.sleep(2)
                general_shared_methods.clear_console()
            
            continue
    
    @staticmethod
    def prompt_for_engineer_field(engineer, user, editable_fields):
        while True:
            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "Update User Data".center(75) + "|")
            print("----------------------------------------------------------------------------")
            user_display_methods.display_user(engineer, current_user=user)
            print("----------------------------------------------------------------------------")
            print("Enter the field you want to update or type 'exit' to cancel. Use '_' for spaces.")
            
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
    def prompt_for_engineer_value(field, engineer=None):
        while True:
            general_shared_methods.clear_console()
            if engineer:
                if field == "username":
                    current = engineer.username
                elif field == "first_name":
                    current = engineer.first_name
                elif field == "last_name":
                    current = engineer.last_name
                elif field == "role":
                    current = engineer.role
                    print(f"Current {field.replace('_', ' ').title()}: {current}")
                    print("Available roles: service_engineer, system_admin")
                    print("----------------------------------------------------------------------------")
                    #NOTE INPUT FIELD
                    new_value = input(f"Enter new role (or type 'exit' to cancel): ").strip().lower()
                    general_shared_methods.clear_console()
                    
                    if new_value.lower() == 'exit':
                        print("Exiting update...")
                        time.sleep(1)
                        general_shared_methods.clear_console()
                        return None
                    
                    if new_value == '':
                        print("Role cannot be empty. Please enter a valid role or type 'exit' to cancel.")
                        time.sleep(1.5)
                        continue
                    
                    return new_value
                
                print(f"Current {field.replace('_', ' ').title()}: {current}")
            print("----------------------------------------------------------------------------")
            
            #NOTE INPUT FIELD
            new_value = input(f"Enter new value for {field} (or type 'exit' to cancel): ").strip()
            general_shared_methods.clear_console()
            
            if new_value.lower() == 'exit':
                print("Exiting update...")
                time.sleep(1)
                general_shared_methods.clear_console()
                return None
            
            if new_value == '':
                print("Value cannot be empty. Please enter a value or type 'exit' to cancel.")
                time.sleep(1.5)
                continue
            
            return new_value
    
    @staticmethod
    def display_delete_engineer(user):
        while True:
            engineers = engineer_display_methods.search_engineer_display(user, update_call=True)
            if engineers is True:
                return
            if engineers is False:
                continue
            
            print("----------------------------------------------------------------------------")
            #NOTE INPUT FIELD
            engineer_id = input("Enter service engineer ID to delete (or type 'exit' to cancel): ").strip()
            general_shared_methods.clear_console()
            
            if engineer_id.lower() == 'exit':
                print("Exiting deletion...")
                time.sleep(1)
                return
            
            if engineer_id == '':
                print("Engineer ID cannot be empty. Please try again.")
                time.sleep(1.5)
                continue
            
            engineer = None
            for eng in engineers:
                if eng.id == engineer_id:
                    engineer = eng
                    break
            
            if engineer is None:
                print(f"No service engineer found with ID {engineer_id}. Please try again.")
                time.sleep(2)
                continue
            
            exit_delete = engineer_display_methods.display_delete_engineer_confirm(engineer, user)
            if exit_delete:
                break
    
    @staticmethod
    def display_delete_engineer_confirm(engineer, user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Delete Service Engineer".center(75) + "|")
        print("----------------------------------------------------------------------------")
        user_display_methods.display_user(engineer)
        print("----------------------------------------------------------------------------")
        
        #NOTE INPUT FIELD
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
            general_shared_methods.clear_console()
            print("Invalid input. Please enter 'yes' or 'no'.")
            time.sleep(1.5)
            return False
import time
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

        #NOTE INPUT FIELD
        search_key = input("Enter a search key (id, name, username, etc.) or type 'exit' to go back: ")
        search_key = search_key.strip()
        general_shared_methods.clear_console()
        
        if search_key.lower() == 'exit':
            print("Exiting search...")
            time.sleep(1)
            general_shared_methods.clear_console()
            return True
        
        admins = UserLogic.search_system_admins(user, search_key)
        if admins is None:
            print("Failed to search for system administrators. Please check your permissions.")
            time.sleep(2)
        if admins and len(admins) > 0:
            print(f"\nFound {len(admins)} system administrator(s) matching '{general_shared_methods.highlight(search_key, search_key)}':")
            time.sleep(1)
            for count, admin in enumerate(admins, 1):
                print("----------------------------------------------------------------------------")
                print("|" + f"search result #{count}".center(75) + "|")
                print("----------------------------------------------------------------------------")
                user_display_methods.display_user(admin, search_key)
            if update_call:
                return admins
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
        
        #NOTE INPUT FIELDS (no type exit and space checking)
        username = input("Enter Username: ").strip()
        #NOTE ALS PASSWORD CHECK FAALT RETURN NAAR DIT SCHERM?
        password = input("Enter Password: ").strip()
        passed, error_msg = UserLogic.check_password_requirements(password)
        if not passed:
            general_shared_methods.clear_console()
            print(error_msg)
            time.sleep(2)
            return None
        password = UserLogic.hash_password(password)

        first_name = input("Enter First Name: ").strip()
        last_name = input("Enter Last Name: ").strip()
        
        if not username or not password or not first_name or not last_name:
            print("All fields are required. Please try again.")
            time.sleep(2)
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
            
            if admin_id.lower() == 'exit':
                print("Exiting update...")
                time.sleep(1)
                return
            
            if admin_id == '':
                print("Administrator ID cannot be empty. Please try again.")
                time.sleep(1.5)
                continue
            
            admin = None
            for adm in admins:
                if adm.id == admin_id:
                    admin = adm
                    break
            
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
        editable_fields = [
            "username",
            "first_name",
            "last_name"
        ]
        
        while True:
            field = admin_display_methods.prompt_for_admin_field(admin, user, editable_fields)
            if field is None:
                return True
            
            new_value = admin_display_methods.prompt_for_admin_value(field, admin)
            if new_value is None:
                continue
            
            general_shared_methods.clear_console()
            if field == "username":
                admin.username = new_value
            elif field == "first_name":
                admin.first_name = new_value
            elif field == "last_name":
                admin.last_name = new_value
            
            if UserLogic.modify_system_admin(user, admin):
                print(f"Updated {field.replace('_', ' ').title()} for administrator {admin.username}.")
                time.sleep(2)
                general_shared_methods.clear_console()
            else:
                print(f"Failed to update administrator. Please check your permissions.")
                time.sleep(2)
                general_shared_methods.clear_console()
            
            continue
    
    @staticmethod
    def prompt_for_admin_field(admin, user, editable_fields):
        while True:
            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "Update System Administrator Data".center(75) + "|")
            print("----------------------------------------------------------------------------")
            user_display_methods.display_user(admin, current_user=user)
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
    def prompt_for_admin_value(field, admin=None):
        while True:
            general_shared_methods.clear_console()
            if admin:
                if field == "username":
                    current = admin.username
                elif field == "first_name":
                    current = admin.first_name
                elif field == "last_name":
                    current = admin.last_name
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
    def display_delete_admin(user):
        while True:
            admins = admin_display_methods.search_admin_display(user, update_call=True)
            if admins is True:
                return
            if admins is False:
                continue
            
            print("----------------------------------------------------------------------------")
            #NOTE INPUT FIELD
            admin_id = input("Enter system administrator ID to delete (or type 'exit' to cancel): ").strip()
            general_shared_methods.clear_console()
            
            if admin_id.lower() == 'exit':
                print("Exiting deletion...")
                time.sleep(1)
                return
            
            if admin_id == '':
                print("Administrator ID cannot be empty. Please try again.")
                time.sleep(1.5)
                continue
            
            admin = None
            for adm in admins:
                if adm.id == admin_id:
                    admin = adm
                    break
            
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
            
            #NOTE INPUT FIELD
            confirm = input(f"Are you sure you want to delete system administrator {admin.username}? (yes/no): ").strip().lower()
            
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


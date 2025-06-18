from Presentation.general_shared_methods import general_shared_methods
from Logic.user_logic import UserLogic
import time


class user_display_methods:
    @staticmethod
    def display_check_users(user):
        general_shared_methods.clear_console()
        users = UserLogic.check_users(user)
        general_shared_methods.clear_console()
        if users == False:
            print("Unauthorized action.")
            time.sleep(2)
            return
        if not users or len(users) == 0:
            print("No users found.")
            time.sleep(2)
            return
        
        print(f"Found {len(users)} users in the system:\n")
        time.sleep(1.5)
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "User List".center(75) + "|")
        print("----------------------------------------------------------------------------")
        for count, user_item in enumerate(users, 1):
            print(f"User #{count}: {user_item.username}")
            print("----------------------------------------------------------------------------")
            user_display_methods.display_user(user_item, "")
            print("----------------------------------------------------------------------------")    


        input("\nPress Enter to continue...")
        general_shared_methods.clear_console()
        return None

    @staticmethod
    def display_user(user, search_key=None, current_user=None):
        if search_key is not None:
            # The search display logic (keep this as is)
            print(f"User ID:           {general_shared_methods.highlight(user.id, search_key)}")
            print(f"Username:          {general_shared_methods.highlight(user.username, search_key)}")
            print(f"Name:              {general_shared_methods.highlight(user.first_name, search_key)} {general_shared_methods.highlight(user.last_name, search_key)}")
            print(f"Role:              {general_shared_methods.highlight(user.role, search_key)}")
            print(f"Registration Date: {general_shared_methods.highlight(user.registration_date, search_key)}")
        else:
            is_editable = False
            role_editable = False
            
            if current_user:
                from DataModels.user import ROLES_HIERARCHY
                viewer_role_level = ROLES_HIERARCHY.get(current_user.role, 0)
                user_role_level = ROLES_HIERARCHY.get(user.role, 0)
                is_editable = viewer_role_level > user_role_level
                role_editable = current_user.role == "super_admin" and is_editable
            
            editable_tag = "[Editable]" if is_editable else ""
            role_editable_tag = "[Editable]" if role_editable else ""
            
            print(f"User ID:           {user.id}")
            print(f"Username:          {user.username:<25}{editable_tag:>12}")
            print(f"First Name:        {user.first_name:<25}{editable_tag:>12}")
            print(f"Last Name:         {user.last_name:<25}{editable_tag:>12}")
            print(f"Role:              {user.role:<25}{role_editable_tag:>12}")
            print(f"Registration Date: {user.registration_date}")
            
    
    @staticmethod
    def display_update_password(user):     
        general_shared_methods.clear_console()
        if user_display_methods.verify_identity(user) is None:
            return
        while True:
            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "Update Password".center(75) + "|")
            print("----------------------------------------------------------------------------")
            #NOTE INPUT FIELD
            new_password = input("Enter your new password: ").strip()
            
            passed, error_msg = UserLogic.check_password_requirements(new_password)

            if not passed:
                general_shared_methods.clear_console()
                print(error_msg)
                time.sleep(2)
                continue
            print("----------------------------------------------------------------------------")
            new_password_confirm = input("Confirm your new password: ").strip()
            general_shared_methods.clear_console()
            if new_password != new_password_confirm:
                print("Passwords do not match. Please try again.")
                time.sleep(2)
                continue

            else:
                general_shared_methods.clear_console()
                print("Updating your password...")
                hashed_password = UserLogic.hash_password(new_password)
                UserLogic.update_own_password(user, hashed_password )
                time.sleep(1.5)
                general_shared_methods.clear_console()
                print("Your password has been successfully updated.")
                time.sleep(1.5)
                break

    @staticmethod
    def verify_identity(user):
        print("To verify your identity, please enter your current password")
        print("----------------------------------------------------------------------------")
        #NOTE INPUT FIELD MOET NOG STERRETJES ZIJN
        input_password = input("Current Password: ").strip()
        general_shared_methods.clear_console()
        print("Verifying your identity...")
        time.sleep(1.5)
        general_shared_methods.clear_console()

        verified = UserLogic.verify_password(user.password_hash, input_password)
        if not verified:
            print("Incorrect password. Returning to menu...")
            time.sleep(2)
            return
        
        print("Identity verified. You can now update your password.")
        time.sleep(1)
        general_shared_methods.clear_console()
        return True
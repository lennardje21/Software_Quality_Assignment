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
    def display_user(user, search_key=None):
        if search_key is not None:
            print(f"User ID:           {general_shared_methods.highlight(user.id, search_key)}")
            print(f"Username:          {general_shared_methods.highlight(user.username, search_key)}")
            print(f"Name:              {general_shared_methods.highlight(user.first_name, search_key)} {general_shared_methods.highlight(user.last_name, search_key)}")
            print(f"Role:              {general_shared_methods.highlight(user.role, search_key)}")
            print(f"Registration Date: {general_shared_methods.highlight(user.registration_date, search_key)}")
        else:
            #Voor users editen
            print("Not implemented yet.")
    
    @staticmethod
    def display_update_password(user):
        from Logic.user_logic import UserLogic
        
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Update Password".center(75) + "|")
        print("----------------------------------------------------------------------------")
        
        #NOTE INPUT FIELD
        new_password = input("Enter your new password: ").strip()
        general_shared_methods.clear_console()
        print("Not implemented yet.")
        time.sleep(1)
        return
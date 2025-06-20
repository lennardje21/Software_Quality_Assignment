from Helpers.input_prompters import InputPrompters
from Helpers.input_validators import InputValidators
from Logic.log_logic import LogLogic
from Presentation.general_shared_methods import general_shared_methods
from Logic.user_logic import UserLogic

import time


class user_display_methods:

    @staticmethod
    def display_check_users(user):
        general_shared_methods.clear_console()
        users = UserLogic.check_users(user)
        general_shared_methods.clear_console()

        if users is False:
            print("Unauthorized action.")
            LogLogic.add_log_to_database(
                username=user.username,
                action="Check Users",
                description="Attempted to access the user list without proper permissions.",
                suspicious="Yes"
            )
            time.sleep(2)
            return

        if not users:
            print("No users found.")
            LogLogic.add_log_to_database(
                username=user.username,
                action="Check Users",
                description="Viewed user list. No users found.",
                suspicious="No"
            )
            time.sleep(2)
            return

        LogLogic.add_log_to_database(
            username=user.username,
            action="Check Users",
            description=f"Viewed list of {len(users)} user(s).",
            suspicious="No"
        )

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

        general_shared_methods.input_password("\nPress any key to continue...")
        general_shared_methods.clear_console()

    @staticmethod
    def display_user(user, search_key=None, current_user=None):
        if search_key is not None:
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
                is_editable = (current_user.id == user.id) or (viewer_role_level > user_role_level)
                role_editable = current_user.role == "super_admin" and viewer_role_level > user_role_level
            
            editable_tag = "[Editable]" if is_editable else ""
            role_editable_tag = "[Editable]" if role_editable else ""
            
            print(f"User ID:           {user.id}")
            print(f"Username:          {user.username:<25}{editable_tag:>12}")
            print(f"First Name:        {user.first_name:<25}{editable_tag:>12}")
            print(f"Last Name:         {user.last_name:<25}{editable_tag:>12}")
            print(f"Role:              {user.role:<25}{role_editable_tag:>12}")
            print(f"Registration Date: {user.registration_date}")
            
    @staticmethod
    def display_update_password(user, temp_password=False):     
        general_shared_methods.clear_console()

        if not temp_password:
            if user_display_methods.verify_identity(user, "update your password") is None:
                return

        while True:
            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "Update Password".center(75) + "|")
            print("----------------------------------------------------------------------------")

            def password_validator(password):
                passed, _ = UserLogic.check_password_requirements(password)
                return passed

            new_password = InputPrompters.prompt_until_valid(
                prompt_msg="Enter your new password: ",
                validate_func=password_validator,
                error_msg="Password does not meet requirements.",
            )
            if new_password is None:
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Update Password",
                    description="Password update cancelled by user.",
                    suspicious="No"
                )
                return

            print("----------------------------------------------------------------------------")
            new_password_confirm = general_shared_methods.input_password("Confirm your new password: ").strip()
            general_shared_methods.clear_console()

            if new_password != new_password_confirm:
                print("Passwords do not match. Please try again.")
                time.sleep(2)
                continue

            general_shared_methods.clear_console()
            print("Updating your password...")
            hashed_password = UserLogic.hash_password(new_password)
            UserLogic.update_own_password(user, hashed_password)
            time.sleep(1.5)
            general_shared_methods.clear_console()
            print("Your password has been successfully updated.")
            time.sleep(1.5)

            LogLogic.add_log_to_database(
                username=user.username,
                action="Update Password",
                description="User updated their password." if not temp_password else "User updated temporary password.",
                suspicious="No"
            )
            break

    @staticmethod
    def verify_identity(user, prompt):
        print("To verify your identity, please enter your current password.")
        print("----------------------------------------------------------------------------")

        attempts = 3
        while attempts > 0:
            input_password = general_shared_methods.input_password("Current Password: ").strip()
            general_shared_methods.clear_console()

            print("Verifying your identity...")
            time.sleep(1.5)
            general_shared_methods.clear_console()

            if UserLogic.verify_password(user.password_hash, input_password):
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Identity Verification",
                    description=f"User verified identity to {prompt}.",
                    suspicious="No"
                )
                print(f"Identity verified. You can now {prompt}.")
                time.sleep(1)
                general_shared_methods.clear_console()
                return True

            attempts -= 1
            if attempts > 0:
                print(f"Incorrect password. {attempts} attempt(s) remaining.")
                time.sleep(1.5)
            else:
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Identity Verification Failed",
                    description=f"User failed to verify identity for: {prompt}.",
                    suspicious="Yes"
                )
                print("Too many failed attempts. Returning to menu...")
                time.sleep(1.5)
                return None

    @staticmethod
    def display_reset_password(user, prompt):
        general_shared_methods.clear_console()
        if user_display_methods.verify_identity(user, f"reset {prompt} password") is None:
            return False
        general_shared_methods.clear_console()
        
        target_user = user_display_methods._find_target_user_for_reset(user, prompt)
        if target_user is None:
            return False
        
        return user_display_methods._perform_password_reset(user, target_user, prompt)

    @staticmethod
    def _find_target_user_for_reset(user, prompt):
        from Presentation.engineer_display_methods import engineer_display_methods
        from Presentation.admin_display_methods import admin_display_methods

        display_map = {
            "Service Engineer": ("engineer", engineer_display_methods.search_engineer_display),
            "System Admin": ("admin", admin_display_methods.search_admin_display),
        }

        if prompt not in display_map:
            print("Something went wrong. Returning to menu...")
            LogLogic.add_log_to_database(
                username=user.username,
                action="Reset Password",
                description=f"Invalid prompt key '{prompt}' for user lookup.",
                suspicious="Yes"
            )
            time.sleep(1.5)
            general_shared_methods.clear_console()
            return None

        user_type, search_func = display_map[prompt]

        while True:
            general_shared_methods.clear_console()
            users = search_func(user, update_call=True)

            if users is True:
                return None
            if not users:
                print(f"No {user_type}s found or search error occurred.")
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Reset Password",
                    description=f"No {user_type}s found during password reset search.",
                    suspicious="No"
                )
                time.sleep(2)
                continue

            user_id = InputPrompters.prompt_until_valid(
                prompt_msg=f"Enter {user_type} ID to reset password (or type 'exit' to cancel): ",
                validate_func=InputValidators.validate_id,
                error_msg="Invalid ID format. Please try again."
            )

            if user_id is None:
                print("Password reset cancelled.")
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Reset Password",
                    description=f"Cancelled password reset for a {user_type}.",
                    suspicious="No"
                )
                time.sleep(1)
                return None

            target_user = next((u for u in users if u.id == user_id), None)
            if not target_user:
                print(f"No {user_type} found with ID {user_id}. Please try again.")
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Reset Password",
                    description=f"Attempted password reset for non-existent {user_type} ID: {user_id}",
                    suspicious="Yes"
                )
                time.sleep(2)
                continue

            LogLogic.add_log_to_database(
                username=user.username,
                action="Reset Password",
                description=f"Selected {user_type} '{target_user.username}' for password reset.",
                suspicious="No"
            )
            return target_user

    @staticmethod
    def _perform_password_reset(user, target_user, prompt):
        while True:
            user_display_methods._show_reset_header(target_user, prompt)

            temp_password = UserLogic.generate_temporary_password()
            hashed_temp_password = UserLogic.hash_password(temp_password)

            print(f"Generated temporary password: {temp_password}")
            print("----------------------------------------------------------------------------")
            input("Press Enter to continue...")
            general_shared_methods.clear_console()

            success = UserLogic.set_temporary_password(user, target_user, hashed_temp_password)

            if success:
                print(f"Password for {target_user.username} has been successfully reset.")
                print("User will be required to change password on next login.")
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Reset Password",
                    description=f"Password reset successfully for user '{target_user.username}'.",
                    suspicious="No"
                )
                time.sleep(2)
                return True
            else:
                print("Failed to reset password. Please check your permissions.")
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Reset Password",
                    description=f"Failed password reset attempt for user '{target_user.username}'.",
                    suspicious="Yes"
                )
                time.sleep(2)
                return False

    @staticmethod
    def _show_reset_header(target_user, prompt):
        """Helper method to display the reset password header"""
        print("----------------------------------------------------------------------------")
        print("|" + f"Reset Password for {prompt}".center(75) + "|")
        print("----------------------------------------------------------------------------")
        user_display_methods.display_user(target_user)
        print("----------------------------------------------------------------------------")

    @staticmethod
    def display_necessary_password_update(user, reset_by_admin=False):
        general_shared_methods.clear_console()
        prompt = (
            "Your password has been reset by a System Admin. You must update it now."
            if reset_by_admin else
            "Your password has been reset by the Super Admin. You must update it now."
        )

        print(prompt)
        time.sleep(2)
        general_shared_methods.clear_console()

        user_display_methods.display_update_password(user, True)

        success = UserLogic.reset_password_upon_login_successful(user)

        if success:
            LogLogic.add_log_to_database(
                username=user.username,
                action="Forced Password Update",
                description="User successfully updated their password after a forced reset.",
                suspicious="No"
            )
            print("Your password has been updated successfully.")
            time.sleep(2)
            general_shared_methods.clear_console()
            return True
        else:
            LogLogic.add_log_to_database(
                username=user.username,
                action="Forced Password Update Failed",
                description="User failed to update password after a forced reset.",
                suspicious="Yes"
            )
            print("Failed to update your password. Please try again later.")
            time.sleep(2)
            general_shared_methods.clear_console()
            return False


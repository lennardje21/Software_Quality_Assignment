# Logic/log_logic.py

from DataModels.user import User

class LogLogic:

    @staticmethod
    def view_logs(user: User):
        if user.is_authorized("system_admin"):
            print("[LogLogic] Viewing logs...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def view_unread_suspicious_logs(user: User):
        if user.is_authorized("system_admin"):
            print("[LogLogic] Viewing unread suspicious logs...")
        else:
            print("Unauthorized action.")

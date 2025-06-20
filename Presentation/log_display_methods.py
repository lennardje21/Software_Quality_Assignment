# Presentation/log_display_methods.py

from Logic.log_logic import LogLogic
from Presentation.general_shared_methods import general_shared_methods


class log_display_methods:

    @staticmethod
    def display_all_logs(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "View All Logs".center(75) + "|")
        print("----------------------------------------------------------------------------")
        logs = LogLogic.get_all_logs(user)
        if not logs:
            print("No logs found.")
        else:
            for log in logs:
                print(f"[{log['timestamp']}] {log['username']} - {log['action']} - {log['description']} | Suspicious: {log['suspicious']} | Seen: {log['seen']}")
        input("\nPress Enter to return...")

    @staticmethod
    def display_unread_suspicious_logs(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Unread Suspicious Logs".center(75) + "|")
        print("----------------------------------------------------------------------------")

        logs = LogLogic.get_unread_suspicious_logs(user)
        if not logs:
            print("No unread suspicious logs.")
        else:
            for log in logs:
                print(f"[{log['timestamp']}] {log['username']} - {log['action']} - {log['description']}")
        input("\nPress Enter to return...")

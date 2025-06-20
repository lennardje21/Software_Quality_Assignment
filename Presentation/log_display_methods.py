# Presentation/log_display_methods.py

from Logic.log_logic import LogLogic
from Presentation.general_shared_methods import general_shared_methods
from tabulate import tabulate

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
            table_headers = ["Time", "User", "Action", "Description", "Suspicious"]
            table_rows = [
                [log[6], log[1], log[2], log[3], log[4]]
                for log in logs
            ]
            print(tabulate(table_rows, headers=table_headers, tablefmt="fancy_grid"))

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
            table_data = []
            for log in logs:
                table_data.append([
                    log[0],
                    log[6],
                    log[1],
                    log[2],
                    log[3]
                ])
            headers = ["ID", "Timestamp", "User", "Action", "Description"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        input("\nPress Enter to continue...")

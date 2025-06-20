# Logic/log_logic.py

from datetime import datetime
from DataAccess.insert_data import InsertData
from DataAccess.get_data import GetData
from DataModels.user import User


class LogLogic:

    @staticmethod
    def add_log_to_database(username: str, action: str, description: str, suspicious: str = "No") -> bool:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert = InsertData()
        try:
            insert.insert_log_entry(username, action, description, suspicious, timestamp)
            return True
        except Exception as e:
            print(f"Log insert failed: {e}")
            return False

    @staticmethod
    def get_all_logs(user: User) -> list[dict]:
        if not user.is_authorized("system_admin"):
            return []
        get = GetData()
        return get.get_all_logs()

    @staticmethod
    def get_unread_suspicious_logs(user: User) -> list[tuple]:
        if not user.is_authorized("system_admin"):
            return []

        logs = LogLogic.get_all_logs(user)
        # suspicious at index 4, seen at index 5
        unread_logs = [log for log in logs if log[4] == "Yes" and log[5] == "no"]

        if unread_logs:
            insertData = InsertData()
            insertData.mark_logs_as_seen([log[0] for log in unread_logs])

        return unread_logs

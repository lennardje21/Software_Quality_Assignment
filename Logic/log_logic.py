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
    def get_unread_suspicious_logs(user: User) -> list[dict]:
        if not user.is_authorized("system_admin"):
            return []
        get = GetData()
        logs = get.get_unread_suspicious_logs()
        if logs:
            get.mark_logs_as_seen([log["id"] for log in logs])
        return logs

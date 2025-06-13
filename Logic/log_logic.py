# Logic/log_logic.py

import sqlite3
from datetime import datetime
from DataModels.user import User

DB_PATH = 'Database/urbanmobility.db'

class LogLogic:

    @staticmethod
    def add_log_to_database(username: str, action: str, description: str, suspicious: str = "No"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO logs (username, action, description, suspicious, seen, timestamp)
            VALUES (?, ?, ?, ?, 'No', ?)
        """, (username, action, description, suspicious, timestamp))
        conn.commit()
        conn.close()

    @staticmethod
    def view_logs(user: User):
        if user.is_authorized("system_admin"):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT id, username, action, description, suspicious, seen, timestamp FROM logs ORDER BY id DESC")
            rows = cur.fetchall()
            conn.close()

            if not rows:
                print("No logs found.")
            else:
                print("\n=== All Logs ===")
                for row in rows:
                    print(f"[{row[6]}] {row[1]} - {row[2]} - {row[3]} | Suspicious: {row[4]}, Seen: {row[5]}")

        else:
            print("Unauthorized action.")

        LogLogic.pause()

    @staticmethod
    def view_unread_suspicious_logs(user: User):
        if user.is_authorized("system_admin"):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT id, username, action, description, timestamp
                FROM logs
                WHERE suspicious = 'Yes' AND seen = 'No'
                ORDER BY id DESC
            """)
            rows = cur.fetchall()

            if not rows:
                print("No unread suspicious logs found.")
            else:
                print("\n=== Unread Suspicious Logs ===")
                for row in rows:
                    print(f"[{row[4]}] {row[1]} - {row[2]} - {row[3]}")

                # Mark them as seen
                ids = [str(row[0]) for row in rows]
                cur.execute(f"UPDATE logs SET seen = 'Yes' WHERE id IN ({','.join(ids)})")
                conn.commit()

            conn.close()
        else:
            print("Unauthorized action.")
        LogLogic.pause()

    @staticmethod
    def pause():
        input("\nPress Enter to return to the menu...\n")
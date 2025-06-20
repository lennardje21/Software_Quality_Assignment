import sqlite3, os, sys
from DataModels.user import User
from DataModels.traveller import Traveller
from DataModels.scooter import Scooter
#from DataModels.log import Log # Nog niet gebruikt

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class GetData:
    def __init__(self):
        self.db_path = os.path.join(sys.path[0], "Database/urbanmobility.db")
    
    def get_all_users(self) -> list[User]:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT *
                FROM users
            '''
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [User(*row) for row in rows]
    
    def get_all_travellers(self) -> list[Traveller]:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT *
                FROM travellers
            '''
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [Traveller(*row) for row in rows]
    
    def get_all_scooters(self) -> list[Scooter]:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT *
                FROM scooter
            '''
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [Scooter(*row) for row in rows]

    def get_user_by_id(self, user_id: str) -> User:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT *
                FROM users
                WHERE UserID = ?
            '''
            cursor = connection.cursor()
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            return User(*row) if row else None

    def get_traveller_by_id(self, traveller_id: str) -> Traveller:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT *
                FROM travellers
                WHERE TravellerID = ?
            '''
            cursor = connection.cursor()    
            cursor.execute(query, (traveller_id,))
            row = cursor.fetchone()
            return Traveller(*row) if row else None

    def get_scooter_by_id(self, scooter_id: str) -> Scooter:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT *
                FROM scooter
                WHERE ScooterID = ?
            '''
            cursor = connection.cursor()
            cursor.execute(query, (scooter_id,))
            row = cursor.fetchone()
            return Scooter(*row) if row else None

    def get_user_by_partial(self, search_key: str) -> list[User]:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT *
                FROM users
                WHERE
                    LOWER(UserID) LIKE LOWER(?) OR
                    LOWER(UserName) LIKE LOWER(?) OR
                    LOWER(FirstName) LIKE LOWER(?) OR
                    LOWER(LastName) LIKE LOWER(?) OR
                    LOWER(Role) LIKE LOWER(?) OR
                    RegistrationDate LIKE ?
            '''
            cursor = connection.cursor()
            search_pattern = f"%{search_key.lower()}%"
            date_pattern = f"%{search_key}%"
            
            params = [search_pattern] * 5 + [date_pattern]
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [User(*row) for row in rows]

    def get_user_by_username(self, username: str) -> User:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT *
                FROM users
                WHERE UserName = ?
            '''
            cursor = connection.cursor()
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            return User(*row) if row else None
            return Scooter(*row) if row else None

    def get_scooter_by_partial(self, search_key: str) -> list[Scooter]:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT *
                FROM scooter
                WHERE
                    LOWER(ScooterID) LIKE LOWER(?) OR
                    LOWER(Brand) LIKE LOWER(?) OR
                    LOWER(Model) LIKE LOWER(?) OR
                    LOWER(SerialNumber) LIKE LOWER(?) OR
                    LOWER(CAST(TopSpeed AS TEXT)) LIKE LOWER(?) OR
                    LOWER(CAST(BatteryCapacity AS TEXT)) LIKE LOWER(?) OR
                    LOWER(CAST(StateOfCharge AS TEXT)) LIKE LOWER(?) OR
                    LOWER(CAST(TargetSOCMin AS TEXT)) LIKE LOWER(?) OR
                    LOWER(CAST(TargetSOCMax AS TEXT)) LIKE LOWER(?) OR
                    LOWER(CAST(Latitude AS TEXT)) LIKE LOWER(?) OR
                    LOWER(CAST(Longitude AS TEXT)) LIKE LOWER(?) OR
                    LOWER(CAST(OutOfServiceStatus AS TEXT)) LIKE LOWER(?) OR
                    LOWER(CAST(Mileage AS TEXT)) LIKE LOWER(?) OR
                    LOWER(LastMaintenanceDate) LIKE LOWER(?) OR
                    LOWER(InServiceDate) LIKE LOWER(?)
            '''
            cursor = connection.cursor()
            search_pattern = f"%{search_key.lower()}%"
            params = [search_pattern] * 15
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [
                Scooter(*row) for row in rows
            ]

    def get_user_by_partial(self, search_key: str) -> list[User]:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT *
                FROM users
                WHERE
                    LOWER(UserID) LIKE LOWER(?) OR
                    LOWER(UserName) LIKE LOWER(?) OR
                    LOWER(FirstName) LIKE LOWER(?) OR
                    LOWER(LastName) LIKE LOWER(?) OR
                    LOWER(Role) LIKE LOWER(?)
            '''
            cursor = connection.cursor()
            search_pattern = f"%{search_key.lower()}%"
            params = [search_pattern] * 5
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [
                User(*row) for row in rows
            ]
        
    def get_all_logs(self) -> list[tuple]:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT id, username, action, description, suspicious, seen, timestamp
                FROM logs
                ORDER BY id DESC
            '''
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    def get_unread_suspicious_logs(self) -> list[tuple]:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT id, username, action, description, suspicious, seen, timestamp
                FROM logs
                WHERE suspicious = 'Yes' AND seen = 'No'
                ORDER BY id DESC
            '''
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    def mark_logs_as_seen(self, log_ids: list[int]):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            for log_id in log_ids:
                cursor.execute("UPDATE logs SET seen = 'Yes' WHERE id = ?", (log_id,))
            connection.commit()

    def get_restore_code_entry(self, code: str, user_id: str) -> dict | None:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT backup_file, used
                FROM restore_codes
                WHERE code = ? AND target_admin_id = ?
            '''
            cursor = connection.cursor()
            cursor.execute(query, (code, user_id))
            row = cursor.fetchone()
            if row:
                return {
                    "backup_file": row[0],
                    "used": bool(row[1])
                }
            return None
        
    def get_restore_codes_for_admin(self, admin_id: str) -> list[tuple]:
        with sqlite3.connect(self.db_path) as conn:
            query = '''
                SELECT code, backup_file
                FROM restore_codes
                WHERE target_admin_id = ?
                ORDER BY rowid DESC
            '''
            cursor = conn.cursor()
            cursor.execute(query, (admin_id,))
            return cursor.fetchall()
        
    def get_all_system_admins(self) -> list[tuple]:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT UserID, FirstName, LastName, UserName
                FROM users
                WHERE role = 'system_admin'
                ORDER BY LastName ASC
            '''
            cursor = connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()




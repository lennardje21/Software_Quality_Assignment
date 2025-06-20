import sqlite3, os, sys
from DataModels.user import User
from DataModels.traveller import Traveller
from DataModels.scooter import Scooter
from Logic.cryptography import Cryptography

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class GetData:
    def __init__(self):
        self.db_path = os.path.join(sys.path[0], "Database/urbanmobility.db")
        self.cryptography = Cryptography()
    
    def get_all_users(self) -> list[User]:
        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()

        users = []
        for row in rows:
            users.append(User(
                id=row[0],
                username=self.cryptography.decrypt(row[1]),
                password_hash=row[2],
                first_name=self.cryptography.decrypt(row[3]),
                last_name=self.cryptography.decrypt(row[4]),
                role=self.cryptography.decrypt(row[5]),
                registration_date=self.cryptography.decrypt(row[6]),
                must_change_password=row[7]
            ))
        return users
    
    def get_all_travellers(self) -> list[Traveller]:
        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM travellers")
            rows = cursor.fetchall()

        travellers: list[Traveller] = []
        for r in rows:
            travellers.append(Traveller(
                r["TravellerID"],
                self.cryptography.decrypt(r["FirstName"]),
                self.cryptography.decrypt(r["LastName"]),
                self.cryptography.decrypt(r["Birthday"]),
                self.cryptography.decrypt(r["Gender"]),
                self.cryptography.decrypt(r["StreetName"]),
                self.cryptography.decrypt(r["HouseNumber"]),
                self.cryptography.decrypt(r["ZipCode"]),
                self.cryptography.decrypt(r["City"]),
                self.cryptography.decrypt(r["Email"]),
                self.cryptography.decrypt(r["MobilePhone"]),
                self.cryptography.decrypt(r["DrivingLicenseNumber"]),
                self.cryptography.decrypt(r["RegistrationDate"])
            ))
        return travellers
    
    def get_all_scooters(self) -> list[Scooter]:
        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM scooter")
            rows = cursor.fetchall()

        scooters: list[Scooter] = []
        for r in rows:
            decrypt = self.cryptography.decrypt
            scooters.append(Scooter(
                r["ScooterID"],
                decrypt(r["Brand"]),
                decrypt(r["Model"]),
                decrypt(r["SerialNumber"]),
                decrypt(r["TopSpeed"]),
                decrypt(r["BatteryCapacity"]),
                decrypt(r["StateOfCharge"]),
                decrypt(r["TargetSOCMin"]),
                decrypt(r["TargetSOCMax"]),
                decrypt(r["Latitude"]),
                decrypt(r["Longitude"]),
                decrypt(r["OutOfServiceStatus"]),
                decrypt(r["Mileage"]),
                decrypt(r["LastMaintenanceDate"]),
                decrypt(r["InServiceDate"])
            ))
        return scooters

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
            
            if row:
                decrypt = self.cryptography.decrypt
                return User(
                    id=row[0],
                    username=decrypt(row[1]),
                    password_hash=row[2],
                    first_name=decrypt(row[3]),
                    last_name=decrypt(row[4]),
                    role=decrypt(row[5]),
                    registration_date=decrypt(row[6]),
                    must_change_password=row[7]
                )
        return None

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
            
            if row:
                decrypt = self.cryptography.decrypt
                return Traveller(
                    row[0],
                    decrypt(row[1]),
                    decrypt(row[2]),
                    decrypt(row[3]),
                    decrypt(row[4]),
                    decrypt(row[5]),
                    decrypt(row[6]),
                    decrypt(row[7]),
                    decrypt(row[8]),
                    decrypt(row[9]),
                    decrypt(row[10]),
                    decrypt(row[11]),
                    decrypt(row[12])
                )
        return None

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
            
            if row:
                decrypt = self.cryptography.decrypt
                return Scooter(
                    row[0],
                    decrypt(row[1]),
                    decrypt(row[2]),
                    decrypt(row[3]),
                    decrypt(row[4]),
                    decrypt(row[5]),
                    decrypt(row[6]),
                    decrypt(row[7]), 
                    decrypt(row[8]),  
                    decrypt(row[9]),  
                    decrypt(row[10]),  
                    decrypt(row[11]), 
                    decrypt(row[12]),  
                    decrypt(row[13]), 
                    decrypt(row[14])  
                )
        return None

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
                    LastMaintenanceDate LIKE ? OR
                    InServiceDate LIKE ?
            '''
            cursor = connection.cursor()
            search_pattern = f"%{search_key.lower()}%"
            date_pattern = f"%{search_key}%"
            
            params = [search_pattern] * 13 + [date_pattern] * 2
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            scooters = []
            for row in rows:
                decrypt = self.cryptography.decrypt
                scooters.append(Scooter(
                    row[0], 
                    decrypt(row[1]), 
                    decrypt(row[2]), 
                    decrypt(row[3]),
                    decrypt(row[4]),
                    decrypt(row[5]), 
                    decrypt(row[6]),
                    decrypt(row[7]),
                    decrypt(row[8]),
                    decrypt(row[9]),
                    decrypt(row[10]),
                    decrypt(row[11]),
                    decrypt(row[12]),
                    decrypt(row[13]),
                    decrypt(row[14])
                ))
            return scooters

    def get_user_by_partial(self, search_key: str) -> list[User]:
        with sqlite3.connect(self.db_path) as connection:
            query = '''SELECT * FROM users'''
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            users = []
            for row in rows:
                decrypt = self.cryptography.decrypt
                decrypted_user = User(
                    id=row[0],
                    username=decrypt(row[1]),
                    password_hash=row[2],
                    first_name=decrypt(row[3]),
                    last_name=decrypt(row[4]),
                    role=decrypt(row[5]),
                    registration_date=decrypt(row[6]),
                    must_change_password=row[7]
                )
                users.append(decrypted_user)

            search_key_lower = search_key.lower()
            filtered = [
                u for u in users if
                search_key_lower in u.id.lower() or
                search_key_lower in u.username.lower() or
                search_key_lower in u.first_name.lower() or
                search_key_lower in u.last_name.lower() or
                search_key_lower in u.role.lower() or
                search_key in u.registration_date
            ]

            return filtered

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
            
            decrypted_rows = []
            for row in rows:
                decrypt = self.cryptography.decrypt
                decrypted_row = (
                    row[0],
                    decrypt(row[1]),
                    decrypt(row[2]),
                    decrypt(row[3]),
                    decrypt(row[4]),
                    decrypt(row[5]), 
                    decrypt(row[6])
                )
                decrypted_rows.append(decrypted_row)
            
            return decrypted_rows

    def get_unread_suspicious_logs(self) -> list[dict]:
        with sqlite3.connect(self.db_path) as connection:
            query = '''
                SELECT id, username, action, description, suspicious, seen, timestamp
                FROM logs
                WHERE suspicious = ? AND seen = ?
                ORDER BY id DESC
            '''
            cursor = connection.cursor()
            cursor.execute(query, (self.cryptography.encrypt('Yes'), self.cryptography.encrypt('No')))
            rows = cursor.fetchall()
            
            decrypted_logs = []
            for row in rows:
                decrypt = self.cryptography.decrypt
                decrypted_log = {
                    "id": row[0],
                    "username": decrypt(row[1]), 
                    "action": decrypt(row[2]),
                    "description": decrypt(row[3]), 
                    "suspicious": decrypt(row[4]),
                    "seen": decrypt(row[5]), 
                    "timestamp": decrypt(row[6]) 
                }
                decrypted_logs.append(decrypted_log)
            
            return decrypted_logs

    def get_restore_code_entry(self, code: str, user_id: str) -> dict | None:
        with sqlite3.connect(self.db_path) as connection:
            query = "SELECT code, target_admin_id, backup_file, used FROM restore_codes"
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
            for row in rows:
                decrypt = self.cryptography.decrypt
                try:
                    decrypted_code = decrypt(row[0])
                    decrypted_admin_id = decrypt(row[1])
                    
                    if decrypted_code == code and decrypted_admin_id == user_id:
                        return {
                            "backup_file": decrypt(row[2]),
                            "used": bool(row[3])
                        }
                except Exception as e:
                    print(f"Error decrypting restore code: {e}")
                    continue
            return None

    def get_restore_codes_for_admin(self, admin_id: str) -> list[tuple]:
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT code, target_admin_id, backup_file FROM restore_codes ORDER BY rowid DESC"
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                decrypt = self.cryptography.decrypt
                try:
                    decrypted_admin_id = decrypt(row[1])
                    if decrypted_admin_id == admin_id:
                        result.append((decrypt(row[0]), decrypt(row[2])))
                except Exception as e:
                    print(f"Error decrypting restore code: {e}")
                    continue
            return result

    def get_all_system_admins(self) -> list[tuple]:
        with sqlite3.connect(self.db_path) as connection:
            query = "SELECT UserID, FirstName, LastName, UserName, Role FROM users"
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                decrypt = self.cryptography.decrypt
                try:
                    decrypted_role = decrypt(row[4])
                    if decrypted_role == 'system_admin':
                        result.append((
                            row[0],
                            decrypt(row[1]), 
                            decrypt(row[2]),
                            decrypt(row[3])
                        ))
                except Exception as e:
                    print(f"Error decrypting user data: {e}")
                    continue
                    
            result.sort(key=lambda x: x[2])
            return result

    def get_unused_restore_codes_for_admin(self, target_admin_id: str) -> list[tuple[str, str]]:
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT code, target_admin_id, backup_file FROM restore_codes WHERE used = 0")
                rows = cursor.fetchall()

                decrypted = []
                for enc_code, enc_admin_id, enc_backup_file in rows:
                    decrypted_admin_id = self.cryptography.decrypt(enc_admin_id)
                    if decrypted_admin_id == target_admin_id:
                        code = self.cryptography.decrypt(enc_code)
                        backup_file = self.cryptography.decrypt(enc_backup_file)
                        decrypted.append((code, backup_file))

                return decrypted
        except Exception as e:
            print(f"Error retrieving restore codes: {e}")
            return []

import sqlite3, os, sys
from DataModels.user import User
from DataModels.traveller import Traveller
from DataModels.scooter import Scooter
from Logic.cryptography import Cryptography
#from DataModels.log import Log # Nog niet gebruikt

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class GetData:
    def __init__(self):
        self.db_path = os.path.join(sys.path[0], "Database/urbanmobility.db")
        self.cryptography = Cryptography()
    
    def get_all_users(self) -> list[User]:
        with sqlite3.connect(self.db_path) as connection:
            # so we can access rows by column name
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()

        users = []
        for row in rows:
            users.append(User(
                id=row[0],
                username=self.cryptography.decrypt(row[1]),  # Decrypt username
                password_hash=row[2],  # Password hash stays as is
                first_name=self.cryptography.decrypt(row[3]),  # Decrypt first name
                last_name=self.cryptography.decrypt(row[4]),  # Decrypt last name
                role=self.cryptography.decrypt(row[5]),  # Decrypt role
                registration_date=self.cryptography.decrypt(row[6]),  # Decrypt reg date
                must_change_password=row[7]  # Integer flag, no encryption
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
                int(decrypt(r["TopSpeed"])),
                int(decrypt(r["BatteryCapacity"])),
                int(decrypt(r["StateOfCharge"])),
                int(decrypt(r["TargetSOCMin"])),
                int(decrypt(r["TargetSOCMax"])),
                float(decrypt(r["Latitude"])),
                float(decrypt(r["Longitude"])),
                int(decrypt(r["OutOfServiceStatus"])),
                int(decrypt(r["Mileage"])),
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
                    id=row[0],  # UserID (not encrypted)
                    username=decrypt(row[1]),  # Username
                    password_hash=row[2],  # Password hash stays as is
                    first_name=decrypt(row[3]),  # FirstName
                    last_name=decrypt(row[4]),  # LastName
                    role=decrypt(row[5]),  # Role
                    registration_date=decrypt(row[6]),  # RegistrationDate
                    must_change_password=row[7]  # MustChangePassword (not encrypted)
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
                    row[0],  # TravellerID (not encrypted)
                    decrypt(row[1]),  # FirstName
                    decrypt(row[2]),  # LastName
                    decrypt(row[3]),  # Birthday
                    decrypt(row[4]),  # Gender
                    decrypt(row[5]),  # StreetName
                    decrypt(row[6]),  # HouseNumber
                    decrypt(row[7]),  # ZipCode
                    decrypt(row[8]),  # City
                    decrypt(row[9]),  # Email
                    decrypt(row[10]),  # MobilePhone
                    decrypt(row[11]),  # DrivingLicenseNumber
                    decrypt(row[12])   # RegistrationDate
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
                    row[0],  # ScooterID (not encrypted)
                    decrypt(row[1]),  # Brand
                    decrypt(row[2]),  # Model
                    decrypt(row[3]),  # SerialNumber
                    int(decrypt(row[4])),  # TopSpeed
                    int(decrypt(row[5])),  # BatteryCapacity
                    int(decrypt(row[6])),  # StateOfCharge
                    int(decrypt(row[7])),  # TargetSOCMin
                    int(decrypt(row[8])),  # TargetSOCMax
                    float(decrypt(row[9])),  # Latitude
                    float(decrypt(row[10])),  # Longitude
                    int(decrypt(row[11])),  # OutOfServiceStatus
                    int(decrypt(row[12])),  # Mileage
                    decrypt(row[13]),  # LastMaintenanceDate
                    decrypt(row[14])   # InServiceDate
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
                    row[0],  # ScooterID (not encrypted)
                    decrypt(row[1]),  # Brand
                    decrypt(row[2]),  # Model
                    decrypt(row[3]),  # SerialNumber
                    int(decrypt(row[4])),  # TopSpeed
                    int(decrypt(row[5])),  # BatteryCapacity
                    int(decrypt(row[6])),  # StateOfCharge
                    int(decrypt(row[7])),  # TargetSOCMin
                    int(decrypt(row[8])),  # TargetSOCMax
                    float(decrypt(row[9])),  # Latitude
                    float(decrypt(row[10])),  # Longitude
                    int(decrypt(row[11])),  # OutOfServiceStatus
                    int(decrypt(row[12])),  # Mileage
                    decrypt(row[13]),  # LastMaintenanceDate
                    decrypt(row[14])   # InServiceDate
                ))
            return scooters

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
            
            users = []
            for row in rows:
                decrypt = self.cryptography.decrypt
                users.append(User(
                    id=row[0],  # UserID (not encrypted)
                    username=decrypt(row[1]),  # Username
                    password_hash=row[2],  # Password hash stays as is
                    first_name=decrypt(row[3]),  # FirstName
                    last_name=decrypt(row[4]),  # LastName
                    role=decrypt(row[5]),  # Role
                    registration_date=decrypt(row[6]),  # RegistrationDate
                    must_change_password=row[7]  # MustChangePassword (not encrypted)
                ))
            return users

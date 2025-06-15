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
            query = ''' SELECT *
                        FROM users'''
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [
                User(*row) for row in rows
            ]
    
    def get_all_travellers(self) -> list[Traveller]:
        with sqlite3.connect(self.db_path) as connection:
            query = ''' SELECT *
                        FROM travellers'''
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [
                Traveller(*row) for row in rows
            ]
    
    def get_all_scooters(self) -> list[Scooter]:
        with sqlite3.connect(self.db_path) as connection:
            query = ''' SELECT *
                        FROM scooter'''
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [
                Scooter(*row) for row in rows
            ]

    def get_user_by_id(self, user_id: int) -> User:
        with sqlite3.connect(self.db_path) as connection:
            query = ''' SELECT *
                        FROM users
                        WHERE UserID = ?'''
            cursor = connection.cursor()
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            return User(*row) if row else None

    def get_traveller_by_id(self, traveller_id: int) -> Traveller:
        with sqlite3.connect(self.db_path) as connection:
            query = ''' SELECT *
                        FROM travellers
                        WHERE TravellerID = ?'''
            cursor = connection.cursor()    
            cursor.execute(query, (traveller_id,))
            row = cursor.fetchone()
            return Traveller(*row) if row else None

    def get_scooter_by_id(self, scooter_id: int) -> Scooter:
        with sqlite3.connect(self.db_path) as connection:
            query = ''' SELECT *
                        FROM scooter
                        WHERE ScooterID = ?'''
            cursor = connection.cursor()
            cursor.execute(query, (scooter_id,))
            row = cursor.fetchone()
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


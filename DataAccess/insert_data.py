import sqlite3, os, sys
from DataModels.user import User
from DataModels.traveller import Traveller
from DataModels.scooter import Scooter
#from DataModels.log import Log  # Nog niet gebruikt

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class InsertData:
    def __init__(self) -> None:
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Database', 'urbanmobility.db')

    def insert_traveller(self, traveller: Traveller) -> bool:
        try:
            with sqlite3.connect(self.db_path) as connection:
                query = '''
                    INSERT OR REPLACE INTO travellers (
                        TravellerID, FirstName, LastName, Birthday, Gender,
                        StreetName, HouseNumber, ZipCode, City, Email,
                        MobilePhone, DrivingLicenseNumber, RegistrationDate
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                cursor = connection.cursor()
                cursor.execute(query, [
                    traveller.id, traveller.first_name, traveller.last_name,
                    traveller.birthday, traveller.gender, traveller.street_name,
                    traveller.house_number, traveller.zip_code, traveller.city,
                    traveller.email_address, traveller.mobile_phone,
                    traveller.driving_license_number, traveller.registration_date
                ])
            return True
        except Exception as e:
            print(f"Error upserting traveller: {e}")
            return False

    def insert_user(self, user: User) -> bool:
        try:
            with sqlite3.connect(self.db_path) as connection:
                query = '''
                    INSERT OR REPLACE INTO users (
                        UserID, UserName, PasswordHash, 
                        FirstName, LastName, Role, RegistrationDate, MustChangePassword
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                '''
                cursor = connection.cursor()
                cursor.execute(query, [
                    user.id, user.username, user.password_hash,
                    user.first_name, user.last_name, user.role, user.registration_date, user.must_change_password
                ])
            return True
        except Exception as e:
            print(f"Error upserting user: {e}")
            return False

    def insert_scooter(self, scooter: Scooter) -> bool:
        try:
            with sqlite3.connect(self.db_path) as connection:
                query = '''
                    INSERT OR REPLACE INTO scooter (
                        ScooterID, Brand, Model, SerialNumber, TopSpeed, BatteryCapacity,
                        StateOfCharge, TargetSOCMin, TargetSOCMax,
                        Latitude, Longitude, OutOfServiceStatus, Mileage,
                        LastMaintenanceDate, InServiceDate
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                cursor = connection.cursor()
                cursor.execute(query, [
                    scooter.id, scooter.brand, scooter.model, scooter.serial_number,
                    scooter.top_speed, scooter.battery_capacity, scooter.state_of_charge,
                    scooter.target_soc_min, scooter.target_soc_max,
                    scooter.latitude, scooter.longitude, scooter.out_of_service_status,
                    scooter.mileage, scooter.last_maintenance_date, scooter.in_service_date
                ])
            return True
        except Exception as e:
            print(f"Error upserting scooter: {e}")
            return False
    
    def insert_log(self, log) -> bool:
        #Nog niet gebruikt
        pass
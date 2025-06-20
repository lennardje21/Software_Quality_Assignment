import sqlite3, os, sys
from DataModels.user import User
from DataModels.traveller import Traveller
from DataModels.scooter import Scooter
from Logic.cryptography import Cryptography
#from DataModels.log import Log  # Nog niet gebruikt

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class InsertData:
    def __init__(self) -> None:
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Database', 'urbanmobility.db')
        self.cryptography = Cryptography()

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
                    traveller.id, self.cryptography.encrypt(traveller.first_name), 
                    self.cryptography.encrypt(traveller.last_name), self.cryptography.encrypt(traveller.birthday), 
                    self.cryptography.encrypt(traveller.gender), self.cryptography.encrypt(traveller.street_name), 
                    self.cryptography.encrypt(traveller.house_number), self.cryptography.encrypt(traveller.zip_code), 
                    self.cryptography.encrypt(traveller.city), self.cryptography.encrypt(traveller.email_address), 
                    self.cryptography.encrypt(traveller.mobile_phone), self.cryptography.encrypt(traveller.driving_license_number), 
                    self.cryptography.encrypt(traveller.registration_date)
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
                    user.id, self.cryptography.encrypt(user.username), user.password_hash,
                    self.cryptography.encrypt(user.first_name), self.cryptography.encrypt(user.last_name),
                    self.cryptography.encrypt(user.role), self.cryptography.encrypt(user.registration_date), user.must_change_password
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
                    scooter.id, self.cryptography.encrypt(scooter.brand), self.cryptography.encrypt(scooter.model), 
                    self.cryptography.encrypt(scooter.serial_number), self.cryptography.encrypt(str(scooter.top_speed)), 
                    self.cryptography.encrypt(str(scooter.battery_capacity)), self.cryptography.encrypt(str(scooter.state_of_charge)),
                    self.cryptography.encrypt(str(scooter.target_soc_min)), self.cryptography.encrypt(str(scooter.target_soc_max)),
                    self.cryptography.encrypt(str(scooter.latitude)), self.cryptography.encrypt(str(scooter.longitude)),
                    self.cryptography.encrypt(str(scooter.out_of_service_status)), self.cryptography.encrypt(str(scooter.mileage)), 
                    self.cryptography.encrypt(scooter.last_maintenance_date), self.cryptography.encrypt(scooter.in_service_date)])
            return True
        except Exception as e:
            print(f"Error upserting scooter: {e}")
            return False
    
    def insert_log(self, log) -> bool:
        #Nog niet gebruikt
        pass
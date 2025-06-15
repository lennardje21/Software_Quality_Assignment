# Logic/scooter_logic.py
from DataAccess.get_data import GetData
from DataModels.user import User
from DataAccess.insert_data import InsertData
from DataModels.scooter import Scooter
from DataAccess.delete_data import DeleteData
import uuid, time


class ScooterLogic:

    @staticmethod
    def create_scooter_object(user: User, brand, model, 
                    serial_number, top_speed, battery_capacity, 
                    state_of_charge, target_soc_min, target_soc_max, 
                    latitude, longitude, out_of_service_status, mileage, 
                    last_maintenance_date):
        if user.is_authorized("system_admin"):
            scooter = Scooter(str(uuid.uuid4()), brand, model, serial_number, 
                              top_speed, battery_capacity, state_of_charge, 
                              target_soc_min, target_soc_max, latitude, 
                              longitude, out_of_service_status, mileage, 
                              last_maintenance_date, time.strftime("%Y-%m-%d"))
            return scooter
        else:
            return False
    
    @staticmethod
    def add_scooter(user: User, scooter: Scooter):
        if user.is_authorized("system_admin"):
            insertData = InsertData()
            insertData.insert_scooter(scooter)
            return True
        else:
            return False

    @staticmethod
    def modify_scooter(user: User, scooter_id: int):
        if user.is_authorized("system_admin"):
            print(f"[ScooterLogic] Modifying scooter {scooter_id}...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def delete_scooter(user: User, scooter_id: int):
        if user.is_authorized("system_admin"):
            deleteData = DeleteData()
            deleteData.delete_scooter(scooter_id)
            return True
        else:
            return False

    @staticmethod
    def update_scooter_partial(user: User, scooter: Scooter):
        if user.is_authorized("service_engineer"):
            insertData = InsertData()
            insertData.insert_scooter(scooter)
            return True
        else:
            return False

    @staticmethod
    def search_scooter(user: User, search_key: str = None) -> list:
        if user.is_authorized("service_engineer"):
            getData = GetData()
            return getData.get_scooter_by_partial(search_key)
        else:
            return None
    
    @staticmethod
    def assign_right_types(scooter, field, value):
        """Convert user input to appropriate types for each field."""
        try:
            if field == "state_of_charge":
                scooter.state_of_charge = int(float(value))
            elif field == "target_soc_min":
                scooter.target_soc_min = int(float(value))
            elif field == "target_soc_max":
                scooter.target_soc_max = int(float(value))
            elif field == "latitude":
                scooter.latitude = float(value)
            elif field == "longitude":
                scooter.longitude = float(value)
            elif field == "out_of_service_status":
                # Convert yes/no/true/false to boolean
                scooter.out_of_service_status = value.lower() in ['yes', 'true', '1', 'y']
            elif field == "mileage":
                scooter.mileage = int(float(value))
            elif field == "last_maintenance_date":
                # No conversion needed - keep as string
                scooter.last_maintenance_date = value
            elif field == "brand":
                scooter.brand = value
            elif field == "model":
                scooter.model = value
            elif field == "serial_number":
                scooter.serial_number = value
            elif field == "top_speed":
                scooter.top_speed = int(float(value))
            elif field == "battery_capacity":
                scooter.battery_capacity = int(float(value))
            else:
                print(f"Field '{field}' is not editable.")
                return False
            return scooter
        except ValueError:
            print(f"Invalid value format for field '{field}'. Please check and try again.")
            time.sleep(2)
            return False

    @staticmethod
    def find_scooter_by_id(scooters, scooter_id):
        for scooter in scooters:
            if scooter.id == scooter_id:
                return scooter
        return None


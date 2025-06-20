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

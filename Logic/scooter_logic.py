# Logic/scooter_logic.py

from DataModels.user import User

class ScooterLogic:

    @staticmethod
    def add_scooter(user: User):
        if user.is_authorized("system_admin"):
            print("[ScooterLogic] Adding new scooter...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def modify_scooter(user: User, scooter_id: int):
        if user.is_authorized("system_admin"):
            print(f"[ScooterLogic] Modifying scooter {scooter_id}...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def delete_scooter(user: User, scooter_id: int):
        if user.is_authorized("system_admin"):
            print(f"[ScooterLogic] Deleting scooter {scooter_id}...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def update_scooter_partial(user: User, scooter_id: int):
        if user.is_authorized("service_engineer"):
            print(f"[ScooterLogic] Updating partial attributes of scooter {scooter_id} (service_engineer)...")
            # NOTE: later when you implement this, limit the fields allowed for service_engineer
        else:
            print("Unauthorized action.")

    @staticmethod
    def search_scooter(user: User):
        if user.is_authorized("service_engineer"):
            print("[ScooterLogic] Searching for scooters...")
        else:
            print("Unauthorized action.")

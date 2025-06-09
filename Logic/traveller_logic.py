# Logic/traveller_logic.py

from DataModels.user import User

class TravellerLogic:

    @staticmethod
    def add_traveller(user: User):
        if user.is_authorized("system_admin"):
            print("[TravellerLogic] Adding new traveller...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def modify_traveller(user: User, traveller_id: int):
        if user.is_authorized("system_admin"):
            print(f"[TravellerLogic] Modifying traveller {traveller_id}...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def delete_traveller(user: User, traveller_id: int):
        if user.is_authorized("system_admin"):
            print(f"[TravellerLogic] Deleting traveller {traveller_id}...")
        else:
            print("Unauthorized action.")

    @staticmethod
    def search_traveller(user: User):
        if user.is_authorized("system_admin"):
            print("[TravellerLogic] Searching for travellers...")
        else:
            print("Unauthorized action.")

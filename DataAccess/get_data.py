import sqlite3, os, sys
from DataModels.user import User
from DataModels.traveller import Traveller
from DataModels.scooter import Scooter
from DataModels.log import Log # Nog niet gebruikt

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class GetData:
    def __init__(self):
        pass

    def get_all_user(self):
        connection = sqlite3.connect(os.path.join(
            sys.path[0], "Database/membermanagement.db"))
        query = ''' SELECT *
                    FROM users'''
    
    def get_all_traveller(self):
        pass
    
    def get_all_scooter(self):
        pass
    
    def get_all_log(self):
        #Nog niet gebruikt
        pass

    def get_user_by_id(self, user_id: int) -> User:
        pass

    def get_traveller_by_id(self, traveller_id: int) -> Traveller:
        pass

    def get_scooter_by_id(self, scooter_id: int) -> Scooter:
        pass

    def get_log_by_id(self, log_id: int) -> Log:
        #Nog niet gebruikt
        pass

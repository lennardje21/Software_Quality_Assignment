from DataAccess.insert_data import InsertData
from DataModels.traveller import Traveller
from DataModels.user import User
from DataModels.scooter import Scooter
from Logic.user_logic import UserLogic
#from DataModels.log import Log # nog niet gebruikt
import os, sys
import uuid

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def seed():
    travellers = [
        Traveller(f"{uuid.uuid4()}", 'John', 'Doe', '01-02-1999', 'Male', 'Main St', '01', '1234AB', 'AMSTERDAM', 'johndoe@email.com', '+31-6-23456778', 'AB1234567', '01-04-2024'), 
        Traveller(f"{uuid.uuid4()}", 'Jane', 'Smith', '01-02-1999', 'Female', 'Elm St', '04', '5432PK', 'ROTTERDAM', 'jane.smith@example.com', '+31-6-15237486', 'AB2231567', '02-04-2024'),
        Traveller(f"{uuid.uuid4()}", 'Mike', 'Johnson', '01-02-1999', 'Male', 'Oak St', '03', '6789AW', 'ALMERE', 'mike.johnson@example.com', '+31-6-04236485', 'AB3231567', '03-04-2024')
    ]

    # Nog geen password hash en super admin moet hard coded zijn zoals if username.lower() == 'super_admin' and password == 'Admin_123?':
    users = [
        User(f"{uuid.uuid4()}", 'systemadmin', UserLogic.hash_password('systemadminpass'), 'System', 'Admin', 'system_admin', '2024-04-01', 0),
        User(f"{uuid.uuid4()}", 'service', UserLogic.hash_password('servicepass'), 'Service', 'Engineer', 'service_engineer', '2024-04-02', 0),
        User(f"{uuid.uuid4()}", 'super_admin', UserLogic.hash_password('Admin_123?'), 'Super', 'Admin', 'super_admin', '2024-04-03', 0),
    ]

    scooters = [
        Scooter(
            f"{uuid.uuid4()}", 'Segway', 'Ninebot Max G30', 'SN1234567890',
            25, 551, 85, 20, 90, 51.9225, 4.47917, False, 1200,
            '2025-04-15', '2025-01-02'
        ),
        Scooter(
            f"{uuid.uuid4()}", 'NIU', 'KQi3 Pro', 'SN9876543210',
            30, 600, 92, 25, 95, 51.9230, 4.48000, False, 800,
            '2025-05-01', '2025-01-01'
        ),
        Scooter(
            f"{uuid.uuid4()}", 'Xiaomi', 'Mi Scooter 4 Pro', 'SN1928374650',
            20, 474, 65, 15, 85, 51.9210, 4.47800, True, 1500,
            '2025-03-10', '2025-01-03'
        )
    ]

    #Logs invoeren

    insertdata = InsertData()
    # Insert dummy data into the database
    for traveller in travellers:
        insertdata.insert_traveller(traveller)

    for user in users:
        insertdata.insert_user(user)

    for scooter in scooters:
        insertdata.insert_scooter(scooter)

if __name__ == "__main__":
    seed()
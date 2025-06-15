# main.py
from Presentation.home_screen import HomeScreen
import os, sys
from DataAccess.create_tables import create_tables
from DataAccess.seeder import seed
from DataAccess.delete_data import DeleteData
import time



# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == "__main__":
    #deleteData = DeleteData()
    #deleteData.clear_database()
    #print("Database cleared.")
    #create_tables()
    #seed()
    #print("Database initialized and seeded with sample data.")
    #time.sleep(1)
    HomeScreen.display()

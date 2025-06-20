# main.py
from Presentation.home_screen import HomeScreen
from DataAccess.create_tables import create_tables
from DataAccess.seeder import seed
from DataAccess.delete_data import DeleteData
import time, os, sys



# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
def clear_and_seed_database():
    deleteData = DeleteData()
    deleteData.clear_database()
    print("Database cleared.")
    create_tables()
    seed()
    print("Database initialized and seeded with sample data.")
    time.sleep(3)

if __name__ == "__main__":
    #clear_and_seed_database()
    HomeScreen.display()

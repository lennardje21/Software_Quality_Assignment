from DataAccess.create_tables import create_tables
from DataAccess.insert_data import InsertData
from DataAccess.seeder import seed
import os, sys

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == "__main__":
    #create_tables()
    seed()

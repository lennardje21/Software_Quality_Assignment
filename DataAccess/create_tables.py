import sqlite3, os, sys

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_tables():
    # Get the project root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database_dir = os.path.join(project_root, 'Database')
    database_path = os.path.join(database_dir, 'urbanmobility.db')
    
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)

    connection = sqlite3.connect(database_path)
    
    create_travellers_table = '''
    CREATE TABLE IF NOT EXISTS travellers (
        TravellerID TEXT PRIMARY KEY,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Birthday TEXT,
        Gender TEXT,
        StreetName TEXT,
        HouseNumber TEXT,
        ZipCode TEXT,
        City TEXT,
        Email TEXT UNIQUE,
        MobilePhone TEXT UNIQUE,
        DrivingLicenseNumber TEXT UNIQUE,
        RegistrationDate TEXT
    );
    '''
    
    create_users_table = '''
    CREATE TABLE IF NOT EXISTS users (
        UserID TEXT PRIMARY KEY,
        UserName TEXT NOT NULL UNIQUE,
        PasswordHash TEXT NOT NULL,
        FirstName TEXT,
        LastName TEXT,
        Role TEXT NOT NULL,
        RegistrationDate TEXT,
        MustChangePassword INTEGER NOT NULL DEFAULT 0
    );
    '''

    create_scooter_table = '''
    CREATE TABLE IF NOT EXISTS scooter (
        ScooterID TEXT PRIMARY KEY,
        Brand TEXT NOT NULL,
        Model TEXT NOT NULL,
        SerialNumber TEXT NOT NULL UNIQUE,
        TopSpeed INTEGER NOT NULL,
        BatteryCapacity INTEGER NOT NULL,
        StateOfCharge INTEGER NOT NULL,
        TargetSOCMin INTEGER NOT NULL,
        TargetSOCMax INTEGER NOT NULL,
        Latitude REAL NOT NULL,
        Longitude REAL NOT NULL,
        OutOfServiceStatus BOOLEAN NOT NULL,
        Mileage INTEGER NOT NULL,
        LastMaintenanceDate TEXT,
        InServiceDate TEXT
    );
    '''

    create_restore_code_table = '''
    CREATE TABLE IF NOT EXISTS restore_codes (
        code TEXT PRIMARY KEY,
        target_admin_id TEXT NOT NULL,
        backup_file TEXT NOT NULL,
        used INTEGER DEFAULT 0
    );
    '''

    create_log_table = '''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        action TEXT NOT NULL,
        description TEXT NOT NULL,
        suspicious TEXT DEFAULT 'No',
        seen TEXT DEFAULT 'No',
        timestamp TEXT NOT NULL
    );
    '''
    
    cursor = connection.cursor()
    cursor.execute(create_travellers_table)
    cursor.execute(create_users_table)
    cursor.execute(create_scooter_table)
    cursor.execute(create_restore_code_table)
    cursor.execute(create_log_table)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
import time
from Logic.scooter_logic import ScooterLogic
from Presentation.general_shared_methods import general_shared_methods



class scooter_display_methods:

    @staticmethod
    def display_scooter(scooter, search_key=None, user=None):
        if user is None:
            print(f"Scooter ID:         {general_shared_methods.highlight(scooter.id, search_key)}")
            print(f"Brand:              {general_shared_methods.highlight(scooter.brand, search_key)}")
            print(f"Model:              {general_shared_methods.highlight(scooter.model, search_key)}")
            print(f"Serial Number:      {general_shared_methods.highlight(scooter.serial_number, search_key)}")
            print(f"Top Speed:          {general_shared_methods.highlight(scooter.top_speed, search_key)} km/h")
            print(f"Battery Capacity:   {general_shared_methods.highlight(scooter.battery_capacity, search_key)} Wh")
            print(f"State Of Charge:    {general_shared_methods.highlight(scooter.state_of_charge, search_key)}%")
            print(f"Target SOC Min:     {general_shared_methods.highlight(scooter.target_soc_min, search_key)}%")
            print(f"Target SOC Max:     {general_shared_methods.highlight(scooter.target_soc_max, search_key)}%")
            print(f"Latitude:           {general_shared_methods.highlight(scooter.latitude, search_key)}")
            print(f"Longitude:          {general_shared_methods.highlight(scooter.longitude, search_key)}")
            print(f"Out Of Service:     {general_shared_methods.highlight('Yes' if scooter.out_of_service_status else 'No', search_key)}")            
            print(f"Mileage:            {general_shared_methods.highlight(scooter.mileage, search_key)} km")
            print(f"Last Maintenance:   {general_shared_methods.highlight(scooter.last_maintenance_date, search_key)}")
            print(f"In Service Date:    {general_shared_methods.highlight(scooter.in_service_date, search_key)}")
        else:
            is_admin = getattr(user, "role", "").lower() in ["super_admin", "system_admin"]
            editable = "[Editable]" if is_admin else ""
            print(f"Scooter ID:         {scooter.id}")
            print(f"Brand:              {scooter.brand:<23}{editable:>12}")
            print(f"Model:              {scooter.model:<23}{editable:>12}")
            print(f"Serial Number:      {scooter.serial_number:<23}{editable:>12}")
            print(f"Top Speed:          {str(scooter.top_speed) + ' km/h':<23}{editable:>12}")
            print(f"Battery Capacity:   {str(scooter.battery_capacity) + ' Wh':<23}{editable:>12}")
            print(f"State Of Charge:    {str(scooter.state_of_charge) + '%':<25}[Editable]")
            print(f"Target SOC Min:     {str(scooter.target_soc_min) + '%':<25}[Editable]")
            print(f"Target SOC Max:     {str(scooter.target_soc_max) + '%':<25}[Editable]")
            print(f"Latitude:           {str(scooter.latitude):<25}[Editable]")
            print(f"Longitude:          {str(scooter.longitude):<25}[Editable]")
            print(f"Out Of Service:     {str('Yes' if scooter.out_of_service_status else 'No'):<25}[Editable]")
            print(f"Mileage:            {str(scooter.mileage) + ' km':<25}[Editable]")
            print(f"Last Maintenance:   {str(scooter.last_maintenance_date):<25}[Editable]")
            print(f"In Service Date:    {scooter.in_service_date}")

    @staticmethod
    def search_scooter_display(user, update_call=False):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Search for Scooter".center(75) + "|")
        print("----------------------------------------------------------------------------")

        #NOTE INPUT FIELD
        search_key = input("Enter a search key (id, brand, mileage, etc.) or type 'exit' to go back: ")
        search_key = search_key.strip()
        general_shared_methods.clear_console()
        if search_key.lower() == 'exit':
            print("Exiting search...")
            time.sleep(1)
            general_shared_methods.clear_console()
            return True
        
        scooters = ScooterLogic.search_scooter(user, search_key)
        if scooters and len(scooters) > 0:
            print(f"\nFound {len(scooters)} scooter(s) matching '{general_shared_methods.highlight(search_key, search_key)}':")
            time.sleep(1)
            for count, scooter in enumerate(scooters, 1):
                print("----------------------------------------------------------------------------")
                print("|" + f"search result #{count}".center(75) + "|")
                print("----------------------------------------------------------------------------")
                scooter_display_methods.display_scooter(scooter, search_key)
            if update_call:
                return scooters
            return None
        else:
            print("No scooters found matching the search criteria.")
            time.sleep(2)
            general_shared_methods.clear_console()
            return False

    @staticmethod
    def display_update_scooter(user):
        while True:
            scooters = scooter_display_methods.search_scooter_display(user, update_call=True)
            if scooters is True:
                return
            if scooters is False:
                continue 
            
            print("----------------------------------------------------------------------------")
            #NOTE INPUT FIELD
            scooter_id = input("Enter scooter ID number to update (or type 'exit' to cancel): #").strip()
            general_shared_methods.clear_console()
            if scooter_id.lower() == 'exit':
                print("Exiting update...")
                time.sleep(1)
                return
            if scooter_id == '':
                print("Scooter ID cannot be empty. Please try again.")
                time.sleep(1.5)
                continue

            scooter = ScooterLogic.find_scooter_by_id(scooters, scooter_id)
            if scooter is None:
                print(f"No scooter found with ID {scooter_id}. Please try again.")
                time.sleep(2)
                continue

            if user.role == "service_engineer":
                while True:
                    exit_update = scooter_display_methods.partial_update_scooter_display(scooter, user)
                    if exit_update:
                        print("Exiting update...")
                        time.sleep(1)
                        break
                break
            else:
                while True:
                    exit_update = scooter_display_methods.update_scooter_fully(scooter, user)
                    if exit_update:
                        print("Exiting update...")
                        time.sleep(1)
                        break

    @staticmethod
    def display_singular_scooter_field(scooter, field):
        if field == "last_maintenance": field = "last_maintenance_date"
        elif field == "out_of_service": field = "out_of_service_status"
        field_map = {
            "id": scooter.id,
            "brand": scooter.brand,
            "model": scooter.model,
            "serial_number": scooter.serial_number,
            "top_speed": f"{scooter.top_speed} km/h",
            "battery_capacity": f"{scooter.battery_capacity} Wh",
            "state_of_charge": f"{scooter.state_of_charge}%",
            "target_soc_min": f"{scooter.target_soc_min}%",
            "target_soc_max": f"{scooter.target_soc_max}%",
            "latitude": scooter.latitude,
            "longitude": scooter.longitude,
            "out_of_service_status": "Yes" if scooter.out_of_service_status else "No",
            "mileage": f"{scooter.mileage} km",
            "last_maintenance_date": scooter.last_maintenance_date,
            "in_service_date": scooter.in_service_date
        }
        value = f"{field.replace('_', ' ').title()}: {field_map.get(field, '')}"
        return value

    @staticmethod
    def update_scooter(scooter, field, value, user):
        ScooterLogic.assign_right_types(scooter, field, value)
        #NOTE Field waardes moeten geparsed naar de juiste types en gevalideerd worden
        if ScooterLogic.update_scooter_partial(user, scooter):
            return True
        else:
            print("Failed to update scooter. Please check your permissions or the field you are trying to update.")
            time.sleep(2)
            return False
    
    @staticmethod
    def update_scooter_fully(scooter, user):
        editable_fields = [
            "brand",
            "model",
            "serial_number",
            "top_speed",
            "battery_capacity",
            "state_of_charge",
            "target_soc_min",
            "target_soc_max",
            "latitude",
            "longitude",
            "out_of_service_status",
            "mileage",
            "last_maintenance",
        ]
        field_aliases = {
            "last_maintenance": "last_maintenance_date",
            "out_of_service": "out_of_service_status"
        }
        while True:
            field = scooter_display_methods.prompt_for_field(scooter, user, editable_fields, field_aliases)
            if field is None:
                return True

            new_value = scooter_display_methods.prompt_for_value(field, scooter)
            if new_value is None:
                continue

            general_shared_methods.clear_console()
            #NOTE TYPE CHECKING AND ASSIGNING
            scooter_display_methods.update_scooter(scooter, field, new_value, user)
            print(f"Updated {field.replace('_', ' ').title()} for scooter {scooter.id}.")
            time.sleep(2)
            general_shared_methods.clear_console()
            return False  # Return to previous menu after one update

    @staticmethod
    def display_delete_scooter(user):
        while True:
            scooters = scooter_display_methods.search_scooter_display(user, update_call=True)
            if scooters is True:
                return
            if scooters is False:
                continue
            
            print("----------------------------------------------------------------------------")
            #NOTE INPUT FIELD
            scooter_id = input("Enter scooter ID number to delete (or type 'exit' to cancel): #").strip()
            general_shared_methods.clear_console()
            if scooter_id.lower() == 'exit':
                print("Exiting deletion...")
                time.sleep(1)
                return
            if scooter_id == '':
                print("Scooter ID cannot be empty. Please try again.")
                time.sleep(1.5)
                continue

            scooter = ScooterLogic.find_scooter_by_id(scooters, scooter_id)
            if scooter is None:
                print(f"No scooter found with ID {scooter_id}. Please try again.")
                time.sleep(2)
                continue

            while True:
                exit_update = scooter_display_methods.display_delete_scooter_confirm(scooter, user)
                if exit_update == True:
                    general_shared_methods.clear_console()
                    print("Exiting Deletion...")
                    time.sleep(1)
                    break
                
    @staticmethod
    def display_delete_scooter_confirm(scooter, user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Delete Scooter".center(75) + "|")
        print("----------------------------------------------------------------------------")
        scooter_display_methods.display_scooter(scooter, scooter.id)
        print("----------------------------------------------------------------------------")
        
        confirm = input(f"Are you sure you want to delete scooter {scooter.id}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            if ScooterLogic.delete_scooter(user, scooter.id):
                general_shared_methods.clear_console()
                print(f"Scooter {scooter.id} has been deleted successfully.")
                time.sleep(2)
                return True
            else:
                print("Failed to delete scooter. Please check your permissions.")
                time.sleep(2)
                return True
        elif confirm == 'no':
            general_shared_methods.clear_console()
            print("Deletion cancelled.")
            time.sleep(1)
            return True
        else:
            general_shared_methods.clear_console()
            print("Invalid input. Please enter 'yes' or 'no'.")
            time.sleep(1.5)
            return
    
    @staticmethod
    def display_add_scooter(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Add New Scooter".center(75) + "|")
        print("----------------------------------------------------------------------------")
        
        scooter = scooter_display_methods.prompt_for_new_scooter_details(user)
        if scooter is None:
            print("Scooter creation cancelled.")
            time.sleep(1.5)
            return False
        
        if ScooterLogic.add_scooter(user, scooter):
            general_shared_methods.clear_console()
            print(f"Scooter {scooter.id} has been added successfully.")
            time.sleep(2)
            general_shared_methods.clear_console()
            scooter_display_methods.display_scooter(scooter)
            print("----------------------------------------------------------------------------")
            input("Press any key to continue...")
            general_shared_methods.clear_console()
            return True
        else:
            print("Failed to add scooter. Please check your permissions.")
            time.sleep(2)
            return False
    
    @staticmethod
    def prompt_for_new_scooter_details(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Enter New Scooter Details".center(75) + "|")
        print("----------------------------------------------------------------------------")
        
        #NOTE INPUT FIELDS (no type exit and space checking)
        scooter_brand = input("Enter Brand: ").strip()
        scooter_model = input("Enter Model: ").strip()
        scooter_serial_number = input("Enter Serial Number: ").strip()
        
        scooter_top_speed = int(float(input("Enter Top Speed (km/h): ").strip()))
        scooter_battery_capacity = int(float(input("Enter Battery Capacity (Wh): ").strip()))
        scooter_state_of_charge = int(float(input("Enter State of Charge (%): ").strip()))
        scooter_target_soc_min = int(float(input("Enter Target SOC Min (%): ").strip()))
        scooter_target_soc_max = int(float(input("Enter Target SOC Max (%): ").strip()))
        
        scooter_latitude = float(input("Enter Latitude: ").strip())
        scooter_longitude = float(input("Enter Longitude: ").strip())
        
        scooter_out_of_service_status = input("Is the scooter out of service? (yes/no): ").strip().lower() == 'yes'
        
        scooter_mileage = int(float(input("Enter Mileage (km): ").strip()))
        
        scooter_last_maintenance_date = input("Enter Last Maintenance Date (YYYY-MM-DD): ").strip()
        
        scooter = ScooterLogic.create_scooter_object(
            user,
            scooter_brand,
            scooter_model,
            scooter_serial_number,
            scooter_top_speed,             
            scooter_battery_capacity,      
            scooter_state_of_charge,       
            scooter_target_soc_min,        
            scooter_target_soc_max,        
            scooter_latitude,              
            scooter_longitude,             
            scooter_out_of_service_status, 
            scooter_mileage,               
            scooter_last_maintenance_date
        )
        
        return scooter
    
    @staticmethod
    def partial_update_scooter_display(scooter, user):
        editable_fields = [
            "state_of_charge",
            "target_soc_min",
            "target_soc_max",
            "latitude",
            "longitude",
            "out_of_service_status",
            "mileage",
            "last_maintenance",
        ]
        field_aliases = {
            "last_maintenance": "last_maintenance_date",
            "out_of_service": "out_of_service_status"
        }

        while True:
            field = scooter_display_methods.prompt_for_field(scooter, user, editable_fields, field_aliases)
            if field is None:
                return True

            new_value = scooter_display_methods.prompt_for_value(field, scooter)
            if new_value is None:
                continue

            general_shared_methods.clear_console()
            #NOTE TYPE CHECKING AND ASSIGNING
            scooter_display_methods.update_scooter(scooter, field, new_value, user)
            print(f"Updated {field.replace('_', ' ').title()} for scooter {scooter.id}.")
            time.sleep(2)
            general_shared_methods.clear_console()
            return False  # Return to previous menu after one update

    @staticmethod
    def prompt_for_field(scooter, user, editable_fields, field_aliases):
        while True:
            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "Update Scooter Data".center(75) + "|")
            print("----------------------------------------------------------------------------")
            scooter_display_methods.display_scooter(scooter, user=user)
            print("----------------------------------------------------------------------------")
            print("Enter the field you want to update (e.g., state_of_charge, etc.) or type 'exit' to cancel. Use '_' for spaces.")
            field = input("Field to update: ").strip().lower()
            general_shared_methods.clear_console()

            if field == 'exit':
                print("Exiting update...")
                time.sleep(1)
                general_shared_methods.clear_console()
                return None

            # Map aliases to real field names
            field = field_aliases.get(field, field)

            valid_fields = [f if f not in field_aliases else field_aliases[f] for f in editable_fields]
            if field not in valid_fields:
                print(f"Invalid field '{field}'. Please choose from one of the editable fields.")
                time.sleep(2)
                continue

            return field

    @staticmethod
    def prompt_for_value(field, scooter=None):
        while True:
            general_shared_methods.clear_console()
            print(scooter_display_methods.display_singular_scooter_field(scooter, field))
            print("----------------------------------------------------------------------------")
            #NOTE INPUT FIELD
            new_value = input(f"Enter new value for {field} (or type 'exit' to cancel): ").strip()
            general_shared_methods.clear_console()
            if new_value.lower() == 'exit':
                print("Exiting update...")
                time.sleep(1)
                general_shared_methods.clear_console()
                return None
            if new_value == '':
                print("Value cannot be empty. Please enter a value or type 'exit' to cancel.")
                time.sleep(1.5)
                continue
            return new_value
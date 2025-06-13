import time
from Logic.scooter_logic import ScooterLogic

class shared_methods:
    @staticmethod
    def display_scooter(scooter, search_key=None, user=None):
        if user is None:
            from main import highlight
            print(f"Scooter ID:         {highlight(scooter.id, search_key)}")
            print(f"Brand:              {highlight(scooter.brand, search_key)}")
            print(f"Model:              {highlight(scooter.model, search_key)}")
            print(f"Serial Number:      {highlight(scooter.serial_number, search_key)}")
            print(f"Top Speed:          {highlight(scooter.top_speed, search_key)} km/h")
            print(f"Battery Capacity:   {highlight(scooter.battery_capacity, search_key)} Wh")
            print(f"State Of Charge:    {highlight(scooter.state_of_charge, search_key)}%")
            print(f"Target SOC Min:     {highlight(scooter.target_soc_min, search_key)}%")
            print(f"Target SOC Max:     {highlight(scooter.target_soc_max, search_key)}%")
            print(f"Latitude:           {highlight(scooter.latitude, search_key)}")
            print(f"Longitude:          {highlight(scooter.longitude, search_key)}")
            print(f"Out Of Service:     {highlight('Yes' if scooter.out_of_service_status else 'No', search_key)}")            
            print(f"Mileage:            {highlight(scooter.mileage, search_key)} km")
            print(f"Last Maintenance:   {highlight(scooter.last_maintenance_date, search_key)}")
            print(f"In Service Date:    {highlight(scooter.in_service_date, search_key)}")
        else:
            is_admin = getattr(user, "role", "").lower() in ["superadmin", "systemadmin"]
            editable = "[Editable]" if is_admin else ""
            print(f"Brand:              {scooter.brand:<25}{editable:>12}")
            print(f"Model:              {scooter.model:<25}{editable:>12}")
            print(f"Serial Number:      {scooter.serial_number:<25}{editable:>12}")
            print(f"Top Speed:          {str(scooter.top_speed) + ' km/h':<25}{editable:>12}")
            print(f"Battery Capacity:   {str(scooter.battery_capacity) + ' Wh':<25}{editable:>12}")
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
        from main import clear_console, highlight
        clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Search for Scooter".center(75) + "|")
        print("----------------------------------------------------------------------------")

        #NOTE INPUT FIELD
        search_key = input("Enter a search key (id, brand, mileage, etc.) or type 'exit' to go back: ")
        search_key = search_key.strip()
        clear_console()
        if search_key.lower() == 'exit':
            print("Exiting search...")
            time.sleep(1)
            clear_console()
            return True
        
        scooters = ScooterLogic.search_scooter(user, search_key)
        if scooters != None and len(scooters) > 0:
            print(f"\nFound {len(scooters)} scooter(s) matching '{highlight(search_key, search_key)}':")
            time.sleep(1)
            
            count = 1
            for scooter in scooters:
                print("----------------------------------------------------------------------------")
                print("|" + f"search result #{count}".center(75) + "|")
                print("----------------------------------------------------------------------------")
                shared_methods.display_scooter(scooter, search_key)
                count += 1
            if update_call:
                return scooters
            return None
        
        else:
            print("No scooters found matching the search criteria.")
            time.sleep(2)
            clear_console()
            return False
        
    @staticmethod
    def display_update_scooter(user):
        from Presentation.service_engineer_screen import ServiceEngineerScreen
        scooters = shared_methods.search_scooter_display(user, update_call=True)
        
        #NOTE INPUT FIELD
        scooter_id = input("Enter scooter ID number to update: #").strip()
        exit = False
        for scooter in scooters:
            if scooter.id == scooter_id:
                if user.role == "service_engineer":
                    while True:
                        exit = ServiceEngineerScreen.partial_update_scooter_display(scooter, user)
                        if exit == True:
                            print("Exiting update...")
                            time.sleep(1)
                            break
                    break
                else:
                    continue # NOG MAKEN SYSTEM EN SUPER ADMIN
        else:
            print(f"No scooter found with ID {scooter_id}. Please try again.")
            return
    
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
            print(f"Updated {field} to {value} for scooter ID {scooter.id}.")
            return True
        else:
            print("Failed to update scooter. Please check your permissions or the field you are trying to update.")
            time.sleep(2)
            return False
    
    @staticmethod
    def display_update_password(user):
        from main import clear_console
        from Logic.user_logic import UserLogic
        
        clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Update Password".center(75) + "|")
        print("----------------------------------------------------------------------------")
        
        #NOTE INPUT FIELD
        new_password = input("Enter your new password: ").strip()
        if not new_password:
            print("Password cannot be empty. Please try again.")
            time.sleep(2)
            return False
        
        if UserLogic.update_own_password(user, new_password):
            print("Password updated successfully.")
            time.sleep(2)
            return True
        else:
            print("Failed to update password. Make sure you are authorized to perform this action.")
            time.sleep(2)
            return False

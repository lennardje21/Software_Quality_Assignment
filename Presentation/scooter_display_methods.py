import time
from Helpers.input_prompters import InputPrompters
from Helpers.input_validators import InputValidators
from Logic.log_logic import LogLogic
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

        search_key = InputPrompters.prompt_until_valid(
            "Enter a search key (id, brand, mileage, etc.) or type 'exit' to go back: ",
            InputValidators.validate_search_key,
            "Invalid search input. Please enter alphanumeric characters or common symbols only."
        )

        if search_key is None:
            print("Exiting search...")
            LogLogic.add_log_to_database(
                username=user.username,
                action="Search Scooter",
                description="Scooter search cancelled by user.",
                suspicious="No"
            )
            time.sleep(1)
            general_shared_methods.clear_console()
            return True

        general_shared_methods.clear_console()
        scooters = ScooterLogic.search_scooter(user, search_key)

        if scooters and len(scooters) > 0:
            log_msg = f"Found {len(scooters)} scooters matching '{search_key}'"
            LogLogic.add_log_to_database(
                username=user.username,
                action="Search Scooter",
                description=log_msg,
                suspicious="No"
            )

            print(f"\n{log_msg}:")
            time.sleep(1)
            for count, scooter in enumerate(scooters, 1):
                print("----------------------------------------------------------------------------")
                print("|" + f"Search Result #{count}".center(75) + "|")
                print("----------------------------------------------------------------------------")
                scooter_display_methods.display_scooter(scooter, search_key)
            if update_call:
                return scooters
            return None
        else:
            LogLogic.add_log_to_database(
                username=user.username,
                action="Search Scooter",
                description=f"No scooters found for search key: '{search_key}'",
                suspicious="No"
            )
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
            scooter_id = InputPrompters.prompt_until_valid(
                "Enter scooter ID number to update (or type 'exit' to cancel): #",
                InputValidators.validate_id,
                "Invalid ID format. Please use alphanumeric characters, dashes, or underscores."
            )
            general_shared_methods.clear_console()

            if scooter_id is None:
                print("Exiting update...")
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Update Scooter",
                    description="Scooter update cancelled by user.",
                    suspicious="No"
                )
                time.sleep(1)
                return

            scooter = ScooterLogic.find_scooter_by_id(scooters, scooter_id)
            if scooter is None:
                print(f"No scooter found with ID {scooter_id}. Please try again.")
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Update Scooter",
                    description=f"Tried updating non-existent scooter ID: {scooter_id}",
                    suspicious="No"
                )
                time.sleep(2)
                continue

            if user.role == "service_engineer":
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Update Scooter",
                    description=f"Partial update started for scooter ID: {scooter_id}",
                    suspicious="No"
                )
                while True:
                    exit_update = scooter_display_methods.partial_update_scooter_display(scooter, user)
                    if exit_update:
                        print("Exiting update...")
                        time.sleep(1)
                        break
                break
            else:
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Update Scooter",
                    description=f"Full update started for scooter ID: {scooter_id}",
                    suspicious="No"
                )
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
        
        if ScooterLogic.update_scooter_partial(user, scooter):
            LogLogic.add_log_to_database(
                username=user.username,
                action="Update Scooter",
                description=f"Field '{field}' updated for scooter ID {scooter.id}.",
                suspicious="No"
            )
            return True
        else:
            print("Failed to update scooter. Please check your permissions or the field you are trying to update.")
            LogLogic.add_log_to_database(
                username=user.username,
                action="Update Scooter",
                description=f"Failed to update field '{field}' for scooter ID {scooter.id}.",
                suspicious="No"
            )
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

        validators = {
            "brand": InputValidators.validate_generic_name,
            "model": InputValidators.validate_generic_name,
            "serial_number": InputValidators.validate_alphanumeric,
            "top_speed": InputValidators.validate_positive_number,
            "battery_capacity": InputValidators.validate_positive_number,
            "state_of_charge": InputValidators.validate_percentage,
            "target_soc_min": InputValidators.validate_percentage,
            "target_soc_max": InputValidators.validate_percentage,
            "latitude": InputValidators.validate_latitude,
            "longitude": InputValidators.validate_longitude,
            "out_of_service_status": InputValidators.validate_boolean,
            "mileage": InputValidators.validate_positive_number,
            "last_maintenance_date": InputValidators.validate_date
        }

        while True:
            field = scooter_display_methods.prompt_for_field(scooter, user, editable_fields, field_aliases)
            if field is None:
                return True

            validator = validators.get(field)
            if not validator:
                print(f"No validator defined for field: {field}")
                time.sleep(1.5)
                continue

            prompt_label = field.replace("_", " ").title()
            new_value = InputPrompters.prompt_until_valid(
                f"Enter new value for {prompt_label} (or type 'exit' to cancel): ",
                validator,
                f"Invalid value for {prompt_label}. Please try again."
            )

            if new_value is None:
                continue  # back to field selection

            general_shared_methods.clear_console()
            #NOTE TYPE CHECKING AND ASSIGNING
            scooter_display_methods.update_scooter(scooter, field, new_value, user)
            print(f"Updated {prompt_label} for scooter {scooter.id}.")
            time.sleep(2)
            general_shared_methods.clear_console()
            return False

    @staticmethod
    def display_delete_scooter(user):
        while True:
            scooters = scooter_display_methods.search_scooter_display(user, update_call=True)
            if scooters is True:
                return
            if scooters is False:
                continue
            
            print("----------------------------------------------------------------------------")
            scooter_id = InputPrompters.prompt_until_valid(
                "Enter scooter ID number to delete (or type 'exit' to cancel): #",
                InputValidators.validate_alphanumeric,
                "Invalid scooter ID format. Only letters, numbers, and hyphens are allowed."
            )

            general_shared_methods.clear_console()

            if scooter_id is None:
                print("Exiting deletion...")
                time.sleep(1)
                return

            scooter = ScooterLogic.find_scooter_by_id(scooters, scooter_id)
            if scooter is None:
                print(f"No scooter found with ID {scooter_id}. Please try again.")
                LogLogic.add_log_to_database(
                    username=user.username,
                    action="Delete Scooter",
                    description=f"Attempted to delete non-existent scooter with ID {scooter_id}.",
                    suspicious="No"
                )
                time.sleep(2)
                continue

            while True:
                exit_update = scooter_display_methods.display_delete_scooter_confirm(scooter, user)
                if exit_update == True:
                    LogLogic.add_log_to_database(
                        username=user.username,
                        action="Delete Scooter",
                        description=f"Deleted scooter with ID {scooter.id}.",
                        suspicious="No"
                    )
                    general_shared_methods.clear_console()
                    print("Exiting Deletion...")
                    time.sleep(1)
                    break
                else:
                    LogLogic.add_log_to_database(
                        username=user.username,
                        action="Delete Scooter",
                        description=f"Cancelled deletion of scooter with ID {scooter.id}.",
                        suspicious="No"
                    )
                    break  # prevent looping on confirmation
            break  # Exit the outer loop after a valid attempt

    @staticmethod
    def display_delete_scooter_confirm(scooter, user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Delete Scooter".center(75) + "|")
        print("----------------------------------------------------------------------------")
        scooter_display_methods.display_scooter(scooter, scooter.id)
        print("----------------------------------------------------------------------------")
        
        confirm = InputPrompters.prompt_until_valid(
            f"Are you sure you want to delete scooter {scooter.id}? (yes/no): ",
            InputValidators.validate_yes_no,
            "Invalid input. Please enter 'yes' or 'no'."
        )

        general_shared_methods.clear_console()

        if confirm is None or confirm == 'no':
            print("Deletion cancelled.")
            time.sleep(1)
            return True

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
            LogLogic.add_log_to_database(
                username=user.username,
                action="Add Scooter",
                description="Scooter creation cancelled by user.",
                suspicious="No"
            )
            time.sleep(1.5)
            return False
        
        success = ScooterLogic.add_scooter(user, scooter)

        general_shared_methods.clear_console()
        if success:
            print(f"Scooter {scooter.id} has been added successfully.")
            LogLogic.add_log_to_database(
                username=user.username,
                action="Add Scooter",
                description=f"Scooter with ID {scooter.id} was added successfully.",
                suspicious="No"
            )
            time.sleep(2)
            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "New scooter".center(75) + "|")
            print("----------------------------------------------------------------------------")
            scooter_display_methods.display_scooter(scooter)
            print("----------------------------------------------------------------------------")
            general_shared_methods.input_password("Press any key to continue...")
            general_shared_methods.clear_console()
            return True
        else:
            print("Failed to add scooter. Please check your permissions.")
            LogLogic.add_log_to_database(
                username=user.username,
                action="Add Scooter",
                description=f"Attempted to add scooter with ID {scooter.id} but failed.",
                suspicious="No"
            )
            time.sleep(2)
            return False

    @staticmethod
    def prompt_for_new_scooter_details(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Enter New Scooter Details".center(75) + "|")
        print("----------------------------------------------------------------------------")
        
        print("Type 'exit' at any prompt to cancel.")

        p = InputPrompters.prompt_until_valid()
        
        brand = p("Enter Brand: ", InputValidators.validate_alphanumeric, "Invalid brand name.")
        if brand is None: return None

        model = p("Enter Model: ", InputValidators.validate_alphanumeric, "Invalid model name.")
        if model is None: return None

        serial = p(
            "Enter Serial Number: ",
            lambda s: InputValidators.validate_alphanumeric(s) and not ScooterLogic.serial_exists(user, s),
            "Invalid or duplicate serial number. It must be alphanumeric and unique."
        )
        if serial is None: return None

        top_speed = int(p("Enter Top Speed (km/h): ", InputValidators.validate_positive_number, "Invalid top speed. Must be a positive number."))
        if top_speed is None: return None

        battery = int(p("Enter Battery Capacity (Wh): ", InputValidators.validate_positive_number, "Invalid battery capacity."))
        if battery is None: return None

        soc = int(p("Enter State of Charge (%): ", InputValidators.validate_percentage, "Invalid SOC (0–100%)."))
        if soc is None: return None

        soc_min = int(p("Enter Target SOC Min (%): ", InputValidators.validate_percentage, "Invalid min SOC (0–100%)."))
        if soc_min is None: return None

        soc_max = int(p("Enter Target SOC Max (%): ", InputValidators.validate_percentage, "Invalid max SOC (0–100%)."))
        if soc_max is None: return None
        
        latitude = float(p("Enter Latitude: ", InputValidators.validate_latitude, "Invalid latitude (-90 to 90)."))
        if latitude is None: return None
        
        longitude = float(p("Enter Longitude: ", InputValidators.validate_longitude, "Invalid longitude (-180 to 180)."))
        if longitude is None: return None
        
        out_of_service = p("Is the scooter out of service? (yes/no): ", InputValidators.validate_yes_no, "Enter 'yes' or 'no'.")
        if out_of_service is None: return None
        out_of_service_bool = out_of_service.lower() == "yes"
        
        mileage = int(p("Enter Mileage (km): ", InputValidators.validate_positive_number, "Invalid mileage. Must be 0 or higher."))
        if mileage is None: return None
        
        last_maintenance = p("Enter Last Maintenance Date (YYYY-MM-DD): ", InputValidators.validate_date, "Invalid date format.")
        if last_maintenance is None: return None
        
        return ScooterLogic.create_scooter_object(
            user,
            brand,
            model,
            serial,
            top_speed,
            battery,
            soc,
            soc_min,
            soc_max,
            latitude,
            longitude,
            out_of_service_bool,
            mileage,
            last_maintenance
        )
            
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

        validators = {
            "state_of_charge": InputValidators.validate_percentage,
            "target_soc_min": InputValidators.validate_percentage,
            "target_soc_max": InputValidators.validate_percentage,
            "latitude": InputValidators.validate_latitude,
            "longitude": InputValidators.validate_longitude,
            "out_of_service_status": InputValidators.validate_boolean,
            "mileage": InputValidators.validate_positive_number,
            "last_maintenance_date": InputValidators.validate_date
        }

        while True:
            field = scooter_display_methods.prompt_for_field(scooter, user, editable_fields, field_aliases)
            if field is None:
                return True

            validator = validators.get(field)
            if not validator:
                print(f"No validator found for field: {field}")
                time.sleep(1.5)
                continue

            current_value = getattr(scooter, field, "")
            prompt_msg = f"Enter new value for {field.replace('_', ' ')} [Current: {current_value}]: "
            error_msg = f"Invalid input for {field.replace('_', ' ')}. Please try again."

            new_value = InputPrompters.prompt_until_valid(prompt_msg, validator, error_msg)
            if new_value is None:
                print("Update cancelled.")
                time.sleep(1.5)
                return False

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
            print("Available fields to update:")

            for field in editable_fields:
                display_name = field.replace("_", " ").title()
                print(f" - {display_name} ({field})")

            print("\nEnter the field you want to update (use snake_case as shown) or type 'exit' to cancel.")
            field_input = input("Field to update: ").strip().lower()
            general_shared_methods.clear_console()

            if field_input == 'exit':
                print("Exiting update...")
                time.sleep(1)
                general_shared_methods.clear_console()
                return None

            if not InputValidators.validate_safe_string(field_input):
                print("Invalid characters in input. Please try again.")
                time.sleep(1.5)
                continue

            # Normalize and resolve alias if needed
            resolved_field = field_aliases.get(field_input, field_input)

            # Compute valid resolved fields
            valid_resolved_fields = [field_aliases.get(f, f) for f in editable_fields]

            if resolved_field not in valid_resolved_fields:
                print(f"'{field_input}' is not a valid field. Please choose from the available options.")
                time.sleep(1.5)
                continue

            return resolved_field
# Presentation/traveller_display_methods.py

from Helpers.input_validators import InputValidators
from Helpers.input_prompters import InputPrompters
from Logic.traveller_logic import TravellerLogic
from DataModels.traveller import Traveller
from Presentation.general_shared_methods import general_shared_methods
import time, uuid, datetime

class traveller_display_methods:

    @staticmethod
    def display_traveller(traveller, search_key=None, user=None):
        from Presentation.general_shared_methods import general_shared_methods

        if user is None:
            print(f"Traveller ID:           {general_shared_methods.highlight(traveller.id, search_key)}")
            print(f"First Name:             {general_shared_methods.highlight(traveller.first_name, search_key)}")
            print(f"Last Name:              {general_shared_methods.highlight(traveller.last_name, search_key)}")
            print(f"Birthday:               {general_shared_methods.highlight(traveller.birthday, search_key)}")
            print(f"Gender:                 {general_shared_methods.highlight(traveller.gender, search_key)}")
            print(f"Street Name:            {general_shared_methods.highlight(traveller.street_name, search_key)}")
            print(f"House Number:           {general_shared_methods.highlight(traveller.house_number, search_key)}")
            print(f"Zip Code:               {general_shared_methods.highlight(traveller.zip_code, search_key)}")
            print(f"City:                   {general_shared_methods.highlight(traveller.city, search_key)}")
            print(f"Email:                  {general_shared_methods.highlight(traveller.email_address, search_key)}")
            print(f"Mobile Phone:           {general_shared_methods.highlight(traveller.mobile_phone, search_key)}")
            print(f"Driving License Number: {general_shared_methods.highlight(traveller.driving_license_number, search_key)}")
            print(f"Registration Date:      {general_shared_methods.highlight(traveller.registration_date, search_key)}")
        else:
            is_admin = getattr(user, "role", "").lower() in ["super_admin", "system_admin"]
            editable = "[Editable]" if is_admin else ""
            print(f"Traveller ID:           {traveller.id}")
            print(f"First Name:             {traveller.first_name:<23}{editable:>12}")
            print(f"Last Name:              {traveller.last_name:<23}{editable:>12}")
            print(f"Birthday:               {traveller.birthday:<23}{editable:>12}")
            print(f"Gender:                 {traveller.gender:<23}{editable:>12}")
            print(f"Street Name:            {traveller.street_name:<23}{editable:>12}")
            print(f"House Number:           {traveller.house_number:<23}{editable:>12}")
            print(f"Zip Code:               {traveller.zip_code:<23}{editable:>12}")
            print(f"City:                   {traveller.city:<23}{editable:>12}")
            print(f"Email:                  {traveller.email_address:<23}{editable:>12}")
            print(f"Mobile Phone:           {traveller.mobile_phone:<23}{editable:>12}")
            print(f"Driving License Number: {traveller.driving_license_number:<23}{editable:>12}")
            print(f"Registration Date:      {traveller.registration_date}")


    @staticmethod
    def display_add_traveller(user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Add New Traveller".center(75) + "|")
        print("----------------------------------------------------------------------------")

        print("Type 'exit' at any prompt to cancel.")

        def prompt(field_name, validator, error_msg, *args):
            return InputPrompters.prompt_until_valid(
                f"{field_name}: ", validator, error_msg, *args
            )

        first_name = prompt("First Name", InputValidators.validate_name, "Invalid first name.")
        if first_name is None: return traveller_display_methods._cancel_add()

        last_name = prompt("Last Name", InputValidators.validate_name, "Invalid last name.")
        if last_name is None: return traveller_display_methods._cancel_add()

        birthday = prompt("Birthday (YYYY-MM-DD)", InputValidators.validate_date, "Invalid date format.")
        if birthday is None: return traveller_display_methods._cancel_add()

        gender = prompt("Gender (male/female)", InputValidators.validate_gender, "Invalid gender.")
        if gender is None: return traveller_display_methods._cancel_add()

        street = prompt("Street Name", InputValidators.validate_street_name, "Invalid street name.")
        if street is None: return traveller_display_methods._cancel_add()

        house_number = prompt("House Number", InputValidators.validate_house_number, "Invalid house number.")
        if house_number is None: return traveller_display_methods._cancel_add()

        zip_code = prompt("Zip Code", InputValidators.validate_zipcode, "Invalid zip code.")
        if zip_code is None: return traveller_display_methods._cancel_add()

        city = traveller_display_methods.prompt_city_selection()
        if city is None: return traveller_display_methods._cancel_add()

        email = prompt("Email", InputValidators.validate_email, "Invalid email.")
        if email is None: return traveller_display_methods._cancel_add()

        mobile = prompt("Mobile Phone (8 digits)", InputValidators.validate_mobile_phone, "Invalid phone number.")
        if mobile is None: return traveller_display_methods._cancel_add()

        license_num = prompt("Driving License Number", InputValidators.validate_driving_license_number,
                            "Invalid license format.")
        if license_num is None: return traveller_display_methods._cancel_add()

        traveller = Traveller(
            id=str(uuid.uuid4()),
            first_name=first_name,
            last_name=last_name,
            birthday=birthday,
            gender=gender,
            street_name=street,
            house_number=house_number,
            zip_code=zip_code,
            city=city,
            email_address=email,
            mobile_phone=mobile,
            driving_license_number=license_num,
            registration_date=str(datetime.date.today())
        )

        success = TravellerLogic.add_traveller(user, traveller)
        general_shared_methods.clear_console()
        if success:
            print("----------------------------------------------------------------------------")
            print(f"Traveller {traveller.first_name} {traveller.last_name} has been added successfully.")
            print("----------------------------------------------------------------------------")
            traveller_display_methods.display_traveller(traveller, user=user)
            general_shared_methods.input_password("Press any key to continue...")
            general_shared_methods.clear_console()
            return True
        else:
            print("Failed to add traveller.")
            time.sleep(2)
            return False

    @staticmethod
    def _cancel_add():
        print("Traveller creation cancelled.")
        time.sleep(1.5)
        return False

    @staticmethod
    def display_update_traveller(user):
        while True:
            travellers = traveller_display_methods.display_search_traveller(user, update_call=True)
            if travellers is True:
                return
            if travellers is False:
                continue

            print("----------------------------------------------------------------------------")
            traveller_id = input("Enter traveller ID to update (or type 'exit' to cancel): #").strip()
            general_shared_methods.clear_console()

            if traveller_id.lower() == 'exit':
                print("Exiting update...")
                time.sleep(1)
                return

            if traveller_id == '':
                print("Traveller ID cannot be empty. Please try again.")
                time.sleep(1.5)
                continue

            traveller = next((t for t in travellers if t.id == traveller_id), None)
            if traveller is None:
                print(f"No traveller found with ID {traveller_id}. Please try again.")
                time.sleep(2)
                continue

            def prompt_update(label, attr, validator, error_msg, *args):
                current = getattr(traveller, attr)
                while True:
                    entry = input(f"{label} [{current}]: ").strip()
                    
                    # If user presses Enter, keep current value
                    if entry == '':
                        return current

                    # Validate entry
                    is_valid = validator(entry, *args) if args else validator(entry)
                    if is_valid:
                        return entry

                    print(error_msg)
                    time.sleep(1.5)


            updated_traveller = traveller.__class__(
                id=traveller.id,
                first_name=prompt_update("First Name", "first_name", InputValidators.validate_name, "Invalid name."),
                last_name=prompt_update("Last Name", "last_name", InputValidators.validate_name, "Invalid name."),
                birthday=prompt_update("Birthday (YYYY-MM-DD)", "birthday", InputValidators.validate_date, "Invalid birthday format."),
                gender=prompt_update("Gender (male/female)", "gender", InputValidators.validate_gender, "Invalid gender."),
                street_name=prompt_update("Street Name", "street_name", InputValidators.validate_street_name, "Invalid street."),
                house_number=prompt_update("House Number", "house_number", InputValidators.validate_house_number, "Invalid house number."),
                zip_code=prompt_update("Zip Code", "zip_code", InputValidators.validate_zipcode, "Invalid zip code."),
                city=traveller_display_methods.prompt_city_selection(current_city=traveller.city),
                email_address=prompt_update("Email", "email_address", InputValidators.validate_email, "Invalid email."),
                mobile_phone=prompt_update("Mobile Phone (8 digits)", "mobile_phone", InputValidators.validate_mobile_phone, "Invalid phone number."),
                driving_license_number=prompt_update("Driving License Number", "driving_license_number", InputValidators.validate_driving_license_number, "Invalid license."),
                registration_date=traveller.registration_date
            )

            success = TravellerLogic.update_traveller(user, updated_traveller)

            if success:
                print("Traveller successfully updated.")
                print("----------------------------------------------------------------------------")
                traveller_display_methods.display_traveller(updated_traveller, user=user)
                general_shared_methods.input_password("Press any key to continue...")
                general_shared_methods.clear_console()
                return True
            else:
                print("Failed to update traveller.")
                time.sleep(2)
                return False

    @staticmethod
    def display_search_traveller(user, update_call=False):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Search for Traveller".center(75) + "|")
        print("----------------------------------------------------------------------------")

        # Get validated search input
        search_key = InputPrompters.prompt_until_valid(
            prompt_msg="Enter a search key (name, email, license, etc.) or type 'exit' to go back: ",
            validate_func=InputValidators.validate_search_key,
            error_msg="Invalid search input. Only letters, numbers, and basic symbols allowed."
        )

        if search_key is None:
            print("Exiting search...")
            time.sleep(1)
            general_shared_methods.clear_console()
            return True

        travellers = TravellerLogic.search_traveller(user, search_key)
        if travellers and len(travellers) > 0:
            print(f"\nFound {len(travellers)} traveller(s) matching '{general_shared_methods.highlight(search_key, search_key)}':")
            time.sleep(1)

            for count, traveller in enumerate(travellers, 1):
                print("----------------------------------------------------------------------------")
                print("|" + f"Search Result #{count}".center(75) + "|")
                print("----------------------------------------------------------------------------")
                traveller_display_methods.display_traveller(traveller, search_key=search_key, user=None)

            if update_call:
                return travellers

            general_shared_methods.input_password("Press any key to continue...")
            general_shared_methods.clear_console()
            return None
        else:
            print("No travellers found matching the search criteria.")
            time.sleep(2)
            general_shared_methods.clear_console()
            return False

    @staticmethod
    def display_delete_traveller(user):
        while True:
            travellers = traveller_display_methods.display_search_traveller(user, update_call=True)
            if travellers is True:
                return
            if travellers is False:
                continue

            print("----------------------------------------------------------------------------")
            traveller_id = InputPrompters.prompt_until_valid(
                prompt_msg="Enter traveller ID to delete (or type 'exit' to cancel): #",
                validate_func=InputValidators.validate_id,
                error_msg="Invalid traveller ID. Use alphanumeric characters only."
            )
            general_shared_methods.clear_console()

            if traveller_id is None:
                print("Exiting deletion...")
                time.sleep(1)
                return

            traveller = next((t for t in travellers if t.id == traveller_id), None)
            if traveller is None:
                print(f"No traveller found with ID {traveller_id}. Please try again.")
                time.sleep(2)
                continue

            # Confirm deletion
            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "Delete Traveller".center(75) + "|")
            print("----------------------------------------------------------------------------")
            traveller_display_methods.display_traveller(traveller, search_key=traveller.id, user=user)
            print("----------------------------------------------------------------------------")

            confirm = InputPrompters.prompt_until_valid(
                prompt_msg=f"Are you sure you want to delete traveller {traveller.first_name} {traveller.last_name}? (yes/no): ",
                validate_func=InputValidators.validate_yes_no,
                error_msg="Invalid input. Please enter 'yes' or 'no'."
            )
            general_shared_methods.clear_console()

            if confirm == 'yes':
                if TravellerLogic.delete_traveller(user, traveller.id):
                    print(f"Traveller {traveller.first_name} {traveller.last_name} has been deleted successfully.")
                    time.sleep(2)
                    return True
                else:
                    print("Failed to delete traveller. Please check your permissions.")
                    time.sleep(2)
                    return False
            else:
                print("Deletion cancelled.")
                time.sleep(1)
                return True

        
    @staticmethod
    def prompt_city_selection(current_city=None):
        allowed_cities = [
            "Rotterdam", "Amsterdam", "Utrecht", "Den Haag", "Eindhoven",
            "Groningen", "Leiden", "Maastricht", "Delft", "Breda"
        ]
        while True:
            print("Available Cities:")
            for i, city in enumerate(allowed_cities, start=1):
                print(f"{i}. {city}")
            if current_city:
                entry = input(f"Choose a city number (or press Enter to keep '{current_city}'): ").strip()
            else:
                entry = input("Choose a city number: ").strip()

            if entry.lower() == "exit":
                return None
            if entry == '' and current_city:
                return current_city
            if entry.isdigit():
                index = int(entry) - 1
                if 0 <= index < len(allowed_cities):
                    return allowed_cities[index]

            print("Invalid selection. Please enter a number from the list.")
            time.sleep(1.5)

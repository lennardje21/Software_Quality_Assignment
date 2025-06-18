# Presentation/traveller_display_methods.py

from Logic.traveller_logic import TravellerLogic
from DataModels.traveller import Traveller
from Presentation.general_shared_methods import general_shared_methods
import time


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

        traveller = TravellerLogic.create_traveller_from_input()
        if traveller is None:
            print("Traveller creation cancelled.")
            time.sleep(1.5)
            return False

        success = TravellerLogic.add_traveller(user, traveller)
        general_shared_methods.clear_console()
        if success:
            print(f"Traveller {traveller.first_name} {traveller.last_name} has been added successfully.")
            print("----------------------------------------------------------------------------")
            traveller_display_methods.display_traveller(traveller, user=user)
            input("Press any key to continue...")
            general_shared_methods.clear_console()
            return True
        else:
            print("Failed to add traveller.")
            time.sleep(2)
            return False

    @staticmethod
    def display_update_traveller(user):
        # Search for travellers first
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

            # Begin update process
            updated_traveller = TravellerLogic.modify_traveller_from_input(traveller)
            success = TravellerLogic.update_traveller(user, updated_traveller)

            if success:
                print("Traveller successfully updated.")
                print("----------------------------------------------------------------------------")
                traveller_display_methods.display_traveller(updated_traveller, user=user)
                input("Press any key to continue...")
                general_shared_methods.clear_console()
                return True
            else:
                print("Failed to update traveller.")
                time.sleep(2)
                return False

    @staticmethod
    def display_delete_traveller(user):
        while True:
            travellers = traveller_display_methods.display_search_traveller(user, update_call=True)
            if travellers is True:
                return
            if travellers is False:
                continue

            general_shared_methods.clear_console()
            print("----------------------------------------------------------------------------")
            print("|" + "Matching Travellers".center(75) + "|")
            print("----------------------------------------------------------------------------")

            for idx, traveller in enumerate(travellers, 1):
                print("----------------------------------------------------------------------------")
                print("|" + f"Traveller #{idx}".center(75) + "|")
                print("----------------------------------------------------------------------------")
                traveller_display_methods.display_traveller(traveller, search_key=traveller.id, user=user)

            print("----------------------------------------------------------------------------")
            traveller_id = input("Enter traveller ID to delete (or type 'exit' to cancel): #").strip()
            general_shared_methods.clear_console()

            if traveller_id.lower() == 'exit':
                print("Exiting deletion...")
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

            while True:
                exit_delete = traveller_display_methods.display_delete_traveller_confirm(traveller, user)
                if exit_delete:
                    general_shared_methods.clear_console()
                    print("Exiting Deletion...")
                    time.sleep(1)
                    break
            break

    @staticmethod
    def display_search_traveller(user, update_call=False):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Search for Traveller".center(75) + "|")
        print("----------------------------------------------------------------------------")

        # NOTE: INPUT FIELD
        search_key = input("Enter a search key (name, email, license, etc.) or type 'exit' to go back: ").strip()
        general_shared_methods.clear_console()

        if search_key.lower() == 'exit':
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
                print("----------------------------------------------------------------------------")
                general_shared_methods.clear_console()
            if update_call:
                return travellers
            return None
        else:
            print("No travellers found matching the search criteria.")
            time.sleep(2)
            general_shared_methods.clear_console()
            return False
        
    @staticmethod
    def display_delete_traveller_confirm(traveller, user):
        general_shared_methods.clear_console()
        print("----------------------------------------------------------------------------")
        print("|" + "Delete Traveller".center(75) + "|")
        print("----------------------------------------------------------------------------")
        traveller_display_methods.display_traveller(traveller, search_key=traveller.id, user=user)
        print("----------------------------------------------------------------------------")

        confirm = input(f"Are you sure you want to delete traveller {traveller.first_name} {traveller.last_name}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            if TravellerLogic.delete_traveller(user, traveller.id):
                general_shared_methods.clear_console()
                print(f"✅ Traveller {traveller.first_name} {traveller.last_name} has been deleted successfully.")
                time.sleep(2)
                return True
            else:
                print("❌ Failed to delete traveller. Please check your permissions.")
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


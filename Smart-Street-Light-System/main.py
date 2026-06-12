from database import create_database, add_street_light, view_all_light, search_street_light, update_light_status, detect_energy_wastage, generate_report
# Smart Street Light Energy Waste Detection System
# Main program with menu-driven interface

def main():
    """
    Main function that displays the menu and handles user interactions
    for the Smart Street Light System.
    """
    create_database()
    # Main program loop - continues until user chooses to exit
    while True:
        # Display the menu
        print("\n==== Smart Street Light System ====")
        print("1. Register Street Light")
        print("2. View Street Light")
        print("3. Search Street Light")
        print("4. Update Light Status")
        print("5. Detect Energy Wastage")
        print("6. Generate Report")
        print("7. Exit")
        
        # Get user input for menu selection
        try:
            choice = input("\nEnter your choice (1-7): ")
            
            # Convert input to integer for comparison
            choice = int(choice)
            
            # Handle each menu option using if-elif-else statements
            if choice == 1:
                light_id = input("Enter Light ID: ")
                area_name = input("Enter Area Name: ")
                pole_number = input("Enter Pole Number: ")
                latitude = float(input("Enter Latitude: "))
                longitude = float(input("Enter Longitude: "))
                installation_date = input("Enter Installation Date (YYYY-MM-DD): ")
                status = input("Enter Status (ON/OFF): ")

                add_street_light(
                    light_id,
                    area_name,
                    pole_number,
                    latitude,
                    longitude,
                    installation_date,
                    status
    )
            elif choice == 2:
                view_all_light()
            elif choice == 3:
                light_id = input("Enter Light ID to search: ")
                search_street_light(light_id)
            elif choice == 4:
                light_id = input("Enter Light ID to update: ")
                status = input("Enter new status (ON/OFF): ")
                update_light_status(light_id, status)
                if status in ["ON", "OFF"]:
                    update_light_status(light_id, status)
                else:
                    print("Invalid status. Please enter ON or OFF.")
            elif choice == 5:
                light_id = input("Enter Light ID to detect energy wastage: ")
                detect_energy_wastage(light_id)
                
                if expected_status in ["ON", "OFF"]:
                    detect_energy_wastage(light_id, expected_status)
                else:
                 print("Invalid status. Please enter ON or OFF.")
            elif choice == 6:
                generate_report()
            elif choice == 7:
                # Exit the program
                print("Thank you for using Smart Street Light System.")
                break
            else:
                # Handle invalid menu choice (out of range)
                print("Invalid choice. Please enter a number between 1 and 7.")
                
        except ValueError:
            # Handle non-integer input
            print("Invalid input. Please enter a valid number (1-7).")
        except Exception as e:
            # Handle any other unexpected errors
            print(f"An error occurred: {e}")

# Entry point of the program
if __name__ == "__main__":
    main()
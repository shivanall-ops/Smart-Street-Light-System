from database import add_street_light
# Smart Street Light Energy Waste Detection System
# Main program with menu-driven interface

def main():
    """
    Main function that displays the menu and handles user interactions
    for the Smart Street Light System.
    """
    
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
                print("View Street Light feature selected.")
            elif choice == 3:
                print("Search Street Light feature selected.")
            elif choice == 4:
                print("Update Light Status feature selected.")
            elif choice == 5:
                print("Detect Energy Wastage feature selected.")
            elif choice == 6:
                print("Generate Report feature selected.")
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
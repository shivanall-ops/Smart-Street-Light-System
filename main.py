"""
Smart Street Light Energy Waste Detection System - Main Module

This module provides a menu-driven interface for managing street light records
and detecting energy waste in the Smart Street Light System.

Author: Smart Street Light System Team
Version: 1.0
"""

from database import (
    create_database,
    add_street_light,
    view_all_light,
    search_street_light,
    update_light_status,
    detect_energy_wastage,
    generate_report
)


def display_menu():
    """
    Displays the main menu options for the Smart Street Light System.
    
    Returns:
        None
    """
    print("\n" + "=" * 50)
    print("  SMART STREET LIGHT ENERGY WASTE DETECTION SYSTEM")
    print("=" * 50)
    print("1. Add Street Light")
    print("2. View All Street Lights")
    print("3. Search Street Light by ID")
    print("4. Update Street Light Status")
    print("5. Detect Energy Waste")
    print("6. Generate Report")
    print("7. Exit")
    print("=" * 50)


def get_valid_input(prompt, input_type=str, validation_func=None):
    """
    Gets and validates user input.
    
    Args:
        prompt (str): The message to display to the user
        input_type (type): The expected type of input (str, int, float)
        validation_func (function): Optional function to validate the input
        
    Returns:
        The validated user input
    """
    while True:
        try:
            user_input = input(prompt)
            
            # Convert to specified type
            if input_type == int:
                user_input = int(user_input)
            elif input_type == float:
                user_input = float(user_input)
            
            # Apply custom validation if provided
            if validation_func and not validation_func(user_input):
                print("Invalid input. Please try again.")
                continue
                
            return user_input
            
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")


def validate_menu_choice(choice):
    """
    Validates the menu choice is between 1 and 7.
    
    Args:
        choice (int): The user's menu choice
        
    Returns:
        bool: True if valid, False otherwise
    """
    return 1 <= choice <= 7


def add_street_light_menu():
    """
    Handles the menu option to add a new street light.
    Collects user input and calls the database function.
    
    Returns:
        None
    """
    print("\n--- Add New Street Light ---")
    
    try:
        light_id = get_valid_input("Enter Light ID: ")
        area_name = get_valid_input("Enter Area Name: ")
        pole_number = get_valid_input("Enter Pole Number: ")
        latitude = get_valid_input("Enter Latitude: ", float)
        longitude = get_valid_input("Enter Longitude: ", float)
        installation_date = get_valid_input("Enter Installation Date (YYYY-MM-DD): ")
        status = get_valid_input("Enter Status (ON/OFF): ").upper()
        
        # Validate status
        while status not in ["ON", "OFF"]:
            print("Status must be either 'ON' or 'OFF'.")
            status = get_valid_input("Enter Status (ON/OFF): ").upper()
        
        add_street_light(
            light_id, area_name, pole_number,
            latitude, longitude, installation_date, status
        )
        
    except Exception as e:
        print(f"Error adding street light: {e}")


def view_all_lights_menu():
    """
    Handles the menu option to view all street lights.
    Calls the database function to display all records.
    
    Returns:
        None
    """
    print("\n--- View All Street Lights ---")
    try:
        view_all_light()
    except Exception as e:
        print(f"Error viewing street lights: {e}")


def search_street_light_menu():
    """
    Handles the menu option to search for a street light by ID.
    Collects the light ID from user and calls the database function.
    
    Returns:
        None
    """
    print("\n--- Search Street Light by ID ---")
    try:
        light_id = get_valid_input("Enter Light ID to search: ")
        search_street_light(light_id)
    except Exception as e:
        print(f"Error searching street light: {e}")


def update_street_light_status_menu():
    """
    Handles the menu option to update a street light's status.
    Collects light ID and new status from user and calls the database function.
    
    Returns:
        None
    """
    print("\n--- Update Street Light Status ---")
    try:
        light_id = get_valid_input("Enter Light ID: ")
        status = get_valid_input("Enter New Status (ON/OFF): ").upper()
        
        # Validate status
        while status not in ["ON", "OFF"]:
            print("Status must be either 'ON' or 'OFF'.")
            status = get_valid_input("Enter New Status (ON/OFF): ").upper()
        
        update_light_status(light_id, status)
        
    except Exception as e:
        print(f"Error updating street light status: {e}")


def detect_energy_waste_menu():
    """
    Handles the menu option to detect energy waste.
    Collects light ID and expected status from user and calls the database function.
    
    Returns:
        None
    """
    print("\n--- Detect Energy Waste ---")
    try:
        light_id = get_valid_input("Enter Light ID: ")
        expected_status = get_valid_input("Enter Expected Status (ON/OFF): ").upper()
        
        # Validate status
        while expected_status not in ["ON", "OFF"]:
            print("Status must be either 'ON' or 'OFF'.")
            expected_status = get_valid_input("Enter Expected Status (ON/OFF): ").upper()
        
        detect_energy_wastage(light_id, expected_status)
        
    except Exception as e:
        print(f"Error detecting energy waste: {e}")


def main():
    """
    Main function that runs the Smart Street Light System menu interface.
    Initializes the database and displays the menu until the user chooses to exit.
    
    Returns:
        None
    """
    # Initialize the database
    print("Initializing Smart Street Light System...")
    create_database()
    print("Database initialized successfully!\n")
    
    # Main menu loop
    while True:
        display_menu()
        
        try:
            # Get and validate menu choice
            choice = get_valid_input(
                "Enter your choice (1-7): ",
                int,
                validate_menu_choice
            )
            
            # Process menu choice using match-case statement
            match choice:
                case 1:
                    add_street_light_menu()
                case 2:
                    view_all_lights_menu()
                case 3:
                    search_street_light_menu()
                case 4:
                    update_street_light_status_menu()
                case 5:
                    detect_energy_waste_menu()
                case 6:
                    generate_report()
                case 7:
                    print("\nThank you for using the Smart Street Light System!")
                    print("Goodbye!")
                    break
                case _:
                    print("Invalid choice. Please select a valid option.")
                    
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
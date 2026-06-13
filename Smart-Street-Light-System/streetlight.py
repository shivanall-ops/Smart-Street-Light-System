"""
Start Street Light Energy Waste Detection System
This module contains the StreetLight class for managing street light information
and detecting energy waste.
"""


class StreetLight:
    """
    A class to represent a street light and detect energy waste.
    
    Attributes:
        light_id (str): Unique identifier for the street light
        area_name (str): Name of the area where the street light is installed
        pole_number (str): Pole number of the street light
        latitude (float): Latitude coordinate of the street light location
        longitude (float): Longitude coordinate of the street light location
        installation_date (str): Date when the street light was installed
        status (str): Current status of the street light (ON or OFF)
    """
    
    def __init__(self, light_id, area_name, pole_number, latitude, longitude, installation_date, status):
        """
        Initialize a StreetLight object with all required attributes.
        
        Parameters:
            light_id (str): Unique identifier for the street light
            area_name (str): Name of the area where the street light is installed
            pole_number (str): Pole number of the street light
            latitude (float): Latitude coordinate of the street light location
            longitude (float): Longitude coordinate of the street light location
            installation_date (str): Date when the street light was installed
            status (str): Current status of the street light (ON or OFF)
        """
        self.light_id = light_id
        self.area_name = area_name
        self.pole_number = pole_number
        self.latitude = latitude
        self.longitude = longitude
        self.installation_date = installation_date
        self.status = status
    
    def display_details(self):
        """
        Print all street light information in a readable format.
        
        This method displays all the attributes of the street light in a
        user-friendly format for easy reading.
        """
        print("=" * 50)
        print("STREET LIGHT DETAILS")
        print("=" * 50)
        print(f"Light ID:           {self.light_id}")
        print(f"Area Name:          {self.area_name}")
        print(f"Pole Number:        {self.pole_number}")
        print(f"Latitude:           {self.latitude}")
        print(f"Longitude:          {self.longitude}")
        print(f"Installation Date:  {self.installation_date}")
        print(f"Current Status:     {self.status}")
        print("=" * 50)
    
    def detect_energy_waste(self, current_status, expected_status):
        """
        Check whether a street light is wasting energy.
        
        This method compares the current status of the street light with the
        expected status. If the light is ON when it should be OFF, it indicates
        energy waste.
        
        Parameters:
            current_status (str): The actual current status of the light (ON or OFF)
            expected_status (str): The expected status based on time/schedule (ON or OFF)
        
        Returns:
            str: "Energy Waste Detected" if the light is ON when it should be OFF,
                 "No Energy Waste Detected" otherwise
        """
        # Check if the light is ON when it should be OFF
        if current_status == "ON" and expected_status == "OFF":
            return "Energy Waste Detected"
        else:
            return "No Energy Waste Detected"


# Example usage of the StreetLight class
if __name__ == "__main__":
    # Create a StreetLight object
    street_light = StreetLight(
        light_id="SL001",
        area_name="Downtown",
        pole_number="P-123",
        latitude=40.7128,
        longitude=-74.0060,
        installation_date="2023-01-15",
        status="ON"
    )
    
    # Display the street light details
    street_light.display_details()
    
    # Test energy waste detection
    print("\nEnergy Waste Detection Tests:")
    print("-" * 50)
    
    # Test case 1: Light is ON when it should be OFF (energy waste)
    result1 = street_light.detect_energy_waste("ON", "OFF")
    print(f"Current: ON, Expected: OFF -> {result1}")
    
    # Test case 2: Light is OFF when it should be OFF (no waste)
    result2 = street_light.detect_energy_waste("OFF", "OFF")
    print(f"Current: OFF, Expected: OFF -> {result2}")
    
    # Test case 3: Light is ON when it should be ON (no waste)
    result3 = street_light.detect_energy_waste("ON", "ON")
    print(f"Current: ON, Expected: ON -> {result3}")
    
    # Test case 4: Light is OFF when it should be ON (no waste, but might need attention)
    result4 = street_light.detect_energy_waste("OFF", "ON")
    print(f"Current: OFF, Expected: ON -> {result4}")

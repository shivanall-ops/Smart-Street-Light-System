# Smart Street Light Energy Waste Detection System

## Project Description

The Smart Street Light Energy Waste Detection System is a Python-based application developed to manage street light information and identify energy wastage. The system provides a menu-driven interface to register street lights, view records, search for specific lights, update their status, detect energy wastage, and generate reports.

## Features

- Register Street Light
- View All Street Lights
- Search Street Light by Light ID
- Update Street Light Status (ON/OFF)
- Detect Energy Wastage
- Generate Reports
- Exit the Application

## Technologies Used

- Python
- SQLite
- Windsurf IDE
- Git & GitHub

## Project Structure

```
smart-street-light-system/
├── main.py
├── database.py
├── streetlight.py
├── reports.py
├── README.md
└── .gitignore
```

## How to Run

1. Clone the repository:
   ```bash
   git clone <repository-link>
   ```

2. Navigate to the project directory:
   ```bash
   cd smart-street-light-system
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Menu Options

1. Register Street Light
2. View Street Light
3. Search Street Light
4. Update Light Status
5. Detect Energy Wastage
6. Generate Report
7. Exit

## Sample Output

```
==== Smart Street Light System ====
1. Register Street Light
2. View Street Light
3. Search Street Light
4. Update Light Status
5. Detect Energy Wastage
6. Generate Report
7. Exit

Enter your choice (1-7): 1

Enter Light ID: SL001
Enter Area Name: Madhapur
Enter Pole Number: P001
Enter Latitude: 17.3850
Enter Longitude: 78.4867
Enter Installation Date (YYYY-MM-DD): 2026-06-12
Enter Status (ON/OFF): ON

Street Light Registered Successfully.
```

## Learning Outcomes

- Developed a menu-driven Python application
- Performed database operations using SQLite
- Implemented exception handling in Python
- Integrated Python with SQLite databases
- Used Git and GitHub for version control
- Improved debugging and problem-solving skills

## Future Enhancements

- Integrate IoT sensors for automatic light monitoring
- Automate energy wastage detection based on time schedules
- Develop a graphical user interface (GUI)
- Generate downloadable reports

## Author

**Shiva**

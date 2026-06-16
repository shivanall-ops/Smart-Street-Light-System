# Restaurant Food Ordering System

## Project Overview
The Restaurant Food Ordering System is a Python-based application that helps manage restaurant orders efficiently. It allows users to place orders, view order details, and generate bills using an SQLite database.

## Features
- Create and manage the restaurant database using SQLite.
- Store menu items with prices and descriptions.
- Place customer orders with multiple food items.
- View all orders or search for a specific order.
- Generate detailed bills with tax calculation.
- Automatically update order status after bill generation.
- Menu-driven interface for easy interaction.

## Technologies Used
- Python 3
- SQLite
- Windsurf IDE
- Git & GitHub

## Project Structure
```
Restaurant-Food-Ordering-System/
│
├── main.py
├── database.py
├── README.md
├── .gitignore
```

## Database Tables
### 1. menu_items
Stores restaurant menu information.

Fields:
- id
- name
- category
- price
- description

### 2. orders
Stores customer order details.

Fields:
- id
- customer_name
- table_number
- order_date
- status

### 3. order_items
Stores ordered items for each order.

Fields:
- id
- order_id
- menu_item_id
- quantity

## How to Run the Project

1. Clone the repository:
```
git clone <repository-url>
```

2. Navigate to the project folder:
```
cd Restaurant-Food-Ordering-System
```

3. Run the application:
```
python main.py
```

## Sample Menu
- Burger
- Pizza
- Ice Cream

## Future Enhancements
- Add a graphical user interface (GUI) using Tkinter.
- Integrate online payment functionality.
- Implement user authentication for administrators.
- Generate downloadable PDF bills.
- Add a search feature for orders.

## Author
Shiva 
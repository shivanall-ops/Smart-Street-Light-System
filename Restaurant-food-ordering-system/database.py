import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Successfully connected to SQLite database: {db_file}")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def create_database(db_file="restaurant_orders.db"):
    """Create the database and required tables for the restaurant ordering system."""
    conn = None
    try:
        conn = create_connection(db_file)
        if conn is None:
            return False
        
        cursor = conn.cursor()
        
        # Create menu_items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT
            )
        ''')
        
        # Create orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                table_number INTEGER,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        # Create order_items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                menu_item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (menu_item_id) REFERENCES menu_items (id)
            )
        ''')
        
        # Insert sample menu items if table is empty
        cursor.execute("SELECT COUNT(*) FROM menu_items")
        if cursor.fetchone()[0] == 0:
            sample_items = [
                ('Burger', 'Main Course', 8.99, 'Juicy beef burger with fresh vegetables'),
                ('Pizza', 'Main Course', 12.99, 'Classic margherita pizza'),
                ('Ice Cream', 'Dessert', 4.99, 'Vanilla ice cream')
            ]
            cursor.executemany(
                "INSERT INTO menu_items (name, category, price, description) VALUES (?, ?, ?, ?)",
                sample_items
            )
   
        conn.commit()
        print("Database and tables created successfully.")
        return True
        
    except Error as e:
        print(f"Error creating database: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()


def place_order(customer_name, table_number, items, db_file="restaurant_orders.db"):
    """
    Place an order with multiple menu items.
    
    Args:
        customer_name (str): Name of the customer
        table_number (int): Table number
        items (list): List of tuples containing (menu_item_name, quantity)
        db_file (str): Path to database file
    
    Returns:
        int: Order ID if successful, None if failed
    """
    conn = None
    try:
        conn = create_connection(db_file)
        if conn is None:
            return None
        
        cursor = conn.cursor()
        
        # Insert the order
        cursor.execute(
            "INSERT INTO orders (customer_name, table_number) VALUES (?, ?)",
            (customer_name, table_number)
        )
        order_id = cursor.lastrowid
        
        # Add each item to the order
        for item_name, quantity in items:
            # Get menu item ID
            cursor.execute(
                "SELECT id, price FROM menu_items WHERE name = ?",
                (item_name,)
            )
            result = cursor.fetchone()
            
            if result is None:
                print(f"Warning: Menu item '{item_name}' not found. Skipping.")
                continue
            
            menu_item_id = result[0]
            
            # Insert order item
            cursor.execute(
                "INSERT INTO order_items (order_id, menu_item_id, quantity) VALUES (?, ?, ?)",
                (order_id, menu_item_id, quantity)
            )
        
        conn.commit()
        print(f"Order placed successfully. Order ID: {order_id}")
        return order_id
        
    except Error as e:
        print(f"Error placing order: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            conn.close()


def view_orders(order_id=None, db_file="restaurant_orders.db"):
    """
    View orders. If order_id is provided, view specific order; otherwise view all orders.
    
    Args:
        order_id (int, optional): Specific order ID to view
        db_file (str): Path to database file
    
    Returns:
        list: List of order details
    """
    conn = None
    try:
        conn = create_connection(db_file)
        if conn is None:
            return []
        
        cursor = conn.cursor()
        
        if order_id:
            # View specific order
            cursor.execute('''
                SELECT o.id, o.customer_name, o.table_number, o.order_date, o.status,
                       mi.name, oi.quantity, mi.price
                FROM orders o
                JOIN order_items oi ON o.id = oi.order_id
                JOIN menu_items mi ON oi.menu_item_id = mi.id
                WHERE o.id = ?
            ''', (order_id,))
        else:
            # View all orders
            cursor.execute('''
                SELECT o.id, o.customer_name, o.table_number, o.order_date, o.status,
                       mi.name, oi.quantity, mi.price
                FROM orders o
                JOIN order_items oi ON o.id = oi.order_id
                JOIN menu_items mi ON oi.menu_item_id = mi.id
                ORDER BY o.order_date DESC
            ''')
        
        results = cursor.fetchall()
        
        if not results:
            print("No orders found.")
            return []
        
        # Display orders
        current_order_id = None
        for row in results:
            order_id_val, customer, table, date, status, item_name, quantity, price = row
            
            if order_id_val != current_order_id:
                if current_order_id is not None:
                    print("-" * 50)
                print(f"\nOrder ID: {order_id_val}")
                print(f"Customer: {customer}")
                print(f"Table: {table}")
                print(f"Date: {date}")
                print(f"Status: {status}")
                print("Items:")
                current_order_id = order_id_val
            
            print(f"  - {item_name} x{quantity} @ ${price:.2f} = ${price * quantity:.2f}")
        
        return results
        
    except Error as e:
        print(f"Error viewing orders: {e}")
        return []
    finally:
        if conn:
            conn.close()


def generate_bill(order_id, db_file="restaurant_orders.db"):
    """
    Generate a bill for a specific order.
    
    Args:
        order_id (int): Order ID to generate bill for
        db_file (str): Path to database file
    
    Returns:
        dict: Dictionary containing bill details or None if failed
    """
    conn = None
    try:
        conn = create_connection(db_file)
        if conn is None:
            return None
        
        cursor = conn.cursor()
        
        # Get order details
        cursor.execute('''
            SELECT o.id, o.customer_name, o.table_number, o.order_date
            FROM orders o
            WHERE o.id = ?
        ''', (order_id,))
        
        order_info = cursor.fetchone()
        
        if order_info is None:
            print(f"Order ID {order_id} not found.")
            return None
        
        order_id_val, customer_name, table_number, order_date = order_info
        
        # Get order items
        cursor.execute('''
            SELECT mi.name, oi.quantity, mi.price
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        
        items = cursor.fetchall()
        
        if not items:
            print(f"No items found for Order ID {order_id}.")
            return None
        
        # Calculate bill
        subtotal = 0.0
        tax_rate = 0.08  # 8% tax
        item_details = []
        
        for item_name, quantity, price in items:
            item_total = price * quantity
            subtotal += item_total
            item_details.append({
                'name': item_name,
                'quantity': quantity,
                'price': price,
                'total': item_total
            })
        
        tax = subtotal * tax_rate
        total = subtotal + tax
        
        # Display bill
        print("\n" + "=" * 50)
        print("RESTAURANT BILL")
        print("=" * 50)
        print(f"Order ID: {order_id_val}")
        print(f"Customer: {customer_name}")
        print(f"Table: {table_number}")
        print(f"Date: {order_date}")
        print("-" * 50)
        print("Items:")
        for item in item_details:
            print(f"  {item['name']} x{item['quantity']} @ ${item['price']:.2f} = ${item['total']:.2f}")
        print("-" * 50)
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Tax (8%): ${tax:.2f}")
        print(f"TOTAL: ${total:.2f}")
        print("=" * 50)
        
        # Update order status to completed
        cursor.execute(
            "UPDATE orders SET status = 'completed' WHERE id = ?",
            (order_id,)
        )
        conn.commit()
        
        return {
            'order_id': order_id_val,
            'customer_name': customer_name,
            'table_number': table_number,
            'order_date': order_date,
            'items': item_details,
            'subtotal': subtotal,
            'tax': tax,
            'total': total
        }
        
    except Error as e:
        print(f"Error generating bill: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            conn.close()
if __name__ == "__main__":
    create_database()

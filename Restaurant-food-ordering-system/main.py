from database import create_database, place_order, view_orders, generate_bill


def main():
    """Main function for Restaurant Food Ordering System."""

    create_database()

    while True:
        print("\n===== Restaurant Food Ordering System =====")
        print("1. Place Order")
        print("2. View All Orders")
        print("3. Generate Bill")
        print("4. Exit")

        try:
            choice = int(input("\nEnter your choice (1-4): "))

            if choice == 1:
                customer_name = input("Enter Customer Name: ")
                table_number = int(input("Enter Table Number: "))

                items = []

                while True:
                    item_name = input("Enter Menu Item Name: ")
                    quantity = int(input("Enter Quantity: "))

                    items.append((item_name, quantity))

                    more = input("Add another item? (yes/no): ").lower()

                    if more != "yes":
                        break

                place_order(customer_name, table_number, items)

            elif choice == 2:
                print("\nViewing all orders...")
                view_orders()

            elif choice == 3:
                order_id = int(input("Enter Order ID: "))
                generate_bill(order_id)

            elif choice == 4:
                print("Thank you for using Restaurant Food Ordering System.")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

        except ValueError:
            print("Invalid input. Please enter valid values.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
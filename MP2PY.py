import csv
import getpass
import os

from prettytable import PrettyTable
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ORIGINAL_FILE = os.path.join(SCRIPT_DIR, 'navy_equipment.csv')

# Valid users and passwords (you can expand this)
VALID_USERS = {
    "sivs": "sivs123",
    "officer": "securepass"
}

# Load equipment data from original CSV
def load_inventory(filename):
    inventory = []
    if not os.path.exists(filename):
        print(f"File '{filename}' not found. Starting with an empty inventory.")
        return inventory
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Strip whitespace from all fields
            inventory.append({k: v.strip() for k, v in row.items()})
    return inventory

# Save inventory to CSV named per user
def export_inventory(inventory, username):
    filename = f"updated_{username}_navy_equipment_tracker.csv"
    try:
        if not inventory:
            print("Inventory is empty. Nothing to export.\n")
            return
        fieldnames = inventory[0].keys()  # Use keys from first item
        full_path = os.path.abspath(filename)
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(inventory)
        print(f"Inventory exported successfully to '{full_path}'.\n")
    except Exception as e:
        print(f"Error exporting inventory: {e}\n")

# Authentication function
def authenticate():
    attempts = 3
    while attempts > 0:
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")
        if username in VALID_USERS and password == VALID_USERS[username]:
            print(f"\nWelcome, {username}!\n")
            return username
        else:
            attempts -= 1
            print(f"Invalid credentials. Attempts left: {attempts}\n")
    print("Too many failed attempts. Exiting.")
    return None

# Confirm password before sensitive actions
def confirm_password(username):
    password = getpass.getpass("Re-enter password for confirmation: ")
    if VALID_USERS.get(username) == password:
        return True
    else:
        print("Password confirmation failed.\n")
        return False

# Function to print data in a neat table without external libraries
def print_table(data, headers):
    if not data:
        print("No data to display.")
        return

    # Calculate max width for each column
    widths = []
    for header in headers:
        max_len = len(header)
        for row in data:
            max_len = max(max_len, len(str(row.get(header, ''))))
        widths.append(max_len)

    # Print header row
    header_row = " | ".join(header.ljust(width) for header, width in zip(headers, widths))
    print(header_row)
    print("-" * len(header_row))

    # Print rows
    for row in data:
        row_str = " | ".join(str(row.get(header, '')).ljust(width) for header, width in zip(headers, widths))
        print(row_str)
    print()

# View all equipment
def view_inventory(inventory):
    if not inventory:
        print("No equipment in inventory.\n")
        return
    headers = ["Equipment", "Units", "Budget"]
    print("\nCurrent Equipment Inventory:")
    print_table(inventory, headers)

# Add new equipment
def add_equipment(inventory, username):
    if not confirm_password(username):
        return
    equipment = input("Enter equipment name: ").strip()
    while True:
        units = input("Enter units: ").strip()
        if units.isdigit():
            break
        print("Units must be a positive integer.")
    budget = input("Enter budget: ").strip()
    if equipment and budget:
        inventory.append({
            "Equipment": equipment,
            "Units": units,
            "Budget": budget
        })
        print("Equipment added successfully.\n")
    else:
        print("All fields except units are required.\n")

# Delete equipment
def delete_equipment(inventory, username):
    if not inventory:
        print("No equipment to delete.\n")
        return
    if not confirm_password(username):
        return
    view_inventory(inventory)
    try:
        choice = int(input("Enter the number of the equipment to delete: "))
        if 1 <= choice <= len(inventory):
            removed = inventory.pop(choice - 1)
            print(f"Equipment '{removed.get('Equipment', 'N/A')}' deleted successfully.\n")
        else:
            print("Invalid selection.\n")
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")

# Modify equipment
def modify_equipment(inventory, username):
    if not inventory:
        print("No equipment to modify.\n")
        return
    if not confirm_password(username):
        return
    view_inventory(inventory)
    try:
        choice = int(input("Enter the number of the equipment to modify: "))
        if 1 <= choice <= len(inventory):
            item = inventory[choice - 1]
            print("Leave blank to keep current value.")
            equipment = input(f"New Equipment [{item.get('Equipment', '')}]: ").strip()
            while True:
                units = input(f"New Units [{item.get('Units', '')}]: ").strip()
                if units == "" or units.isdigit():
                    break
                print("Units must be a positive integer.")
            budget = input(f"New Budget [{item.get('Budget', '')}]: ").strip()

            if equipment:
                item['Equipment'] = equipment
            if units:
                item['Units'] = units
            if budget:
                item['Budget'] = budget
            print("Equipment entry updated successfully.\n")
        else:
            print("Invalid selection.\n")
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")

# Display main menu
def display_menu():
    print("""\nNavy Equipment Tracker
[1] View Equipment Inventory
[2] Add New Equipment
[3] Delete Equipment
[4] Modify Equipment Entry
[5] Export Inventory to CSV
[0] Exit Program
""")

def main():
    username = authenticate()
    if not username:
        return
    inventory = load_inventory(ORIGINAL_FILE)

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            view_inventory(inventory)
        elif choice == '2':
            add_equipment(inventory, username)
        elif choice == '3':
            delete_equipment(inventory, username)
        elif choice == '4':
            modify_equipment(inventory, username)
        elif choice == '5':
            export_inventory(inventory, username)
        elif choice == '0':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.\n")

if __name__ == "__main__":
    main()

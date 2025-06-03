import csv      
import getpass  # For password masking

# File names
ORIGINAL_FILE = 'navy_directory.csv'
UPDATED_FILE = 'updated_navy_directory.csv'

# Define valid users (username: password)
VALID_USERS = {
    "sivs": "sivs123",
    "officer": "securepass"
}

# Helper function to get field ignoring case and whitespace
def get_field(person, field):
    for key in person.keys():
        if key.strip().lower() == field.lower():
            return person[key]
    return 'N/A'

# Authentication function
def authenticate():
    attempts = 3
    while attempts > 0:
        username = input("Enter username: ").strip()
        password = getpass.getpass("Enter password: ")
        if username in VALID_USERS and password == VALID_USERS[username]:
            print(f"Access granted. Welcome, {username}!\n")
            return True
        else:
            attempts -= 1
            print(f"Incorrect username or password. Attempts left: {attempts}")
    print("Access denied. Exiting program.")
    return False

# Step 1: Read the data from the original CSV file into a list
def load_directory(filename):
    directory = []
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                directory.append(row)
    except FileNotFoundError:
        print(f"File '{filename}' not found. Starting with an empty directory.")
    return directory

# Display the main menu (includes option 7 for logout)
def display_menu():
    print("""
==================================================
| Philippine Navy Personnel Directory Management |
| [1] View All Personnel                         |
| [2] Add New Entry                              |
| [3] Delete an Entry                            |
| [4] Modify an Entry                            |
| [5] Export to updated_navy_directory.csv       |
| [6] Search Personnel                           |
| [7] Logout                                    |
| [0] Exit Program                               |
==================================================
""")

# View all entries
def view_all(directory):
    if not directory:
        print("No personnel entries to display.\n")
        return
    print("\nCurrent Navy Personnel Directory:")
    for idx, person in enumerate(directory, start=1):
        unit = get_field(person, 'Unit')
        print(f"{idx}. Name: {person.get('Name', 'N/A')}, Rank: {person.get('Rank', 'N/A')}, Unit: {unit}")
    print()

# Add a new entry
def add_entry(directory):
    name = input("Enter name: ").strip()
    rank = input("Enter rank: ").strip()
    unit = input("Enter unit: ").strip()
    if name and rank and unit:
        directory.append({'Name': name, 'Rank': rank, 'Unit': unit})
        print("Entry added successfully.\n")
    else:
        print("Invalid input. Name, rank, and unit are required.\n")

# Delete an existing entry
def delete_entry(directory):
    view_all(directory)
    try:
        index = int(input("Enter the entry number to delete: ")) - 1
        if 0 <= index < len(directory):
            removed = directory.pop(index)
            print(f"Entry '{removed.get('Name', 'N/A')}' deleted successfully.\n")
        else:
            print("Invalid entry number.\n")
    except ValueError:
        print("Please enter a valid number.\n")

# Modify an existing entry
def modify_entry(directory):
    view_all(directory)
    try:
        index = int(input("Enter the entry number to modify: ")) - 1
        if 0 <= index < len(directory):
            name = input("Enter new name (leave blank to keep current): ").strip()
            rank = input("Enter new rank (leave blank to keep current): ").strip()
            unit = input("Enter new unit (leave blank to keep current): ").strip()
            if name:
                directory[index]['Name'] = name
            if rank:
                directory[index]['Rank'] = rank
            if unit:
                directory[index]['Unit'] = unit
            print("Entry updated successfully.\n")
        else:
            print("Invalid entry number.\n")
    except ValueError:
        print("Please enter a valid number.\n")

# Export the updated directory to a new CSV file
def export_to_csv(directory, filename):
    with open(filename, mode='w', newline='') as file:
        fieldnames = ['Name', 'Rank', 'Unit']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(directory)
    print(f"Directory exported to '{filename}' successfully.\n")

# Search personnel by name, rank, or unit
def search_personnel(directory):
    keyword = input("Enter name, rank, or unit to search: ").strip().lower()
    results = [
        person for person in directory
        if keyword in person.get('Name', '').lower()
        or keyword in person.get('Rank', '').lower()
        or keyword in get_field(person, 'Unit').lower()
    ]

    if results:
        print("\nSearch Results:")
        for idx, person in enumerate(results, start=1):
            unit = get_field(person, 'Unit')
            print(f"{idx}. Name: {person.get('Name', 'N/A')}, Rank: {person.get('Rank', 'N/A')}, Unit: {unit}")
    else:
        print("No matching personnel found.\n")

# Main program loop with logout feature
def main():
    directory = load_directory(ORIGINAL_FILE)

    while True:
        # Require login
        if not authenticate():
            break  # Exit if authentication fails

        while True:
            display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                view_all(directory)
            elif choice == '2':
                add_entry(directory)
            elif choice == '3':
                delete_entry(directory)
            elif choice == '4':
                modify_entry(directory)
            elif choice == '5':
                export_to_csv(directory, UPDATED_FILE)
            elif choice == '6':
                search_personnel(directory)
            elif choice == '7':  # Logout
                print("Logging out...\n")
                break  # Break inner loop to go back to login
            elif choice == '0':
                print("Exiting program. Goodbye!")
                return
            else:
                print("Invalid option. Please choose from 1 - 7 only.\n")

# Entry point
if __name__ == '__main__':
    main()


# username: officer pass: securepass
# username: sivs pass: sivs123
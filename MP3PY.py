import csv
import os
from tkinter import Tk, filedialog

# === Step 1: Secure Access ===

AUTHORIZED_KEY = "2c1743a391305fbf367df8e4f069f9f9"  # Plain text key you want to use

def get_access_key_file():
    """Open a file dialog for user to select access.key file."""
    root = Tk()
    root.withdraw()  # Hide main window
    file_path = filedialog.askopenfilename(
        title="Select Access Key File", 
        filetypes=[("Key files", "*.txt *.key")]
    )
    root.destroy()
    return file_path

def verify_access_key(file_path):
    if not file_path or not os.path.exists(file_path):
        print("Access key file not found.")
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()  # strip whitespace/newlines
    except Exception as e:
        print(f"Error reading access key file: {e}")
        return False

    # Remove any internal whitespace just in case
    content = "".join(content.split())

    print(f"DEBUG: File content read: '{content}'")

    if content == AUTHORIZED_KEY:
        print("Access Granted.\n")
        return True
    else:
        print("Access Denied: Invalid key.\n")
        return False


# === Data Files ===

PERSONNEL_FILE = "personnel_directory.csv"
EQUIPMENT_FILE = "equipment_inventory.csv"

# === Load Data ===

def load_csv(file_path):
    data = []
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found. Starting empty.")
        return data
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({k: v.strip() for k, v in row.items()})
    return data

# === Save Data ===

def export_csv(data, file_path):
    if not data:
        print(f"No data to export to {file_path}.")
        return
    fieldnames = list(data[0].keys())
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data exported to '{file_path}' successfully.\n")

# === Print Table Helper ===

def print_table(data, headers):
    if not data:
        print("No data to display.\n")
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

    # Print rows with index
    for idx, row in enumerate(data, 1):
        row_str = " | ".join(str(row.get(header, '')).ljust(width) for header, width in zip(headers, widths))
        print(f"{str(idx).rjust(3)}. {row_str}")
    print()

# === Common Menu and Actions ===

def display_menu(title, options):
    print(f"\n{title}")
    for key, val in options.items():
        print(f"[{key}] {val}")
    choice = input("Choose an option: ").strip()
    return choice

def view_entries(data):
    if not data:
        print("No entries available.\n")
        return
    headers = list(data[0].keys())
    print_table(data, headers)

def add_entry(data, fields):
    new_entry = {}
    print("Enter new entry details:")
    for field in fields:
        val = input(f"{field}: ").strip()
        while val == "":
            print(f"{field} cannot be empty.")
            val = input(f"{field}: ").strip()
        new_entry[field] = val
    data.append(new_entry)
    print("Entry added successfully.\n")

def delete_entry(data):
    if not data:
        print("No entries to delete.\n")
        return
    view_entries(data)
    try:
        idx = int(input("Enter entry number to delete: "))
        if 1 <= idx <= len(data):
            removed = data.pop(idx - 1)
            print("Deleted entry:", removed)
        else:
            print("Invalid selection.\n")
    except ValueError:
        print("Invalid input.\n")

def modify_entry(data, fields):
    if not data:
        print("No entries to modify.\n")
        return
    view_entries(data)
    try:
        idx = int(input("Enter entry number to modify: "))
        if 1 <= idx <= len(data):
            entry = data[idx - 1]
            print("Leave input empty to keep current value.")
            for field in fields:
                current = entry.get(field, "")
                new_val = input(f"{field} [{current}]: ").strip()
                if new_val:
                    entry[field] = new_val
            print("Entry updated.\n")
        else:
            print("Invalid selection.\n")
    except ValueError:
        print("Invalid input.\n")

# === Personnel Management ===

PERSONNEL_FIELDS = ["Name", "Rank"]

def manage_personnel(data):
    while True:
        choice = display_menu(
            "Personnel Directory Menu",
            {
                "1": "View Personnel",
                "2": "Add Personnel",
                "3": "Modify Personnel",
                "4": "Delete Personnel",
                "0": "Return to Main Menu",
            },
        )
        if choice == "1":
            view_entries(data)
        elif choice == "2":
            add_entry(data, PERSONNEL_FIELDS)
        elif choice == "3":
            modify_entry(data, PERSONNEL_FIELDS)
        elif choice == "4":
            delete_entry(data)
        elif choice == "0":
            break
        else:
            print("Invalid option.")

# === Equipment Management ===

EQUIPMENT_FIELDS = ["Equipment", "Units", "Budget"]

def manage_equipment(data):
    while True:
        choice = display_menu(
            "Equipment Inventory Menu",
            {
                "1": "View Equipment",
                "2": "Add Equipment",
                "3": "Modify Equipment",
                "4": "Delete Equipment",
                "0": "Return to Main Menu",
            },
        )
        if choice == "1":
            view_entries(data)
        elif choice == "2":
            add_entry(data, EQUIPMENT_FIELDS)
        elif choice == "3":
            modify_entry(data, EQUIPMENT_FIELDS)
        elif choice == "4":
            delete_entry(data)
        elif choice == "0":
            break
        else:
            print("Invalid option.")

# === Main Program ===

def main():
    print("=== INAM - Integrated Naval Asset Manager ===")

    # Step 1: Secure Access
    key_file = get_access_key_file()
    if not verify_access_key(key_file):
        print("Exiting program.")
        return

    # Load data
    personnel_data = load_csv(PERSONNEL_FILE)
    equipment_data = load_csv(EQUIPMENT_FILE)

    while True:
        choice = display_menu(
            "Main Menu",
            {
                "1": "Manage Personnel Directory",
                "2": "Manage Equipment Inventory",
                "3": "Export Update Files",
                "0": "Exit",
            },
        )
        if choice == "1":
            manage_personnel(personnel_data)
        elif choice == "2":
            manage_equipment(equipment_data)
        elif choice == "3":
            export_csv(personnel_data, "updated_personnel_directory.csv")
            export_csv(equipment_data, "updated_equipment_inventory.csv")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()

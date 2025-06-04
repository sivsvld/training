import csv
import getpass

# Dictionary mapping of database names to CSV file names
DATABASES = {
    "armament": "armament.csv",
    "personnel": "personnel.csv",
    "operations": "operations.csv"
}

# Function to load all users from users.csv
def load_users():
    users = {}
    try:
        with open("users.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users[row["username"]] = {
                    "password": row["password"],
                    "role": row["role"],
                    "assigned_db": row["assigned_db"]
                }
    except FileNotFoundError:
        # Create default admin if file doesn't exist
        users["admin"] = {"password": "admin", "role": "Admin", "assigned_db": "all"}
        save_users(users)
    return users

# Function to save all user accounts to users.csv
def save_users(users):
    with open("users.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["username", "password", "role", "assigned_db"])
        writer.writeheader()
        for username, data in users.items():
            writer.writerow({
                "username": username,
                "password": data["password"],
                "role": data["role"],
                "assigned_db": data["assigned_db"]
            })

# Function to handle user login
def login(users):
    print("\n=== LOGIN ===")
    username = input("Username: ")
    password = getpass.getpass("Password: ")  # Hides input for security
    user = users.get(username)
    if user and user["password"] == password:
        print(f"\n✅ Login successful! Role: {user['role']}")
        return username, user
    print("\n❌ Invalid username or password.")
    return None, None

# Load a database file, return its header and rows
def load_db(filename):
    try:
        with open(filename, "r") as f:
            reader = list(csv.reader(f))
            return reader[0], reader[1:]
    except FileNotFoundError:
        # Create default structure if file not found
        header = ["ID", "Name", "Info"]
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
        return header, []

# Save data to a CSV database
def save_db(filename, header, rows):
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"\n✅ Changes saved to {filename}.")

# Export a copy of the database
def export_db(filename, header, rows):
    export_filename = "exported_" + filename
    with open(export_filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"\n✅ Exported database to {export_filename}")

# Display contents of the database
def display_db(header, rows):
    print("\n--- DATABASE CONTENT ---")
    print("No. | " + " | ".join(header))
    print("-" * (6 + len(header) * 15))
    for i, row in enumerate(rows):
        print(f"{i:<3} | " + " | ".join(row))

# Add a new record to the database
def add_record(header, rows):
    print("\n--- ADD NEW RECORD ---")
    new_row = []
    for field in header:
        val = input(f"{field}: ")
        new_row.append(val)
    rows.append(new_row)
    print("✅ Record added.")

# Update a record by index
def update_record(header, rows):
    print("\n--- UPDATE RECORD ---")
    display_db(header, rows)
    try:
        index = int(input("Enter index of record to update: "))
        if 0 <= index < len(rows):
            for i, field in enumerate(header):
                current = rows[index][i]
                val = input(f"{field} [{current}]: ")
                if val.strip() != "":
                    rows[index][i] = val
            print("✅ Record updated.")
        else:
            print("❌ Invalid index.")
    except ValueError:
        print("❌ Invalid input.")

# Delete a record by index
def delete_record(filename, header, rows):
    print("\n--- DELETE RECORD ---")
    display_db(header, rows)
    try:
        index = int(input("Enter index of record to delete: "))
        if 0 <= index < len(rows):
            confirm = input(f"Are you sure you want to delete record #{index}? (y/n): ").lower()
            if confirm == "y":
                rows.pop(index)
                save_db(filename, header, rows)  # Save changes immediately
                print("✅ Record deleted.")
            else:
                print("❌ Deletion canceled.")
        else:
            print("❌ Invalid index.")
    except ValueError:
        print("❌ Invalid input.")

# Create a new user account
def create_user(users):
    print("\n--- CREATE NEW USER ---")
    username = input("New username: ").strip()
    if username == "":
        print("❌ Username cannot be empty.")
        return
    if username in users:
        print("❌ Username already exists.")
        return
    password = getpass.getpass("Password: ")
    role = input("Role [Admin/Supervisor/User]: ").capitalize()
    if role not in ["Admin", "Supervisor", "User"]:
        print("❌ Invalid role.")
        return
    if role == "Admin":
        assigned_db = "all"
    else:
        print("Assign database:")
        for key in DATABASES:
            print(f"- {key}")
        assigned_db = input("Assigned DB: ").lower()
        if assigned_db not in DATABASES:
            print("❌ Invalid database.")
            return
    users[username] = {
        "password": password,
        "role": role,
        "assigned_db": assigned_db
    }
    save_users(users)
    print(f"✅ User '{username}' created.")

# Delete an existing user account
def delete_user(users):
    print("\n--- DELETE USER ---")
    username = input("Enter username to delete: ")
    if username not in users:
        print("❌ User not found.")
        return
    if username == "admin":
        print("⚠️ Cannot delete the default admin user.")
        return
    confirm = input(f"Are you sure you want to delete user '{username}'? (y/n): ").lower()
    if confirm == "y":
        del users[username]
        save_users(users)
        print(f"✅ User '{username}' has been deleted.")
    else:
        print("❌ Deletion canceled.")

# Show menu options depending on user role
def show_db_menu(role):
    print("\nChoose an action:")
    print("[1] View Database")
    if role == "Admin":
        print("[2] Add Record")
        print("[3] Update Record")
        print("[4] Delete Record")
        print("[5] Export Database")
        print("[6] Back to Main Menu")
    else:
        print("[2] Back to Main Menu")
    return input("Select option: ")

# Main program loop
def main():
    while True:
        users = load_users()
        username, user = login(users)
        if not username:
            continue

        role = user["role"]
        assigned_db = user["assigned_db"]

        while True:
            # Display accessible databases
            print("\nAccessible Databases:")
            if role in ["Admin", "Supervisor"]:
                accessible_dbs = list(DATABASES.keys())
            else:
                accessible_dbs = [assigned_db]

            for i, db in enumerate(accessible_dbs):
                print(f"[{i}] {db.title()}")
            if role == "Admin":
                print(f"[{len(accessible_dbs)}] Create New User")
                print(f"[{len(accessible_dbs)+1}] Delete User")
                print(f"[{len(accessible_dbs)+2}] Log out")
            else:
                print(f"[{len(accessible_dbs)}] Log out")

            try:
                choice = int(input("Select an option: "))
            except ValueError:
                print("❌ Invalid input.")
                continue

            # Admin special options
            if role == "Admin":
                if choice == len(accessible_dbs):
                    create_user(users)
                    continue
                elif choice == len(accessible_dbs) + 1:
                    delete_user(users)
                    continue
                elif choice == len(accessible_dbs) + 2:
                    print("\nLogging out...\n")
                    break
            else:
                if choice == len(accessible_dbs):
                    print("\nLogging out...\n")
                    break

            # Handle DB actions
            if 0 <= choice < len(accessible_dbs):
                selected_db = accessible_dbs[choice]
                filename = DATABASES[selected_db]
                header, rows = load_db(filename)

                while True:
                    action = show_db_menu(role)
                    if action == "1":
                        display_db(header, rows)
                    elif action == "2" and role == "Admin":
                        add_record(header, rows)
                    elif action == "3" and role == "Admin":
                        update_record(header, rows)
                    elif action == "4" and role == "Admin":
                        delete_record(filename, header, rows)
                    elif action == "5" and role == "Admin":
                        export_db(filename, header, rows)
                    elif (action == "6" and role == "Admin") or (action == "2" and role != "Admin"):
                        save_db(filename, header, rows)
                        break
                    else:
                        print("❌ Invalid option.")
            else:
                print("❌ Invalid option.")

# Run the program
if __name__ == "__main__":
    main()

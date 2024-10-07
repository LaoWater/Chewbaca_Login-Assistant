import json
import threading
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from scripts.database_engine import database_login_engine

# Function to access Webshare
def access_webshare(entry):
    driver = webdriver.Chrome()  # Ensure you have the correct WebDriver for your browser
    driver.maximize_window()  # Maximize window to ensure visibility of elements

    try:
        # Access the Webshare URL
        webshare_url = entry["Webshare"]
        driver.get(webshare_url)

        # Wait for the page to load and check if the Username field exists
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Username")))

        # Use JavaScript to set the value of the Username field
        driver.execute_script("document.getElementById('Username').value = arguments[0];", entry["User Name"])

        # Use JavaScript to set the value of the hidden Password field
        driver.execute_script("document.getElementById('Password').value = arguments[0];", entry["Password"])
        driver.execute_script("document.getElementById('Password_Text').style.display = 'none';")
        driver.execute_script("document.getElementById('Password').style.display = 'inline';")

        # Use JavaScript to set the value of the Server field
        driver.execute_script("document.getElementById('Server').value = arguments[0];", entry["DB Server"])

        # Use JavaScript to set the value of the Database field
        driver.execute_script("document.getElementById('Database').value = arguments[0];", entry["DB Name"])

        # Use JavaScript to click the Login button
        driver.execute_script("document.getElementById('cmdLogin').click();")

        # Wait until the browser window is closed by the user
        while len(driver.window_handles) > 0:
            time.sleep(1)

    except Exception as e:
        pass

    finally:
        driver.quit()


# Function to update the LastLogin field in the JSONL file
def update_last_login(jsonl_file, entry):
    updated_entries = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(jsonl_file, "r") as file:
        for line in file:
            data = json.loads(line.strip())
            if data["Project"] == entry["Project"]:
                data["Last Login"] = current_time
            updated_entries.append(data)

    with open(jsonl_file, "w") as file:
        for updated_entry in updated_entries:
            file.write(json.dumps(updated_entry) + "\n")

    print(f"Last Login updated for Project: {entry['Project']} to {current_time}")


# Function to delete an entry from the JSONL file
def delete_entry(jsonl_file, entry):
    updated_entries = []
    with open(jsonl_file, "r") as file:
        for line in file:
            data = json.loads(line.strip())
            if data["Project"] != entry["Project"]:
                updated_entries.append(data)

    with open(jsonl_file, "w") as file:
        for updated_entry in updated_entries:
            file.write(json.dumps(updated_entry) + "\n")

    print(f"Entry deleted for Project: {entry['Project']}")


# Function to add a new database entry to the JSONL file
def add_entry(jsonl_file):
    user_input = simpledialog.askstring("Add Database", "Please paste the database information:")

    if user_input:
        # Parse the user input into the correct format
        entry = {}
        for line in user_input.split("\n"):
            key, value = line.split(": ", 1)
            entry[key] = value

        # Ensure all required fields are present
        required_fields = ["Project", "Client Pin", "Client Name", "User Name", "Password", "DB Server", "Instance", "DB Name", "Webshare"]
        if all(field in entry for field in required_fields):
            entry["Last Login"] = "Never"

            # Append the new entry to the JSONL file
            with open(jsonl_file, "a") as file:
                file.write(json.dumps(entry) + "\n")

            print(f"New entry added: {entry['Client Name']}")
        else:
            messagebox.showerror("Error", "Incomplete database information.")


# Function to execute the access_webshare() when login button is pressed
def login(entry, login_button, root):
    def run():
        try:
            access_webshare(entry)
            # root.after(0, lambda: messagebox.showinfo("Success", "Login successful"))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
        finally:
            root.after(0, lambda: login_button.config(state=tk.NORMAL))

    threading.Thread(target=run).start()


# Load data from JSONL file
def load_data(jsonl_file="docs/parsed_chewbaca.jsonl"):
    try:
        with open(jsonl_file, "r") as file:
            entries = [json.loads(line.strip()) for line in file]
        return entries if entries else []
    except FileNotFoundError:
        messagebox.showerror("Error", f"JSONL file '{jsonl_file}' not found.")
        return []


# Main function to set up and run the GUI
def main(jsonl_file):
    entries = load_data(jsonl_file)
    if entries:
        root = tk.Tk()
        root.title("Webshare Databases")

        tk.Label(root, text="Databases (Project - Last Login):").pack()

        listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=50)
        for idx, entry in enumerate(entries):
            last_login = entry.get("Last Login", "Never")
            listbox.insert(idx, f"{idx + 1}. {entry['Project']} - Last Login: {last_login}")
        listbox.pack()

        # Login button
        def on_login():
            selection = listbox.curselection()
            if selection:
                selected_entry = entries[selection[0]]
                update_last_login(jsonl_file, selected_entry)
                login_button.config(state=tk.DISABLED)
                login(selected_entry, login_button, root)
            else:
                messagebox.showwarning("No Selection", "Please select a database from the list.")

        login_button = tk.Button(root, text="Login", command=on_login)
        login_button.pack(side=tk.LEFT)

        # Delete button
        def on_delete():
            selection = listbox.curselection()
            if selection:
                selected_entry = entries.pop(selection[0])
                delete_entry(jsonl_file, selected_entry)
                listbox.delete(selection[0])
            else:
                messagebox.showwarning("No Selection", "Please select a database to delete.")

        delete_button = tk.Button(root, text="Delete Database", command=on_delete)
        delete_button.pack(side=tk.LEFT)

        # Add button
        def on_add():
            add_entry(jsonl_file)
            root.quit()

        add_button = tk.Button(root, text="Add Database", command=on_add)
        add_button.pack(side=tk.LEFT)

        # Exit button
        def on_exit():
            root.quit()

        exit_button = tk.Button(root, text="Exit", command=on_exit)
        exit_button.pack(side=tk.LEFT)

        root.bind('<Escape>', lambda event: on_exit())

        root.mainloop()
    else:
        messagebox.showwarning("No Entries", "No entries found in the JSONL file.")


# Example usage
if __name__ == "__main__":
    jsonl_file="docs/parsed_chewbaca.jsonl"
    data = load_data(jsonl_file)
    print(data)
    database_login_engine("New Rent Roll")
    time.sleep(3)
    main(jsonl_file)

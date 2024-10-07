# Version 6 - Modularized, Improved GUI UX and flow 
# Covered many bugs in the whole work flow
# Now can be used continous and distributex in .exe

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
            entry["Current Step"] = ''

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


# Function to format the date as "DD/MM/YYYY HH:SS"
def format_date(last_login):
    if last_login != "Never":
        try:
            date_object = datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S')
            return date_object.strftime('%d/%m/%Y %H:%M')
        except ValueError:
            return last_login  # In case of formatting issues, return as-is
    return last_login

# Function to populate the Listbox with database entries
def populate_listbox(listbox, entries):
    fixed_spacing_login = 28  # Define the position where "Last Login" should start
    fixed_spacing_step = 42   # Define the position where "Current Step" should start

    for idx, entry in enumerate(entries):
        last_login = entry.get("Last Login", "Never")
        formatted_login = format_date(last_login)
        project_name = entry.get('Project', 'Unknown Project')
        current_step = entry.get('Current Step', '')  # Get the current step (default to empty string)

        # Calculate the number of spaces to add after the project name and last login
        padding_login = ' ' * (fixed_spacing_login - len(project_name))  # Ensure alignment of Last Login
        padding_step = ' ' * (fixed_spacing_step - (len(project_name) + len(formatted_login)))  # Ensure alignment of Current Step

        # Create the final string for the listbox entry
        entry_string = f"{project_name}{padding_login}{formatted_login}{padding_step}{current_step}"

        # Insert the entry into the listbox
        listbox.insert(idx, entry_string)



# Function to add notes for the current step of the project
def on_add_notes(listbox, entries):
    selection = listbox.curselection()
    if selection:
        selected_entry = entries[selection[0]]
        project_name = selected_entry['Project']
        
        # Prompt user for input
        note = simpledialog.askstring("Add Notes", f"Enter notes for '{project_name}':")
        
        if note:
            update_project_notes(jsonl_file, project_name, note)
        else:
            messagebox.showwarning("No Notes Entered", "No notes were added.")
    else:
        messagebox.showwarning("No Selection", "Please select a database from the list.")


# Function to update the notes (Current Step) for a project in the JSONL file
def update_project_notes(jsonl_file, project_name, new_note):
    # Load the current entries from the JSONL file
    entries = []
    with open(jsonl_file, 'r') as file:
        for line in file:
            entries.append(json.loads(line))
    
    # Locate the project by its name and update the "Current Step" field
    project_found = False
    for entry in entries:
        if entry.get('Project') == project_name:
            try:
                # Add the 'Current Step' field if it doesn't exist
                if 'Current Step' not in entry or entry['Current Step'] is None:
                    entry['Current Step'] = new_note  # Initialize with the new note
                else:
                    entry['Current Step'] += f"\n{new_note}"  # Append the new note
                
                project_found = True
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while updating 'Current Step': {str(e)}")
            break
    
    # If the project was not found, show an error message
    if not project_found:
        messagebox.showerror("Error", f"Project '{project_name}' not found in the JSONL file.")
        return
    
    # Save the updated entries back to the JSONL file
    try:
        with open(jsonl_file, 'w') as file:
            for entry in entries:
                file.write(json.dumps(entry) + '\n')
        messagebox.showinfo("Success", f"Notes for '{project_name}' have been updated.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving updates: {str(e)}")



# Login function for the selected database
def on_login(listbox, entries, jsonl_file, login_button, root):
    selection = listbox.curselection()
    if selection:
        selected_entry = entries[selection[0]]
        update_last_login(jsonl_file, selected_entry)
        login_button.config(state=tk.DISABLED)
        login(selected_entry, login_button, root)
    else:
        messagebox.showwarning("No Selection", "Please select a database from the list.")

# Delete function for the selected database
def on_delete(listbox, entries, jsonl_file):
    selection = listbox.curselection()
    if selection:
        selected_entry = entries.pop(selection[0])
        delete_entry(jsonl_file, selected_entry)
        listbox.delete(selection[0])
    else:
        messagebox.showwarning("No Selection", "Please select a database to delete.")

# Add function to add a new database entry
def on_add(jsonl_file, root):
    add_entry(jsonl_file)
    root.quit()

# Access database function
def on_access_database(listbox, entries):
    selection = listbox.curselection()
    if selection:
        selected_entry = entries[selection[0]]
        project_name = selected_entry['Project']
        database_login_engine(project_name)
    else:
        messagebox.showwarning("No Selection", "Please select a database to access.")



# Main function to set up and run the GUI
def main(jsonl_file):
    entries = load_data(jsonl_file)

    if entries:
        root = tk.Tk()
        root.title("Chewbaca")
        root.geometry("800x450")  # Larger window size for better layout

        # Setting the background color to grey
        root.configure(bg='#D3D3D3')

        # Heading label
        tk.Label(root, text="Databases", font=("Arial", 14), bg='#D3D3D3').pack(pady=10)

        # Frame for column labels
        column_frame = tk.Frame(root, bg='#D3D3D3')
        # Column labels
        tk.Label(column_frame, text="Project", font=("Courier", 12), width=25, anchor='w', bg='#D3D3D3').pack(side=tk.LEFT, padx=10)
        tk.Label(column_frame, text="Last Login", font=("Courier", 12), width=23, anchor='w', bg='#D3D3D3').pack(side=tk.LEFT)
        tk.Label(column_frame, text="Current Step", font=("Courier", 12), width=20, anchor='w', bg='#D3D3D3').pack(side=tk.LEFT)

        column_frame.pack()

        # Frame to hold the listbox and scrollbar
        frame = tk.Frame(root)
        frame.pack(pady=10)

        # Listbox to display database entries with columns for Databases, Last Login, and Current Step
        listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=85, height=15, bg='#F0F0F0', font=("Courier", 12))  # Adjusted width to better fit the window
        populate_listbox(listbox, entries)  # Populate the listbox with formatted data
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        # Button Frame for layout organization
        button_frame = tk.Frame(root, bg='#D3D3D3')
        button_frame.pack(pady=10)

        # Login button
        login_button = tk.Button(button_frame, text="Login", command=lambda: on_login(listbox, entries, jsonl_file, login_button, root), width=12, font=("Courier", 12), bg='#A9A9A9')
        login_button.pack(side=tk.LEFT, padx=5)

        # Add button
        add_button = tk.Button(button_frame, text="Add", command=lambda: on_add(jsonl_file, root), width=12, font=("Courier", 12), bg='#A9A9A9')
        add_button.pack(side=tk.LEFT, padx=5)

        # Access Database button
        access_button = tk.Button(button_frame, text="SQL Access", command=lambda: on_access_database(listbox, entries), width=12, font=("Courier", 12), bg='#A9A9A9')
        access_button.pack(side=tk.LEFT, padx=5)

        # Add Notes button
        add_notes_button = tk.Button(button_frame, text="Add Notes", command=lambda: on_add_notes(listbox, entries), width=12, font=("Courier", 12), bg='#A9A9A9')
        add_notes_button.pack(side=tk.LEFT, padx=5)

        # Delete button
        delete_button = tk.Button(button_frame, text="Delete", command=lambda: on_delete(listbox, entries, jsonl_file), width=12, font=("Courier", 12), bg='#A9A9A9')
        delete_button.pack(side=tk.LEFT, padx=5)

        # Exit button
        exit_button = tk.Button(button_frame, text="Exit", command=root.quit, width=12, font=("Courier", 12), bg='#A9A9A9')
        exit_button.pack(side=tk.LEFT, padx=5)

        root.bind('<Escape>', lambda event: root.quit())

        root.mainloop()
    else:
        messagebox.showwarning("No Entries", "No entries found in the JSONL file.")




# Example usage
if __name__ == "__main__":
    jsonl_file="docs/parsed_chewbaca.jsonl"
    data = load_data(jsonl_file)
    main(jsonl_file)

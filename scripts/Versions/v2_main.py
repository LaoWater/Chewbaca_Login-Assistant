import json
import subprocess
from tkinter import Tk, Label, Button, Listbox, SINGLE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

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

        print(f"Successfully logged in for Case/CPR: {entry['Case/CPR']}")
        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

# Function to update the LastLogin field in the JSONL file
def update_last_login(jsonl_file, entry):
    updated_entries = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(jsonl_file, "r") as file:
        for line in file:
            data = json.loads(line.strip())
            if data["Case/CPR"] == entry["Case/CPR"]:
                data["Last Login"] = current_time
            updated_entries.append(data)
    
    with open(jsonl_file, "w") as file:
        for updated_entry in updated_entries:
            file.write(json.dumps(updated_entry) + "\n")
    
    print(f"Last Login updated for Case/CPR: {entry['Case/CPR']} to {current_time}")

# Function to execute the access_webshare() when login button is pressed
def login(entry):
    if entry:
        access_webshare(entry)

# Modified GUI Setup to show Last Login
def setup_gui(entries):
    root = Tk()
    root.title("Webshare Databases")

    Label(root, text="Databases (Case/CPR - Last Login):").pack()

    # Listbox to display all available projects with Case/CPR and Last Login
    listbox = Listbox(root, selectmode=SINGLE)
    for idx, entry in enumerate(entries):
        last_login = entry.get("Last Login", "Never")  # Display "Never" if Last Login is not set
        listbox.insert(idx, f"{idx + 1}. {entry['Case/CPR']} - Last Login: {last_login}")
    listbox.pack()

    # Login button that executes access_webshare() when clicked
    def on_login():
        selection = listbox.curselection()
        if selection:
            selected_entry = entries[selection[0]]
            update_last_login(jsonl_file, selected_entry)  # Update LastLogin before login
            login(selected_entry)
            root.destroy()  # Close the current GUI window to restart the loop

    Button(root, text="Login", command=on_login).pack()

    root.mainloop()

# Load data from JSONL file and initialize the GUI
def load_data_and_start_gui(jsonl_file):
    with open(jsonl_file, "r") as file:
        entries = [json.loads(line.strip()) for line in file]

    if entries:
        return entries
    else:
        print("No entries found in the JSONL file.")
        return []

def main_loop(jsonl_file):
    entries = load_data_and_start_gui(jsonl_file)  # Load entries once
    if entries:
        keep_running = True  # Variable to control the loop
        while keep_running:
            root = Tk()  # Create the GUI
            root.title("Webshare Databases")

            Label(root, text="Databases:").pack()

            # Listbox to display all available projects
            listbox = Listbox(root, selectmode=SINGLE)
            for idx, entry in enumerate(entries):
                listbox.insert(idx, f"{idx + 1}. {entry['Case/CPR']}")
            listbox.pack()

            # Login button that executes access_webshare() when clicked
            def on_login():
                selection = listbox.curselection()
                if selection:
                    selected_entry = entries[selection[0]]
                    root.quit()  # Disengage the GUI after selection (without closing the loop)
                    update_last_login(jsonl_file, selected_entry)  # Update LastLogin before login
                    login(selected_entry)  # Call the login function
                    root.destroy()  # Close the window after login attempt

            Button(root, text="Login", command=on_login).pack()

            # Exit function to quit the program
            def on_exit(event=None):
                nonlocal keep_running
                keep_running = False
                root.quit()
                root.destroy()

            # Exit button to quit the program
            Button(root, text="Exit", command=on_exit).pack()

            # Bind the Escape key to the exit function
            root.bind('<Escape>', on_exit)

            root.mainloop()  # Keeps the GUI running until login or exit is pressed


# Example usage
if __name__ == "__main__":
    jsonl_file = "docs/parsed_chewbaca.jsonl"
    main_loop(jsonl_file)

import json
import threading
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from my_package import database_parser

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
        messagebox.showerror("Error", f"An error occurred: {e}")

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
def login(entry, login_button):
    def run():
        try:
            access_webshare(entry)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during login: {str(e)}")
        finally:
            # Re-enable the login button after login attempt
            login_button.config(state=tk.NORMAL)

    # Run the blocking access_webshare in a separate thread
    threading.Thread(target=run).start()

# Load data from JSONL file
def load_data(jsonl_file):
    with open(jsonl_file, "r") as file:
        entries = [json.loads(line.strip()) for line in file]

    if entries:
        return entries
    else:
        print("No entries found in the JSONL file.")
        return []

# Main function to set up and run the GUI
def main(jsonl_file):
    entries = load_data(jsonl_file)  # Load entries once
    if entries:
        root = tk.Tk()
        root.title("Webshare Databases")

        tk.Label(root, text="Databases (Case/CPR - Last Login):").pack()

        # Listbox to display all available projects with Case/CPR and Last Login
        listbox = tk.Listbox(root, selectmode=tk.SINGLE)
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
                login_button.config(state=tk.DISABLED)  # Disable the button during login
                login(selected_entry, login_button)

        login_button = tk.Button(root, text="Login", command=on_login)
        login_button.pack()

        # Exit button to quit the program
        def on_exit():
            if messagebox.askokcancel("Quit", "Do you really want to quit?"):
                root.quit()

        exit_button = tk.Button(root, text="Exit", command=on_exit)
        exit_button.pack()

        # Bind the Escape key to the exit function
        root.bind('<Escape>', lambda event: on_exit())

        root.mainloop()
    else:
        messagebox.showwarning("No Entries", "No entries found in the JSONL file.")

# Example usage
if __name__ == "__main__":
    regenerate_json = True
    if regenerate_json:
        database_parser.parse_txt_to_jsonl()

    jsonl_file = "docs/parsed_chewbaca.jsonl"
    main(jsonl_file)

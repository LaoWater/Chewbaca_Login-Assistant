import pyautogui
import time
import subprocess
import os
import pygetwindow as gw 
import json
import re

# Open SSMS and wait for it to load
ssms_path = r'C:/Program Files (x86)/Microsoft SQL Server Management Studio 19/Common7/IDE/ssms.exe'
subprocess.Popen(ssms_path)

# Loop to wait until the correct SSMS window is found, then activate it
def bring_ssms_to_foreground():
    ssms_window = None
    while ssms_window is None:
        # Search for SSMS windows and ignore those with "rdiapp" in the title
        for window in gw.getAllTitles():
            if "SQL Server Management Studio" in window and "rdiapp" not in window:
                ssms_window = gw.getWindowsWithTitle(window)[0]
                break
        
        # If the correct SSMS window is not found, wait and try again
        if ssms_window is None:
            print("Waiting for SSMS to open and initialize...")
            time.sleep(3)  # Wait 1 second before checking again


    
    print("SSMS found, wait an additional 3 seconds to allow full initialization and Activate")
    time.sleep(1)
    
    # Bring SSMS window to the foreground
    print(ssms_window)
    ssms_window.activate()
    print("Activating Window...")
    time.sleep(1)  # Give it a moment to become active

# Call the function to bring SSMS to the foreground
bring_ssms_to_foreground()

# Move the mouse to the 'Server Name' field (coordinates: 850, 280) and click
pyautogui.moveTo(1033, 444)  # Replace with the actual coordinates if needed
pyautogui.click()  # Click on the 'Server Name' field

exit()
####################
## Phase 2: Login ##
####################

# Step 1: Define the base path and navigate to the correct directory
base_path = r'C:/Users/RaulBa/Desktop/Neo/Chewbaca/Chewbaca_python/docs'
os.chdir(base_path)  # Change to the target directory

# File name
file_name = 'parsed_chewbaca.jsonl'

# Read the JSONL file
def load_jsonl(file_name):
    data = []
    with open(file_name, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

# Load the data from the JSONL file
data = load_jsonl(file_name)

# Step 2: Define the login function
def login(case_cpr):
    # Step 2.1: Find the entry that matches the provided 'Case/CPR'
    entry = None
    for item in data:
        if item.get('Case/CPR') == case_cpr:
            entry = item
            break
    
    if not entry:
        print(f"No match found for Case/CPR: {case_cpr}")
        return

    # Step 2.2: Extract necessary information from the matched entry
    username = entry['User Name']
    password = entry['Password']
    db_server = entry['DB Server']

    # Extract the last 2 or 3 digits of the DB server
    db_last_digits = re.search(r"(\d{2,3})$", db_server).group(1)  # Match the last 2 or 3 digits

    # Construct the adjusted server URL for SSMS login
    server_address = f"crdb.yardiapp.com,30{db_last_digits.zfill(3)}"

    # Step 3: Fill in the SSMS login form fields (assuming you have already clicked on 'Server Name')
    print(f"Logging in to Case/CPR: {case_cpr}")
    print(f"Server Address: {server_address}")
    print(f"Username: {username}")
    print(f"Password: {password}")

    # Move the mouse to the 'Server Name' field and write the server address
    pyautogui.write(server_address)
    time.sleep(2)

    # Move to authentication and select SQL Server Authentication
    pyautogui.press('tab')  # Move to authentication
    time.sleep(2)
    pyautogui.press('down')  # Switch to SQL Server Authentication
    time.sleep(2)
    pyautogui.press('tab')  # Move to 'Login' field
    time.sleep(2)

    # Enter the extracted username and password
    pyautogui.write(username)
    time.sleep(2)
    pyautogui.press('tab')
    time.sleep(2)
    pyautogui.write(password)
    time.sleep(2)

    # Press Enter or click to login
    pyautogui.press('enter')  # Or adjust to the button coordinates

# Example: SSMS is already started and you've clicked on 'Server Name'
login("Rent Roll")  # Example Case/CPR value, replace with your desired Case/CPR
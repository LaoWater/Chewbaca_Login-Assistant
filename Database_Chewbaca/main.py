import pyautogui
import time
import json
import re
import subprocess
import os

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

# Step 2: Extract the first element's values (username, password, DB Server last 2 or 3 digits)
first_entry = data[0]  # This selects the first entry; we will add a GUI for dynamic selection later

username = first_entry['User Name']
password = first_entry['Password']
db_server = first_entry['DB Server']

# Extract the last 2 or 3 digits of the DB server
db_last_digits = re.search(r"(\d{2,3})$", db_server).group(1)  # Match the last 2 or 3 digits

# Construct the adjusted server URL for SSMS login
# If it's a 2-digit string, use '300XX', if it's 3 digits, use as is.
server_address = f"crdb.yardiapp.com,30{db_last_digits.zfill(3)}"

# Step 3: Automate opening SSMS and filling in the form
# Path to SSMS
subprocess.Popen(r'C:/Program Files (x86)/Microsoft SQL Server Management Studio 19/Common7/IDE/ssms.exe')
time.sleep(25)  # Adjust based on how long SSMS takes to load

# Automate filling server name
pyautogui.click(850, 280)  # Replace with coordinates for 'Server Name'
pyautogui.write(server_address)

# Move to authentication and select SQL Server Authentication
pyautogui.press('tab')  # Move to authentication
pyautogui.press('down')  # Switch to SQL Server Authentication
pyautogui.press('tab')  # Move to 'Login' field

# Enter the extracted username and password
pyautogui.write(username)
pyautogui.press('tab')
pyautogui.write(password)

# Press Enter or click to login
pyautogui.press('enter')  # Or adjust to the button coordinates

# Optional: Add time.sleep or validation after login
time.sleep(5)

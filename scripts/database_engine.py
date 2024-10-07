import pyautogui
import time
import subprocess
import os
import pygetwindow as gw
import json
import re
import win32gui
import win32con
import random

# SSMS behavior with both win32gui and pygetwindow:
# If no mouse & keyboard input is made, window initializes as main and script recoginze it.
# Example: Click on anohter window, alt tab, random typing on keyboard
# If any input is given, window is found but both library fail to activate it - and the manipulated window remains the one active.
# Still, not fatal - with exception catching the mouse continues movement
# It's like at second 0 when ssms.exe is initialized - it creates his main window position and holds that until opened, not allowing interference just at the end.
# Interesting behavior

# Function to read the JSONL file and extract login information
def get_login_information(project):
    from scripts.v6_main import load_data
    # Load the data from the JSONL file
    data = load_data()
    # print(data)
   
    # Step 2: Search for the project in the JSON data
    for entry in data:
        if entry.get('Project') == project: 
            # Extract relevant fields
            username = entry['User Name'].strip()
            password = entry['Password'].strip()
            db_server = entry['DB Server'].strip()
            project_name = entry['Project'].strip()
            webshare = entry['Webshare'].strip()

    # Extract the last 2 or 3 digits of the DB server
    db_last_digits = re.search(r"(\d{2,3})$", db_server).group(1)  # Match the last 2 or 3 digits

    # Construct the adjusted server URL for SSMS login
    server_address = f"crdb.yardiapp.com,30{db_last_digits.zfill(3)}"

    return username, password, server_address, project_name, webshare


def alt_tab_to_ssms():
    print("Finding SSMS window position...")
    windows = gw.getAllTitles()  # Get a list of all open windows

    # Filter out empty, whitespace-only, or irrelevant window titles (e.g., "Windows Input Experience")
    valid_windows = [
        window for window in windows if window.strip() 
        and "Windows Input Experience" not in window 
        and "Program Manager" not in window
    ]
    # Print out all valid window titles with their indices for easier debugging
    print("\nList of valid open windows:")
    for i, window in enumerate(valid_windows):
        print(f"{i + 1}: {window}")

    total_valid_windows = len(valid_windows)  # Total number of valid windows
    print(f"\nTotal valid windows counted: {total_valid_windows}")

    if total_valid_windows == 0:
        print("No windows found.")
        return

    print(f"SSMS is expected to be the last window. Performing {total_valid_windows - 1} Alt-Tab(s)...")

    # Perform Alt-Tab (total_valid_windows - 3) times to reach the SSMS window, as if we reach this part of code, it will be last element
    pyautogui.keyDown('alt')  # Hold down Alt key
    for _ in range(total_valid_windows - 1):
        pyautogui.press('tab')  # Press Tab to cycle through windows
        time.sleep(0.07)  # Small delay between Tab presses
    pyautogui.keyUp('alt')  # Release Alt key

    print("Reached SSMS window via Alt-Tab.")


# Loop to wait until the correct SSMS window is found, then activate it
def bring_ssms_to_foreground(retries=100, delay=1):
    ssms_window = None
    attempt = 0
    # Absolute mininum time to initialize
    time.sleep(7)
    while ssms_window is None and attempt < retries:
        attempt += 1
        # Search for SSMS windows and ignore those with "rdiapp" in the title
        for window in gw.getAllTitles():
            if "SQL Server Management Studio" in window and "rdiapp" not in window:
                ssms_window = gw.getWindowsWithTitle(window)[0]
                break

        if ssms_window is None and attempt%7 == 0:
            print(f"Attempt {attempt}: Waiting for SSMS to open and initialize...")
            time.sleep(delay)  # Wait before checking again

    if ssms_window is None:
        raise Exception("SSMS window could not be found after multiple attempts.")

    print("SSMS found, wait an additional 1 seconds to allow full initialization and activate.")
    time.sleep(1)  # Allow SSMS to fully initialize

    # Activate SSMS window using pywin32
    try:
        hwnd = ssms_window._hWnd  # Get the window handle
        win32gui.SetForegroundWindow(hwnd)  # Bring to foreground
        # win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)  # Maximize if needed
        print("SSMS window activated.")
    except Exception as e:
        print(f"Error while activating SSMS window: {e} \n Entered alt-tab save_Method")
        # Call the Alt-Tab function if activation fails, this means there has been key/mouse input between initialization and Activation
        location = find_new_query_image()
        if not location:
            alt_tab_to_ssms()
        print("Continuing with mouse movement...")


# Function to interact with the SSMS login form
def fill_ssms_login(server_name, username, password):
    time.sleep(0.33)  # Small delay before starting

    # Step 1: Find and click the 'Server Name' field based on the image
    click_on_server_name()
    time.sleep(0.15)
    pyautogui.hotkey('ctrl', 'a')  # Select all text (Ctrl + A)
    time.sleep(0.15)

    # Step 2: Paste the built-up server name
    pyautogui.write(server_name)
    time.sleep(0.15)

    # Step 3: Tab to the Authentication field (do nothing)
    pyautogui.press('tab')
    time.sleep(0.15)

    # Step 4: Tab to the 'Username' field
    pyautogui.press('tab')
    time.sleep(0.15)

    # Step 5: Paste the username
    pyautogui.write(username)
    time.sleep(0.15)

    # Step 6: Tab to the 'Password' field
    pyautogui.press('tab')
    time.sleep(0.15)

    # Step 7: Paste the password
    pyautogui.write(password)
    time.sleep(0.15)

    # Step 8: Tab to 'Remember Me' (do nothing)
    pyautogui.press('tab')
    time.sleep(0.15)

    # Step 9: Press Enter to login
    pyautogui.press('enter')
    time.sleep(0.15)


# Function to find the SSMS Server Name field image and click
def click_on_server_name():
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Construct the full image path using os.path.join
    image_path = os.path.join(current_directory, 'docs/ssms server name.png')
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=0.9) # Find image with 90% confidence
        if location:
            x, y = location.left, location.top  # Get the top-left coordinates of the image
            print(f"Found SSMS Server Name image at: ({x}, {y})")
            # Adjust coordinates: move 10 pixels down and 170 pixels to the right
            adjusted_x = x + 200
            adjusted_y = y + 10
            pyautogui.moveTo(adjusted_x, adjusted_y)
            pyautogui.click()
        else:
            print("Could not find the SSMS server name image.")
    except Exception as e:
        print(f"Finding Image Issue {e}")


def find_new_query_image():
    # Step 1: Locate the "ssms new query" image on the screen
    image_path = os.path.join(os.getcwd(), 'docs/ssms new query.png')
    location = None
    
    try:
        # Locate the image on the screen
        location = pyautogui.locateOnScreen(image_path, confidence=0.9)
    except Exception as e:
        print(f"Could not find SSMS New Query, Windows is not main: {e}")

    return location



# Function to perform the required steps
def save_query_with_project_name(project_name):
    # Step 1: Locate the "ssms new query" image on the screen
    location = find_new_query_image()
    
    if location:
        # Get the top-left coordinates of the image and normalize to center of image
        x, y = location.left + 12, location.top + 12  
        # print(f"Found image at: ({x}, {y})")
        
        # Move the mouse to the new query button and click
        pyautogui.moveTo(x, y)
        pyautogui.click()

        # Step 2: Wait for New Query to load
        time.sleep(2.1)

        # Step 3: Press Ctrl + S (Save As)
        pyautogui.hotkey('ctrl', 's')
        time.sleep(0.5)  # Small delay to allow the save dialog to appear


        # Step 4: Write the project name field value
        # Generate a random number between 1 and 333
        random_number = random.randint(1, 333)
        # Concatenate the project name with the random number for handlding Duplicates in case of multiple acceses
        name_with_random = f"{project_name}_{random_number}"
        pyautogui.write(name_with_random)
        time.sleep(0.5)

        # Step 5: Hit Enter to save
        pyautogui.press('enter')
        print(f"Saved file as: {project_name}")
    else:
        print("Could not find the 'ssms new query' image.")


# Function to transform the Webshare field into the desired format
def transform_webshare(webshare):
    # Extract the IP part from the webshare URL using regex
    ip_match = re.search(r"https://(\d+)\.crweb\.yardiapp\.com", webshare)
    if ip_match:
        ip_part = ip_match.group(1)
        # Split the Webshare URL by ".com/" and take the part after it
        path_part = webshare.split(".com/")[1]
        # Remove anything after the first `/` in the remaining path to clean up "pages/Login.aspx"
        path_part = path_part.split("/")[0]
        # Replace the URL with the new format
        transformed_path = f"\\\\10.242.1.{ip_part}\\sandbox\\{path_part}\\Reports\\"
        return transformed_path
    else:
        return None




# Function to run the SQL query and press F5
def run_sql_query(webshare):
    from scripts.sensitive_data import get_sql_query

    # Step 1: Write the "Hello, World!" query
    query = "SELECT 'Hello, World!';"
    
    # Move the mouse to the SQL editor (Assuming you're already in the SQL Query window)
    pyautogui.write(query)
    time.sleep(0.5)

    # Step 2: Press F5 to run the script
    pyautogui.press('f5')
    print("SQL query executed: Hello, World!")

    # Step 3: Transform the webshare and fetch the SQL query using the new function
    transformed_path = transform_webshare(webshare)
    sql_query = get_sql_query(transformed_path)

    # Use regular expression to format the query string
    formatted_sql_query = re.sub(r' {2,}', '', sql_query)
    
    # Write the useful queries as comments in the query editor
    pyautogui.write(formatted_sql_query)
    time.sleep(0.2)


# Main function to execute the flow with a given project
def database_login_engine(project):
    # Step 1: Get login information for the given project from the JSONL file
    username, password, server_address, project_name, webshare = get_login_information(project)

    # If the project is found, proceed
    if username and password and server_address:
        # Open SSMS and wait for it to load
        ssms_path = r'C:/Program Files (x86)/Microsoft SQL Server Management Studio 19/Common7/IDE/ssms.exe'
        subprocess.Popen(ssms_path)

        # Call the function to bring SSMS to the foreground
        bring_ssms_to_foreground()

        # Call the function to fill in the SSMS login details
        fill_ssms_login(server_address, username, password)

        # Save the query using the project name
        save_query_with_project_name(project_name)

        # Run the SQL query using the Webshare information
        run_sql_query(webshare)

        print("Enjoy your Flight!")
    else:
        print(f"Could not find login information for project '{project}'.")
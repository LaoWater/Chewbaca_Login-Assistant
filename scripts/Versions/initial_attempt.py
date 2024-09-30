import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

def access_webshare(project, jsonl_file):
    # Load the data from JSONL file
    with open(jsonl_file, "r") as file:
        entries = [json.loads(line.strip()) for line in file]

    # Find the entry for the given project (Case/CPR)
    entry = next((item for item in entries if item["Case/CPR"] == project), None)
    
    if not entry:
        print(f"No matching project found for Case/CPR: {project}")
        return

    # Launch the browser using Selenium
    driver = webdriver.Chrome()  # Make sure you have the appropriate WebDriver in your PATH
    driver.maximize_window()  # Maximize window to ensure visibility of elements

    try:
        # Access the Webshare URL
        webshare_url = entry["Webshare"]
        driver.get(webshare_url)

        # Wait until the Username field is visible and interactable
        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "Username"))
            )
            username_field.send_keys(entry["User Name"])
        except TimeoutException:
            print("Username field is not visible or interactable.")
            return

        # Wait for the password field to become visible
        try:
            password_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "Password_Text"))
            )
            password_field.send_keys(entry["Password"])
        except TimeoutException:
            print("Password field is not visible or interactable.")
            return

        # Wait for the server field to become visible
        try:
            server_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "Server"))
            )
            server_field.send_keys(entry["DB Server"])
        except TimeoutException:
            print("Server field is not visible or interactable.")
            return

        # Wait for the database field to become visible
        try:
            database_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "Database"))
            )
            database_field.send_keys(entry["DB Name"])
        except TimeoutException:
            print("Database field is not visible or interactable.")
            return

        # Submit the form
        # driver.find_element(By.ID, "cmdLogin").click()

        print(f"Successfully filled in the form for Case/CPR: {project}")

        # Pause to keep the browser open for manual inspection
        input("Press Enter to close the browser...")

    except ElementNotInteractableException as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

# Example usage
if __name__ == "__main__":
    access_webshare("Rent Roll", "docs/parsed_chewbaca.jsonl")

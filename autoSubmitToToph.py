import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables from .env file
load_dotenv()

# Variables from .env
TOPH_USERNAME = os.getenv('TOPH_USERNAME')
TOPH_PASSWORD = os.getenv('TOPH_PASSWORD')
WAIT_TIME = int(os.getenv('WAIT_TIME'))

COMMON_URL_PREFIX = "https://toph.co/p/"
SUBMISSION_URL_PREFIX = "https://toph.co/s/"

def login(tophHandle, tophPassword):
    """Login to Toph.co using provided credentials."""
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        driver.get("https://toph.co/login")
        print("Navigated to Toph login page.")

        username_input = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, 'handle'))
        )
        password_input = driver.find_element(By.NAME, 'password')

        username_input.send_keys(tophHandle)
        password_input.send_keys(tophPassword)
        password_input.send_keys(Keys.RETURN)
        print("Logged in successfully.")
        return driver
    except Exception as e:
        print(f"Error during login: {e}")

def submit(driver, problem_id, code):
    """Submit the given code to the specified problem and return the submission ID."""
    try:
        submission_url = COMMON_URL_PREFIX + problem_id
        driver.get(submission_url)
        print(f"Opened problem URL: {submission_url}")

        # Wait for the "Open Editor" button to become clickable and click it
        open_editor_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Open Editor']"))
        )
        open_editor_button.click()
        print("Clicked on 'Open Editor' button.")

        # Add a delay to allow the editor panel to fully load
        time.sleep(3)

        # Scroll to the dropdown to make sure it's in view
        language_dropdown_trigger = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'aside[data-codepanel-problemslug="add-them-up"] div.dropdown.-select'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", language_dropdown_trigger)
        print("Scrolled to language dropdown.")

        # Use JavaScript to directly open the dropdown and select the C++23 language
        driver.execute_script("""
            let dropdown = document.querySelector('aside[data-codepanel-problemslug="add-them-up"] div.dropdown.-select');
            dropdown.click();  // Open the dropdown

            let options = dropdown.querySelectorAll('a');
            options.forEach(function(option) {
                if (option.textContent.includes('C++23 GCC 13.2')) {
                    option.click();  // Select C++23 GCC 13.2
                }
            });
        """)
        print("Selected 'C++23 GCC 13.2' language via JavaScript.")

        # Wait for the editor to be ready
        editor = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'cm-content'))
        )

        # Clear the editor and paste the code
        driver.execute_script("arguments[0].innerText = arguments[1];", editor, code)
        print("Code has been pasted into the editor.")

        # Click the "Submit" button
        submit_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit']"))
        )
        submit_button.click()
        print("Clicked on 'Submit' button.")

        # Wait for the submission result row to appear
        result_row = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'syncer')]"))
        )

        # Extract the submission ID from the first <td>
        submission_id = result_row.find_element(By.XPATH, ".//td[1]").text
        print(f"Submission ID: {submission_id}")

        return int(submission_id)

    except Exception as e:
        print(f"Error while trying to submit the code: {e}")
        return None

def get_status(driver, submission_id):
    """Fetch the status of a submission using the submission ID."""
    try:
        # Open the submission URL
        submission_url = SUBMISSION_URL_PREFIX + str(submission_id)
        driver.get(submission_url)
        print(f"Opened submission URL: {submission_url}")

        # Wait for the submission result row to appear
        result_row = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, f"//tr[@id='trSubmission{submission_id}']"))
        )

        # Extract the submission status from the 6th <td>
        submission_status = result_row.find_element(By.XPATH, ".//td[6]").text
        print(f"Submission status for {submission_id}: {submission_status}\n\n\n")

        return submission_status

    except Exception as e:
        print(f"Error while trying to fetch the submission status: {e}")
        return None

def main():
    driver = login(TOPH_USERNAME, TOPH_PASSWORD)

    if driver:
        print("Logged in and browser is open. Ready for submissions.")
        
        problem_id = "add-them-up"
        code = """#include <iostream>
using namespace std;

int main() {
    int a, b; 
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}"""
        submission_id = submit(driver, problem_id, code)
        print(f"Returned Submission ID: {submission_id}")

        # Fetch the submission status
        if submission_id:
            status = get_status(driver, submission_id)

if __name__ == "__main__":
    main()

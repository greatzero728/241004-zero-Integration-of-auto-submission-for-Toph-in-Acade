import os
import re
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables from .env file
load_dotenv()

# Variables from .env
TOPH_USERNAME = os.getenv('TOPH_USERNAME')
TOPH_PASSWORD = os.getenv('TOPH_PASSWORD')
WAIT_TIME = int(os.getenv('WAIT_TIME'))

COMMON_URL_PREFIX = "https://toph.co/p/"
SUBMISSION_URL_PREFIX = "https://toph.co/s/"

driver = None

def init_driver():
    """Initialize the Chrome WebDriver."""
    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()

def login(tophHandle, tophPassword):
    """Login to Toph.co using provided credentials."""
    global driver
    init_driver()

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
        return True
    except Exception as e:
        print(f"Error during login: {e}")
        return False

def submit(problem_id, code):
    """Submit the given code to the specified problem and return the submission ID."""
    try:
        # Only remain alphabets, numbers and symbols in problem_id
        problem_id = problem_id.strip()
        problem_id = re.sub(r'[^a-zA-Z0-9!@#$%^&*()_+=-]', '', problem_id)
        # Open the problem URL
        submission_url = COMMON_URL_PREFIX + problem_id
        driver.get(submission_url)
        print(f"Opened problem URL: {submission_url}")

        # Refresh the page to ensure it's clean for new interaction
        driver.refresh()
        time.sleep(2)  # Wait for the page to fully reload

        # Wait for the "Open Editor" button to become clickable and click it
        open_editor_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Open Editor']"))
        )
        
        # Scroll into view of the button (ensure it's in the viewport)
        driver.execute_script("arguments[0].scrollIntoView(true);", open_editor_button)
        time.sleep(1)  # Just to ensure smoothness

        # Try clicking it using JavaScript to bypass obstruction
        driver.execute_script("arguments[0].click();", open_editor_button)
        print("Clicked on 'Open Editor' button using JavaScript.")

        time.sleep(3)  # Add a delay to allow the editor panel to fully load
        
        # Wait for the language dropdown to become clickable
        language_dropdown_trigger = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'aside[data-codepanel-problemslug="{problem_id}"] div.dropdown.-select'))
        )
        print("language_dropdown", language_dropdown_trigger)
        driver.execute_script("arguments[0].scrollIntoView(true);", language_dropdown_trigger)
        print("Scrolled to language dropdown.")

        # Add a delay before clicking the dropdown
        time.sleep(2)  # Wait for 2 seconds before interacting with the dropdown

        # Check if any C++ option is available, otherwise mark as invalid task
        options = driver.execute_script(f"""
            let dropdown = document.querySelector('aside[data-codepanel-problemslug="{problem_id}"] div.dropdown.-select');
            dropdown.click();  // Open the dropdown

            let options = dropdown.querySelectorAll('a');
            return Array.from(options).map(option => option.textContent);
        """)

        # Handle the case where C++ is not found
        if not any('C++' in option for option in options):  # Check for any C++ option
            print("There is no C++, so this task is an invalid task!")
            return -1

        # Select the language option C++23 GCC 13.2 if available
        driver.execute_script(f"""
            let dropdown = document.querySelector('aside[data-codepanel-problemslug="{problem_id}"] div.dropdown.-select');
            let options = dropdown.querySelectorAll('a');
            options.forEach(function(option) {"{"}
                if (option.textContent.includes('C++23 GCC 13.2')) {"{"}
                    option.click();
                {"}"}
            {"}"});
        """)
        print("Selected 'C++23 GCC 13.2' language.")

        # Wait for the code editor to be ready and insert code
        editor = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'cm-content'))
        )

        # Paste the code into the editor
        driver.execute_script("arguments[0].innerText = arguments[1];", editor, code)
        print("Code has been pasted into the editor.")

        # Wait for the submit button to be clickable
        submit_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit']"))
        )
        
        # Scroll into view and force-click the submit button
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked on 'Submit' button using JavaScript.")

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

def get_status(submission_id):
    """Fetch the status of a submission using the submission ID."""
    global driver
    init_driver()

    try:
        submission_url = SUBMISSION_URL_PREFIX + str(submission_id)
        driver.get(submission_url)
        print(f"Opened submission URL: {submission_url}")

        result_row = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, f"//tr[@id='trSubmission{submission_id}']"))
        )

        submission_status = result_row.find_element(By.XPATH, ".//td[6]").text
        print(f"Submission status for {submission_id}: {submission_status}")

        return submission_status

    except Exception as e:
        print(f"Error while trying to fetch the submission status: {e}")
        return None

import os
import time  # Import the time module
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

def login(tophHandle, tophPassword):
    """Login to Toph.co using provided credentials."""
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        driver.get("https://toph.co/login")
        print("Navigated to Toph login page.")

        # Wait for the username and password fields to load
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
    """Submit the given code to the specified problem."""
    try:
        # Construct the problem URL and open it
        submission_url = COMMON_URL_PREFIX + problem_id
        driver.get(submission_url)
        print(f"Opened problem URL: {submission_url}")

        # Delay to check the opened problem page
        time.sleep(1000)  # Wait for 1000 seconds (you can adjust this duration)

        # Display the code that would be submitted (submission logic can be added later)
        print("Code to be submitted:")
        print(code)

        # You can extend this to automate selecting language and submitting the code.
    
    except Exception as e:
        print(f"Error while trying to open the problem page: {e}")

def main():
    # Step 1: Login
    driver = login(TOPH_USERNAME, TOPH_PASSWORD)

    if driver:
        print("Logged in and browser is open. Ready for submissions.")
        
        # Step 2: Call submit function with problem_id and code
        problem_id = "add-them-up"
        code = """#include <iostream>
using namespace std;

int main() {
    int a, b; 
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}"""
        submit(driver, problem_id, code)

if __name__ == "__main__":
    main()

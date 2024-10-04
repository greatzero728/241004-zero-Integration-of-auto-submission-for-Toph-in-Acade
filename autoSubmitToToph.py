import os
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

def login(tophHandle, tophPassword):
    """Login to Toph.co using provided credentials."""
    # Setup Chrome options to open in guest/incognito mode
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        # Open the login page
        driver.get("https://toph.co/login")
        print("Navigated to Toph login page.")

        # Wait for the username and password fields to load
        username_input = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, 'handle'))
        )
        password_input = driver.find_element(By.NAME, 'password')

        # Enter the username and password
        username_input.send_keys(tophHandle)
        password_input.send_keys(tophPassword)
        print("Entered username and password.")

        # Submit the form
        password_input.send_keys(Keys.RETURN)
        
        # Wait for a successful login by checking for a user-specific element (adjust as needed)
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'dashboard'))  # Adjust to appropriate post-login element
        )
        print("Logged in successfully.")
        
        return driver  # Keep the driver session active for subsequent actions like submission and status check
    
    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()

def main():
    # Login using credentials from .env
    driver = login(TOPH_USERNAME, TOPH_PASSWORD)

    if driver:
        print("Logged in and browser is open. Ready for further actions.")
        # Do not close the driver; the browser stays open for subsequent tasks.

if __name__ == "__main__":
    main()

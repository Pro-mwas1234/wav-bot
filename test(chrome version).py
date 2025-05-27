from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service  # Import Chrome Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Initialize the WebDriver with the path to Chrome WebDriver
# Make sure the path to chromedriver.exe is correct
service = Service(executable_path=r"C:\Users\de._.hacker\Desktop\mwask\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # Update with your ChromeDriver path
driver = webdriver.Chrome(service=service)

try:
    # Open the website
    print("Opening the website...")
    driver.get('https://kenya-admin.wavumbuzi.africa/admin/login')
    print("Website opened successfully.")

    # Wait for the email field to be present and enter login credentials
    print("Locating the username field...")
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, '_username'))
    )
    print("Username field located.")

    print("Locating the password field...")
    password_field = driver.find_element(By.NAME, '_password')
    print("Password field located.")

    # Enter credentials and log in
    print("Entering credentials...")
    username_field.send_keys("pkamau1997@gmail.com")
    password_field.send_keys("123456")
    password_field.send_keys(Keys.RETURN)
    print("Credentials entered and submitted.")

    # Wait for an element that confirms a successful login
    # Replace 'apps' with the actual element ID, class, or other unique identifier
    print("Waiting for post-login element...")
    post_login_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'dynamicModal'))  # Example, update with actual ID or class
    )
    print("Login successful, and dashboard element located.")

    # Loop to refresh the page every 3 seconds
    print("Starting refresh loop...")
    while True:
        time.sleep(3)  # Wait before refreshing
        driver.refresh()
        print("Page refreshed.")

except TimeoutException as e:
    print(f"TimeoutException: {e}")
except NoSuchElementException as e:
    print(f"NoSuchElementException: {e}")
except KeyboardInterrupt:
    print("Stopped by user.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Close the WebDriver
    driver.quit()
    print("WebDriver closed.")

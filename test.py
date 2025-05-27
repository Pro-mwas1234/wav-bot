from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

def highlight(element, color="red", border=3):
    """Highlight an element with colored border"""
    driver.execute_script(
        f"arguments[0].style.border='{border}px solid {color}';",
        element
    )

# Initialize WebDriver with debugging capabilities
service = Service(executable_path=r"C:\Users\de._.hacker\Desktop\mwask\selenium-4.29.0\msedgedriver.exe")
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)  # Keep browser open
driver = webdriver.Edge(service=service, options=options)

try:
    # 1. Login with detailed debugging
    print("\n=== LOGIN PHASE ===")
    driver.get('https://kenya-admin.wavumbuzi.africa/admin/login')
    print(f"Current URL: {driver.current_url}")
    
    # Debug: Show page title
    print(f"Page title: {driver.title}")
    
    # Take screenshot before login
    driver.save_screenshot('before_login.png')
    
    # Login with credentials
    username = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.NAME, '_username'))
    )
    password = driver.find_element(By.NAME, '_password')
    
    username.send_keys("pkamau1997@gmail.com")
    password.send_keys("123456")
    password.send_keys(Keys.RETURN)
    print("Credentials submitted")
    
    # 2. Wait for dashboard with multiple verification points
    print("\n=== DASHBOARD VERIFICATION ===")
    try:
        WebDriverWait(driver, 20).until(
            lambda d: "dashboard" in d.current_url.lower() or 
                     "teacher" in d.current_url.lower()
        )
        print(f"Dashboard URL: {driver.current_url}")
        
        # Check for multiple dashboard elements
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(., 'Teacher') or contains(., 'Dashboard')]"))
        )
        print("Dashboard elements found")
        
        # Take screenshot of dashboard
        driver.save_screenshot('dashboard_loaded.png')
        
    except Exception as e:
        print(f"Dashboard verification failed: {str(e)}")
        raise

    # 3. Finding Submission Reviews with multiple approaches
    print("\n=== FINDING SUBMISSION REVIEWS ===")
    submission_link = None
    locators = [
        # Exact href you provided
        (By.XPATH, "//a[@href='/admin/teacher/dashboard/teacher_homepage_SubmissionReviews_tab']"),
        # Alternative if href varies
        (By.XPATH, "//a[contains(@href, 'SubmissionReviews')]"),
        # By link text
        (By.LINK_TEXT, "Submission Reviews"),
        # By partial link text
        (By.PARTIAL_LINK_TEXT, "Submission"),
        # By tab position (if consistent)
        (By.XPATH, "(//a[@role='tab'])[4]")
    ]
    
    for locator in locators:
        try:
            submission_link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(locator)
            )
            highlight(submission_link, "green")
            print(f"Found using {locator}")
            break
        except:
            continue
    
    if not submission_link:
        raise Exception("Could not find Submission Reviews link with any locator")
    
    # Click with JavaScript
    driver.execute_script("arguments[0].click();", submission_link)
    print("Clicked Submission Reviews")
    time.sleep(2)  # Wait for page transition
    driver.save_screenshot('submission_reviews.png')
    
    # 4. Click Review Challenge button
    print("\n=== REVIEW CHALLENGE BUTTON ===")
    review_locators = [
        (By.XPATH, "//a[@href='/admin/submission/review' and contains(@class, 'btn-primary')]"),
        (By.LINK_TEXT, "Review a challenge"),
        (By.XPATH, "//a[contains(., 'Review a challenge')]"),
        (By.CSS_SELECTOR, "a.btn-primary")
    ]
    
    review_btn = None
    for locator in review_locators:
        try:
            review_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(locator)
            )
            highlight(review_btn, "blue")
            print(f"Found review button using {locator}")
            break
        except:
            continue
    
    if not review_btn:
        raise Exception("Could not find Review Challenge button")
    
    driver.execute_script("arguments[0].click();", review_btn)
    print("Clicked Review Challenge button")
    
    # Final verification
    WebDriverWait(driver, 20).until(
        EC.or_(
            EC.url_contains('/admin/submission/review'),
            EC.presence_of_element_located((By.XPATH, "//*[contains(., 'Submission Review')]"))
        )
    )
    print("\n=== SUCCESS ===")
    print("Review page loaded successfully")
    driver.save_screenshot('success.png')

    # 5. Handle the review assessment dropdowns
    print("\n=== REVIEW ASSESSMENT ===")
    try:
        # First dropdown - critical assessment
        dropdown1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "rule_182"))
        )
        highlight(dropdown1, "purple")
        select1 = Select(dropdown1)
        select1.select_by_visible_text("It is a good answer")
        print("Selected 'It is a good answer' for first criteria")

        # Second dropdown - practical steps
        dropdown2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "rule_183"))
        )
        highlight(dropdown2, "purple")
        select2 = Select(dropdown2)
        select2.select_by_visible_text("It is a good answer")
        print("Selected 'It is a good answer' for second criteria")

        # Take screenshot after selection
        driver.save_screenshot('assessment_completed.png')

        # Optional: Submit the form if needed
        # submit_button = driver.find_element(By.ID, "assessmentForm")
        # submit_button.click()
        # print("Submitted assessment form")

    except Exception as e:
        print(f"Failed to complete assessment: {str(e)}")
        raise

except Exception as e:
    print(f"\n=== FAILURE ===")
    print(f"Error: {str(e)}")
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    driver.save_screenshot(f'error_{timestamp}.png')
    with open(f'page_source_{timestamp}.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print(f"Screenshot and page source saved for debugging")

finally:
    # Keep browser open - remove for production
    input("Press Enter to quit browser...")
    driver.quit()
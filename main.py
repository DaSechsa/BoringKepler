from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Helper function to save debugging data
def save_debug_data(driver, name):
    driver.save_screenshot(f"{name}.png")
    with open(f"{name}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

try:
    # Initialize WebDriver
    print("Initializing WebDriver...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    # Open the target URL
    print("Opening the webpage...")
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Check for iframe containing popups
    print("Checking for iframe...")
    try:
        iframe = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe"))
        )
        print("Iframe found. Switching to iframe context...")
        driver.switch_to.frame(iframe)
    except TimeoutException:
        print("No iframe detected. Proceeding with main page context.")

    # Handle Notification Popup
    print("Checking for the notification popup...")
    try:
        notification_popup = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'NEIN DANKE')]"))
        )
        notification_popup.click()
        print("Notification popup closed.")
    except TimeoutException:
        print("Notification popup not found or could not be closed. Proceeding...")
        save_debug_data(driver, "notification_debug")

    # Handle Cookie Banner
    print("Handling the cookie banner...")
    try:
        cookie_banner = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Alle akzeptieren')]"))
        )
        cookie_banner.click()
        print("Cookie banner accepted.")
    except TimeoutException:
        print("Cookie banner not found or could not be interacted with.")
        save_debug_data(driver, "cookie_debug")

    # Exit iframe if switched
    driver.switch_to.default_content()

    print("Page ready for further actions.")

except Exception as e:
    print(f"Error encountered: {e}")
    save_debug_data(driver, "final_debug")
finally:
    print("Closing WebDriver...")
    driver.quit()

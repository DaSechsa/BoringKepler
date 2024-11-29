from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

try:
    # Initialize WebDriver
    driver = webdriver.Chrome()
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")
    print("Opening the webpage...")

    # Wait for the notification popup and handle it
    try:
        print("Checking for the notification popup...")
        notification_popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gb-widget-popup"))
        )
        # Close the notification popup if found
        print("Notification popup found. Closing it...")
        close_button = notification_popup.find_element(By.XPATH, '//button[contains(text(), "NEIN DANKE")]')
        ActionChains(driver).move_to_element(close_button).click().perform()
        print("Notification popup closed.")
    except Exception as e:
        print(f"Notification popup not found or could not be closed. Proceeding...")

    # Handle the cookie banner
    try:
        print("Handling the cookie banner...")
        cookie_banner = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "didomi-host"))
        )
        accept_button = cookie_banner.find_element(By.XPATH, '//button[contains(text(), "Alle akzeptieren")]')
        ActionChains(driver).move_to_element(accept_button).click().perform()
        print("Cookie banner accepted.")
    except Exception as e:
        print(f"Cookie banner not found or could not be interacted with. Error: {e}")

    # Perform any additional actions (e.g., navigation or scraping)
    print("Page ready for further actions.")

except Exception as main_error:
    print(f"Error encountered: {main_error}")
finally:
    print("Closing WebDriver...")
    driver.quit()

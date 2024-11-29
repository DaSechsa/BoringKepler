from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialisiere WebDriver mit Optionen
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def save_debug_data(context):
    """Speichert einen Screenshot und die HTML-Seite für Debugging."""
    timestamp = int(time.time())
    try:
        driver.save_screenshot(f"{context}_debug_{timestamp}.png")
        with open(f"{context}_debug_{timestamp}.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as e:
        print(f"Fehler beim Speichern von Debug-Daten: {e}")

try:
    print("Opening the webpage...")
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    print("Checking for iframe...")
    try:
        iframe = driver.find_element(By.CSS_SELECTOR, "iframe[name='teamVoting']")
        print("Iframe found. Switching to iframe context...")
        driver.switch_to.frame(iframe)
        save_debug_data("iframe_context")
    except Exception as e:
        print(f"No iframe found or could not switch context: {e}")
        save_debug_data("no_iframe")
    
    print("Checking for the notification popup...")
    try:
        notification_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'NEIN DANKE')]"))
        )
        notification_button.click()
        print("Notification popup closed.")
    except Exception as e:
        print(f"Notification popup not found or could not be closed: {e}")
        save_debug_data("notification_popup")

    print("Handling the cookie banner...")
    try:
        driver.switch_to.default_content()  # Zurück zur Hauptseite
        accept_cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Alle akzeptieren')]"))
        )
        accept_cookies_button.click()
        print("Cookie banner accepted.")
    except Exception as e:
        print(f"Cookie banner not found or could not be interacted with: {e}")
        save_debug_data("cookie_banner")

    print("Page ready for further actions.")

finally:
    print("Closing WebDriver...")
    try:
        save_debug_data("final_state")
    except Exception as e:
        print(f"Fehler beim Speichern des letzten Zustands: {e}")
    driver.quit()

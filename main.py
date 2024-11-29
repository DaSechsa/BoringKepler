from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Webdriver-Optionen festlegen
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Entferne für Debugging
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')

# Verwende den Service-Wrapper mit ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    print("Öffne die Webseite...")
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")
    driver.save_screenshot("page_loaded.png")

    # Akzeptiere die Cookies
    print("Klicke auf den Cookie-Banner...")
    try:
        accept_cookies_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
        )
        accept_cookies_button.click()
        print("Cookie-Banner erfolgreich geklickt.")
    except Exception as e:
        driver.save_screenshot("cookie_error.png")
        print(f"Fehler beim Cookie-Banner: {e}")

    # Warte auf das Laden der Seite
    print("Warte auf das Laden der Seite...")
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Seite vollständig geladen.")
    except Exception as e:
        driver.save_screenshot("page_load_error.png")
        print(f"Fehler beim Laden der Seite: {e}")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.quit()
        exit()

    # Überprüfe Dropdown-Element
    print("Überprüfe Dropdown-Element...")
    try:
        dropdown_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@data-target, '#collapse-230')]"))
        )
        print("Dropdown-Element gefunden. Öffne das Dropdown...")
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_button)
        dropdown_button.click()
        driver.save_screenshot("dropdown_opened.png")
    except Exception as e:
        driver.save_screenshot("dropdown_not_found.png")
        print(f"Dropdown-Element wurde nicht gefunden: {e}")
        driver.quit()
        exit()

finally:
    print("Schließe den Webdriver...")
    driver.quit()

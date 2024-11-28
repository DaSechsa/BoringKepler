from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Webdriver-Optionen festlegen
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Entferne dies bei lokalem Debugging
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--window-size=1920x1080')

# Verwende den Service-Wrapper mit ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    print("Öffne die Webseite...")
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")

    print("Warte auf den iFrame des Cookie-Banners...")
    try:
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='privacymanager.io']"))
        )
        print("Akzeptiere die Cookies...")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "save"))
        ).click()
        driver.switch_to.default_content()
    except Exception as e:
        print(f"Cookie-Banner nicht gefunden: {e}")
        driver.switch_to.default_content()

    print("Wechsel zum iframe mit dem Voting-Formular...")
    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='iframe-loader-mk2.html']"))
    )

    print("Überprüfe das Dropdown-Element...")
    collapse_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[@data-target='#collapse-230']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", collapse_button)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-target='#collapse-230']"))).click()

    time.sleep(2)

    print("Wähle den Radiobutton aus...")
    driver.execute_script("document.querySelector('input[id=\"voteItem-400329\"]').checked = true;")

    time.sleep(2)

    print("Klicke auf den Abstimmen-Button...")
    driver.execute_script("document.querySelector('input[id=\"playerOneUp\"]').click()")

    print("Abstimmung erfolgreich abgeschlossen!")

except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")
    driver.save_screenshot("debug_screenshot.png")  # Screenshot für Debugging
finally:
    print("Schließe den Webdriver...")
    driver.quit()

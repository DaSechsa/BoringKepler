from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Deaktiviere temporär bei Bedarf
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--window-size=1920x1080')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

try:
    print("Öffne die Webseite...")
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")

    print("Warte auf den iFrame des Cookie-Banners...")
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='privacymanager.io']"))
    )

    print("Akzeptiere die Cookies...")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "save"))
    ).click()
    driver.switch_to.default_content()

    print("Wechsel zum Voting-iFrame...")
    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='iframe-loader-mk2.html']"))
    )

    print("Finde und klicke auf das Dropdown...")
    collapse_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@data-target='#collapse-230']"))
    )
    collapse_button.click()

    time.sleep(2)

    print("Wähle den Radiobutton aus...")
    driver.execute_script("document.querySelector('input[id=\"voteItem-400329\"]').checked = true;")

    time.sleep(2)

    print("Klicke auf den Abstimmen-Button...")
    driver.execute_script("document.querySelector('input[id=\"playerOneUp\"]').click()")

    print("Abstimmung erfolgreich abgeschlossen!")

except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")
    driver.save_screenshot("debug_screenshot.png")
    with open("debug.log", "w") as log_file:
        log_file.write("Fehlerbeschreibung: " + str(e))

finally:
    print("Schließe den Webdriver...")
    driver.quit()

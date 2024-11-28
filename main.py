from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Webdriver-Optionen festlegen
options = webdriver.ChromeOptions()
# Entferne den Headless-Modus für Debugging
# options.add_argument('--headless')
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

    # Warte, bis die Seite vollständig geladen ist
    print("Warte auf das Laden der Seite...")
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='card-header border-0 border-bottom-1 p-0']"))
        )
        print("Seite erfolgreich geladen.")
    except Exception as e:
        driver.save_screenshot("element_load_error.png")
        print(f"Fehler beim Warten auf das Element: {e}")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.quit()
        exit()

    # Klicke auf das Dropdown-Menü
    print("Öffne das Dropdown-Menü...")
    try:
        dropdown_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-target='#collapse-230']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_button)
        dropdown_button.click()
        print("Dropdown-Menü erfolgreich geöffnet.")
    except Exception as e:
        driver.save_screenshot("dropdown_error.png")
        print(f"Fehler beim Öffnen des Dropdowns: {e}")
        driver.quit()
        exit()

    # Wähle den Radiobutton aus
    print("Wähle den Radiobutton aus...")
    try:
        radiobutton = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "voteItem-400329"))
        )
        driver.execute_script("arguments[0].click();", radiobutton)
        print("Radiobutton erfolgreich ausgewählt.")
    except Exception as e:
        driver.save_screenshot("radiobutton_error.png")
        print(f"Fehler beim Auswählen des Radiobuttons: {e}")
        driver.quit()
        exit()

    # Klicke auf den Abstimmen-Button
    print("Klicke auf den Abstimmen-Button...")
    try:
        submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "playerOneUp"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()
        print("Abstimmung erfolgreich abgeschlossen!")
    except Exception as e:
        driver.save_screenshot("submit_button_error.png")
        print(f"Fehler beim Klicken auf den Abstimmen-Button: {e}")

finally:
    print("Schließe den Webdriver...")
    driver.quit()

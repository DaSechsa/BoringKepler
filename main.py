from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Webdriver-Optionen festlegen
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Läuft in headless
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')

# Verwende den Service-Wrapper mit ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def save_debug_info(filename_prefix="debug"):
    """Speichert die HTML-Struktur und einen Screenshot für Debugging."""
    try:
        with open(f"{filename_prefix}_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot(f"{filename_prefix}_screenshot.png")
        print(f"Debugging-Daten gespeichert: {filename_prefix}_page_source.html und {filename_prefix}_screenshot.png")
    except Exception as e:
        print(f"Fehler beim Speichern von Debugging-Daten: {e}")

try:
    print("Öffne die Webseite...")
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")
    driver.save_screenshot("page_loaded.png")

    # Schließe den Benachrichtigungsdialog, falls vorhanden
    print("Prüfe, ob der Benachrichtigungsdialog vorhanden ist...")
    try:
        notification_close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'NEIN DANKE')]"))
        )
        notification_close_button.click()
        print("Benachrichtigungsdialog geschlossen.")
    except Exception as e:
        print("Benachrichtigungsdialog nicht gefunden oder konnte nicht geschlossen werden. Fahre fort...")

    # Akzeptiere die Cookies
    print("Klicke auf den Cookie-Banner...")
    try:
        accept_cookies_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
        )
        accept_cookies_button.click()
        print("Cookie-Banner erfolgreich geklickt.")
    except Exception as e:
        print(f"Fehler beim Cookie-Banner: {e}")
        save_debug_info("cookie_error")
        raise e  # Forciere den Fehlerstatus

    # Warte auf das Laden der Seite
    print("Warte auf das Laden der Seite...")
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Seite vollständig geladen.")
    except Exception as e:
        print(f"Fehler beim Laden der Seite: {e}")
        save_debug_info("page_load_error")
        raise e  # Forciere den Fehlerstatus

finally:
    print("Schließe den Webdriver...")
    driver.quit()

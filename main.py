from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

# Webdriver initialisieren
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Headless-Modus für CI
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')

driver = webdriver.Chrome(options=options)

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
    time.sleep(3)  # Warte auf das Laden der Seite

    # Benachrichtigungsdialog schließen
    try:
        print("Prüfe, ob der Benachrichtigungsdialog vorhanden ist...")
        notification_close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "NEIN DANKE")]'))
        )
        notification_close_button.click()
        print("Benachrichtigungsdialog geschlossen.")
    except Exception:
        print("Benachrichtigungsdialog nicht gefunden oder konnte nicht geschlossen werden. Fahre fort...")

    # Cookie-Banner akzeptieren
    try:
        print("Klicke auf den Cookie-Banner...")
        accept_cookies_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Alle akzeptieren")]'))
        )
        accept_cookies_button.click()
        print("Cookie-Banner erfolgreich geklickt.")
    except Exception as e:
        print(f"Fehler beim Cookie-Banner: {str(e)}")
        save_debug_info("cookie_error")
        raise e

finally:
    print("Schließe den Webdriver...")
    save_debug_info("final_state")  # Speichert immer den letzten Zustand
    driver.quit()

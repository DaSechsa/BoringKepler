from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def save_debug_data(driver, filename_prefix):
    """Speichert einen Screenshot und die HTML-Quelle der aktuellen Seite."""
    if driver:
        driver.save_screenshot(f"{filename_prefix}_screenshot.png")
        with open(f"{filename_prefix}_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

driver = None  # Initialisiere den Driver als None

try:
    print("Öffne die Webseite...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Headless-Modus für CI
    options.add_argument("--disable-gpu")  # Deaktiviere GPU für CI-Umgebungen
    options.add_argument("--no-sandbox")  # Deaktiviere Sandbox
    options.add_argument("--disable-dev-shm-usage")  # Nutze shared memory
    options.add_argument("--remote-debugging-port=9222")  # Debugging-Port
    options.add_argument("--window-size=1920,1080")  # Fenstergröße setzen

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")

    print("Prüfe, ob der Benachrichtigungsdialog vorhanden ist...")
    try:
        notification_close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "NEIN DANKE")]'))
        )
        notification_close_button.click()
        print("Benachrichtigungsdialog geschlossen.")
    except Exception:
        print("Benachrichtigungsdialog nicht gefunden oder konnte nicht geschlossen werden. Fahre fort...")
        save_debug_data(driver, "notification_error")

    print("Klicke auf den Cookie-Banner...")
    try:
        accept_cookies_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Alle akzeptieren"]'))
        )
        accept_cookies_button.click()
        print("Cookie-Banner akzeptiert.")
    except Exception as e:
        print(f"Fehler beim Cookie-Banner: {e}")
        save_debug_data(driver, "cookie_error")
        raise e

    print("Speichere den finalen Zustand der Seite...")
    save_debug_data(driver, "final_state")

finally:
    if driver:
        print("Schließe den Webdriver...")
        driver.quit()

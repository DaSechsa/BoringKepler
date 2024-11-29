from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

driver = None  # Sicherstellen, dass driver nur definiert wird, wenn er erfolgreich initialisiert wird

try:
    print("Öffne die Webseite...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)  # Initialisiere den Webdriver mit Optionen
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")

    print("Prüfe, ob der Benachrichtigungsdialog vorhanden ist...")
    try:
        notification_close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "NEIN DANKE")]'))
        )
        notification_close_button.click()
        print("Benachrichtigungsdialog geschlossen.")
    except Exception:
        print("Benachrichtigungsdialog nicht gefunden oder konnte nicht geschlossen werden. Fahre fort...")

    print("Klicke auf den Cookie-Banner...")
    try:
        accept_cookies_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Alle akzeptieren"]'))
        )
        accept_cookies_button.click()
        print("Cookie-Banner akzeptiert.")
    except Exception as e:
        print(f"Fehler beim Cookie-Banner: {e}")
        driver.save_screenshot("cookie_error_screenshot.png")
        with open("cookie_error_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise e

finally:
    if driver:
        print("Schließe den Webdriver...")
        driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

try:
    print("Öffne die Webseite...")
    driver = webdriver.Chrome()
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde")

    # Cookie-Banner finden und klicken
    try:
        print("Klicke auf den Cookie-Banner...")
        accept_cookies_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Akzeptieren")]'))
        )
        accept_cookies_button.click()
    except Exception as e:
        print(f"Fehler beim Cookie-Banner: {e}")
        driver.save_screenshot("cookie_error_screenshot.png")
        with open("cookie_error_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise e

    # Warten bis Seite vollständig geladen ist
    time.sleep(5)
    print("Seite vollständig geladen.")

    # Zum iframe wechseln
    try:
        print("Wechsle in das iframe...")
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[name="teamVoting"]'))
        )
        driver.switch_to.frame(iframe)

        # Im iframe das gewünschte Element anklicken
        print("Klicke auf das gewünschte Element im iframe...")
        target_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="heading-230"]/h5/a'))
        )
        target_button.click()

        print("Element erfolgreich geklickt.")
    except Exception as e:
        print(f"Fehler im iframe: {e}")
        driver.save_screenshot("iframe_error_screenshot.png")
        with open("iframe_error_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise e

finally:
    print("Schließe den Webdriver...")
    driver.quit()

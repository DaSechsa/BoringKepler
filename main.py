from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")

try:
    # Handle Notification Popup
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Nein Danke']"))
    ).click()

    # Handle Cookie Banner
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Alle akzeptieren']"))
    ).click()

except Exception as e:
    print("Error handling popups or banners:", e)
finally:
    # Ensure WebDriver quits
    driver.quit()

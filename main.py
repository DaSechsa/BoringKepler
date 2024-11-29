from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # Open the webpage
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")
    wait = WebDriverWait(driver, 10)
    
    # Check if page contains an iframe
    try:
        iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe)
        print("Switched to iframe context.")
    except TimeoutException:
        print("No iframe found. Proceeding with the main content.")

    # Handle Notification Popup (if any)
    try:
        notification_popup = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Nein Danke")]'))
        )
        notification_popup.click()
        print("Notification popup handled.")
    except TimeoutException:
        print("Notification popup not found.")

    # Handle Cookie Banner
    try:
        cookie_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Alle akzeptieren")]'))
        )
        cookie_button.click()
        print("Cookie banner accepted.")
    except TimeoutException:
        print("Cookie banner not found.")

    # Locate Player 'Alisic Adin'
    try:
        player = wait.until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Alisic Adin")]/ancestor::div[contains(@class, "player-entry")]'))
        )
        print("Player found.")

        # Click Vote Button
        vote_button = player.find_element(By.XPATH, './/button[contains(text(), "Abstimmen")]')
        vote_button.click()
        print("Voted for Alisic Adin.")

    except NoSuchElementException:
        print("Player 'Alisic Adin' not found in the list.")
    except TimeoutException:
        print("Timeout while locating the player or button.")

finally:
    # Always close the driver
    driver.quit()

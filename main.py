from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def switch_to_iframe(driver, iframe_name=None):
    """Switch to iframe if found."""
    try:
        if iframe_name:
            iframe = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, iframe_name))
            )
        else:
            iframe = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
        driver.switch_to.frame(iframe)
        print(f"Switched to iframe: {iframe.get_attribute('name') or 'unnamed'}")
        return True
    except TimeoutException:
        print("No iframe found. Continuing in the main context.")
        return False

def handle_notification_popup(driver):
    """Handle notification popup if it appears."""
    try:
        notification_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Nein Danke")]'))
        )
        notification_button.click()
        print("Notification popup handled.")
    except TimeoutException:
        print("Notification popup not found.")

def handle_cookie_banner(driver):
    """Handle cookie banner if it appears."""
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Alle akzeptieren")]'))
        )
        cookie_button.click()
        print("Cookie banner accepted.")
    except TimeoutException:
        print("Cookie banner not found.")

def vote_for_player(driver, player_name):
    """Locate the player and vote."""
    try:
        player_entry = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//span[contains(text(), "{player_name}")]/ancestor::div[contains(@class, "player-entry")]'))
        )
        print(f"Player {player_name} found.")
        vote_button = player_entry.find_element(By.XPATH, './/button[contains(text(), "Abstimmen")]')
        vote_button.click()
        print(f"Voted for {player_name}.")
    except TimeoutException:
        print(f"Timeout while locating player {player_name} or vote button.")
    except NoSuchElementException:
        print(f"Player {player_name} or vote button not found.")

# Main execution
driver = webdriver.Chrome()

try:
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")
    wait = WebDriverWait(driver, 10)
    
    # Handle Notification Popup in Main Context
    handle_notification_popup(driver)
    
    # Handle Cookie Banner in Main Context
    handle_cookie_banner(driver)
    
    # Switch to Voting Iframe
    if switch_to_iframe(driver, "teamVoting"):  # Use iframe name if known
        # Attempt to vote for the player in the iframe context
        vote_for_player(driver, "Alisic Adin")
        # Return to the main context
        driver.switch_to.default_content()
        print("Switched back to main context.")
    
    # Handle any additional actions in the main context if needed
    
finally:
    driver.quit()

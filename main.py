from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def locate_and_switch_to_relevant_iframe(driver):
    """Locate relevant iframe and switch to it."""
    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Found {len(iframes)} iframe(s) on the page.")
        
        for index, iframe in enumerate(iframes):
            iframe_src = iframe.get_attribute('src')
            iframe_name = iframe.get_attribute('name')
            iframe_id = iframe.get_attribute('id')

            print(f"Checking iframe {index + 1}/{len(iframes)}: name={iframe_name}, id={iframe_id}, src={iframe_src}")
            
            # Skip irrelevant system iframes
            if "tcfapiLocator" in (iframe_name or "") or "about:blank" in (iframe_src or ""):
                print(f"Skipping irrelevant iframe: {iframe_name or iframe_id or 'unknown'}")
                continue
            
            # Attempt to switch to iframe
            driver.switch_to.frame(iframe)
            print(f"Switched to iframe: {iframe_name or iframe_id or 'unnamed'}.")
            
            # Check if iframe contains the target content
            if "Alisic Adin" in driver.page_source:
                print("Correct iframe identified!")
                return True
            
            # Capture iframe content for debugging
            with open(f"iframe_{index + 1}_debug.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print(f"Saved iframe {index + 1} content for debugging.")

            # Switch back to main content
            driver.switch_to.default_content()
        
        print("No relevant iframe found.")
        return False
    except Exception as e:
        print(f"Error while locating or switching to iframe: {e}")
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
    except Exception as e:
        print(f"Error handling notification popup: {e}")


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
    except Exception as e:
        print(f"Error handling cookie banner: {e}")


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
    except Exception as e:
        print(f"Error while voting for {player_name}: {e}")


# Main execution
driver = webdriver.Chrome()

try:
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")
    wait = WebDriverWait(driver, 10)
    
    # Handle Notification Popup in Main Context
    handle_notification_popup(driver)
    
    # Handle Cookie Banner in Main Context
    handle_cookie_banner(driver)
    
    # Attempt to locate and switch to relevant iframe
    if locate_and_switch_to_relevant_iframe(driver):
        vote_for_player(driver, "Alisic Adin")
        driver.switch_to.default_content()  # Switch back to the main context
        print("Switched back to main content.")
    else:
        print("Could not locate the iframe or the iframe does not contain the desired content.")

finally:
    driver.quit()

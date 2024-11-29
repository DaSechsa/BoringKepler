from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to handle iframe switching
def switch_to_iframe(driver, iframe_name):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, iframe_name))
        )
        driver.switch_to.frame(iframe_name)
        print(f"Switched to iframe: {iframe_name}")
        return True
    except Exception as e:
        print(f"Error while switching to iframe {iframe_name}: {e}")
        return False

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # Open the main page
    driver.get("https://www.ligaportal.at/ooe/2-klasse/2-klasse-sued/spieler-der-runde/109918-2-klasse-sued-waehle-den-beliebtesten-siberia-spieler-der-herbstsaison-2024")

    # Switch to iframe_2
    if switch_to_iframe(driver, "teamVoting"):
        try:
            # Locate and click on the player "Alisic Adin"
            player_radio = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Alisic Adin']"))
            )
            player_radio.click()
            print("Selected 'Alisic Adin'.")
            
            # Submit the form
            submit_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Vote')]"))
            )
            submit_button.click()
            print("Vote submitted.")
        except Exception as e:
            print(f"Error interacting with voting elements: {e}")
    else:
        print("Iframe not found or could not switch.")

finally:
    driver.quit()

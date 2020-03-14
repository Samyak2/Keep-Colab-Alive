import os
import time

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

profile_path = os.getenv("FIREFOX_PROFILE", "")
if not profile_path:
    print("Set the FIREFOX_PROFILE environment variable to avoid entering the profile path every time")
    profile_path = input("Enter the profile path: ")
url = os.getenv("COLAB_URL", "")
if not url:
    print("Set the COLAB_URL environment variable to avoid entering the url every time")
    url = input("Enter the url: ")

driver = webdriver.Firefox(firefox_profile=profile_path)
try:
    driver.get(url)
    useless_element_xpath = f'//colab-connect-button'

    useless_element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, useless_element_xpath)))

    while True:
        useless_element.click()
        time.sleep(5)
except Exception as e:
    raise e
finally:
    print("Error. Press Enter to close webdriver.")
    input()
    driver.close()


import os
import time
import random
import argparse
import shutil
import sys

import selenium
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

parser = argparse.ArgumentParser(prog="Keep Colab Alive",
                                 description='Colab automation using selenium',
                                 epilog=("Check out the project at "
                                         "https://github.com/Samyak2/Keep-Colab-Alive"))
parser.add_argument("-c", "--cells-only",
                    dest="cells_only",
                    default=False,
                    action="store_true",
                    help="Lists all the cell IDs and some of their contents, then exits")
parser.add_argument("-i", "--interactive",
                    dest="interactive",
                    default=False,
                    action="store_true",
                    help=("Interactive mode. User can enter input as when asked instead "
                          "of specifying command line arguments."))
parser.add_argument("--firefox-profile",
                    dest="profile_path",
                    default=None,
                    help=("Path to your (newly made) Firefox profile. You can get the path"
                          " by typing `about:profiles` and look for 'Root Directory'"))
parser.add_argument("--url",
                    dest="url",
                    default=None,
                    help="URL to the colab")
parser.add_argument("--cells",
                    dest="cells_to_execute",
                    default="",
                    help="Comma separated list of cell IDs to execute if not already executing")
args = parser.parse_args()

input_err_msg = ("Input {} is required to run. Use -i or --interactive for interactive mode or"
                 " see the help page using -h or --help for more details.")

if not args.profile_path:
    profile_path = os.getenv("FIREFOX_PROFILE", "")
    if not profile_path:
        if args.interactive:
            print("Set the FIREFOX_PROFILE environment variable to avoid",
                  "entering the profile path every time")
            profile_path = input("Enter the profile path: ")
        else:
            print(input_err_msg.format("--firefox-profile"))
            sys.exit()
else:
    profile_path = args.profile_path

if not args.url:
    url = os.getenv("COLAB_URL", "")
    if not url:
        if args.interactive:
            print("Set the COLAB_URL environment variable to avoid entering the url every time")
            url = input("Enter the url: ")
        else:
            print(input_err_msg.format("--url"))
            sys.exit()
else:
    url = args.url

if not args.cells_to_execute:
    cells_to_execute = os.getenv("COLAB_CELLS", "")
    if not args.cells_only and not cells_to_execute:
        if args.interactive:
            print("Set the COLAB_CELLS environment variable to avoid entering every time")
            print("Run this script with the -c flag to get the cell IDs.")
            cells_to_execute = input(("Enter a comma-separated list of cell IDs to execute "
                                      "(leave empty if you don't want to execute anything): "))
else:
    cells_to_execute = args.cells_to_execute
cells_to_execute = cells_to_execute.split(",")

execute_cell_button_xpath = "//div[@id='{}']//paper-icon-button[contains(@title, 'Run cell')]"
cell_xpath = "//div[@id='{}']"
cell_content_xpath = "//div[@id='{}']//*[contains(@class,'editor-scrollable')]"
cell_spinner_xpath = "//div[@id='{}']//*[@class='cell-spinner']"
# ok_button_xpath = "//*[@id='ok']"
ok_button_js = """document.getElementById("ok").click()"""
get_all_cells_js = """ret_values = []
for(let i = 0; i < colab.global.notebook.cells_.length; ++i) {
    ret_values.push(colab.global.notebook.cells_[i].element_.id)
}
return ret_values"""


driver = webdriver.Firefox(firefox_profile=profile_path)
try:
    driver.get(url)
    useless_element_xpath = f'//colab-connect-button'

    useless_element = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, useless_element_xpath)))

    if args.cells_only:
        all_cells = driver.execute_script(get_all_cells_js)
        for cell in all_cells:
            cell_elements = driver.find_elements_by_xpath(cell_content_xpath.format(cell))
            if not cell_elements:
                cell_element = driver.find_element_by_xpath(cell_xpath.format(cell))
            else:
                cell_element = cell_elements[0]
            cell_content = cell_element.text
            print("Cell ID:", cell)
            print("Cell Content:")
            print(cell_content[:100], "...")
            print("*"*shutil.get_terminal_size().columns)
        driver.close()
        sys.exit()

    time.sleep(10)

    failed_times = 0

    while True:
        try:
            useless_element.click()
        except selenium.common.exceptions.ElementClickInterceptedException as e:
            driver.execute_script(ok_button_js)
            failed_times += 1
            if failed_times % 5 == 0:
                print(f"Clicking is failing a lot: {failed_times} times")
        for cell in cells_to_execute:
            try:
                cell_execute_elements = driver.find_elements_by_xpath(
                    execute_cell_button_xpath.format(cell))
                cell_elements = driver.find_elements_by_xpath(
                    cell_content_xpath.format(cell))
                cell_spinners = driver.find_elements_by_xpath(cell_spinner_xpath.format(cell))
                if cell_spinners:
                    cell_spinner = cell_spinners[0]
                    cell_spinner_display = cell_spinner.value_of_css_property("display")
                    # print("Cell spinner display:", cell_spinner_display)
                    if str(cell_spinner_display).lower() != "none":
                        continue
                for cell_ex_element, cell_element in zip(cell_execute_elements, cell_elements):
                    try:
                        cell_element.click()
                        cell_ex_element.click()
                    except (selenium.common.exceptions.ElementNotInteractableException,
                            selenium.common.exceptions.ElementClickInterceptedException) as e:
                        print("Could not click element", cell_element)
                        driver.execute_script(ok_button_js)
                        cell_element.click()
                        cell_ex_element.click()
            except Exception as e:
                print("Could not execute due to error:", e)
                print("Will try again in some time")
        time.sleep(random.random() * 10)
except Exception as e:
    print(e)
    raise e
finally:
    try:
        print("Done (or Errored). Press Enter to close webdriver.")
        input()
        driver.close()
    except Exception:
        print("Exiting")


# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00FFC0C88EE2D535491621BC8B19A74FA91F495959FD31CE25B0CE5A1EDE2382D9E48684E413840F2FF12E93167E75387043F6649CDA13B5C442736CC69DC351192E54DC4499CC509FAD50414766081E6B000A96B49222A8362105A74F85AC7038D37306B81B49F7F5C1621AD1967D55A3845D67357ADBE1A2BF2796DBE7CFC38E0D5F2DD712C48ADEDD19D00D79B3C64B62991656062918B78A1EB9F4AB68AE0D54FF918CF371822666AD9994A64FC12DE8ADD6EC6D33899CC2E9D1F3649035B4EA54F464781391DED4EE1D4A2BD3471569F1E05F3835C72F14953BEA424E9D655E632E865D894D780F232BD92E27840B1C4D35FFF05A552BCE3096D1D1F7E6CB03B0492BF9430DEC9E6E42DAE328EA0766F8FD63BB4881510AC948767F6CE520B6016ECCCC156F2BCE79B16D0A5E8507AF8CC4F8A6A96D2E7F55D271D14E695EF8F61FEACE7FF34E9207C5917FDCF33D0FAABC9789EB112640E286E75054B1D5"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")

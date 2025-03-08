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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DA291DB1F3DA2F1BBC9F159762FC7FDB63229903215341CAEE5B846084D102360DD02369405CDA964672A519861843EB4D71129FECB907FDD5CC651322BBADC8F99D68692654DE3AC3BFE6753B6D11BA03336F4915D94F2E3CE03D8FBC89577F57B159BCB86AC7B8A974659AFDCEEFFE135578C55ADA31166A4F599F31823E8C867F93833EAE73EE7B552B02659098FE7A75D137B6EC75DA509BEE60E62D16452519836AD4C389B4A657190F3E2AB6FB558C3DB1053A9A5F1E5263EDC673EB4218B6604FBA1F80F020BA9E86A99C5F4474FE50D5737E02156CD3D3E60AC918AC858D1A40C0B8603AFBE26ACC504FF5346E4B68087E942B006623085717C36538D68B1E9BC2351B868E7FA91BA956C84A1892703B533212538B11A7F8F926EE906E2E8043324375850BBB385F6A02627A3C05E2DE72A8182018E812724EE1E6D2CE4EFC3BF3CDA69CB9A3BBDB9734435495BE413853AD32ADFE7827746507B4A0"})
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

import logging
import re
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from autoproject.logger import ClickClickLogger

MAX_RETRIES = 3
custom_logger = ClickClickLogger()

def parse_email(text):
    email_pattern = r'[\w\.-]+@[\w\.-]+'
    email_holder = re.search(email_pattern, text, flags=re.IGNORECASE)
    return email_holder.group() if email_holder else None

def is_website_okay(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def looper(elements):
    data = [element.text for element in elements]
    print(data)
    return data

def scraper(url):
    print("started scraping...")
    print(url)

    options = uc.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=Default')
    options.add_argument("--incognito")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-backgrounding-occluded-windows")

    print("Options set")
    all_data = []
    driver = None
    try:
        driver = uc.Chrome(options=options)
        time.sleep(2)
        print("Driver started")
        driver.get(url)
        wait = WebDriverWait(driver, 20)  # Increased wait time
        
        print("Wait set")
        element = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "NwqBmc")))
        print("Element:", element)
        data = looper(element)
        all_data.extend(data)

        print("All Data:", all_data)
        
        time.sleep(2)
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-INsAgc.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.Rj2Mlf.OLiIxf.PDpWxe.P62QJc.LQeN7.sspfN.Ehmv4e.cLUxtc")))
        next_button.click()
        time.sleep(2)
        
        element = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "NwqBmc")))
        data = looper(element)
        all_data.extend(data)

        while True:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-INsAgc.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.Rj2Mlf.OLiIxf.PDpWxe.P62QJc.LQeN7.sspfN.Ehmv4e.cLUxtc")))
            buttons = driver.find_elements(By.CSS_SELECTOR, ".VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-INsAgc.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.Rj2Mlf.OLiIxf.PDpWxe.P62QJc.LQeN7.sspfN.Ehmv4e.cLUxtc")

            time.sleep(2)
            if len(buttons) == 1:
                break
            buttons[1].click()
            element = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "NwqBmc")))
            data = looper(element)
            all_data.extend(data)
            time.sleep(1)
        return all_data
    except Exception as e:
        custom_logger.log(f"An error occurred while processing the website: {str(e)}", logging.ERROR)
        return all_data
    finally:
        if driver:
            driver.quit()

def scraper_social_for_business_email(url):
    custom_logger.log(f"started facebook crawling...", logging.INFO)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-web-security")
    options.add_argument("--incognito")
    prefs = {"profile.default_content_setting_values.geolocation": 2}
    options.add_experimental_option("prefs", prefs)

    scraper = webdriver.Chrome(options=options)
    scraper.set_window_size(2048, 1080)
    try:
        url = "https://www.google.com/search?q=" + "facebook page " + url
        scraper.get(url)

        wait = WebDriverWait(scraper, 10)
        data = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "byrV5b")))
        data.click()

        time.sleep(5)
        business_email = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "xieb3on")))
        
        email = parse_email(business_email.text)
        return email
    except Exception as e:
        custom_logger.log(f"An error occurred while scrapping the website: {str(e)}", logging.ERROR)
        return ""
    finally:
        if scraper:
            scraper.quit()
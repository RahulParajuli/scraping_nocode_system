import logging
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from autoproject.logger import ClickClickLogger

MAX_RETRIES = 3
custom_logger = ClickClickLogger()

def parse_email(text):
    email_pattern = r'[\w\.-]+@[\w\.-]+'
    email_holder = re.search(email_pattern, text, flags=re.IGNORECASE)
    email = email_holder.group() if email_holder else None
    return email

def is_website_okay(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def looper(element):
    data = []
    for i in element:
        content = i.text
        data.append(content)
    return data

def click_accept_all_cookies(driver):
    try:
        accept_all_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.XWZjwc"))
        )
        accept_all_button.click()
        time.sleep(1)  # Wait for the button click to take effect
    except Exception as e:
        custom_logger.log(f"Accept all cookies button not found: {str(e)}", logging.WARNING)

def scraper(url):
    option = uc.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument('--disable-gpu')
    option.add_argument('--disable-extensions')
    option.add_argument('--profile-directory=Default')
    option.add_argument("--incognito")
    option.add_argument("--disable-plugins-discovery")
    option.add_argument("--start-maximized")
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument("--disable-infobars")
    option.add_argument("--disable-blink-features")
    option.add_argument("--headless")

    all_data = []
    try:
        driver = uc.Chrome(use_subprocess=True, options=option)
        print(driver)
        driver.get(url)
        
        # Try to click "Accept All" cookies button if it appears
        click_accept_all_cookies(driver)
        
        time.sleep(1.5)
        element = driver.find_elements(By.CLASS_NAME, "NwqBmc")
        data = looper(element)
        all_data.extend(data)
        next_button = driver.find_element(By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-INsAgc.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.Rj2Mlf.OLiIxf.PDpWxe.P62QJc.LQeN7.sspfN.Ehmv4e.cLUxtc")
        next_button.click()
        time.sleep(1.5)
        element = driver.find_elements(By.CLASS_NAME, "NwqBmc")
        data = looper(element)
        all_data.extend(data)

        while True:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-INsAgc.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.Rj2Mlf.OLiIxf.PDpWxe.P62QJc.LQeN7.sspfN.Ehmv4e.cLUxtc")))
            buttons = driver.find_elements(By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-INsAgc.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.Rj2Mlf.OLiIxf.PDpWxe.P62QJc.LQeN7.sspfN.Ehmv4e.cLUxtc")
            time.sleep(1.5)
            if len(buttons) == 1:
                break
            buttons[1].click()
            element = driver.find_elements(By.CLASS_NAME, "NwqBmc")
            data = looper(element)
            all_data.extend(data)
            time.sleep(1)
        return all_data
    except Exception as e:
        custom_logger.log(f"An error occurred while processing the website: {str(e)}", logging.ERROR)
        return all_data
    finally:
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
    prefs = {"profile.default_content_setting_values.geolocation" :2}
    options.add_experimental_option("prefs",prefs)

    options.add_argument("--disable-geolocation")
    
    scraper = webdriver.Chrome(options=options)
    scraper.set_window_size(2048, 1080)
    try:
        url = "https://www.google.com/search?q=" + "facebook page "+ url
        scraper.get(url)

        # Try to click "Accept All" cookies button if it appears
        click_accept_all_cookies(scraper)

        data = scraper.find_element(By.CLASS_NAME, "byrV5b")
        data.click()

        time.sleep(5)
        business_email = scraper.find_element(By.CLASS_NAME, "xieb3on")
        
        email = parse_email(business_email.text)
        scraper.quit()
        return email
    except Exception as e:
        custom_logger.log(f"An error occurred while scrapping the website: {str(e)}", logging.ERROR)
        return ""

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

def parse_fb_address(text):
    address_pattern = r'^([^\n]+)\n[\+\d\s\(\)\-\.\/\w]{7,}'
    address_holder = re.search(address_pattern, text)
    address = address_holder.group() if address_holder else None
    return address

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
        accept_all_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.XWZjwc"))
        )
        accept_all_button.click()
        time.sleep(1)  # Wait for the button click to take effect
    except Exception as e:
        custom_logger.log(f"Accept all cookies button not found (Google): {e.msg if hasattr(e, 'msg') else str(e)}")

def close_popup_if_present(driver):
    try:
        popup_close_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm"))
        )
        popup_close_button.click()
        time.sleep(1) 
    except Exception as e:
        custom_logger.log(f"Facebook popup not found: {e.msg if hasattr(e, 'msg') else str(e)}")
    
def click_accept_all_other_cookie(driver):
    try:
        accept_all_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "tHlp8d"))
        )
        accept_all_button.click()
        time.sleep(1) 
    except Exception as e:
        custom_logger.log(f"Accept all cookies button not found (facebook): {e.msg if hasattr(e, 'msg') else str(e)}")

def create_driver():
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
    option.add_argument("--headless")  # Run Chrome in headless mode
    option.add_argument("--no-sandbox")  # Required for running in a Docker container
    option.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    option.add_argument("--remote-debugging-port=9222")  # Add this to avoid "DevToolsActivePort" error
    option.add_argument("--disable-web-security")  # Disable web security for cross-origin requests

    prefs = {"profile.default_content_setting_values.geolocation": 2}
    option.add_experimental_option("prefs", prefs)
    option.add_argument("--disable-geolocation")

    driver = uc.Chrome(use_subprocess=True, options=option)
    driver.set_window_size(2048, 1080)
    return driver

def scraper(url):
    driver = create_driver()
    all_data = []
    try:
        driver.get(url)
        click_accept_all_cookies(driver)
        click_accept_all_other_cookie(driver)
        
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
        custom_logger.log(f"An error occurred while processing the website: {str(e)}")
        return all_data

def scraper_social_for_business_email(url):
    driver = create_driver()
    try:
        search_url = "https://www.google.com/search?q=" + "facebook page " + url
        driver.get(search_url)

        click_accept_all_cookies(driver)
        click_accept_all_other_cookie(driver)

        wait = WebDriverWait(driver, 3)
        data = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "byrV5b")))

        time.sleep(1)
        close_popup_if_present(driver)

        driver.execute_script("arguments[0].scrollIntoView(true);", data)
        driver.execute_script("arguments[0].click();", data)

        time.sleep(1)

        close_popup_if_present(driver)

        business_email = driver.find_element(By.CLASS_NAME, "xieb3on")

        # location = parse_fb_address(business_email.text)
        # print("location: ",location)

        email = parse_email(business_email.text)
        return email
    except Exception as e:
        custom_logger.log(f"Accept all cookies button not found (Google): {e.msg if hasattr(e, 'msg') else str(e)}")
        return ""
    finally:
        driver.quit()

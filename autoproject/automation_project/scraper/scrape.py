import re
import time
import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from undetected_chromedriver import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


MAX_RETRIES = 3

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
        driver = uc.Chrome(options=option)
        driver.get(url)
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
        print(f"An error occurred while processing the website: {str(e)}")
        return all_data
    finally:
        driver.quit()

def scraper_social_for_business_email(url):
    print("started facebook crawling...")
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

        data = scraper.find_element(By.CLASS_NAME, "byrV5b")
        data.click()
        
        time.sleep(3)
        # username_box = scraper.find_elements(By.NAME, 'email')[1]
        # username_box.send_keys("9813350184")
       
        
        # password_box = scraper.find_element(By.NAME, 'pass')
        # password_box.send_keys("Aszx12#c")[1]
        
        # login_box = scraper.find_element(By.XPATH, '//*[@id="login_popup_cta_form"]/div/div[5]/div/div')
        # login_box.click()
        
        time.sleep(5)
        business_email = scraper.find_element(By.CLASS_NAME, "xieb3on")
        
        email = parse_email(business_email.text)
        scraper.quit()
        return email
    except Exception as e:
        print(e)
        return ""
    
   
        
if __name__ == '__main__':
    #content = input('Enter the content to search: ')
    #url = f"https://www.google.com/localservices/prolist?g2lbs=AP8S6ENVYaPlUqcpp5HFvzYE-khspk5ZxM7UvCPm_mrThLHuOOuoVhvujWM4YXtq4ZMQsSh1MG2ABSTirzgWdxto0NPXtv1pZWmQ6kYBduBDBF9QJC4dd9HZd4niObLIbzEuBxwPcxvE&hl=en-NP&gl=np&cs=1&ssta=1&oq={content}&src=2&sa=X&q={content}&ved=0CAUQjdcJahgKEwjg8IiHroyBAxUAAAAAHQAAAAAQ4wI&scp=ChdnY2lkOnJlYWxfZXN0YXRlX2FnZW5jeRIAGgAqDEVzdGF0ZSBBZ2VudA%3D%3D&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAA%3D%3D"
    schools = [
        "Littel Angels School Hattiban", 
        "Rai School", 
        "Kathmandu Model College",
        "Kathmandu BernHardt College",
        "Kathmandu University School of Management",
    ]
    for url in schools:
    # print(is_website_okay(url))
        print(scraper_social_for_business_email(url))

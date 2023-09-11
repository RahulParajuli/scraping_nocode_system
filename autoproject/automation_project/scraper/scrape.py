import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from undetected_chromedriver import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MAX_RETRIES = 3

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

if __name__ == '__main__':
    content = input('Enter the content to search: ')
    url = f"https://www.google.com/localservices/prolist?g2lbs=AP8S6ENVYaPlUqcpp5HFvzYE-khspk5ZxM7UvCPm_mrThLHuOOuoVhvujWM4YXtq4ZMQsSh1MG2ABSTirzgWdxto0NPXtv1pZWmQ6kYBduBDBF9QJC4dd9HZd4niObLIbzEuBxwPcxvE&hl=en-NP&gl=np&cs=1&ssta=1&oq={content}&src=2&sa=X&q={content}&ved=0CAUQjdcJahgKEwjg8IiHroyBAxUAAAAAHQAAAAAQ4wI&scp=ChdnY2lkOnJlYWxfZXN0YXRlX2FnZW5jeRIAGgAqDEVzdGF0ZSBBZ2VudA%3D%3D&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAA%3D%3D"
    print(is_website_okay(url))
    print(scraper(url))

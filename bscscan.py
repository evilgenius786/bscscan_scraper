import csv
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

t = 1
timeout = 10

debug = False

headless = True
images = False
max = True

incognito = True

file = "BscScan-safemoon.csv"
headers = ["Rank", "Address", "Quantity", "Percentage", "Value"]


def main():
    os.system("color 0a")
    logo()
    if not os.path.isfile(file):
        with open(file, 'w', newline='') as csvfile:
            csv.writer(csvfile).writerow(headers)
    driver = getChromeDriver()
    driver.get("https://www.bscscan.com/token/0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3#balances")
    driver.switch_to.frame('tokeholdersiframe')
    for i in range(int(getElement(driver, '//*[@class="page-link text-nowrap"]/strong[2]').text)):
        rows = []
        for tr in getElements(driver, '//table[@class="table table-md-text-normal table-hover"]/tbody/tr'):
            row = []
            for td in getElements(tr, './td'):
                if len(td.text) > 0:
                    row.append(td.text)
            rows.append(row)
            print(row)
        with open(file, 'a', newline='') as csvfile:
            csv.writer(csvfile).writerows(rows)
        driver.switch_to.default_content()
        driver.switch_to.frame('tokeholdersiframe')
        click(driver, '//a[@aria-label="Next"]')


def logo():
    print(f"""
                    (                      
       (            )\ )                   
     ( )\          (()/(         )         
     )((_) (    (   /(_)) (   ( /(   (     
    ((_)_  )\   )\ (_))   )\  )(_))  )\ )  
     | _ )((_) ((_)/ __| ((_)((_)_  _(_/(  
     | _ \(_-</ _| \__ \/ _| / _` || ' \)) 
     |___//__/\__| |___/\__| \__,_||_||_|  
=================================================
      Binance (BNB) Blockchain Explorer
        (SAFEMOON) Token Scraper by:
      fiverr.com/users/muhammadhassan7
=================================================
Output file: {file}""")


def click(driver, xpath, js=False):
    if js:
        driver.execute_script("arguments[0].click();", getElement(driver, xpath))
    else:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


def getElement(driver, xpath):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


def getElements(driver, xpath):
    return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))


def sendkeys(driver, xpath, keys, js=False):
    if js:
        driver.execute_script(f"arguments[0].value='{keys}';", getElement(driver, xpath))
    else:
        getElement(driver, xpath).send_keys(keys)


def getChromeDriver(proxy=None):
    options = webdriver.ChromeOptions()
    if debug:
        # print("Connecting existing Chrome for debugging...")
        options.debugger_address = "127.0.0.1:9222"
    if not images:
        # print("Turning off images to save bandwidth")
        options.add_argument("--blink-settings=imagesEnabled=false")
    if headless:
        # print("Going headless")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
    if max:
        # print("Maximizing Chrome ")
        options.add_argument("--start-maximized")
    if proxy:
        # print(f"Adding proxy: {proxy}")
        options.add_argument(f"--proxy-server={proxy}")
    if incognito:
        # print("Going incognito")
        options.add_argument("--incognito")
    return webdriver.Chrome(options=options)


def getFirefoxDriver():
    options = webdriver.FirefoxOptions()
    if not images:
        # print("Turning off images to save bandwidth")
        options.set_preference("permissions.default.image", 2)
    if incognito:
        # print("Enabling incognito mode")
        options.set_preference("browser.privatebrowsing.autostart", True)
    if headless:
        # print("Hiding Firefox")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
    return webdriver.Firefox(options)


if __name__ == "__main__":
    main()

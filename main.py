from lib2to3.pgen2 import driver
from weakref import proxy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
import time
import sys

global final_proxies
final_proxies = []

class nprox:
    def __init__(self, driver) -> None:
        self.prox(driver)
        driver.close()

    def __len__(self) -> int:
        return len(final_proxies)

    def get_prox(self, driver) -> str:
        driver.get('https://sslproxies.org')

        table = driver.find_element(By.TAG_NAME, 'table')
        thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
        tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

        headers = []
        for th in thead:
            headers.append(th.text.strip())

        proxies = []
        for tr in tbody:
            proxy_data = {}
            tds = tr.find_elements(By.TAG_NAME, 'td')
            for i in range(len(headers)):
                proxy_data[headers[i]] = tds[i].text.strip()
            proxies.append(proxy_data)
        
        for i in proxies:
            final_proxies.append(f'{i["IP Address"]}:{i["Port"]}')
        
    def prox(self, driver):
        if len(final_proxies) == 0:
            self.get_prox(driver=driver)
        return(random.choice(final_proxies))   

class oplegends():
    def __init__(self, option, driver, user=".GoAmeer030") -> None:
        self.user = user
        self.option = option
        self.driver = driver
        self.msl(self.option, self.driver)
        

    def msl(self, option, driver):
        driver = main.change_prox(option=option, driver=driver)
        driver.get("https://minecraft-server-list.com/server/443038/vote/")
        print("MSL opened")
        text = driver.find_element(By.NAME, 'ignn')
        text.send_keys(self.user)
        time.sleep(3)
        button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="voteform"]/input[5]')))
        button.click()
        print("Clicked")
        try:
            result = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="voteerror"]')))
        except:
            button.click()
            result = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="voteerror"]')))
        while((result.text in ("Please Wait....", "Error with the Anti Spam check - Please try again. (Click F5 to reload the page).", "")) or ("Username already voted today!" in result.text)):
            if (result.text == "Please Wait...."):
                time.sleep(1)
                result = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="voteform"]/input[5]')))
            elif ("Username already voted today!" in result.text):
                print("elif")
                break
            else:
                print("Recu")
                self.msl(option = option, driver = driver)
        print(result.text)
        driver.close()

class main:

    def __init__(self, user='.GoAmeer030') -> None:
        option = webdriver.ChromeOptions()
        # self.option.add_argument("headless")
        option.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=option, executable_path=r'./chromedriver.exe')
        
        oplegends(option = option, driver = driver, user = user)

    def change_prox(option, driver):
        proxy = nprox(driver=driver)
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": proxy,
            "ftpProxy": proxy,
            "sslProxy": proxy,
            "proxyType": "MANUAL",

        }
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True
        driver = webdriver.Chrome(options=option, executable_path=r'.\chromedriver.exe')
        return(driver)

if __name__ == "__main__" :
    main(sys.argv[1])
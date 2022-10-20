from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import random
import time
import sys

global final_proxies
# noinspection PyRedeclaration
final_proxies = []


class new_proxy:
    def __len__(self) -> int:
        return len(final_proxies)

    @staticmethod
    def get_proxy(driver) -> None:
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

    @staticmethod
    def proxy(driver) -> str:
        if len(final_proxies) == 0:
            new_proxy.get_proxy(driver=driver)
        driver.close()
        return str(random.choice(final_proxies))


class Oplegends:
    def __init__(self, option, driver, user=".GoAmeer030") -> None:
        self.user = user
        self.option = option
        self.driver = driver
        self.minecraft_server_list(self.option, self.driver)

    def minecraft_server_list(self, option, driver):
        driver = main.change_proxy(option=option, driver=driver)
        driver.get("https://minecraft-server-list.com/server/443038/vote/")
        # print("MSL opened")
        text = driver.find_element(By.NAME, 'ignn')
        text.send_keys(self.user)
        time.sleep(3)
        button = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="voteform"]/input[5]')))
        button.click()
        # print("Clicked")
        # noinspection PyBroadException
        try:
            result = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="voteerror"]')))
        except Exception:
            button.click()
            result = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="voteerror"]')))
        while ((result.text in (
                "Please Wait....", "Error with the Anti Spam check - Please try again. (Click F5 to reload the page).",
                "")) or ("Username already voted today!" in result.text)):
            if result.text == "Please Wait....":
                time.sleep(1)
                result = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="voteform"]/input[5]')))
            elif "Username already voted today!" in result.text:
                # print("elif")
                break
            else:
                # print("recursion")
                self.minecraft_server_list(option=option, driver=driver)
        else:
            print(result.text)
            driver.close()


class main:

    def __init__(self, user='.GoAmeer030') -> None:
        option = webdriver.ChromeOptions()
        # self.option.add_argument("headless")
        option.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(service=Service(r'./chromedriver.exe'), options=option)

        Oplegends(option=option, driver=driver, user=user)

    @staticmethod
    def change_proxy(option, driver):
        proxy = new_proxy.proxy(driver=driver)
        # print(proxy)
        # webdriver.DesiredCapabilities.CHROME['proxy'] = {
        #     "httpProxy": proxy,
        #     "ftpProxy": proxy,
        #     "sslProxy": proxy,
        #     "proxyType": "MANUAL",
        # }
        # webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
        option.add_argument(f'--proxy-server={proxy}')
        driver = webdriver.Chrome(service=Service(r'.\chromedriver.exe'), options=option)
        return driver


if __name__ == "__main__":
    main(sys.argv[1])
    # main(".dhiangarvijay27")
    # main()
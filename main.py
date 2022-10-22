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
    """
    Some Times only this will work because I don't know how to make it work
    """

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

        final_proxies.append(f'{i["IP Address"]}:{i["Port"]}' for i in proxies if
                             i["Code"] in ["US", "IN", "SG", "DE", "CA"] and i["Google"] in ["yes", "no"])

    @staticmethod
    def proxy(driver) -> str:
        if len(final_proxies) == 0:
            new_proxy.get_proxy(driver=driver)
        driver.close()
        return str(random.choice(final_proxies))


class Oplegends:
    def __init__(self, option, user, is_proxy_change) -> None:
        self.user = user
        self.option = option
        self.driver = webdriver.Chrome(
            service=Service(r'.\chromedriver.exe'), options=self.option)
        self.is_proxy_change = is_proxy_change
        self.minecraft_server_list()
        self.driver_close()

    def minecraft_server_list(self):
        driver = main.change_proxy(option=self.option) if self.is_proxy_change == "-y" else self.driver
        driver.get("https://minecraft-server-list.com/server/443038/vote/")
        # print("MSL opened")
        text = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'ignn')))
        text.send_keys(self.user)
        time.sleep(3)
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="voteform"]/input[5]')))
        button.click()
        # print("Clicked")
        time.sleep(3)
        result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="voteerror"]')))
        print("Oplegends : Minecraft Server List:", result.text)
        while ((result.text in ("Error with the Anti Spam check - Please try again. (Click F5 to reload the page).",
                "")) or ("Username already voted today!" in result.text)):
            if "Username already voted today!" in result.text:
                # print("elif")
                break
            else:
                # print("recursion")
                self.minecraft_server_list()

    def driver_close(self) -> None:
        self.driver.close()


class main:

    def __init__(self, user='.GoAmeer030', is_proxy_change='-n') -> None:
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        option.add_experimental_option('useAutomationExtension', False)

        Oplegends(option=option, user=user, is_proxy_change=is_proxy_change)

    @staticmethod
    def change_proxy(option):
        driver = webdriver.Chrome(service=Service(r'.\chromedriver.exe'), options=option)
        proxy = new_proxy.proxy(driver=driver)
        # print(proxy)
        option.add_argument(f'--proxy-server={proxy}')
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
        driver = webdriver.Chrome(service=Service(r'.\chromedriver.exe'), options=option)
        return driver


if __name__ == "__main__":
    try:
        main(sys.argv[1], sys.argv[2])
    except IndexError:
        main()
        # main(".dhiangarvijay27")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

import random
import time
import sys

global final_proxies, web_results
final_proxies = []
web_results = []


class NewProxy:
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
            NewProxy.get_proxy(driver=driver)
        driver.close()
        return str(random.choice(final_proxies))


class OpLegends:
    def __init__(self, option, user, is_proxy_change, msl_server="server/443038/vote/", ms_server="vote/580828",
                 mmp_server="server/252752/vote/", bms_server="server-oplegends.4667/vote") -> None:
        self.user = user
        self.option = option
        self.driver = webdriver.Chrome(
            service=Service('./chromedriver'), options=self.option)
        self.is_proxy_change = is_proxy_change

        self.msl_server = msl_server
        self.ms_server = ms_server
        self.mmp_server = mmp_server
        self.bms_server = bms_server

        self.minecraft_server_list_com()
        self.minecraftservers_org()
        self.minecraft_mp_com()
        self.best_minecraft_servers_co()

        self.driver_close()

    def minecraft_server_list_com(self):
        driver = Main.change_proxy(option=self.option) if self.is_proxy_change == "-y" else self.driver
        driver.get("https://minecraft-server-list.com/" + self.msl_server)
        # print("MSL opened")
        text = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'ignn')))
        time.sleep(2)
        text.send_keys(self.user)
        time.sleep(1)
        button = driver.find_element(By.NAME, 'button')
        driver.execute_script("arguments[0].click();", button)
        # print("Clicked")
        time.sleep(5)
        result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="voteerror"]')))
        web_results.append(result.text)
        print("OpLegends: Minecraft Server List:", web_results[-1])
        while ((web_results[-1] in ("Error with the Anti Spam check - Please try again. (Click F5 to reload the page).",
                "")) or ("Username already voted today!" in web_results[-1])):
            if "Username already voted today!" in web_results[-1]:
                # print("elif")
                break
            else:
                # print("recursion")
                self.minecraft_server_list_com()

    def minecraftservers_org(self):
        driver = Main.change_proxy(option=self.option) if self.is_proxy_change == "-y" else self.driver
        driver.get('https://minecraftservers.org/' + self.ms_server)

    def minecraft_mp_com(self):
        driver = Main.change_proxy(option=self.option) if self.is_proxy_change == "-y" else self.driver
        driver.get("https://minecraft-mp.com/" + self.mmp_server)
        text = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'nickname')))
        time.sleep(2)
        text.send_keys(self.user)
        time.sleep(1)
        check_box = driver.find_element(By.XPATH, '//*[@id="accept"]')
        check_box.click()
        time.sleep(1)
        button = driver.find_element(By.XPATH, '//*[@id="voteBtn"]')
        button.click()
        time.sleep(5)
        try:
            result = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="vote_form"]/div[1]')))
            web_results.append(result.text)
        except Exception:
            result = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[6]/div[1]/p[1]/strong')))
            web_results.append(result.text)
        print("OpLegends: Minecraft MP:", web_results[-1])

    def best_minecraft_servers_co(self):
        driver = Main.change_proxy(option=self.option) if self.is_proxy_change == "-y" else self.driver
        driver.get("https://best-minecraft-servers.co/" + self.bms_server)

    def driver_close(self) -> None:
        self.driver.close()


class Main:

    def __init__(self, user='.GoAmeer030', is_proxy_change='-n') -> None:
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        option.add_experimental_option('useAutomationExtension', False)

        OpLegends(option=option, user=user, is_proxy_change=is_proxy_change)

    @staticmethod
    def change_proxy(option):
        driver = webdriver.Chrome(service=Service('./chromedriver'), options=option)
        proxy = NewProxy.proxy(driver=driver)
        # print(proxy)
        option.add_argument(f'--proxy-server={proxy}')
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
        driver = webdriver.Chrome(service=Service('./chromedriver'), options=option)
        return driver


if __name__ == "__main__":
    try:
        Main(sys.argv[1], sys.argv[2])
    except IndexError:
        Main()
        # main(".dhiangarvijay27")

from servers import *
from servers.changeproxy import ChangeProxy


class OpLegends:
    def __init__(self, option, msl_server="server/443038/vote/", ms_server="vote/580828",
                 mmp_server="server/252752/vote/", bms_server="server-oplegends.4667/vote") -> None:
        self.user = global_variables.config_data["username"]
        self.option = option
        self.driver = webdriver.Chrome(
            service=Service('./chromedriver'), options=self.option)
        self.is_proxy_change = global_variables.config_data["is_proxy_change"]

        self.msl_server = msl_server
        self.ms_server = ms_server
        self.mmp_server = mmp_server
        self.bms_server = bms_server

        if 'minecraft_server_list_com' in global_variables.config_server_data['OpLegends']:
            self.minecraft_server_list_com()

        if 'minecraftservers_org.c' in global_variables.config_server_data['OpLegends']:
            self.minecraftservers_org()

        if 'minecraft_mp_com.c' in global_variables.config_server_data['OpLegends']:
            self.minecraft_mp_com()

        if 'best_minecraft_servers_co' in global_variables.config_server_data['OpLegends']:
            self.best_minecraft_servers_co()

        self.driver_close()

    def minecraft_server_list_com(self):
        driver = ChangeProxy.change_proxy(option=self.option) if self.is_proxy_change is True else self.driver
        driver.get("https://minecraft-server-list.com/" + self.msl_server)
        text = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'ignn')))
        time.sleep(2)
        text.send_keys(self.user)
        time.sleep(1)
        button = driver.find_element(By.NAME, 'button')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(5)
        result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="voteerror"]')))
        global_variables.web_results.append(result.text)
        print("OpLegends: Minecraft Server List:", global_variables.web_results[-1])
        while ((global_variables.web_results[-1] in ("Error with the Anti Spam check - Please try again. (Click F5 to "
                                                     "reload the page).", "")) or ("Username already voted today!" in
                                                                                   global_variables.web_results[-1])):
            if "Username already voted today!" in global_variables.web_results[-1]:
                break
            else:
                self.minecraft_server_list_com()

    def minecraftservers_org(self):
        driver = ChangeProxy.change_proxy(option=self.option) if self.is_proxy_change is True else self.driver
        driver.get('https://minecraftservers.org/' + self.ms_server)
        try:
            result = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="error-message"]')))
            print("OpLegends: Minecraft servers:", result.text)
        except Exception:
            check_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="checkbox"]')))
            time.sleep(3)
            check_box.click()
            time.sleep(2)
            text = driver.find_element(By.XPATH, '//*[@id="vote-form"]/ul/li/input')
            text.send_keys(self.user)
            time.sleep(1)
            button = driver.find_element(By.XPATH, '//*[@id="vote-btn"]')
            button.click()
            result = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="error-message"]')))
            print("OpLegends: Minecraft servers:", result.text)

    def minecraft_mp_com(self):
        driver = ChangeProxy.change_proxy(option=self.option) if self.is_proxy_change is True else self.driver
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
        time.sleep(2)
        if EC.presence_of_element_located((By.XPATH, '/html/body/div')):
            print("OpLegends: Minecraft MP: Captcha arise!! Solve it!!")
            time.sleep(10)
        time.sleep(5)
        try:
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="vote_form"]/div[1]')))
            global_variables.web_results.append(result.text)
        except Exception:
            result = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[6]/div[1]/p[1]/strong')))
            global_variables.web_results.append(result.text)
        print("OpLegends: Minecraft MP:", global_variables.web_results[-1])

    def best_minecraft_servers_co(self):
        driver = ChangeProxy.change_proxy(option=self.option) if self.is_proxy_change is True else self.driver
        driver.get("https://best-minecraft-servers.co/" + self.bms_server)
        text = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div/input[3]')))
        time.sleep(2)
        text.send_keys(self.user)
        button = driver.find_element(By.XPATH, '//*[@id="main-content"]/button')
        time.sleep(1)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(5)
        try:
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section/div[1]/p')))
            global_variables.web_results.append(result.text)
        except Exception:
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section/div[1]/p')))
            global_variables.web_results.append(result.text)
        print("OpLegends: Best Minecraft Server:", global_variables.web_results[-1])

    def driver_close(self) -> None:
        self.driver.close()

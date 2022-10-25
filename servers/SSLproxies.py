from servers import *


class NewProxy:
    """
    Some Times only this will work because I don't know how to make it work
    """

    def __len__(self) -> int:
        return len(global_variables.final_proxies)

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

        global_variables.final_proxies.append(f'{i["IP Address"]}:{i["Port"]}' for i in proxies if
                                              i["Code"] in ["US", "IN", "SG", "DE", "CA"] and i["Google"] in ["yes",
                                                                                                              "no"])

    @staticmethod
    def proxy(driver) -> str:
        if len(global_variables.final_proxies) == 0:
            NewProxy.get_proxy(driver=driver)
        print("SSL proxies: Proxies got successfully")
        driver.close()
        return str(random.choice(global_variables.final_proxies))

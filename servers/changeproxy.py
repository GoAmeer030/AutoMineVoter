from servers import *
from servers.SSLproxies import NewProxy


class ChangeProxy:
    @staticmethod
    def change_proxy(option):
        driver = webdriver.Chrome(service=Service('./chromedriver'), options=option)
        proxy = NewProxy.proxy(driver=driver)
        print(proxy)
        option.add_argument(f'--proxy-server={proxy}')
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
        driver = webdriver.Chrome(service=Service('./chromedriver'), options=option)
        return driver

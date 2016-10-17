from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Navigator():
    def __init__(self, driver, host, timeout, print_debug_func):
        self.driver = driver
        self.host = host
        self.timeout = timeout
        self.print_debug_func = print_debug_func

    def get_page(self, url):
        request = 'http://' + self.host + url
        self.driver.get(request)
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.ID, "test-done")))
            return self.driver.find_element(By.TAG_NAME, 'body').text
        except Exception as e:
            self.print_debug_func()
            raise e



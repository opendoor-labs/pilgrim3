from pytest import fixture
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Debugging Helpers
# logs = self.driver.get_log("har")
# logs = self.driver.get_log("browser")
# screenshot_loc = "log/%f.png" % time.time()
# print('error ocured while using selenium, see ' + screenshot_loc)
# self.driver.save_screenshot(screenshot_loc)

class Navigator():
    def __init__(self, driver, host, timeout, debug_logs):
        self.driver = driver
        self.host = host
        self.timeout = timeout
        self.debug_logs = debug_logs

    def get_page(self, url):
        request = 'http://' + self.host + url
        self.driver.get(request)
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.ID, "test-done")))
            return self.driver.find_element(By.TAG_NAME, 'body').text
        except Exception as e:
            print("error occurred on page, see logs below")
            print(e)

            for debug_log in self.debug_logs:
                print("**** %s ****" % debug_log[0])
                with open(debug_log[1], "r") as f:
                    print(f.read())
                print("******************")

            raise e


@fixture()
def navigator(server_did_boot, driver, test_host, timeout, debug_logs):
    assert server_did_boot, "server did not start up"
    yield Navigator(driver, test_host, timeout, debug_logs)


def test_file_comment(navigator):
    assert 'file-comment' in navigator.get_page("/#/files/example/types.proto")

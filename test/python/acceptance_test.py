from pytest import fixture
from pytest import mark
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
            print_logs(self.debug_logs)

            raise e

def print_logs(debug_logs):
    for debug_log in debug_logs:
        print("**** %s ****" % debug_log[0])
        with open(debug_log[1], "r") as f:
            print(f.read())
        print("******************")

@fixture()
def navigator(server_did_boot, driver, test_host, timeout, debug_logs):
    if server_did_boot:
        yield Navigator(driver, test_host, timeout, debug_logs)
    else:
        print_logs(debug_logs)
        assert server_did_boot, "server did not start up"


memoization = {}


@fixture()
def file_proto_page(navigator):
    if 'file_proto' not in memoization:
        memoization['file_proto'] = navigator.get_page('/#/files/example/types.proto')
    yield memoization['file_proto']


@fixture()
def message_proto_page(navigator):
    if 'message_proto' not in memoization:
        memoization['message_proto'] = navigator.get_page('/#/messages/.example.Message')
    yield memoization['message_proto']


def test_file_comment(file_proto_page):
    assert 'file-comment' in file_proto_page


@mark.parametrize("comment_string", [
    ("message-comment"),
    ("message-field-comment"),
    ("message-oneof-comment"),
    ("message-oneof-field[0]-comment"),
    ("message-oneof-field[1]-comment"),
])
def test_message_comment(comment_string, message_proto_page):
    assert comment_string in message_proto_page

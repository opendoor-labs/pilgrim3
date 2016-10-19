from pytest import fixture
from selenium import webdriver
import httplib
import logging

FAIL = '\033[91m'
ENDC = '\033[0m'


@fixture(scope="session")
def port():
    yield webdriver.common.utils.free_port()


@fixture(scope="session")
def hostname():
    yield "localhost"


@fixture(scope="session")
def test_host(hostname, port):
    yield "%s:%i" % (hostname, port)


@fixture(scope="session")
def timeout():
    yield 5


# Boot timeout can be really low because we retry many times
@fixture(scope="session")
def boot_timeout():
    yield 0.1


@fixture(scope="session")
def app_log_path():
    yield "log/app.test.log"


@fixture(scope="session")
def ghostdriver_log_path():
    yield "log/ghostdriver.log"


# use a provider to make connection to server after it has been booted
@fixture(scope="session")
def client_provider(hostname, port, timeout):
    def get():
        return httplib.HTTPConnection(hostname, port, timeout=timeout)

    yield get


# Reset app logs every time so each test gets fresh logs when failure occurs
@fixture(autouse=True)
def set_app_log(app_log_path):
    log_names = ['werkzeug']
    app_logs = map(lambda log_name: logging.getLogger(log_name), log_names)
    file_handler = logging.FileHandler(app_log_path, 'w')

    for app_log in app_logs:
        for hdlr in app_log.handlers[:]:  # remove all old handlers
            app_log.removeHandler(hdlr)

        app_log.addHandler(file_handler)


@fixture(scope="module")
def driver(ghostdriver_log_path):
    driver = webdriver.PhantomJS(service_log_path=ghostdriver_log_path)
    driver.set_window_size("1120", "550")
    yield driver
    driver.quit()


@fixture()
def debug_logs(app_log_path, ghostdriver_log_path):
    yield (("App Log", app_log_path), ("PhantomJS Log", ghostdriver_log_path))


@fixture
def print_debug_func(debug_logs):
    def print_logs():
        for debug_log in debug_logs:
            print("**** %s ****" % debug_log[0])
            with open(debug_log[1], "r") as f:
                print(f.read())
            print("******************")

    yield print_logs

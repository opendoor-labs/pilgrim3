from flask import request
from test.python.navigator import Navigator
from pilgrim3.app import app as pilgrim_app
from pytest import fixture
from selenium import webdriver
from socket import error as socket_error
from test.python.memoize import memoize
from test.python.memoize import clear_memoized_cache
from threading import Thread
import httplib
import logging
import time

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


@fixture(scope="session")
def app_with_shutdown_endpoints():
    # OMG there is no signaling of threads in python 2.x - so
    # the only way to tell the flask app to shutdown is this.
    # I searched far and wide, jesus christ. http://flask.pocoo.org/snippets/67/
    #
    # The app thread should be started as a damon so we get a kill -9 after the timeout expires
    @pilgrim_app.route('/shutdown', methods=['GET'])
    def shutdown():
        request.environ.get('werkzeug.server.shutdown')()
        return "shutdown"

    @pilgrim_app.route('/booted', methods=['GET'])
    def booted():
        return "booted"

    yield pilgrim_app


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


@fixture(scope="module")
def server_thread(app, hostname, port, client_provider):
    server = Thread(target=lambda: app.run(host=hostname, port=port, threaded=True))
    server.daemon = True
    yield server
    try:
        client_provider().request("GET", "/shutdown")
    except (httplib.CannotSendRequest, socket_error):
        print FAIL + "Error shutting down" + ENDC

    server.join(1)
    if server.is_alive():
        print FAIL + "Unable to gracefully shutdown server"
        print "Resources may not have been released" + ENDC


@fixture(scope="module")
def server_did_boot(server_thread, hostname, port, boot_timeout):
    server_thread.start()
    retry_count = 0
    booted = False
    while True:
        try:
            boot_client = httplib.HTTPConnection(hostname, port, timeout=boot_timeout)
            boot_client.request("GET", "/booted")
            boot_client.getresponse()
            booted = True
        except (httplib.CannotSendRequest, socket_error):
            print "error trying to startup:, connecting again"
            time.sleep(0.1)
            retry_count = retry_count + 1
            if retry_count < 200:  # 20 seconds
                continue
        break
    yield booted


@fixture(scope="module")
def app(app_with_shutdown_endpoints, proto_bundle_path):
    app_with_shutdown_endpoints.config['proto-bundle'] = proto_bundle_path
    yield app_with_shutdown_endpoints


## Params


@fixture(params= [
    ("file-comment"),
    ("Enums (1)"),
    ("Services (1)"),
    ("Messages (2)"),
])
def file_proto_comment(request):
    yield request.param

@fixture(params=[
    ("message-comment"),
    ("message-field-comment"),
    ("message-oneof[0]-comment"),
    ("message-oneof[0]-field[0]-comment"),
    ("message-oneof[0]-field[1]-comment"),
    ("message-oneof[1]-comment"),
    ("message-oneof[1]-field[0]-comment"),
    ("message-oneof[1]-field[1]-comment"),
])
def message_proto_comment(request):
    yield request.param


@fixture(params=[
    ("nested-message-comment"),
    ("nested-message-field-comment"),
    ("nested-message-oneof-comment"),
    ("nested-message-oneof-field[0]-comment"),
    ("nested-message-oneof-field[1]-comment"),
])
def nested_message_proto_comment(request):
    yield request.param


@fixture(params=[
    ("recursive-message-comment"),
    ("recursive-message-field-comment"),
    ("recursive-message-oneof-comment"),
    ("recursive-message-oneof-field[0]-comment"),
    ("recursive-message-oneof-field[1]-comment"),
])
def recursive_message_proto_comment(request):
    yield request.param


@fixture(params=[
    ('enum-comment'),
    ('enum-val[0]-comment'),
    ('enum-val[1]-comment'),
])
def enum_proto_comment(request):
    yield request.param


@fixture(params=[
    ('nested-enum-comment'),
    ('nested-enum-val[0]-comment'),
    ('nested-enum-val[1]-comment'),
])
def nested_enum_proto_comment(request):
    yield request.param


@fixture(params= [
    ('recursive-enum-comment'),
    ('recursive-enum-val[0]-comment'),
    ('recursive-enum-val[1]-comment'),
])
def recursive_enum_proto_comment(request):
    yield request.param

@fixture(params= [
    ("service-comment"),
    ("action-comment"),
])
def service_proto_comment(request):
    yield request.param

## Fixtures
@fixture
def navigator(server_did_boot, driver, test_host, timeout, print_debug_func):
    if server_did_boot:
        yield Navigator(driver, test_host, timeout, print_debug_func)
    else:
        print_debug_func()
        assert server_did_boot, "server did not start up"


@fixture
def types_file_url():
    yield '/#/files/example/types.proto'


@fixture
def example_message_url():
    yield '/#/messages/example.ExampleMessage'


@fixture
def example_nested_message_url():
    yield '/#/messages/example.ExampleNestingScope.ExampleNestedMessage'


@fixture
def example_recursive_message_url():
    yield '/#/messages/example.ExampleNestingScope.RecursiveProvingScope.ExampleRecursiveMessoge '


@fixture
def example_enum_url():
    yield '#/enums/example.ExampleEnum'


@fixture
def example_nested_enum_url():
    yield '/#/enums/example.ExampleNestingScope.ExampleNestedEnum'


@fixture
def example_recursive_enum_url():
    yield '/#/enums/example.ExampleNestingScope.RecursiveProvingScope.ExampleRecursiveEnum'


@fixture
def example_service_url():
    yield '#/services/example.ExampleService'


@fixture
@memoize
def file_proto_page(navigator, types_file_url):
    yield navigator.get_page(types_file_url)


@fixture
@memoize
def message_proto_page(navigator, example_message_url):
    yield navigator.get_page(example_message_url)


@fixture
@memoize
def nested_message_proto_page(navigator, example_nested_message_url):
    yield navigator.get_page(example_nested_message_url)


@fixture
@memoize
def recursive_message_proto_page(navigator, example_recursive_message_url):
    yield navigator.get_page(example_recursive_message_url)


@fixture
@memoize
def service_proto_page(navigator, example_service_url):
    yield navigator.get_page(example_service_url)


@fixture
@memoize
def enum_proto_page(navigator, example_enum_url):
    yield navigator.get_page(example_enum_url)


@fixture
@memoize
def nested_enum_proto_page(navigator, example_nested_enum_url):
    yield navigator.get_page(example_nested_enum_url)


@fixture
@memoize
def recursive_enum_proto_page(navigator, example_recursive_enum_url):
    yield navigator.get_page(example_recursive_enum_url)

@fixture(autouse=True, scope="module")
def clear_cache():
    clear_memoized_cache()

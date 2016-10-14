from pytest import fixture

import os
from threading import Thread

import time
import logging

import httplib
from socket import error as socket_error

from pilgrim3.app import app as pilgrim_app
from flask import request

from selenium import webdriver

FAIL = '\033[91m'
ENDC = '\033[0m'


@fixture(scope="session")
def port():
    yield 9151


@fixture(scope="session")
def hostname():
    yield "localhost"


@fixture(scope="session")
def test_host(hostname, port):
    yield "%s:%i" % (hostname, port)


@fixture(scope="session")
def timeout():
    yield 5


@fixture()
def app_log_path():
    yield "log/app.test.log"

@fixture()
def ghostdriver_log_path():
    yield "log/ghostdriver.log"


@fixture(scope="session")
def app():
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

    pilgrim_app.config['proto-bundle'] = os.path.abspath("test/support/build/types.build")
    yield pilgrim_app


@fixture(scope="session")
def server_thread(app, hostname, port, client):
    server = Thread(target=lambda: app.run(host=hostname, port=port, threaded=True))
    server.daemon = True
    yield server
    try:
        client.request("GET", "/shutdown")
    except (httplib.CannotSendRequest, socket_error):
        print FAIL + "Error shutting down" + ENDC

    server.join(1)
    if server.is_alive():
        print FAIL + "Unable to gracefully shutdown server"
        print "Resources may not have been released" + ENDC


@fixture(scope="session")
def client(hostname, port, timeout):
    yield httplib.HTTPConnection(hostname, port, timeout=timeout)


@fixture(scope="session")
def server_did_boot(server_thread, client):
    server_thread.start()
    retry_count = 0
    booted = False
    while True:
        try:
            client.request("GET", "/booted")
            client.getresponse()
            booted = True
        except (httplib.CannotSendRequest, socket_error):
            time.sleep(0.1)
            retry_count = retry_count + 1
            if retry_count < 100:  # 10 seconds
                continue
        break
    yield booted


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


@fixture()
def driver(ghostdriver_log_path):
    driver = webdriver.PhantomJS(service_log_path=ghostdriver_log_path)
    driver.set_window_size("1120", "550")
    yield driver
    print("Tearing down")
    driver.quit()

@fixture()
def debug_logs(app_log_path, ghostdriver_log_path):
    yield (("App Log", app_log_path), ("PhantomJS Log", ghostdriver_log_path))

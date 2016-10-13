import unittest
import os

import time
from pilgrim3.app import app
from threading import Thread
from flask import request
import logging

import httplib
from socket import error as socket_error

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FAIL = '\033[91m'
ENDC = '\033[0m'

# OMG there is no signaling of threads in python 2.x - so
# the only way to tell the flask app to shutdown is this.
# I searched far and wide, jesus christ. http://flask.pocoo.org/snippets/67/
#
# The app thread should be started as a damon so we get a kill -9 after the timeout expires
@app.route('/shutdown', methods=['GET'])
def shutdown():
    request.environ.get('werkzeug.server.shutdown')()
    return "shut down"

@app.route('/booted', methods=['GET'])
def booted():
    return "yes"

class CommentTestCase(unittest.TestCase):
    @classmethod
    def configure_server_in_thread(cls, hostname, port):
        # for now compile this by running test/support/proto3/compile
        app.config['proto-bundle'] = os.path.abspath("test/support/build/types.build")
        server = Thread(target=lambda: app.run(host=hostname, port=port, threaded=True))
        server.daemon = True
        server.start()
        return server

    @classmethod
    def configure_client(cls, hostname, port):
        return httplib.HTTPConnection(hostname, port, timeout=5)

    @classmethod
    def wait_for_boot(cls, client):
        retry_count = 0
        while True:
            try:
                client.request("GET", "/booted")
                client.getresponse()
            except (httplib.CannotSendRequest, socket_error):
                time.sleep(0.1)
                retry_count = retry_count + 1
                if retry_count < 100:  # 10 seconds
                    continue
            break

    @classmethod
    def redirect_app_logs(cls, filepath):
        log_names = ['werkzeug']
        app_logs = map(lambda logname: logging.getLogger(logname), log_names)
        file_handler = logging.FileHandler('log/app.test.log', 'w+')

        for app_log in app_logs:
            for hdlr in app_log.handlers[:]:  # remove all old handlers
                app_log.removeHandler(hdlr)

            app_log.addHandler(file_handler)

    @classmethod
    def setUpClass(cls):
        cls.client = cls.configure_client("localhost", 9151)
        cls.server = cls.configure_server_in_thread("localhost", 9151)
        cls.wait_for_boot(cls.client)
        cls.redirect_app_logs("log/app.test.log")

    @classmethod
    def tearDownClass(cls):
        try:
            cls.client.request("GET", "/shutdown")
        except httplib.CannotSendRequest:
            print FAIL + "Error shutting down" + ENDC

        cls.server.join(1)
        if cls.server.is_alive():
            print FAIL + "Unable to gracefully shutdown server"
            print "Resources may not have been released" + ENDC

    def setUp(self):
        self.driver = webdriver.PhantomJS(service_log_path='log/ghostdriver.log')
        self.driver.set_window_size("1120", "550")

    def tearDown(self):
        self.driver.quit()

    def get(self, url):
        request = 'http://localhost:9151' + url
        self.driver.get(request)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "test-done")))
            result = self.driver.find_element(By.TAG_NAME, 'body').text
            return result
        except Exception as e:
            # logs = self.driver.get_log("har")
            # logs = self.driver.get_log("browser")
            # screenshot_loc = "log/%f.png" % time.time()
            # print('error ocured while using selenium, see ' + screenshot_loc)
            # self.driver.save_screenshot(screenshot_loc)
            print(e)
            print("**** App Logs ****")
            f = open("log/app.test.log", "r")
            print(f.read())
            f.close
            print("******************")
            print("*** Phantom JS ***")
            f = open("log/ghostdriver.log", "r")
            print(f.read())
            f.close
            print("******************")
            raise e

    def test_file_comment(self):
        self.assertIn("file-comment", self.get("/#/files/example/types.proto"))

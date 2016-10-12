import unittest
import os

import time
from pilgrim3.app import app
from threading import Thread
import httplib
from flask import request
import logging

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
        while True:
            try:
                client.request("GET", "/booted")
                client.getresponse()
            except httplib.CannotSendRequest:
                time.sleep(0.1)
                continue
            break

    @classmethod
    def redirect_app_logs(cls, filepath):
        log_names = ['werkzeug']
        app_logs = map(lambda logname: logging.getLogger(logname), log_names)
        file_handler = logging.FileHandler('log/app.test.log', 'w')

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

        cls.server.join(5)
        if cls.server.is_alive():
            print FAIL + "Unable to gracefully shutdown server"
            print "Resources may not have been released" + ENDC

    def get(self, url):
        self.__class__.client.request("GET", url)
        return self.__class__.client.getresponse().read()

    def test_message(self):
        self.get("/booted")

    def test_another(self):
        self.assertTrue(1);

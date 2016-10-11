import unittest
import os

import time
from pilgrim3.app import app
from threading import Thread
import httplib
from flask import request

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
    return "done"

class CommentTestCase(unittest.TestCase):
    def __init__(self, message):
        self.server = None
        unittest.TestCase.__init__(self, message)


    def setUp(self):
        # for now compile this by running test/support/proto3/compile
        app.config['proto-bundle'] = os.path.abspath("test/support/build/types.build")
        self.server = Thread(target=lambda: app.run(host="localhost", port=9151, threaded=True))
        self.server.daemon = True
        self.server.start()
        time.sleep(1)  # todo replace with bootstrap class which curls status URL

    def tearDown(self):
        conn = httplib.HTTPConnection("localhost", 9151)
        conn.request("GET", "/shutdown")

        self.server.join(5)
        if self.server.is_alive():
            print FAIL + "Unable to gracefully shutdown server"
            print "Resources may not have been released" + ENDC

    def test_message(self):
        self.assertTrue(True)

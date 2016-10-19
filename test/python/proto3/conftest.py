from flask import request
from pilgrim3.app import app as pilgrim_app
from pytest import fixture
from socket import error as socket_error
from threading import Thread
import httplib
import os
import time

@fixture(scope="module")
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

    pilgrim_app.config['proto-bundle'] = os.path.abspath("test/support/build/types-proto3.build")
    yield pilgrim_app


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

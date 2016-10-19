from pytest import fixture
from socket import error as socket_error
from threading import Thread
import httplib
import os
import time


@fixture(scope="module")
def app(app_with_shutdown_endpoints):
    app_with_shutdown_endpoints.config['proto-bundle'] = os.path.abspath("test/support/build/types-proto2.build")
    yield app_with_shutdown_endpoints


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

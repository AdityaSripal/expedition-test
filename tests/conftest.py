import pytest
import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

import et
import et.gui
import et.server
import et.logs

@pytest.fixture(scope="class")
def client(request):
    control = et.get_control(hostname, web_user, web_pass, ssh_user, ssh_pass)
    control.gui.initialize()
    control.logs.initialize()
    control.server.initialize()
    yield control
    control.gui.finalize()
    control.server.finalize()
    control.logs.finalize()

@pytest.fixture(scope="class")
def backend(request):
    control = et.get_control(hostname, web_user, web_pass, ssh_user, ssh_pass)
    control.logs.initialize()
    control.server.initialize()
    yield control
    control.server.finalize()
    control.logs.finalize()

@pytest.fixture(scope='class')
def gui(request):
    gui = et.gui.UINavigator(hostname, web_user, web_pass)
    gui.initialize()
    yield gui
    gui.finalize()

@pytest.fixture(scope='class')
def server(request):
    server = et.server.ServerConnection(hostname, web_user, web_pass)
    server.initialize()
    yield server
    server.finalize()

@pytest.fixture(scope='class')
def logs(request):
    logs = et.logs.LogCollector(hostname, ssh_user, ssh_pass)
    logs.initialize()
    yield logs
    logs.finalize()

def init():
    """
    Environment Variables:
        HOSTNAME
        WEB_USER
        WEB_PASS
        SSH_USER
        SSH_PASS
    """
    global hostname
    global web_user
    global web_pass
    global ssh_user
    global ssh_pass
    try:
        hostname = os.environ["HOSTNAME"]
        web_user = os.environ["WEB_USER"]
        web_pass = os.environ["WEB_PASS"]
        ssh_user = os.environ["SSH_USER"]
        ssh_pass = os.environ["SSH_PASS"]
    except KeyError as e:
        raise Exception('Missing Environment variable: "{0}"'.format(e))

init()

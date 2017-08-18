import pytest
import os

from . import gui
from . import server
from . import logs

def get_control(ip, web_user, web_pass, ssh_user, ssh_pass):
    return Controller(ip, web_user, web_pass, ssh_user, ssh_pass)

class Controller:
    def __init__(self, ip, web_user, web_pass, ssh_user, ssh_pass):
        self.gui = gui.UINavigator(ip, web_user, web_pass)
        self.logs = logs.LogCollector(ip, ssh_user, ssh_pass)
        self.server = server.ServerConnection(ip, web_user, web_pass)

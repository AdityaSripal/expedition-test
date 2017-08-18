import et
import pytest
import time

class TestMultiUser():
    def test_two_users(self, gui, server):
        gui.navigate.tab('DEVICES')
        gui.device.add_device('first', 'vm-series', '1.2.3.4', '99')
        server.remove_device('99')
        gui.navigate.tab('DEVICES')
        assert '99' not in gui.device.device_dictionary()
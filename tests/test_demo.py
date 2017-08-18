import pytest
import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

import et

class TestDevice():
    def test_add(self, client):
        client.gui.navigate.tab("DEVICES")
        client.gui.device.add_device("CiscoACI", "pa3000", "10.5.172.25", '001801028983')
        client.server.add_device('dummy', 'vm-series', '1.2.3.4', '7')
        client.gui.navigate.tab("DEVICES")
        devices = client.gui.device.device_dictionary()
        assert "7" in devices
        devs = client.server.devices
        for dev in devs:
            if dev['devicename'] == 'CiscoACI':
                return
        assert False
    
    def test_edit(self, client):
        client.gui.device.gen_apikey('001801028983')
        window = client.gui.device.edit_device('001801028983')
        key_table = client.gui.navigate.bridge('devices_keys_grid')
        keys = client.gui.device.row_iterator(key_table, key_type='Role')
        assert 'admin' in keys
        print(keys)
        buttons = client.gui.navigate.element_dictionary('x-btn', driver=window)
        print(buttons)
        for btn in buttons:
            if 'Close' in btn:
                client.gui.navigate.bridge(buttons[btn]).click()
        client.gui.device.retrieve_contents('001801028983', 'Running Configuration')

    def test_remove(self, client):
        client.server.remove_device('7')
        client.gui.navigate.tab('DEVICES')
        devices = client.gui.device.device_dictionary()
        assert '7' not in devices

class TestProject():
    def test_add(self, client):
        client.gui.navigate.tab('PROJECTS')
        client.gui.project.add_project('daemon', contents='CiscoACI')
        client.gui.refresh()
        client.gui.navigate.tab('PROJECTS')
        assert 'daemon' in client.gui.project.project_dictionary()

    def test_enter(self, client):
        client.gui.project.enter_project('daemon')

    def test_import(self, client):
        project_tabs = client.gui.navigate.bridge('ProjectOptionsTabBar')
        client.gui.navigate.tab('IMPORT', project_tabs)
        import_tabs = client.gui.navigate.bridge('ImportPANTabBar')
        client.gui.navigate.tab('SNIPPETS', import_tabs)
        snippets = client.gui.project.snippet_dictionary()
        snippets['icmp_source_quench'].click()
        snip_bar = client.gui.navigate.bridge('ImportSnippetsBar')
        client.gui.click('green-button', uid_type='CLASS_NAME', driver=snip_bar)

    def test_remove(self, client):
        client.gui.refresh()
        client.gui.navigate.tab('PROJECTS')
        client.gui.project.remove_project('daemon')
        assert 'daemon' not in client.gui.project.project_dictionary()

class TestCleanup():
    def test_cleaned(self, client):
        client.server.remove_device('CiscoACI')
        client.gui.refresh()
        client.gui.navigate.tab('DEVICES')
        assert 'CiscoACI' not in client.gui.device.device_dictionary()

    

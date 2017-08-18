import pytest
import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

import et

class TestDevice():
    def test_add(self, gui):
        gui.navigate.tab("DEVICES")
        gui.device.add_device("refactor", "vm-series", "10.5.174.105", '56')
        gui.navigate.tab("DEVICES")
        devices = gui.device.device_dictionary()
        assert "56" in devices

    def test_remove(self, gui):
        gui.device.remove_device('56')
        gui.navigate.tab('DEVICES')
        devices = gui.device.device_dictionary()
        assert '56' not in devices

class TestProject():
    def test_enter(self, gui):
        gui.navigate.tab("PROJECTS")
        projects = gui.project.project_dictionary()
        gui.double_click(projects['TestQA'])

    def test_import(self, gui):
        gui.navigate.tab('IMPORT')
        import_tabs = gui.navigate.bridge('ImportPANTabBar')
        gui.navigate.tab('SNIPPETS', import_tabs)        
        snippets = gui.project.snippet_dictionary()
        snippets['icmp_source_quench'].click()
        snip_bar = gui.navigate.bridge("ImportSnippetsBar")
        gui.click("green-button", uid_type="CLASS_NAME", driver=snip_bar)

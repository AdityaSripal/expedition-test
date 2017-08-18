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

    def test_edit(self, gui):
        gui.device.gen_apikey('001801028983')
        window = gui.device.edit_device('001801028983')
        key_table = gui.navigate.bridge('devices_keys_grid')
        keys = gui.navigate.row_dictionary(key_table, key_type='Role')
        assert 'admin' in keys
        buttons = gui.navigate.element_dictionary('x-btn', driver=window)
        for btn in buttons:
            if 'Close' in btn:
                buttons[btn].click()
        gui.device.retrieve_contents('001801028983', 'Running Configuration')
        window = gui.device.edit_device('001801028983')
        gui.navigate.tab('CONTENTS', window)
        table = gui.navigate.bridge('files_grid', driver=window)
        rows = gui.navigate.row_dictionary(table, key_type='Filename', driver=window)
        assert len(rows) > 1

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
  
class TestPractice():
    def test_enter(self, gui):
        gui.navigate.tab("PROJECTS")
        projects = gui.project.project_dictionary()
        gui.double_click(projects["TestQA"])

    def test_bp(self, gui):
        gui.navigate.tab("BEST PRACTICES")
        bp_tab_bar = gui.navigate.bridge('BestPracticesTabBar')
        dev_setup = gui.navigate.tab('Analysis', driver=bp_tab_bar)
        bp_dict = gui.project.bp_topic_iterator()
        bp_dict['Authentication Settings'].click()
        bp_table = gui.navigate.bridge('bpatBPchecks')
        bp_rows = gui.navigate.row_dictionary(bp_table)
        bp_rows['Idle Timeout'].click()
        btn_dictionary = gui.navigate.element_dictionary('green-button')
        list(btn_dictionary.values())[0].click()
        rem_window = gui.navigate.bridge('RemediateRulesWindow')
        window_btn = gui.navigate.bridge('green-button', uid_type='CLASS_NAME', driver=rem_window)
        window_btn.click()

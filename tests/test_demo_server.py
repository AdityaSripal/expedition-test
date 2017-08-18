import pytest
import os
import sys
import json
import time

import et

class TestDevice():
    def test_add(self, server):
        prev_total = server.device_total
        res = server.add_device("TestAdd", "vm-series", "10.5.174.110", "72")
        assert res['success']
        curr_total = server.device_total
        assert curr_total - prev_total == 1
        for dev in server.devices:
            if dev['devicename'] == 'TestAdd':
                return
        raise Exception("Device not added correctly")

    def test_edit(self, server):
        res1 = server.gen_api_key('001801028983', 'admin')
        assert res1['success']
        keys = server.get_keys('001801028983')
        assert keys['total'] == 1
        res2 = server.configuration('001801028983', 'running')
        assert res2['success']
        time.sleep(10)
        res3 = server.dev_contents('001801028983')
        assert res3['state'] == 'completed'
        assert res3['contents'] != {}

    def test_remove(self, server):
        prev_total = server.device_total
        res = server.remove_device("72")
        assert res["success"]
        curr_total = server.device_total
        assert prev_total - curr_total == 1
        for dev in server.devices:
            if dev["devicename"] == "TestAdd":
                raise Exception("Device not deleted!")

class TestProjects():
    def test_add(self, server):
        prev_total = server.project_total
        res = server.add_project("hello", "Migration")
        assert res['success']
        assert server.project_total - prev_total == 1
        for proj in server.projects:
            if proj['name'] == "hello":
                return
        raise Exception("hello project not added!")

    def test_remove(self, server):
        prev_total = server.project_total
        res = server.remove_project("hello")
        assert res['success']
        assert prev_total - server.project_total == 1
        for proj in server.projects:
            if proj['name'] == "hello":
                raise Exception("hello project not deleted!")
                
class TestSnippets():
    def test_add(self, server):
        res = server.add_snippet('TestQA', 'Logs2Panorama', 'Main Group')
        assert res['success']

class TestBestPractices():
    def test_remediate(self, server):
        res = server.remediate('TestQA', 'device_setup', 'device/setup/management/panorama_settings', 'Certificate Type', cat_mode='device')
        assert res['success']
        confirm = server.device_setup('TestQA')
        assert confirm['bpchecks'] == []

    

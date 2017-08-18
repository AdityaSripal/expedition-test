import pytest
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from collections import OrderedDict

class DeviceNavigator():
    def __init__(self, parent):
        self.parent = parent

    def device_table(self):
        return self.parent.navigate.bridge("DevicesGrid-body")

    def device_dictionary(self):
        """Returns a dictionary where the keys are serial # of device and value is ID of row"""
        return self.parent.navigate.row_dictionary(self.device_table(), key_type="Serial #")

    def add_device(self, name, model, ip, serial, **kwargs):
        """Provide configuration for the device
        If you wish to override default args use kwargs passed in as a dictionary.
        Refer to fill_fieldset function"""
        table = self.parent.navigate.bridge('DevicesGrid')
        self.parent.click("x-tool-plus", uid_type="CLASS_NAME", driver=table)
        config = {
            'Device Name:': name,
            'Model:': model,
            'Hostname/IP:': ip,
            'Serial #:': serial
        }
        config.update(kwargs)
        form = self.parent.navigate.bridge('DeviceForm-body')
        self.parent.fill_fieldset(config, form)
        window = self.parent.navigate.bridge('DeviceWindow')
        self.parent.click('device_update_button', driver=window)

    def remove_device(self, serial):
        row = self.device_dictionary()[serial]
        self.parent.click('fa-times', uid_type="CLASS_NAME", driver=row)
        confirm = self.parent.navigate.bridge('x-message-box', uid_type="CLASS_NAME")
        self.parent.text_choices("Yes", driver=confirm)

    def edit_device(self, serial):
        """edit_device(serial) returns the edit window element for further use in the script"""
        row = self.device_dictionary()[serial]
        self.parent.click('x-action-col-0', uid_type="CLASS_NAME", driver=row)
        return self.parent.navigate.bridge('DeviceWindow')

    def retrieve_contents(self, serial, configtype):
        """Retrieves contents from device.
        Non-blocking: you should wait before assuming all contents have been downloaded"""
        window = self.edit_device(serial)
        self.parent.navigate.tab('CONTENTS', driver=window)
        self.parent.click('retrieve_owner_button', driver=window)
        configs = self.parent.navigate.element_dictionary('x-menu-item-text')
        configs[configtype].click()
        self.parent.click('device_update_button', driver=window)

    def gen_apikey(self, serial, **kwargs):
        """Generates API key using username and password and closes window"""
        auth = {
            'Username': self.parent.user,
            'Password': self.parent.password
        }
        auth.update(kwargs)
        window = self.edit_device(serial)
        self.parent.navigate.bridge("fieldset", uid_type="TAG_NAME", driver=window)
        self.parent.click("x-tool-plus", uid_type="CLASS_NAME", driver=window)
        forms = window.find_elements_by_tag_name('fieldset')
        key_form = forms[1]
        self.parent.fill_fieldset(auth, key_form)
        self.parent.click("blue-button", uid_type="CLASS_NAME", driver=window)
        self.parent.click('device_update_button', driver=window)
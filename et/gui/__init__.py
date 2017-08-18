import pytest
import re
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import et.gui.navigate
import et.gui.expect
import et.gui.device
import et.gui.project

from collections import OrderedDict

class UINavigator:
    attributes = {"ID": By.ID, "TAG_NAME": By.TAG_NAME, "NAME": By.NAME, "CLASS_NAME": By.CLASS_NAME, "XPATH": By.XPATH}
    special_keys = {"RETURN": Keys.RETURN, "NULL": Keys.NULL, "TAB": Keys.TAB}

    def __init__(self, ip, user, passwd):
        self.ip = ip
        self.user = user
        self.password = passwd
        self.driver = None
        self.navigate = navigate.Navigator(self)
        self.expect = expect.Expector(self)
        self.device = device.DeviceNavigator(self)
        self.project = project.ProjectNavigator(self)

    def initialize(self):
        self.url("https://{0}".format(self.ip))
        self.login()

    def url(self, link):
        options = webdriver.ChromeOptions()
        """options.add_argument('--ignore-certificate-errors')
        options.add_argument('headless')"""
        #driver = webdriver.Chrome(chrome_options=options)
        driver = webdriver.Chrome()
        driver.set_window_size(1600, 1000)
        driver.get(link)
        driver.get(driver.current_url)
        self.driver = driver

    def finalize(self):
        if self.driver is not None:
            self.driver.quit()

    def input(self, uid, content, driver=None, uid_type="ID", key=None):
        """Provide a unique identifier and content to be sent
        Currently you can only send one key at the end of content
        Currently supported keys: RETURN, NULL, TAB"""
        if driver is None:
            driver = self.driver
        field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((self.attributes[uid_type], uid)))
        field.clear()
        field.send_keys(content)
        if key is not None:
            field.send_keys(self.special_keys[key])

    def click(self, uid, uid_type="ID", driver=None):
        """Wrapper for the driver.click method. Equivalent calls:
        elem.click()
        self.click(elem['id'], elem)
        self.click(elem['class_name'], 'CLASS_NAME', elem)
        etc."""
        if driver is None:
            driver = self.driver
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((self.attributes[uid_type], uid)))
        button.click()

    def double_click(self, elem):
        """To double-click you must pass in the element itself
        Currently only works on Chrome Webdriver"""
        actionChains = ActionChains(self.driver)
        actionChains.double_click(elem).perform()

    def drag_and_drop(self, source, target):
        """Driver must contain both source and target element
        Source is element to be dragged
        Target is element where source is dropped
        Currently only works on Firefox Webdriver"""
        actionChains = ActionChains(self.driver)
        actionChains.drag_and_drop(source, target).perform()
        time.sleep(3)

    def find_by_text(self, text, driver=None):
        """Do not use"""
        if driver is None:
            driver = self.driver
        regexp = "//*[contains(text(), {0})]".format(re.escape(text))
        elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), {0})]".format(re.escape(text)))))
        return elem

    def multi_click(self, *chain):
        """Takes in arguments of type string or a two-element tuple
        If arg is string it is interpreted to be an ID and corresponding element will be clicked.
        If tuple, first element is driver to be used as bridge and second is class_name of element to be clicked."""
        for action in chain:
            if type(action) != str:
                driver, uid = action
                self.click(uid, uid_type='CLASS_NAME', driver=driver)
            else:
                self.click(uid)

    def multi_input(self, inputs):
        """Takes dictionary with key being ID of element and value being content to be inputted into form element"""
        for uid, content in inputs.items():
            self.input(uid, content)

    def refresh(self):
        """With expedition, refresh brings you back to main dashboard
        Use to 'reset' UI or force UI to update with new info"""
        self.driver.get(self.driver.current_url)

    def login(self):
        self.input("user_name_login-inputEl", "admin")
        self.input("user_password_login-inputEl", "paloalto")
        div = self.navigate.bridge("LoginForm-innerCt")
        self.click("submit_login", driver=div)

    def logout(self):
        self.refresh()
        self.click("username_button")

    def pop_up(self):
        return self.driver.switch_to_alert()

    def fill_fieldset(self, inputs, driver=None):
        """Takes in a driver and an input dictionary with keys being the text before input and value being the input value.
        Driver must be the div containing the fieldset
        Example: In Add Device Form there is field like--
        Device Name: ________
        Hostname/IP: ________
        inputs = {"Device Name:": "DevName", "Hostname/IP.": "10.5.174.104"}"""
        if driver is None:
            driver = self.driver
        self.navigate.bridge("x-form-item-label", uid_type="CLASS_NAME", driver=driver)
        self.navigate.bridge("x-form-item-body", uid_type="CLASS_NAME", driver=driver)
        fields = self.navigate.element_dictionary("x-field", driver=driver)
        for key, field in fields.items():
            if key in inputs:
                input = self.navigate.bridge("input", uid_type="TAG_NAME", driver=field)
                input.send_keys(inputs[key])
    
    def text_choices(self, choice, driver=None):
        """Do not use with the web driver. It is recommended that you narrow the driver with the bridge function and then pass it in.
        Example use cases: confirmation boxes. To be used when there are a limited range of text choices to be clicked."""
        if driver is None:
            driver = self.driver
        choices = self.navigate.element_dictionary("x-btn", driver=driver)
        choices[choice].click()

    #TODO: Create bp_iterator method that does custom handling of bp_table so that bp key includes category

    def _parse_num(self, uid):
        """Pulls dynamic id number from id attribute. Useful when multiple elements share the same dynamic ID number"""
        return ''.join(list(filter(str.isdigit, uid)))

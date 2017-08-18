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

class Expector():
    def __init__(self, parent):
        self.parent = parent

    def expect_url(self, url):
        """Checks if URL is as expected"""
        assert self.parent.driver.current_url == url

    def expect_element(self, uid, uid_type="ID", driver=None, text=None):
        """Checks if specified element is attached to DOM"""
        if driver is None:
            driver = self.parent.driver
        element = self.parent.navigate.bridge(uid, uid_type=uid_type)
        if text:
            assert element.text == text

    def expect_popup(self):
        """Checks if you get browser alert"""
        WebDriverWait(self.parent.driver, 10).until(EC.alert_is_present())
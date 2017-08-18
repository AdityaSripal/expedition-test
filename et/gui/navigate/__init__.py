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
from functools import reduce

class Navigator():
    """Contains all the navigation methods used in GUI testing"""
    def __init__(self, parent):
        self.parent = parent

    def bridge(self, uid, uid_type="ID", driver=None):
        """Returns element denoted by uid
        If non-unique, returns first element attached to page
        Used to narrow search for other methods"""
        if driver is None:
            driver = self.parent.driver
        return WebDriverWait(driver, 10).until(EC.presence_of_element_located((self.parent.attributes[uid_type], uid)))

    def tab(self, name, driver=None):
        """Pass in text in tab. Optional driver argument to narrow tabs to single tab_bar"""
        if driver is None:
            driver = self.parent.driver
        tabs = self.element_dictionary("x-tab-inner", driver=driver)
        tabs[name].click()

    def id_dictionary(self, uid, uid_type='CLASS_NAME', driver=None):
        """Finds multiple elements with the same uid.
        Returns dictionary with key corresponding to text in element and value is ID of element"""
        if driver is None:
            driver = self.parent.driver
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((self.parent.attributes[uid_type], uid)))
        elems = driver.find_elements_by_class_name(uid)
        id_dict = OrderedDict()
        for el in elems:
            id_dict[self._scrub_string(el.text)] = el.get_attribute("id")
        if '' in id_dict:
            del id_dict['']
        return id_dict

    def element_dictionary(self, uid, uid_type="CLASS_NAME", driver=None):
        """Finds multiple elements with the same uid.
        Returns dictionary with key corresponding to text in element and value is ID of element"""
        if driver is None:
            driver = self.parent.driver
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((self.parent.attributes[uid_type], uid)))
        elems = driver.find_elements_by_class_name(uid)
        elem_dict = OrderedDict()
        for el in elems:
            elem_dict[self._scrub_string(el.text)] = el
        if '' in elem_dict:
            del elem_dict['']
        return elem_dict

    def row_dictionary(self, table, key_type="Name", driver=None):
        """Provide the selenium element that contains the table.
        Table should have columns with labels
        Recommended to use the element that contains x-grid class.
        Returns a dictionary with keys being the value in the column specified by key_type
        (default key_type is Name column)
        Value of dictionary is row element
        Default behavior: Returns dictionary with [Name Entry]: [Row ID] key-value pairs
        """
        if driver is None:
            driver = self.parent.driver
        header = self.bridge("x-grid-header-ct", uid_type="CLASS_NAME")
        col_dict = self.id_dictionary("x-column-header", uid_type="CLASS_NAME", driver=driver)
        self.bridge("x-grid-item", uid_type="CLASS_NAME")
        rows = self.id_dictionary("x-grid-item", driver=table)
        dyn_id = self.parent._parse_num(col_dict[key_type])
        iterator = OrderedDict()
        for string, id in rows.items():
            outer_row = self.bridge(id, driver=table)
            inner_row = self.bridge("x-grid-row", uid_type="CLASS_NAME", driver=outer_row)
            key = self.bridge("x-grid-cell-gridcolumn-{0}".format(dyn_id), uid_type="CLASS_NAME", driver=inner_row).text
            iterator[self._scrub_string(key)] = inner_row
        return iterator

    def _scrub_string(self, text):
        lines = text.splitlines()
        words = [line.split(' ') for line in lines]
        words = sum(words, [])
        if words == []:
            return ''
        if len(words[0]) != len(words[0].encode()):
            words= words[1:]
        i = 0
        while i < len(words):
            if words[i].startswith('('):
                break
            i += 1
        words = words[:i]
        text = reduce(lambda x, y: x + ' ' + y, words, '').strip()
        return text

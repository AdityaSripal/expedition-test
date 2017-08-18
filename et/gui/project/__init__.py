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

class ProjectNavigator():
    def __init__(self, parent):
        self.parent = parent

    def project_dictionary(self):
        table = self.parent.navigate.bridge("ProjectsGridPanel")
        return self.parent.navigate.row_dictionary(table)

    def add_project(self, name, contents='default', packs='default', description='', purpose='Migration'):
        """Provide name to create project, use named arguments to override defaults"""
        project_grid = self.parent.navigate.bridge('ProjectsGridPanel')
        self.parent.click('x-tool-plus', uid_type='CLASS_NAME', driver=project_grid)
        add_window = self.parent.navigate.bridge('newProjectWindow')
        fields = self.parent.navigate.element_dictionary('x-field')
        self.parent.input('project-inputEl', name, driver=add_window)
        self.parent.input('project_tag-inputEl', description, driver=add_window)
        selects = add_window.find_elements_by_tag_name('fieldset')
        self.parent.input('x-form-field', contents, uid_type='CLASS_NAME', driver=selects[0])
        self.parent.input('x-form-field', packs, uid_type='CLASS_NAME', driver=selects[1])
        button_div = selects[2]
        buttons = self.parent.navigate.element_dictionary('x-btn', driver=button_div)
        buttons[purpose].click()
        self.parent.click('green-button', uid_type="CLASS_NAME", driver=add_window)

    def enter_project(self, name):
        for proj, elem in self.project_dictionary().items():
            if proj == name:
                self.parent.double_click(elem)

    def remove_project(self, name):
        projects = self.project_dictionary()
        for proj, row in projects.items():
            if proj == name:
                self.parent.click('x-action-col-1', uid_type='CLASS_NAME', driver=row)
        buttons = self.parent.navigate.element_dictionary('x-btn-inner')
        buttons['Yes'].click()

    def snippet_category_id_dictionary(self):
        """Iterate through Snippet Categories"""
        snip_table = self.parent.navigate.bridge("ImportSnippets")
        self.parent.navigate.bridge("x-group-hd-container", uid_type="CLASS_NAME", driver=snip_table)
        return self.parent.navigate.id_dictionary("x-grid-item", driver=snip_table)
        
    def snippet_dictionary(self):
        """Iterate through all snippets"""
        categories = self.snippet_category_id_dictionary()
        for n, id in categories.items():
            WebDriverWait(self.parent.driver, 10).until(EC.presence_of_element_located((By.ID, id))).click()
        table = self.parent.navigate.bridge("ImportSnippets")
        snip_dict = self.parent.navigate.row_dictionary(table)
        for cat in categories:
            if cat in snip_dict:
                del snip_dict[cat]
        return snip_dict

    def bp_topic_iterator(self):
        bp_cat_table = self.parent.navigate.bridge('x-tree-lines', uid_type='CLASS_NAME')
        container = self.parent.navigate.bridge('x-grid-item-container', uid_type='CLASS_NAME', driver=bp_cat_table)
        col_dict = self.parent.navigate.id_dictionary('x-column-header')
        dyn_id = self.parent._parse_num(col_dict['Topics'])
        expandables = self.parent.navigate.id_dictionary('x-grid-item', driver=container)
        for exp, id in expandables.items():
            elem = self.parent.navigate.bridge(id, driver=container)
            self.parent.double_click(elem)
        rows = self.parent.navigate.id_dictionary('x-grid-item', driver=container)
        for topic in expandables:
            if topic in rows:
                del rows[topic]
        iterator = OrderedDict()
        for key, val in rows.items():
            outer_row = self.parent.navigate.bridge(val, driver=container)
            inner_row = self.parent.navigate.bridge('x-grid-row', uid_type='CLASS_NAME', driver=outer_row)
            cell = self.parent.navigate.bridge('x-grid-cell-treecolumn-{0}'.format(dyn_id), uid_type='CLASS_NAME', driver=inner_row)
            new_key = self.parent.navigate.bridge('x-tree-node-text', uid_type='CLASS_NAME', driver=cell).text
            iterator[new_key.strip().split('\n')[0]] = inner_row
        return iterator

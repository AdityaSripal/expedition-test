import et
import pytest
import time

class TestEdit():
    def test_edit_project(self, gui):
        gui.navigate.tab('PROJECTS')
        project_dict = gui.project.project_dictionary()
        gui.click('x-action-col-0', uid_type='CLASS_NAME', driver=project_dict['TestQA'])
        edit_window = gui.navigate.bridge('ProjectEditWindow')
        gui.navigate.tab('DEVICES', driver=edit_window)
        available_grid = gui.navigate.bridge('AvailableGrid')
        available_dict = gui.navigate.element_dictionary('x-grid-cell-treecolumn', driver=available_grid)
        allowed_grid = gui.navigate.bridge('AllowedGrid')
        allowed_dict = gui.navigate.element_dictionary('x-grid-cell-treecolumn', driver=allowed_grid)
        gui.drag_and_drop(available_dict['ipython'], allowed_dict['Allowed Devices'])
        #refreshed_window = gui.navigate.bridge('ProjectEditWindow')
        time.sleep(2)
        green_btns = gui.navigate.element_dictionary('green-button', driver=edit_window)
        green_btns['Save'].click()
    
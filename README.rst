==================================
Palo Alto Networks Expedition Test
==================================

Most of the documentation for Expedition-Test is housed in the ipython notebooks. The following is necessary information about pytest and miscellaneous information about ET that may prove useful.

Create the test files in the tests directory and import the same modules that are imported in the example files. Make sure that the test file starts with test_*
Test Classes start with Test*
and test methods start with test_*

To run the tests you may enter these commands in a terminal:

1) pytest tests (runs all test files in tests directory)

2) pytest tests/individual_test_file

3) python3 setup.py test (runs all test files in test directory)


Any print statements will only be released to STDOUT if print statement was executed in a failed test case

pytest -v ==> Verbose

pytest -s ==> Releases to STDOUT as print statements are executed


Pytest Fixtures: client, gui, server, logs

Passing in a fixture as a function argument allows for its use within function body

client - allows for use of all ET namespaces
client.gui, client.server, client.logs

gui - allows for use of gui namespace
server - use of server namespace
logs - use of logs namespace


Note: All dictionaries from the gui namespace are ORDERED DICTIONARIES. Thus, iterating through the dictionary is the same as iterating through the UI in order.


Steps to run ipython notebook on your own:

1) Install Jupyter Notebook seperately or through the Anaconda distribution.

2) pip install ipykernel (inside virtual-env for Expedition)

3) python -m ipykernel install --user --name={expedition-virtual-env}

4) Run ipython notebook. Kernel -> Change Kernel -> {expedition-virtual-env}


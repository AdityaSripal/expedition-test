import time
import urllib

import requests

# Disable the SSL cert warnings
requests.packages.urllib3.disable_warnings()

class ServerConnection(object):
    def __init__(self, hostname, username, password, verify=False):
        """Initializes a new server connection.

        Args:
            hostname (str): hostname
            username (str): username
            password (str): password
            verify (bool): Verify the SSL cert or not

        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.verify = verify

        self.con = None

    def initialize(self):
        """Initialize this connection type for use."""
        self.con = requests.Session()
        self.login(self.username, self.password)

    def finalize(self):
        """Close the connection"""
        self.con.close()

    # PROPERTIES

    @property
    def _dc(self):
        """Returns time.time() as an int for the _dc param in query strings."""
        return int(time.time() * 1000)

    @property
    def device_total(self):
        return self.get_devices()['total']

    @property
    def devices(self):
        """Returns a list of devices, where each device entry is a dictionary of device attributes"""
        return self.get_devices()['devices']

    @property
    def project_total(self):
        return self.get_projects()['total']

    @property
    def projects(self):
        """Returns list of current projects, where each project entry is a dictionary of project attributes"""
        return self.get_projects()['projects']

    @property
    def pack_total(self):
        return self.get_packs()['total']

    @property
    def packs(self):
        return self.get_packs()['packs']

    @property
    def snippet_total(self):
        return self.get_snippets()['total']

    @property
    def snippets(self):
        return self.get_snippets()['snippets']

    @property
    def user_total(self):
        return self.get_users()['total']

    @property
    def users(self):
        return self.get_users()['users']

    # GENERAL SERVER-SIDE METHODS

    def login(self, username=None, password=None):
        """Perform a login.

        Specifying the username or password will override that auth parameter
        that's stored in this class.

        Args:
            username (str): username
            password (str): password

        Returns:
            bool. True if logged in ok, else False.

        """
        url = 'https://{0}/bin/Auth.php'.format(self.hostname)
        data = {
            'action': 'get',
            'type': 'login_users',
            'password': password or self.password,
            'user': username or self.username,
        }

        ans = self.con.post(url, data=data, verify=self.verify).json()
        return ans['success']

    def get_list(self, path, **kwargs):
        """Provide the path name for the file excluding the .php file extension.
           Optional keyword arguments allow you to pass in more request params than the
           ones provided. Returns the JSON response. Use when response is list-like.
           Example:
           URL request to get devices: https://10.5.172.196/bin/authentication/devices/devices.php?_dc=1500405060327&scope=direct&page=1&start=0&limit=25
           Function call: get_list("/bin/authentication/devices/devices", scope='direct')
        """
        url = "https://{0}/{1}.php"
        params = {
            '_dc': self._dc,
            'page': 1,
            'start': 0,
            'limit': 200,
        }
        params.update(kwargs)
        url = url.format(self.hostname, path)

        return self.con.get(url, params=params, verify=self.verify).json()

    def get(self, path, params):
        url = 'https://{0}/{1}.php'.format(self.hostname, path)
        return self.con.get(url, params=params, verify=self.verify).json()

    def post(self, path, data, params=None, flag=False):
        """Convenience method that makes it easier to write custom post test methods
        path is path to PHP file, exclude .php extension in argument
        Data is a dictionary containing form data to be posted.
        Params is optional dictionary containing URL params
        Returns JSON response
        Example:
        post('www.example.com', {'arg1': 1, 'arg2': 2}, params= {'_dc': 33, 'scope': 'direct'})"""

        url = "https://{0}/{1}.php"
        url = url.format(self.hostname, path)
        if params:
            url = url + '?' + urllib.parse.urlencode(params)
        if flag:
            return self.con.post(url, data=data, verify=self.verify).json()
        return self.con.post(url, json=data, verify=self.verify).json()

    def delete(self, path, params=None, data=None, **kwargs):
        url = 'https://{0}/{1}.php'.format(self.hostname, path)
        if params:
            url = url + '?' + urllib.parse.urlencode(params)
        opts = {}
        if data is not None:
            opts.update(data)
        opts.update(kwargs)
        return self.con.delete(url, **opts).json()

    def put(self, path, data, params=None, flag=False, **kwargs):
        url = 'https://{0}/{1}.php'.format(self.hostname, path)
        if params:
            url = url + '?' + urllib.parse.urlencode(params)
        if flag:
            return self.con.put(path, json=data, **kwargs)
        return self.con.put(path, data=data, **kwargs).json()

    # METHODS FOR SPECIFIC REST CALLS

    def get_devices(self):
        """Returns the JSON response from calling the devices.php file.
        Contains both the total and devices property in a dictionary"""
        return self.get_list("bin/authentication/devices/devices", scope='direct')

    def cpu_status(self):
        """Gets CPU / RAM / DISK info."""
        return self.get_list("libs/cpu_status")

    def jobs(self):
        """Gets the list of jobs."""
        return self.get_list("bin/jobs/listJobs", mode='pending')

    def get_snippets(self):
        return self.get_list("bin/Snippets")

    def statistics(self, project, mode, node=''):
        """Example Usage:
        statistics('TestQA', 'percentage')
        statistics('TestQA', 'heatmap', node='root')
        """
        params = {
            'project': project,
            'mode': mode,
            'node': node
        }
        return self.get_list("bin/projects/bpat/statistics", **params)

    def check(self):
        return self.get_list("bin/jobs/check", process='readOrders')

    def get_projects(self):
        """Returns JSON response of REST call to retrieve project list.
        Contains project_total and projects property"""
        return self.get_list("bin/authentication/projects/projects")

    def add_device(self, name, model, ip, serial, **kwargs):
        """
        Provide name, model, hostname, and unique serial # to add device.
        Advanced Configuration. To override the default values in config below,
        pass in desired values as keyword arguments.
        Ex: Override port # to port 22
        add_device(self, name, model, ip, serial, port=22)
        """
        url = "https://{0}/bin/authentication/devices/devices.php?{1}"
        config = {
            'active': True,
            'appreleasedate': "0000-00-00 00:00:00",
            'apps': "0",
            'appversion': "0",
            'assigned': False,
            'config': "0",
            'description': "",
            'devicename': name,
            'hostname': ip,
            'id': "MT3.model.Devices-1",
            'ispanorama': "0000-00-00 00:00:00",
            'logtype': "csv",
            'panos': "",
            'port': 443,
            'serial': serial,
            'serialHA': "",
            'threatreleasedate': "0000-00-00 00:00:00",
            'threats': "0",
            'threatversion': "0",
            'type': model,
            'vsys': "vsys1",
        }
        config.update(kwargs)
        params = {
            '_dc': self._dc,
            'scope': 'direct',
        }
        url = url.format(self.hostname, urllib.parse.urlencode(params))
        
        return self.con.post(url, json=config, verify=self.verify).json()

    def remove_device(self, serial):
        """Provide the serial # of device to delete."""
        url = "https://{0}/bin/authentication/devices/devices.php/{1}?{2}"
        params = {
            '_dc': self._dc,
            'scope': 'direct',
        }
        dev_list = self.devices
        for dev in dev_list:
            if dev['serial'] == serial:
                config = dev
                break

        url = url.format(self.hostname, config['id'], urllib.parse.urlencode(params))

        return self.con.delete(url, json=config, verify=False).json()

    def get_packs(self):
        return self.get_list("bin/authentication/bestpractices/packs")

    def add_pack(self, name, description):
        url = "https://{0}/bin/authentication/bestpractices/benchmarks.php"
        data = {'name': name, 'description': description}
        url = url.format(self.hostname)
        return self.con.post(url, data=data, verify=False).json()

    def remove_pack(self, name):
        for pack in self.packs:
            if pack['name'] == name:
                del_pack = pack
                break
        url = "https://{0}/bin/authentication/bestpractices/packs.php/{1}?{2}"
        params = {
            '_dc': self._dc,
        }
        url = url.format(self.hostname, del_pack['id'], urllib.parse.urlencode(params))
        return self.con.delete(url, data=del_pack, verify=False).json()

    def snippet_action(self, action, name, description, snip_type, panos, data, id):
        url = "https://{0}/bin/Snippets.php".format(self.hostname)
        payload = {
            'action': action,
            'name': name,
            'description': description,
            'type': snip_type,
            'panos': panos,
            'data': data,
            'id': id,
        }
        return self.con.post(url, data=payload, verify=False).json()

    def add_snippet(self, project, snippet_name, vsys):
        url = "https://{0}/bin/Snippets.php".format(self.hostname)
        for snip in self.snippets:
            if snip['name'] == snippet_name:
                added = snip
                break
        payload = {
            'action': 'import',
            'project': project,
            'type': 'snippets',
            'vsys': vsys,
            'ids': added['id'],
            'source': 1
        }
        return self.con.post(url, data=payload, verify=False).json()

    def get_users(self):
        return self.get_list("bin/authentication/users/userManagement", type='users')

    def servers(self, server_type):
        """Provide type of server: (serverLDAP or serverRadius)"""
        return self.get_list("bin/authentication/servers/loginServers", **{'type': server_type})

    def add_user(self, email, fname, lname, location, password, role, timezone):
        data = {
            'email': email,
            'first_name': fname,
            'last_name': lname,
            'location': location,
            'password': password,
            'password_confirm': password,
            'role': role,
            'timezone': timezone
        }
        params = {
            '_dc': self._dc,
            'type': 'users'
        }
        return self.post('bin/authentication/users/userManagement', data, params=params)

    def remove_user(self, email):
        url = 'https://{0}/bin/authentication/users/userManagement.php/{1}?{2}'
        for user in self.users:
            if user['email'] == email:
                deleted = user
                break
        
        url = url.format(self.hostname, deleted['id'], urllib.parse.urlencode({'_dc': self._dc, 'type': 'users'}))
        return self.con.delete(url, json=deleted, verify=self.verify).json()

    def add_project(self, name, purpose, **kwargs):
        """Provide a name for the project.
        Advanced Configuration. To override the default values in config below,
        pass in desired values as keyword arguments.
        Ex: Override packs to '3' and tag to Testing
        self.add_project(name, purpose, packs='3', tag='Testing')
        """
        url = "https://{0}/bin/authentication/projects/projects.php?{1}"
        params = {'_dc': self._dc}

        config = {
            'admin': False,
            'date': "",
            'name': name,
            'packs': "1",
            'progress': "",
            'progress_value': 0,
            'purpose': purpose,
            'source': '',
            'tag': "",
            'vendors': ''
        }
        url = url.format(self.hostname, urllib.parse.urlencode(params))
        return self.con.post(url, json=config, verify=False).json()

    def remove_project(self, name):
        """Provide the name of the project to be removed"""
        url = "https://{0}/bin/authentication/projects/projects.php/{1}?{2}"
        params = {'_dc': self._dc}

        for proj in self.projects:
            if proj['name'] == name:
                config = proj
                break

        url = url.format(self.hostname, config['id'], urllib.parse.urlencode(params))
        return self.con.delete(url, json=config, verify=self.verify).json()

    def project_dashboard(self, project, action, dash_type):
        return self.get_list("bin/Dashboard", project=project, action=action, type=dash_type)

    def project_configuration(self, project, action, config_type):
        return self.get_list("bin/Configuration", project=project, action=action, type=config_type)

    def project_filters(self, project, action, mode, node, filter_list=False):
        url = "https://{0}/bin/projects/tools/filters.php?{1}"
        params = {
            '_dc': self._dc,
            'project': project,
            'action': action,
            'mode': mode,
            'node': node,
        }
        if filter_list:
            params.update({'page': 1, 'start': 0, 'limit': 200})
        url = url.format(self.hostname, urllib.parse.urlencode(params))
        return self.con.get(url, verify=False).json()

    def project_attributes(self, path, project, mode, filter_num, **kwargs):
        """Allows you to get attributes of a project such as address groups, service groups, application groups, etc."""
        params = {
            'project': project,
            'mode': mode,
            'objfilter': filter_num,
            'objsearch': "",
            'vsys': "all",
        }
        params.update(kwargs)
        return self.get_list(path, **params)

    def device_usage(self, project):
        data = {
            'dusage_platform': '',
            'dusage_version': '8.0',
            'dusage_vsys': 'all',
            'dusage_source': '1',
            'type': 'get',
            'project': project,
            'action': 'statistics'
        }
        return self.get_list('bin/DeviceUsage', **data)

    def get_rules(self, project, rule_type):
        """Provide the project name and the rule type (e.g. 'SecurityRules' or 'NatRules') and get the rules as JSON response"""
        params = {
            'project': project,
            'vsys': 'all',
            'action': 'get',
            'type': 'rules',
        }
        path = 'bin/{0}'.format(rule_type)
        return self.get_list(path, **params)

    def regions(self, project, mode):
        return self.get_list("bin/projects/discovery/regions", project=project, mode=mode)

    def monitor(self, project):
        """Returns Migration Logs for a given project"""
        params = {
            'project': project,
            'action': 'get',
            'type': 'logs',
            'type_log': 1,
            'log_search_message': '',
            'log_search_action': ''
        }
        return self.get_list('bin/Monitor', **params)

    def cron_job(self, action, cron_type):
        return self.get_list("bin/CronJobs", action=action, type=cron_type)

    def ml_settings(self):
        return self.get_list('bin/authentication/ml_settings/ml_settings')

    def device_setup(self, project, mode=None):
        params = {
            'project': project
        }
        if mode:
            params.update({'mode': mode})
        return self.get_list('bin/projects/bpat/device_setup', **params)

    def remediate_all(self, project, topic, mode):
        """Remediate takes the project name, the topic to be remediated (e.g device_setup) and the mode or template used to remediate.
        Returns JSON response
        """
        data = {
            'project': project,
            'topic': topic,
            'mode': mode
        }
        return self.post('bin/projects/bpat/remediate', data)

    #TODO: RemediateRule REST call

    def remediate(self, project, category, xpath, rule_name, mode='same', cat_mode=None):
        """Similar to remediate() but takes action on single rule. Provide rule name as arguement.
        If mode is a URL param in REST call, supply mode in cat_mode argument"""
        url = "bin/projects/bpat/{0}".format(category)
        params = {
            'project': project,
        }
        if cat_mode:
            params.update({'mode': cat_mode})
        topic_list = self.get_list(url, **params)
        for bp in topic_list['bpchecks']:
            if bp['xpath'] == xpath and bp['name'] == rule_name:
                imported = bp
                break

        data = {
            'project': project,
            'rules': imported['bpcheck_id'],
            'topic': category,
            'mode': mode,
        }

        return self.post('bin/projects/bpat/remediate', data, flag=True)

    def upload(self, vendor, project, device):
        data = {
            'vendor': vendor,
            'project': project,
            'device': device
        }
        return self.post('bin/configurations/parsers/uploader', data)

    def load(self, project, vendor, **kwargs):
        data = {
            'action': 'import',
            'afa_hostname': '',
            'checkpoint_name': '',
            'password': '',
            'project': project,
            'signatureid': '',
            'username': '',
            'vendor': vendor
        }
        data.update(kwargs)
        return self.post('bin/configrations/parsers/loader', data)

    def gen_api_key(self, serial, role, **kwargs):
        for dev in self.devices:
            if dev['serial'] == serial:
                device = dev
                break
        data = {
            'all_roles': '0',
            'api_key': '',
            'devicename': device['devicename'],
            'combo-4088-inputEl': 'user_password',
            'role': role,
            'id': 'MT3.model.DevicesKeys-8',
            'serial': serial,
            'user_name': self.username,
            'user_password': self.password
        }
        data.update(kwargs)
        params = {
            '_dc': self._dc,
            'serial': serial,
            'devicename': device['devicename']
        }
        return self.post('bin/authentication/devices/assignKeys', data, params=params)

    def get_keys(self, serial):
        for dev in self.devices:
            if dev['serial'] == serial:
                key_device = dev
                break
        params = {
            'serial': serial,
            'devicename': key_device['devicename']
        }
        return self.get_list('bin/authentication/devices/assignKeys', **params)

    def bpat(self, project):
        return self.post('bin/projects/bpat/bpat', {'project': project})

    def configuration(self, serial, configtype):
        for dev in self.devices:
            if dev['serial'] == serial:
                configdev = dev
        data = {
            'serial': serial,
            'devicename': configdev['devicename'],
            'configype': configtype
        }
        return self.post('bin/authentication/devices/configurations', data)

    def dev_contents(self, serial):
        return self.get_list('bin/authentication/devices/contents', serial=serial)




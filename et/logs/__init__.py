import pexpect


class LogCollector(object):
    """Collects the error logs during a test's execution."""
    ERROR_LOG_FILE = '/var/log/apache2/error.log'

    def __init__(self, hostname, username, password):
        """Initialize the log collector for this expedition host.

        Args:
            hostname (str): hostname
            username (str): username
            password (str): password

        """
        self.hostname = hostname
        self.username = username
        self.password = password

        self.apache_error_log_lines = None

    def initialize(self):
        """Initializes the log collector with current errors."""
        self.apache_error_log_lines = self._wc(self.ERROR_LOG_FILE)

    def finalize(self):
        pass

    def get_new_errors(self):
        """Gets the list of new error logs.

        Returns:
            list of strings; the new error logs

        """
        end_lines = self._wc(self.ERROR_LOG_FILE)
        new_lines = end_lines - self.apache_error_log_lines
        if new_lines <= 0:
            return []

        return self.run('tail -n {0} {1}'.format(
            new_lines, self.ERROR_LOG_FILE))

    def get_all_errors(self):
        """Returns a list of strings of all errors, new or old."""
        return self.run('cat {0}'.format(self.ERROR_LOG_FILE))

    def _spawn_args(self, cmd):
        """Builds the args to pass in to pexpect.spawn."""
        return {
            'command': 'ssh',
            'args': [
                '-o', 'UserKnownHostsFile=/dev/null',
                '-o', 'StrictHostKeyChecking=no',
                '{0}@{1}'.format(self.username, self.hostname),
                cmd,
            ],
            'timeout': 10,
        }

    def run(self, cmd):
        """Run the specified command and exit.

        Empty lines are removed from the returned output.

        Args:
            cmd (str): The command to execute

        Returns:
            list of strings; stdout

        """
        args = self._spawn_args(cmd)
        c = pexpect.spawn(**args)
        c.expect('assword:')
        c.sendline(self.password)
        c.expect(pexpect.EOF)

        return [x.strip() for x in c.before.split(b'\r\n') if x.strip()]

    def start_log(self):
        """Returns a fresh instance of LogCollector
        Useful when you want to see logs recorded over a small span of actions"""
        new_log = LogCollector(self.hostname, self.username, self.password)
        new_log.initialize()
        return new_log

    def _wc(self, filename):
        """Do 'wc -l <filename>'."""
        cmd = 'wc -l {0}'.format(filename)
        ans = self.run(cmd)
        return int(ans[0].split()[0])

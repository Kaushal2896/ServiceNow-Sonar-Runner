from scp import SCPClient
from paramiko import Transport
from paramiko import SSHClient
from paramiko import AutoAddPolicy
import re, os

class SonarScanner(object):

    sonar_properties = 'sonar-project.properties'
    ssh_port = 22
    sonar_scanner_command = 'sonar-scanner'
    success_regex = r'.*?EXECUTION SUCCESS.*?'
    sonar_ui_port = 9000

    def __init__(self, sonar_host, username, password):        
        self.sonar_host = sonar_host
        self.username = username
        self.password = password

    def generate_props(self, local_project_path, project_key, project_name, project_version = 1.0, properties_path = '.'):
        self.project_key = project_key
        self.project_name = project_name
        self.project_version = project_version
        self.properties_path = properties_path
        self.local_project_path = local_project_path

        with open(os.path.join(local_project_path, self.sonar_properties), 'w+') as props:
            props.write('''sonar.projectKey={0}\nsonar.projectName={1}\nsonar.projectVersion={2}\nsonar.sources={3}'''.format(self.project_key, self.project_name, str(self.project_version), self.properties_path))
    
    def upload_dir(self, remote_path):
        transport = Transport((self.sonar_host, self.ssh_port))
        transport.connect(username = self.username, password = self.password)

        with SCPClient(transport) as scp:
            scp.put(self.local_project_path, recursive = True, remote_path = remote_path)
            scp.put(os.path.join(self.local_project_path, self.sonar_properties), remote_path = os.path.join(remote_path, self.local_project_path.split(os.sep)[-1]))

        # execute command
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(self.sonar_host, username = self.username, password = self.password)
        sh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cd {0} && {1}'.format(remote_path + '/' + self.local_project_path.split(os.sep)[-1], self.sonar_scanner_command))
        ssh_stdout = ssh_stdout.read().decode('utf-8')
        if re.search(self.success_regex, ssh_stdout):
            print ('Link to dashboard: http://{0}:{1}/dashboard?id={2}'.format(self.sonar_host, self.sonar_ui_port, self.project_key))
        else:
            print ('Failed to generate Sonar Qube report. Error:\n{0}'.format(ssh_stdout))
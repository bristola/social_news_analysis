from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

# pip install paramiko
# pip install scp

class Connection_Utils:

    def __init__(self, pem_location, username="ubuntu"):
        self.pem_location = pem_location
        self.username = username
        self.client = SSHClient()


    def run_commands(self, ip, commands):
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(ip, username=self.username, key_filename=self.pem_location)
        for command in commands:
            stdin, stdout, stderr = self.client.exec_command(command)
            stdout.channel.recv_exit_status()
        self.client.close()


    def transfer_files(self, ip, files, destinations):
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(ip, username=self.username, key_filename=self.pem_location)
        with SCPClient(self.client.get_transport()) as scp_conn:
            for file, destination in zip(files, destinations):
                scp_conn.put(file, destination)

    def run_and_transfer(self, ip, commands, files, destinations):
        self.run_commands(ip, commands)
        self.transfer_files(ip, files, destinations)

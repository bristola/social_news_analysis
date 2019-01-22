from paramiko import SSHClient
from scp import SCPClient

# pip install paramiko

class Connection_Utils:

    def __init__(self, pem_location, username="ubuntu"):
        self.pem_location = pem_location
        self.username = username
        self.client = SSHClient()


    def run_commands(self, ip, commands):
        self.client.connect(ip, username=self.username, pkey=self.pem_location)
        for command in commands:
            stdin, stdout, stderr = self.client.exec_command(command)
            stdout.channel.recv_exit_status()
        self.client.close()


    def transfer_files(self, ip, files, destinations):
        self.client.connect(ip, username=self.username, pkey=self.pem_location)
        with SCPClient(self.client.get_transport()) as scp_conn:
            for file, destination in zip(files, destinations):
                scp_conn.put(file, destination)

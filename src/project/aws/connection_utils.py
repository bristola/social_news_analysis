from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from threading import Lock

# pip install paramiko
# pip install scp

# MAYBE HAVE A STATIC variable and method to run the commands and then add the stdout to the list and then wait for it to exit

class Connection_Utils:

    def __init__(self, pem_location, username="ubuntu"):
        self.pem_location = pem_location
        self.username = username
        self.lock = Lock()


    def run_commands(self, ip, commands):
        client = SSHClient()
        self.lock.acquire()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(ip, username=self.username, key_filename=self.pem_location)
        self.lock.release()
        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            stdout.channel.recv_exit_status()
        client.close()


    def transfer_files(self, ip, files, destinations):
        client = SSHClient()
        self.lock.acquire()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(ip, username=self.username, key_filename=self.pem_location)
        self.lock.release()
        with SCPClient(client.get_transport()) as scp_conn:
            for file, destination in zip(files, destinations):
                scp_conn.put(file, destination)

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from threading import Lock

# pip install paramiko
# pip install scp

class Connection_Utils:

    def __init__(self, pem_location, username="ubuntu"):
        self.pem_location = pem_location
        self.username = username


    def run_commands(self, ip, commands):
        """
        Connects to the ip usig SSH, and executes the list of bash commands.
        """
        # Create SSH client
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        # Lock all other threads so that the pem file is being accessed one at a time
        lock = Lock()
        lock.acquire()
        client.connect(ip, username=self.username, key_filename=self.pem_location)
        lock.release()
        for command in commands:
            # Execute command and wait for it to finish
            stdin, stdout, stderr = client.exec_command(command)
            stdout.channel.recv_exit_status()
        client.close()


    def transfer_files(self, ip, files, destinations):
        """
        Connects to ip address and transports specified local files to a
        destination on the connected server.
        """
        # Create SSH client
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        # Lock all other threads so that the pem file is being accessed one at a time
        lock = Lock()
        lock.acquire()
        client.connect(ip, username=self.username, key_filename=self.pem_location)
        lock.release()
        # Open an SCP client with SSH connection
        with SCPClient(client.get_transport()) as scp_conn:
            # Transfer each file to their respective destination
            for file, destination in zip(files, destinations):
                scp_conn.put(file, destination)

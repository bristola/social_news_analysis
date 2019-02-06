from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import psycopg2

class External_Connector:

    def __init__(self, pem_name, database_ip, collector_user="ubuntu", database_name="analysis", database_user="postgres", database_password="admin"):
        self.pem_name = pem_name
        self.database_ip = database_ip
        self.collector_user = collector_user
        self.database_name = database_name
        self.database_user = database_user
        self.database_password = database_password


    def get_data_files(self, ips, file_names):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        for ip, file_name in zip(ips, file_names):
            client.connect(ip, username=self.collector_user, key_filename=self.pem_name)
            with SCPClient(client.get_transport()) as scp_conn:
                scp_conn.get("data.txt", file_name)


    def execute_insertion(self, insert_str):
        try:
            conn = psycopg2.connect(dbname=self.database_name, host=self.database_ip, user=self.database_user, password=self.database_password)
            with conn.cursor() as cur:
                cur.execute(insert_str)
            if conn is not None:
                conn.close()
        except Exception as e:
            pass


    def insert_sentiment(self, sentiment_dict):
        pass


    def insert_mood(self, mood_dict):
        pass


    def insert_emoticon(self, emoticon_dict):
        pass

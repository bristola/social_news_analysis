from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import psycopg2

class External_Connector:

    def __init__(self, pem_name, database_ip, collector_user="ubuntu", database_name="postgres", database_user="postgres", database_password="admin"):
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
            conn.commit()
            if conn is not None:
                conn.close()
        except Exception as e:
            pass


    def insert_sentiment(self, run_id, type, sentiment_dict):
        if len(sentiment_dict) == 0:
            return
        insert_str = "INSERT INTO SENTIMENT (RUN_ID, TYPE, VALUE, WEIGHT) VALUES "
        addition_frag = "(%d, '%s', %0.8f, %d)"
        frags = list()
        for value, weight in sentiment_dict.items():
            addition_frag.append(addition_frag % (run_id, type, value, weight))
        insert_str += ','.join(frags)
        self.execute_insertion(insert_str)


    def insert_mood(self, run_id, type, mood_dict):
        if len(mood_dict) == 0:
            return
        insert_str = "INSERT INTO MOOD (RUN_ID, TYPE, MOOD, AMOUNT) VALUES "
        addition_frag = "(%d, '%s', '%s', %d)"
        frags = list()
        for mood, amount in mood_dict.items():
            addition_frag.append(addition_frag % (run_id, type, mood, amount))
        insert_str += ','.join(frags)
        self.execute_insertion(insert_str)


    def insert_emoticon(self, run_id, type, emoticon_dict):
        if len(emoticon_dict) == 0:
            return
        insert_str = "INSERT INTO EMOTICON (RUN_ID, TYPE, EMOTE, AMOUNT) VALUES "
        addition_frag = "(%d, '%s', '%s', %d)"
        frags = list()
        for emote, amount in emoticon_dict.items():
            addition_frag.append(addition_frag % (run_id, type, emote, amount))
        insert_str += ','.join(frags)
        self.execute_insertion(insert_str)

# ec = External_Connector(None, 'DATABASE_IP')
# ec.execute_insertion("INSERT INTO JOBS (TOPIC) VALUES ('NEW TEST');")

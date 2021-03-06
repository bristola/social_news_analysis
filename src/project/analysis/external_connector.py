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
        """
        Gets all input files from data collectors.
        """
        client = SSHClient()
        # By pass need to have ip preset
        client.set_missing_host_key_policy(AutoAddPolicy())
        for ip, file_name in zip(ips, file_names):
            # Connect to current data collector
            client.connect(ip, username=self.collector_user, key_filename=self.pem_name)
            with SCPClient(client.get_transport()) as scp_conn:
                # Get data.txt and save it to this machine as current file name
                scp_conn.get("data.txt", file_name)


    def execute_insertion(self, insert_str):
        """
        Inserts data into database using given SQL statement.
        """
        try:
            conn = psycopg2.connect(dbname=self.database_name, host=self.database_ip, user=self.database_user, password=self.database_password)
            # Execute insert statement using cursor
            with conn.cursor() as cur:
                cur.execute(insert_str)
            # Commit changes to database
            conn.commit()
            if conn is not None:
                conn.close()
        except Exception as e:
            pass


    def insert_sentiment(self, run_id, type, sentiment_dict):
        """
        Develops sentiment results insert SQL statement using dictionary.
        """
        if len(sentiment_dict) == 0:
            return
        insert_str = "INSERT INTO SENTIMENT (RUN_ID, TYPE, VALUE, WEIGHT) VALUES "
        # Fragment to be added to end of insert statement
        addition_frag = "(%s, '%s', %0.8f, %d)"
        frags = list()
        for value, weight in sentiment_dict.items():
            # Fill in blanks of the fragment with current data values
            frags.append(addition_frag % (run_id, type, value, weight))
        # Create multi insert statement
        insert_str += ','.join(frags)
        self.execute_insertion(insert_str)


    def insert_mood(self, run_id, type, mood_dict):
        """
        Develops mood results insert SQL statement using dictionary.
        """
        if len(mood_dict) == 0:
            return
        insert_str = "INSERT INTO MOOD (RUN_ID, TYPE, MOOD, AMOUNT) VALUES "
        # Fragment to be added to end of insert statement
        addition_frag = "(%s, '%s', '%s', %d)"
        frags = list()
        for mood, amount in mood_dict.items():
            # Fill in blanks of the fragment with current data values
            frags.append(addition_frag % (run_id, type, mood, amount))
        # Create multi insert statement
        insert_str += ','.join(frags)
        self.execute_insertion(insert_str)


    def insert_emoticon(self, run_id, type, emoticon_dict):
        """
        Develops emoticon results insert SQL statement using dictionary.
        """
        if len(emoticon_dict) == 0:
            return
        insert_str = "INSERT INTO EMOTICON (RUN_ID, TYPE, EMOTE, AMOUNT) VALUES "
        # Fragment to be added to end of insert statement
        addition_frag = "(%s, '%s', '%s', %d)"
        frags = list()
        for emote, amount in emoticon_dict.items():
            # Fill in blanks of the fragment with current data values
            frags.append(addition_frag % (run_id, type, emote, amount))
        # Create multi insert statement
        insert_str += ','.join(frags)
        self.execute_insertion(insert_str)

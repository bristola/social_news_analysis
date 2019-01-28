from aws.aws_utils import AWS_Utils
from aws.connection_utils import Connection_Utils
import aws.commands as commands
import threading

class AWS_Runner:

    def __init__(self, key_name, machine_type, security_group, image_id, pem_location):
        self.aws = AWS_Utils(key_name, machine_type, security_group, image_id)
        self.conn = Connection_Utils(pem_location)


    def setup_instances(self):
        ids, ips = self.aws.create_instance(5)

        self.conn.run_commands(ips[0], commands.twitter_collector_cmd)
        self.conn.transfer_files(ips[0], commands.twitter_files, commands.twitter_destinations)

        self.conn.run_commands(ips[1], commands.news_collector_cmd)
        self.conn.transfer_files(ips[1], commands.news_files, commands.news_destinations)

        self.conn.run_commands(ips[2], commands.analytics_cmd)
        self.conn.transfer_files(ips[2], commands.analytics_files, commands.analytics_destinations)

        self.conn.run_commands(ips[3], commands.analytics_cmd)
        self.conn.transfer_files(ips[3], commands.analytics_files, commands.analytics_destinations)

        self.conn.run_commands(ips[4], commands.database_cmd)
        self.conn.transfer_files(ips[4], commands.database_files, commands.database_destinations)

        return ids, ips


    def execute_system(self, session, config, topic):
        # Execute data collection processes

        ip = session['Twitter Collector IP']
        twitter_key = config['Twitter API key']
        twitter_secret = config['Twitter API secret key']
        twitter_token = config['Twitter Access token']
        twitter_token_secret = config['Twitter Access token secret']
        command = commands.data_exec_twitter % (topic, twitter_key, twitter_secret, twitter_token, twitter_token_secret)
        self.conn.run_commands(ip, command)

        ip = session['News Collector IP']
        news_key = config['News API key']
        command = commands.data_exec_news % (topic, news_key)
        self.conn.run_commands(ip, command)

        # Determine how many data analytics servers to create based on how many are running

        # Start analytics machines and set them up

        # Transfer data to analytics machines

        # Execute data analytics

        # Output will be in the database, just return the results ID

        pass


    def end_session(self, config):
        ids = [value for key, value in config.items() if "ID" in key]
        self.aws.end_instances(ids)

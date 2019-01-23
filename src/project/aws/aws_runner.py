from aws.aws_utils import AWS_Utils
from aws.connection_utils import Connection_Utils
import aws.commands as commands

class AWS_Runner:

    def __init__(self, key_name, machine_type, security_group, image_id, pem_location):
        self.aws = AWS_Utils(key_name, machine_type, security_group, image_id)
        self.conn = Connection_Utils(pem_location)


    def setup_instances(self):
        ids, ips = self.aws.create_instance(4)

        self.conn.run_commands(ips[0], commands.twitter_collector_cmd)
        self.conn.transfer_files(ips[0], commands.twitter_files, commands.twitter_destinations)

        self.conn.run_commands(ips[1], commands.news_collector_cmd)
        self.conn.transfer_files(ips[1], commands.news_files, commands.news_destinations)

        # Spark Installation and Setup

        # Database Installation and Setup

        return ids, ips


    def execute_system(self, ids, ips):
        pass

    def end_session(self, config):
        ids = [value for key, value in config.items() if "ID" in key]
        self.aws.end_instances(ids)

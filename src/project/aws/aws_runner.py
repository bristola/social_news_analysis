from aws.aws_utils import AWS_Utils
from aws.connection_utils import Connection_Utils
import aws.commands as commands
from multiprocessing.pool import ThreadPool

class AWS_Runner:

    def __init__(self, key_name, machine_type, security_group, image_id, pem_location):
        self.aws = AWS_Utils(key_name, machine_type, security_group, image_id)
        self.conn = Connection_Utils(pem_location)


    def setup_instances(self):
        """
        Creates aws instances for collection, analysis, and storage. Executes
        file transfers and installation commands on individual threads. Returns
        the ids and ips of the AWS ec2 machines.
        """
        ids, ips = self.aws.create_instance(5)

        # Parameters for thread pool. Each tuple is their own thread.
        parameters = [
            (ips[0], commands.twitter_collector_cmd, commands.twitter_files, commands.twitter_destinations),
            (ips[1], commands.news_collector_cmd, commands.news_files, commands.news_destinations),
            (ips[2], commands.analytics_cmd, commands.analytics_files, commands.analytics_destinations),
            (ips[3], commands.analytics_cmd, commands.analytics_files, commands.analytics_destinations),
            (ips[4], commands.database_cmd, commands.database_files, commands.database_destinations)
        ]

        # Carry out threading execution and await completion
        pool = ThreadPool(5)
        pool.map(self.installation_thread, parameters)
        pool.close()
        pool.join()

        return ids, ips


    def execute_system(self, session, config, topic):

        # Insert Job into database if it's a new job

        # Insert Run into database and save it's ID for the analytics code

        # Data collection commands to be executed. Put in data from configuration
        command1 = commands.data_exec_twitter % (topic, config['Twitter API key'], config['Twitter API secret key'], config['Twitter Access token'], config['Twitter Access token secret'])
        command2 = commands.data_exec_news % (topic, config['News API key'])

        # Parameters for thread pool. Each tuple is their own thread.
        parameters = [
            (session['Twitter Collector IP'], [command1]),
            (session['News Collector IP'], [command2])
        ]

        # Carry out threading execution and await completion of data collection
        pool = ThreadPool(2)
        pool.map(self.data_collection_thread, parameters)
        pool.close()
        pool.join()

        # Determine how many data analytics servers to create based on how many are running

        # Start analytics machines and set them up

        # Transfer data to analytics machines (Need to transfer PEM file aswell from config)

        # Execute data analytics

        # Output will be in the database, just return the results ID


    def end_session(self, config):
        """
        Take out all ids from config dictionary and end the respective ec2
        machines.
        """
        ids = [value for key, value in config.items() if "ID" in key]
        self.aws.end_instances(ids)


    def installation_thread(self, params):
        """
        Thread for setting up the machines.
        """
        self.conn.transfer_files(params[0], params[2], params[3])
        self.conn.run_commands(params[0], params[1])


    def data_collection_thread(self, params):
        """
        Thread for executing data collection.
        """
        self.conn.run_commands(params[0], params[1])

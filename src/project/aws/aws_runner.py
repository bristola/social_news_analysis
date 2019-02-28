from aws.aws_utils import AWS_Utils
from aws.connection_utils import Connection_Utils
from aws.database_connector import Database_Connector
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
        """
        Run the actual system, including the data collection and data analytics.
        Inputs the session data, the configuration data, and a specified topic.
        Also, option to enter an existing job_id that we are rerunning. After it
        will return the run_id that is associated with the results.
        """
        database = Database_Connector(session['Database IP'])

        job_id = database.get_job_from_topic(topic)

        # Insert Job into database if it's a new job
        if (job_id is None):
            job_id = database.create_new_job(topic)

        # Insert Run into database and save it's ID for the analytics code
        run_id = database.create_new_run(job_id)

        # Data collection commands to be executed. Put in data from configuration
        command1 = commands.data_exec_twitter % ('"'+topic+'"', config['Twitter API key'], config['Twitter API secret key'], config['Twitter Access token'], config['Twitter Access token secret'])
        command2 = commands.data_exec_news % ('"'+topic+'"', config['News API key'])

        # Parameters for thread pool. Each tuple is their own thread.
        parameters = [
            (session['Twitter Collector IP'], [command1]),
            (session['News Collector IP'], [command2])
        ]

        # Carry out threading execution and await completion of data collection
        pool = ThreadPool(2)
        pool.map(self.command_run_thread, parameters)
        pool.close()
        pool.join()

        # Transfer data to analytics machines (Need to transfer PEM file aswell from config)
        self.conn.transfer_files(session['Twitter Analyzer IP'], [config['Path to pem']], [config['AWS Key Name']+".pem"])
        self.conn.transfer_files(session['News Analyzer IP'], [config['Path to pem']], [config['AWS Key Name']+".pem"])

        # Execute data analytics
        command1 = commands.analtyics_exec % ("Twitter", run_id, config['AWS Key Name']+".pem", session['Database IP'], session['Twitter Collector IP'])
        command2 = commands.analtyics_exec % ("News", run_id, config['AWS Key Name']+".pem", session['Database IP'], session['News Collector IP'])

        parameters = [
            (session['Twitter Analyzer IP'], [command1]),
            (session['News Analyzer IP'], [command2])
        ]

        # Carry out threading execution and await completion of data analytics
        pool = ThreadPool(2)
        pool.map(self.command_run_thread, parameters)
        pool.close()
        pool.join()

        # Output will be in the database, just return the run id
        return run_id


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


    def command_run_thread(self, params):
        """
        Thread for executing data collection.
        """
        self.conn.run_commands(params[0], params[1])

from aws.aws_utils import AWS_Utils
from aws.connection_utils import Connection_Utils
import aws.commands as commands
from multiprocessing.pool import ThreadPool

class AWS_Runner:

    def __init__(self, key_name, machine_type, security_group, image_id, pem_location):
        self.aws = AWS_Utils(key_name, machine_type, security_group, image_id)
        self.conn = Connection_Utils(pem_location)


    def setup_instances(self):
        ids, ips = self.aws.create_instance(5)

        parameters = list()
        parameters.append((ips[0], commands.twitter_collector_cmd, commands.twitter_files, commands.twitter_destinations))
        parameters.append((ips[1], commands.news_collector_cmd, commands.news_files, commands.news_destinations))
        parameters.append((ips[2], commands.analytics_cmd, commands.analytics_files, commands.analytics_destinations))
        parameters.append((ips[3], commands.analytics_cmd, commands.analytics_files, commands.analytics_destinations))
        parameters.append((ips[4], commands.database_cmd, commands.database_files, commands.database_destinations))

        pool = ThreadPool(5)
        pool.map(self.installation_thread, parameters)
        pool.close()
        pool.join()

        return ids, ips


    def execute_system(self, session, config, topic):
        # Execute data collection processes
        ip = session['Twitter Collector IP']
        twitter_key = config['Twitter API key']
        twitter_secret = config['Twitter API secret key']
        twitter_token = config['Twitter Access token']
        twitter_token_secret = config['Twitter Access token secret']
        command = commands.data_exec_twitter % (topic, twitter_key, twitter_secret, twitter_token, twitter_token_secret)
        self.conn.run_commands(ip, [command])

        ip = session['News Collector IP']
        news_key = config['News API key']
        command = commands.data_exec_news % (topic, news_key)
        self.conn.run_commands(ip, [command])

        # Determine how many data analytics servers to create based on how many are running

        # Start analytics machines and set them up

        # Transfer data to analytics machines

        # Execute data analytics

        # Output will be in the database, just return the results ID

        pass


    def end_session(self, config):
        ids = [value for key, value in config.items() if "ID" in key]
        self.aws.end_instances(ids)

    def installation_thread(self, params):
        print(str(params))
        self.conn.run_commands(params[0], params[1])
        self.conn.transfer_files(params[0], params[2], params[3])

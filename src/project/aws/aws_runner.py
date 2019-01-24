from aws.aws_utils import AWS_Utils
from aws.connection_utils import Connection_Utils
import aws.commands as commands
import threading

class AWS_Runner:

    def __init__(self, key_name, machine_type, security_group, image_id, pem_location):
        self.aws = AWS_Utils(key_name, machine_type, security_group, image_id)
        self.conn = Connection_Utils(pem_location)


    def setup_instances(self):
        ids, ips = self.aws.create_instance(4)

        threads = list()

        threads.append(threading.Thread(target=self.conn.run_and_transfer,
                                        args=(ips[0],
                                              commands.twitter_collector_cmd,
                                              commands.twitter_files,
                                              commands.twitter_destinations,)))

        threads.append(threading.Thread(target=self.conn.run_and_transfer,
                                        args=(ips[1],
                                              commands.news_collector_cmd,
                                              commands.news_files,
                                              commands.news_destinations,)))

        threads.append(threading.Thread(target=self.conn.run_and_transfer,
                                        args=(ips[2],
                                              commands.spark_cmd,
                                              commands.spark_files,
                                              commands.spark_destinations,)))

        threads.append(threading.Thread(target=self.conn.run_commands,
                                        args=(ips[3],
                                              commands.database_cmd,)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return ids, ips


    def execute_system(self, ids, ips):
        pass


    def end_session(self, config):
        ids = [value for key, value in config.items() if "ID" in key]
        self.aws.end_instances(ids)

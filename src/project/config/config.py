import os
import os.path
import datetime
from config.session_exceptions import NoSessionFoundException, SessionExistsException


class Config:

    def __init__(self, config_file_name="config.txt", session_file_name="session.txt"):
        self.file = config_file_name
        self.session_file = session_file_name


    def get_config_contents(self):
        config_dict = dict()
        with open(self.file, 'r') as config_contents:
            for line in config_contents:
                line_list = [i.strip() for i in line.split("=")]
                if len(line_list) != 2:
                    continue
                else:
                    config_dict[line_list[0]] = line_list[1]
        return config_dict


    def create_session(self):
        if self.check_session():
            raise SessionExistsException()
        with open(self.session_file, 'w+') as session:
            cur_time = datetime.datetime.now()
            line = "start_time = %s" % (str(cur_time))
            session.write(line)


    def get_session_contents(self):
        if not self.check_session():
            raise NoSessionFoundException
        session_dict = dict()
        with open(self.session_file, "r") as session:
            for line in session:
                line_list = [i.strip() for i in line.split("=")]
                if len(line_list) != 2:
                    continue
                else:
                    session_dict[line_list[0]] = line_list[1]
        return session_dict


    def add_to_session(self, name, value):
        if not self.check_session():
            raise NoSessionFoundException()
        with open(self.session_file, "a") as session:
            line = "\n%s = %s" % (name, value)
            session.write(line)


    def add_session_info(self, ids, ips):
        self.add_to_session("Twitter Collector ID", ids[0])
        self.add_to_session("Twitter Collector IP", ips[0])
        self.add_to_session("News Collector ID", ids[1])
        self.add_to_session("News Collector IP", ips[1])
        self.add_to_session("Twitter Analyzer ID", ids[2])
        self.add_to_session("Twitter Analyzer IP", ips[2])
        self.add_to_session("News Analyzer ID", ids[3])
        self.add_to_session("News Analyzer IP", ips[3])
        self.add_to_session("Database ID", ids[4])
        self.add_to_session("Database IP", ips[4])


    def check_session(self):
        if os.path.isfile(self.session_file) and os.access(self.session_file, os.R_OK):
            return True
        else:
            return False


    def end_session(self):
        if not self.check_session():
            raise NoSessionFoundException
        os.remove(self.session_file)

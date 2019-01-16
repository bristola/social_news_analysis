import os
import os.path
import datetime
from session_exceptions import NoSessionFoundException. SessionExistsException

class Config:

    def __init__(self, config_file_name="config.txt", session_file_name="session.txt"):
        self.file = config_file_name
        self.session_file = session_file_name
        self.read_in_config_items(config_file_name)


    def read_in_config_items(self, file_name):
        self.config_dict = dict()
        with open(file_name, 'r') as config_contents:
            for line in config_contents:
                line_list = [i.strip() for i in line.split("=")]
                if len(line_list) != 2:
                    continue
                else:
                    self.config_dict[line_list[0]] = line_list[1]


    def get_config_contents(self):
        return self.config_dict


    def create_session(self):
        if self.check_session():
            raise SessionExistsException()
        with open(self.session_file, 'w+') as session:
            cur_time = datetime.datetime.now()
            line = "start_time = %s" % (str(cur_time))
            session.write(line)


    def add_to_session(self, name, value):
        if not self.check_session():
            raise NoSessionFoundException()
        with open(self.session_file, "a") as session:
            line = "%s = %s" % (name, value)
            session.write(line)


    def check_session(self):
        if os.path.isfile(self.session_file) and os.access(self.session_file, os.R_OK):
            return True
        else:
            return False


    def end_session(self):
        if not self.check_session():
            raise NoSessionFoundException
        os.remove(self.session_file)

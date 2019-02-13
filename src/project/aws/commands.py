twitter_collector_cmd = ["sudo apt-get -y update",
                         "sudo apt-get install -y python3-pip",
                         "sudo pip3 install --upgrade pip",
                         "sudo pip3 install --ignore-installed newspaper3k",
                         "sudo pip3 install newsapi-python",
                         "sudo pip3 install python-twitter"]

twitter_files = ["data_collector/runner.py",
                 "data_collector/data_collector.py",
                 "data_collector/news_collector.py",
                 "data_collector/twitter_collector.py"]

twitter_destinations = ["runner.py",
                        "data_collector.py",
                        "news_collector.py",
                        "twitter_collector.py"]

news_collector_cmd = ["sudo apt-get -y update",
                      "sudo apt-get install -y python3-pip",
                      "sudo pip3 install --upgrade pip",
                      "sudo pip3 install --ignore-installed newspaper3k",
                      "sudo pip3 install newsapi-python",
                      "sudo pip3 install python-twitter"]

news_files = ["data_collector/runner.py",
              "data_collector/data_collector.py",
              "data_collector/news_collector.py",
              "data_collector/twitter_collector.py"]

news_destinations = ["runner.py",
                     "data_collector.py",
                     "news_collector.py",
                     "twitter_collector.py"]

analytics_cmd = ["sudo apt-get update",
                 "sudo apt-get install -y python3-pip",
                 "sudo pip3 install --upgrade pip",
                 "sudo pip3 install paramiko",
                 "sudo pip3 install scp",
                 "sudo pip3 install psycopg2",
                 "sudo pip3 install nltk"]

analytics_files = ["analysis/analysis.py",
                   "analysis/external_connector.py",
                   "analysis/runner.py",
                   "analysis/words.py"]

analytics_destinations = ["analysis.py",
                          "external_connector.py",
                          "runner.py",
                          "words.py"]

database_cmd = ["sudo apt-get update",
                "sudo apt-get install -y postgresql postgresql-contrib",
                "sudo sed -i -- 's|127.0.0.1/32|0.0.0.0/0|g' ../../etc/postgresql/9.3/main/pg_hba.conf",
                "sudo sed -i -- \"s/#listen_addresses = 'localhost'/listen_addresses = '*'/g\" ../../etc/postgresql/9.3/main/postgresql.conf",
                "sudo service postgresql restart",
                "sudo -u postgres psql -f database_schema.sql"]

database_files = ["database_schema.sql"]

database_destinations = ["database_schema.sql"]

data_exec_twitter = "python3 runner.py Twitter %s %s %s %s %s"

data_exec_news = "python3 runner.py News %s %s"

analtyics_exec = "python3 runner.py %s %s %s %s %s"

twitter_collector_cmd = ["sudo apt-get update",
                         "sudo apt-get install -y python3-pip",
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
                      "sudo pip3 install newsapi-python"]

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
                 "sudo pip3 install -U textblob",
                 "python3 -m textblob.download_corpora"]

analytics_files = ["analysis/analysis.py"]

analytics_destinations = ["analysis.py"]

database_cmd = []

database_files = ["database_schema.sql"]

database_destinations = ["database_schema.sql"]

data_exec_twitter = "python3 runner.py Twitter %s %s %s %s %s"

data_exec_news = "python3 runner.py News %s %s"

twitter_collector_cmd = ["sudo apt-get update",
                         "sudo apt-get install -y python3-pip",
                         "sudo pip3 install python-twitter"]

twitter_files = ["data_collector/data_collector.py",
                 "data_collector/twitter_collector.py"]

twitter_destinations = ["data_collector.py",
                        "twitter_collector.py"]

news_collector_cmd = ["sudo apt-get update",
                      "sudo apt-get install -y python3-pip",
                      "sudo pip3 install newsapi-python",
                      " sudo pip3 install feedparser",
                      "",
                      "sudo pip3 install newspaper3k"]

news_files = ["data_collector/data_collector.py",
              "data_collector/news_collector.py"]

news_destinations = ["data_collector.py",
                     "news_collector.py"]

spark_cmd = []

database_cmd = []

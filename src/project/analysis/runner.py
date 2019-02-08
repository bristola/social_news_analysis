from analysis import Analyzer
from external_connector import External_Connector
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("run_id", help="The run ID for the results being placed into the database.")
parser.add_argument("pem_name", help="Name of the PEM file that is needed to connect to the data collection servers.")
parser.add_argument("database_ip", help="IP of the Postgres database that the results will be put into.")
parser.add_argument("data_collector_ips", nargs='+', help="List of IPs of the data collection servers.")

args = parser.parse_args()

ec = External_Connector(args.pem_name, args.database_ip)

files = ["twitter.txt"]
files.extend(["news%d.txt" % (i) for i in range(1, len(args.data_collector_ips))])

ec.get_data_files(args.data_collector_ips, files)

a = Analyzer()

type = "Twitter"
for f in files:
    sentiment, mood, emoticon = a.run(type, f)
    ec.insert_sentiment(args.run_id, type, sentiment)
    ec.insert_mood(args.run_id, type, mood)
    ec.insert_emoticon(args.run_id, type, emoticon)
    type = "News"
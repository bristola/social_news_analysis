import psycopg2
from aws.sql_statements import *

# pip install psycopg2

class Database_Connector:

    def __init__(self, database_ip, database_name="postgres", database_user="postgres", database_password="admin"):
        self.database_ip = database_ip
        self.database_name = database_name
        self.database_user = database_user
        self.database_password = database_password


    def execute_selection(self, select_str):
        """
        Executes the SQL Select statement on the database and return the
        results.
        """
        results = None
        try:
            conn = psycopg2.connect(dbname=self.database_name, host=self.database_ip, user=self.database_user, password=self.database_password)
            with conn.cursor() as cur:
                cur.execute(select_str)
                results = cur.fetchall()
            if conn is not None:
                conn.close()
        except Exception as e:
            pass
        return results


    def execute_insertion(self, insert_str):
        """
        Inserts data into database using given SQL statement.
        """
        return_val = None
        try:
            conn = psycopg2.connect(dbname=self.database_name, host=self.database_ip, user=self.database_user, password=self.database_password)
            # Execute insert statement using cursor
            with conn.cursor() as cur:
                cur.execute(insert_str)
                return_val = cur.fetchone()[0]
            # Commit changes to database
            conn.commit()
            if conn is not None:
                conn.close()
        except Exception as e:
            pass
        return return_val


    def create_new_job(self, topic):
        """
        At the start of a new topic, we need to create a new Job entry.
        """
        insert_str = new_job % (str(topic))
        job_id = self.execute_insertion(insert_str)
        return job_id


    def create_new_run(self, job_id):
        """
        Every system execution we need a run entry to associate results to.
        """
        insert_str = new_run % (str(job_id))
        run_id = self.execute_insertion(insert_str)
        return run_id


    def get_sentiment_totals(self):
        """
        Executes SQL select to get total sentiment across both types of data.
        """
        results = self.execute_selection(twitter_sentiment)
        twitter = results[0][0]
        results = self.execute_selection(news_sentiment)
        news = results[0][0]
        return twitter, news


    def get_sentiment_groups(self):
        """
        Breaks sentiment results into 5 sections and counts totals in each.
        """
        fifths = list()
        for group in sentiment_groups:
            results = self.execute_selection(group)
            fifths.append(results[0][0])
        return fifths


    def get_mood_totals(self):
        """
        Gets the total counts of each emotion type for each type of data.
        """
        twitter_moods = dict()
        results = self.execute_selection(twitter_mood)
        for result in results:
            twitter_moods[result[0]] = result[1]
        news_moods = dict()
        results = self.execute_selection(news_mood)
        for result in results:
            news_moods[result[0]] = result[1]
        return twitter_moods, news_moods


    def get_emoticon_totals(self):
        """
        Collects the top 10 most used emoticons in our data collection.
        """
        emotes = dict()
        results = self.execute_selection(emoticon)
        for result in results:
            emotes[result[0]] = result[1]
        return emotes

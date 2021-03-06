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


    def get_jobs_and_runs(self):
        """
        Gets all the previously created jobs and their run_id that are
        associated.
        """
        jobs = self.execute_selection(all_jobs)
        runs = self.execute_selection(all_runs)
        jobs_and_runs = dict()
        for job in jobs:
            out = list()
            for run in runs:
                if run[1] == job[0]:
                    out.append((run[0],run[2].strftime("%B %d, %Y at %I:%M %p")))
            jobs_and_runs[job[1]] = out
        return jobs_and_runs


    def get_job_from_topic(self, topic):
        """
        Gets the job id for a given topic if one exists.
        """
        results = self.execute_selection(get_job % (str(topic)))
        if len(results) == 0:
            return None
        else:
            topic = results[0][0]
            return topic


    def get_sentiment_totals(self, topic, run_id):
        """
        Executes SQL select to get total sentiment across both types of data.
        """
        select_str = twitter_sentiment_all % (str(topic)) if run_id is None else twitter_sentiment % (str(run_id))
        results = self.execute_selection(select_str)
        twitter = results[0][0]
        select_str = news_sentiment_all % (str(topic)) if run_id is None else news_sentiment % (str(run_id))
        results = self.execute_selection(select_str)
        news = results[0][0]
        return twitter, news


    def get_sentiment_groups(self, topic, run_id):
        """
        Breaks sentiment results into 5 sections and counts totals in each.
        """
        fifths = list()
        for group_all, group in zip(sentiment_groups_all, sentiment_groups):
            select_str = group_all % (str(topic)) if run_id is None else group % (str(run_id))
            results = self.execute_selection(select_str)
            fifths.append(results[0][0])
        return fifths


    def get_mood_totals(self, topic, run_id):
        """
        Gets the total counts of each emotion type for each type of data.
        """
        select_str = twitter_mood_all % (str(topic)) if run_id is None else twitter_mood % (str(run_id))
        twitter_moods = dict()
        results = self.execute_selection(select_str)
        for result in results:
            twitter_moods[result[0]] = result[1]
        select_str = news_mood_all % (str(topic)) if run_id is None else news_mood % (str(run_id))
        news_moods = dict()
        results = self.execute_selection(select_str)
        for result in results:
            news_moods[result[0]] = result[1]
        return twitter_moods, news_moods


    def get_emoticon_totals(self, topic, run_id):
        """
        Collects the top 10 most used emoticons in our data collection.
        """
        select_str = emoticon_all % (str(topic)) if run_id is None else emoticon % (str(run_id))
        emotes = dict()
        results = self.execute_selection(select_str)
        for result in results:
            emotes[result[0]] = result[1]
        return emotes


    def get_time_series(self, topic):
        results = self.execute_selection(time_series_twitter % topic)
        twitter_data = [result[0] for result in results]
        results = self.execute_selection(time_series_news % topic)
        news_data = [result[0] for result in results]
        results = self.execute_selection(time_series_dates % topic)
        dates = [result[0] for result in results]
        return (twitter_data, news_data), dates

import psycopg2

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
        conn = psycopg2.connect(dbname=self.database_name, host=self.database_ip, user=self.database_user, password=self.database_password)
        # Execute insert statement using cursor
        with conn.cursor() as cur:
            cur.execute(insert_str)
            return_val = cur.fetchone()[0]
        # Commit changes to database
        conn.commit()
        if conn is not None:
            conn.close()
        return return_val


    def create_new_job(self, topic):
        insert_str = "INSERT INTO JOB (TOPIC) VALUES ('%s') RETURNING ID" % (str(topic))
        job_id = self.execute_insertion(insert_str)
        return job_id


    def create_new_run(self, job_id):
        insert_str = "INSERT INTO RUN (JOB_ID, RUN_TIME) VALUES (%s, CURRENT_TIMESTAMP) RETURNING ID" % (str(job_id))
        run_id = self.execute_insertion(insert_str)
        return run_id


    def get_sentiment_groups(self):
        pass


    def get_sentiment_totals(self):
        pass


    def get_mood_totals(self):
        pass

    def get_emoticon_totals(self):
        pass

new_job = "INSERT INTO JOB (TOPIC) VALUES ('%s') RETURNING ID"
new_run = "INSERT INTO RUN (JOB_ID, RUN_TIME) VALUES (%s, CURRENT_TIMESTAMP) RETURNING ID"
all_jobs = "SELECT * FROM JOB ORDER BY ID"
all_runs = "SELECT * FROM RUN ORDER BY JOB_ID"
get_job = "SELECT ID FROM JOB WHERE TOPIC = '%s'"
twitter_sentiment = "SELECT SUM(weighted_value)/SUM(weight) FROM (SELECT value * weight as weighted_value, weight FROM SENTIMENT WHERE type = 'Twitter' AND RUN_ID = %s) AS SUB_QUERY"
twitter_sentiment_all = "SELECT SUM(weighted_value)/SUM(weight) FROM (SELECT value * weight as weighted_value, weight FROM SENTIMENT WHERE type = 'Twitter' AND RUN_ID IN (SELECT ID FROM RUN WHERE JOB_ID = (SELECT ID FROM JOB WHERE TOPIC = '%s'))) AS SUB_QUERY"
news_sentiment = "SELECT AVG(value) FROM SENTIMENT WHERE type = 'News' AND RUN_ID = %s"
news_sentiment_all = "SELECT AVG(value) FROM SENTIMENT WHERE type = 'News' AND RUN_ID IN (SELECT ID FROM RUN WHERE JOB_ID = (SELECT ID FROM JOB WHERE TOPIC = '%s'))"
sentiment_groups = ["SELECT SUM(weight) FROM SENTIMENT WHERE value <= -.6 AND RUN_ID = %s",
                    "SELECT SUM(weight) FROM SENTIMENT WHERE value > -.6 AND value <= -.2 AND RUN_ID = %s",
                    "SELECT SUM(weight) FROM SENTIMENT WHERE value > -.2 AND value < .2 AND RUN_ID = %s",
                    "SELECT SUM(weight) FROM SENTIMENT WHERE value >= .2 AND value < .6 AND RUN_ID = %s",
                    "SELECT SUM(weight) FROM SENTIMENT WHERE value >= .6 AND RUN_ID = %s"]
sentiment_groups_all = ["SELECT SUM(weight) FROM SENTIMENT WHERE value <= -.6 AND RUN_ID IN (SELECT ID FROM RUN WHERE JOB_ID = (SELECT ID FROM JOB WHERE TOPIC = '%s'))",
                        "SELECT SUM(weight) FROM SENTIMENT WHERE value > -.6 AND value <= -.2 AND RUN_ID IN (SELECT ID FROM RUN WHERE JOB_ID = (SELECT ID FROM JOB WHERE TOPIC = '%s'))",
                        "SELECT SUM(weight) FROM SENTIMENT WHERE value > -.2 AND value < .2 AND RUN_ID IN (SELECT ID FROM RUN WHERE JOB_ID = (SELECT ID FROM JOB WHERE TOPIC = '%s'))",
                        "SELECT SUM(weight) FROM SENTIMENT WHERE value >= .2 AND value < .6 AND RUN_ID IN (SELECT ID FROM RUN WHERE JOB_ID = (SELECT ID FROM JOB WHERE TOPIC = '%s'))",
                        "SELECT SUM(weight) FROM SENTIMENT WHERE value >= .6 AND RUN_ID IN (SELECT ID FROM RUN WHERE JOB_ID = (SELECT ID FROM JOB WHERE TOPIC = '%s'))"]
twitter_mood = "SELECT mood, SUM(amount) as totals FROM MOOD WHERE type = 'Twitter' AND RUN_ID = %s GROUP BY mood ORDER BY totals DESC"
twitter_mood_all = "SELECT mood, SUM(amount) as totals FROM MOOD WHERE type = 'Twitter' AND RUN_ID IN (SELECT ID FROM RUN WHERE JOB_ID = (SELECT ID FROM JOB WHERE TOPIC = '%s')) GROUP BY mood ORDER BY totals DESC"
news_mood = "SELECT mood, SUM(amount) as totals FROM MOOD WHERE type = 'News' AND RUN_ID = %s GROUP BY mood ORDER BY totals DESC"
news_mood_all = "SELECT mood, SUM(amount) as totals FROM MOOD WHERE type = 'News' AND RUN_ID IN (SELECT ID FROM RUN WHERE JOB_ID = (SELECT ID FROM JOB WHERE TOPIC = '%s')) GROUP BY mood ORDER BY totals DESC"
emoticon = "SELECT emote, SUM(amount) as totals FROM EMOTICON WHERE RUN_ID = %s GROUP BY emote ORDER BY totals DESC LIMIT 10"
emoticon_all = "SELECT emote, SUM(amount) as totals FROM EMOTICON WHERE RUN_ID IN (SELECT ID FROM RUN WHERE JOB_ID = (SELECT ID FROM JOB WHERE TOPIC = '%s')) GROUP BY emote ORDER BY totals DESC LIMIT 10"

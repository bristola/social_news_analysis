new_job = "INSERT INTO JOB (TOPIC) VALUES ('%s') RETURNING ID"
new_run = "INSERT INTO RUN (JOB_ID, RUN_TIME) VALUES (%s, CURRENT_TIMESTAMP) RETURNING ID"
twitter_sentiment = "SELECT SUM(weighted_value)/SUM(weight) FROM (SELECT value * weight as weighted_value, weight FROM SENTIMENT WHERE RUN_ID = %s) AS SUB_QUERY"
news_sentiment = "SELECT AVG(value) FROM SENTIMENT WHERE type = 'News' WHERE RUN_ID = %s"
sentiment_groups = ["SELECT SUM(weight) FROM SENTIMENT WHERE value <= -.6 AND RUN_ID = %s",
                    "SELECT SUM(weight) FROM SENTIMENT WHERE value > -.6 AND value <= -.2 AND RUN_ID = %s",
                    "SELECT SUM(weight) FROM SENTIMENT WHERE value > -.2 AND value < .2 AND RUN_ID = %s",
                    "SELECT SUM(weight) FROM SENTIMENT WHERE value >= .2 AND value < .6 AND RUN_ID = %s",
                    "SELECT SUM(weight) FROM SENTIMENT WHERE value >= .6"]
twitter_mood = "SELECT mood, SUM(amount) as totals FROM MOOD WHERE type = 'Twitter' AND RUN_ID = %s GROUP BY mood ORDER BY totals DESC"
news_mood = "SELECT mood, SUM(amount) as totals FROM MOOD WHERE type = 'News' AND RUN_ID = %s GROUP BY mood ORDER BY totals DESC"
emoticon = "SELECT emote, SUM(amount) as totals FROM EMOTICON WHERE RUN_ID = %s GROUP BY emote ORDER BY totals DESC LIMIT 10"

new_job = "INSERT INTO JOB (TOPIC) VALUES ('%s') RETURNING ID"
new_run = "INSERT INTO RUN (JOB_ID, RUN_TIME) VALUES (%s, CURRENT_TIMESTAMP) RETURNING ID"
twitter_sentiment = "SELECT SUM(weighted_value)/SUM(weight) FROM (SELECT value * weight as weighted_value, weight FROM SENTIMENT) AS SUB_QUERY"
news_sentiment = "SELECT AVG(value) FROM SENTIMENT WHERE type = 'News'"
sentiment_groups = ["SELECT SUM(weight) FROM SENTIMENT WHERE value <= -.6",
                    "SELECT SUM(weight) FROM SENTIMENT WHERE value > -.6 AND value <= -.2",
                    "SELECT SUM(weight) FROM SENTIMENT WHERE value > -.2 AND value < .2",
                    "SELECT SUM(weight) FROM SENTIMENT WHERE value >= .2 AND value < .6",
                    "SELECT SUM(weight) FROM SENTIMENT WHERE value >= .6"]
twitter_mood = "SELECT mood, SUM(amount) as totals FROM MOOD WHERE type = 'Twitter' GROUP BY mood ORDER BY totals DESC"
news_mood = "SELECT mood, SUM(amount) as totals FROM MOOD WHERE type = 'News' GROUP BY mood ORDER BY totals DESC"
emoticon = "SELECT emote, SUM(amount) as totals FROM EMOTICON GROUP BY emote ORDER BY totals DESC LIMIT 10"

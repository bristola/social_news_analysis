# Social and News Media Analysis
### By: Austin Bristol

This project was completed for a senior thesis project at Allegheny College. The system was written in Python 3, and uses a suite of technologies to perform sentiment analysis of social media and news data.

## Overview

This software system allows users to collect large amounts of media data from Twitter and various news sources, and analyzes this information to extract valuable insights in the sentiment that users display on the platforms. By using a easy-to-use web interface, users can set up a cluster of AWS machines to perform the analytics with a click of a button. Also, the user can easily query the system for whatever search topic that they want to perform analytics on, as well as saving previous results to be viewed later. Visualizations are produced as a result of the analytics, and can be used to gain insights on the input topic.

### Examples

You can view how the system works all together by viewing the following [demo video](https://youtu.be/oO-sEbG8oZI). Also, Below shows various example visualizations that are produced by this software system. Included, the overall sentiment visualization, a sentiment bar graph, mood pie chart, sentiment change line graph, and emoticon table.

<img src="./img/sentiment_totals.png" width="60%"></img>

<img src="./img/sentiment_groups.png" width="60%"></img>

<img src="./img/moods.png" width="60%"></img>

<img src="./img/sentiment_change.png" width="60%"></img>

<img src="./img/emoticons.PNG" width="60%"></img>

### Technology

There were a suite of technologies used in the development of the project. Specifically, a lot of different Python packages were used to complete this project. Also, Amazon Web Services were used in great detail as well. Below is a listing of the technologies that were used in this project:

- [Python 3.6](<https://www.python.org/>)

- [Flask](<http://flask.pocoo.org/>)

- [python-twitter](<https://python-twitter.readthedocs.io/en/latest/>)

- [News API](<https://newsapi.org/docs/client-libraries/python>)

- [Newspaper3k](<https://github.com/codelucas/newspaper>)

- [Natural Language Toolkit](<https://www.nltk.org/>)

- [Matplotlib](<https://matplotlib.org/>)

- [Paramiko](http://www.paramiko.org/)

- [scp](https://pypi.org/project/scp/)

- [AWS SDK for Python](<https://aws.amazon.com/sdk-for-python/>)

- [AWS EC2](<https://aws.amazon.com/ec2/>)

- [PostgreSQL](<https://www.postgresql.org/>)

## Prerequisites

In order to be able to correctly install this software system and get it up and running, there are few things you need to do. This ranges from creating accounts on different platforms, as well as set up internal files. Below is a list of tasks that must be completed before installing the system.

1. Create a developer account on Twitter. Traverse to this [link](https://developer.twitter.com/) and create an account. You can create. Then, you will be able to go to the [apps](https://developer.twitter.com/en/apps) page, and create a new app. Here you can create new application by following the prompts. Finally, once the app is created, you will need to save the all keys and tokens found in the 'Keys and tokens' tab of the details.

1. Create an account on the [newsapi](https://newsapi.org/) website. Once you create a free account, you will need to save the API key found in the [account](https://newsapi.org/account) page.

1. Create an account on [AWS](https://aws.amazon.com/). This will make you set up your account with a credit card and other information.

1. Set up your credentials file on you local machine. In order to use any AWS APIs, you will need to set up a credentials file on your machine. First, create a new set of keys by going to the [credentials](https://console.aws.amazon.com/iam/home?region=us-east-2#/security_credentials) page of your AWS console, and traversing to the 'Access keys' tab. Next, you will need to place this content in a credentials file located at *~/.aws/credentials* on Linux, macOS, or Unix and *C:\Users\USERNAME\.aws\credentials* on Windows. The contents of the *credentials* file should appear in the following way:

   ```
   [default]
   aws_access_key_id = your_access_key_id
   aws_secret_access_key = your_secret_access_key
   ```

   For more information on how this works, please checkout the following web page: <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html>

## Installation

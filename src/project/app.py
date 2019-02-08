from config.config import Config
from aws.aws_runner import AWS_Runner
from flask import render_template, Flask, Response, redirect, url_for, request, abort
import time

# pip install flask

app = Flask(__name__)

# Set up variables needed for execution
conf = Config()
conf_contents = conf.get_config_contents()

aws = AWS_Runner(conf_contents['AWS Key Name'],
                 conf_contents['AWS Machine Type'],
                 conf_contents['AWS Security Group ID'],
                 conf_contents['AWS Image ID'],
                 conf_contents['Path to pem'])


@app.route("/", methods=["GET"])
def home_get():
    """
    Home page controller. HTML changes based on whether or not a session has
    already been started.
    """
    s = conf.check_session()
    return render_template('home.html', started = s)


@app.route("/", methods=["POST"])
def home_post():
    """
    If there is a session, then we can start the system based on a input topic.
    We redirect to system execution with the input topic.
    """
    t = request.form['topic']
    return redirect(url_for('run_system', topic = t))


@app.route("/setup_instances")
def setup_instances():
    """
    When no session has been created, we can start up ec2 instances and set them
    up to be ready to execute the data analysis system.
    """
    if conf.check_session():
        return redirect(url_for('home_get'))

    # IDs and IPs of the instances we set up for the system
    ids, ips = aws.setup_instances()

    # Create a session and add all information to it
    conf.create_session()

    conf.add_to_session("Twitter Collector ID", ids[0])
    conf.add_to_session("Twitter Collector IP", ips[0])
    conf.add_to_session("News Collector ID", ids[1])
    conf.add_to_session("News Collector IP", ips[1])
    conf.add_to_session("Twitter Analyzer ID", ids[2])
    conf.add_to_session("Twitter Analyzer IP", ips[2])
    conf.add_to_session("News Analyzer ID", ids[3])
    conf.add_to_session("News Analyzer IP", ips[3])
    conf.add_to_session("Database ID", ids[4])
    conf.add_to_session("Database IP", ips[4])

    return redirect(url_for('home_get'))


@app.route("/destroy_instances")
def destroy_instances():
    """
    Stop session and terminate servers.
    """
    if not conf.check_session():
        return redirect(url_for('home_get'))

    aws.end_session(conf.get_session_contents())
    conf.end_session()

    return redirect(url_for('home_get'))


@app.route("/run_system/<topic>")
def run_system(topic):
    """
    Runs the system using the input topic.
    """
    if not conf.check_session():
        return redirect(url_for('home_get'))

    print("Running system with topic:", topic)

    # Run code from executor.py
    ips = [value for key, value in conf.get_session_contents().items() if "IP" in key]
    aws.execute_system(conf.get_session_contents(), conf.get_config_contents(), topic)

    return render_template("results.html")


if __name__ == "__main__":
    app.run()

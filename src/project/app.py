from config.config import Config
from aws.aws_runner import AWS_Runner
from flask import render_template, Flask, Response, redirect, url_for, request, abort
import time


app = Flask(__name__)

conf = Config()
conf_contents = conf.get_config_contents()

aws = AWS_Runner(conf_contents['AWS Key Name'],
                 conf_contents['AWS Machine Type'],
                 conf_contents['AWS Security Group ID'],
                 conf_contents['AWS Image ID'],
                 conf_contents['Path to pem'])


@app.route("/", methods=["GET"])
def home_get():
    s = conf.check_session()
    return render_template('home.html', started = s)


@app.route("/", methods=["POST"])
def home_post():
    t = request.form['topic']
    return redirect(url_for('run_system', topic = t))


@app.route("/setup_instances")
def setup_instances():
    if conf.check_session():
        return redirect(url_for('home_get'))

    ids, ips = aws.setup_instances()

    conf.create_session()

    conf.add_to_session("Twitter Collector ID", ids[0])
    conf.add_to_session("Twitter Collector IP", ips[0])
    conf.add_to_session("News Collector ID", ids[1])
    conf.add_to_session("News Collector IP", ips[1])
    conf.add_to_session("Spark ID", ids[2])
    conf.add_to_session("Spark IP", ips[2])
    conf.add_to_session("Database ID", ids[3])
    conf.add_to_session("Database IP", ips[3])

    return redirect(url_for('home_get'))


@app.route("/destroy_instances")
def destroy_instances():
    if not conf.check_session():
        return redirect(url_for('home_get'))

    aws.end_session(conf.get_session_contents())
    conf.end_session()

    return redirect(url_for('home_get'))


@app.route("/run_system/<topic>")
def run_system(topic):
    if not conf.check_session():
        return redirect(url_for('home_get'))

    print("Running system with topic:", topic)

    # Run code from executor.py

    return render_template("results.html")


if __name__ == "__main__":
    app.run()

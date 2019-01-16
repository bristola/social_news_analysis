from config.config import Config
import setup.instance_setup
from flask import render_template, Flask, Response, redirect, url_for, request, abort
import time


app = Flask(__name__)
conf = Config()


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

    # Run code from instance_setup.py

    # Add ips and other info to the session file
    conf.create_session()

    return redirect(url_for('home_get'))


@app.route("/destroy_instances")
def destroy_instances():
    if not conf.check_session():
        return redirect(url_for('home_get'))

    # Code for removing aws instances
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

import config.config
import setup.instance_setup
from flask import render_template, Flask, Response, redirect, url_for, request, abort

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home_get():
    # Use config.py to determine if instances have been started

    s = True
    return render_template('home.html', started = s)


@app.route("/", methods=["POST"])
def home_post():
    t = request.form['topic']
    return redirect(url_for('run_system', topic = t))


@app.route("/setup_instances")
def setup_instances():
    print("Setting up instances...")
    # Run code from instance_setup.py

    return redirect(url_for('home_get'))


@app.route("/run_system/<topic>")
def run_system(topic):
    print("Running system with topic ", topic)
    # Run code from executor.py

    return render_template("results.html")


if __name__ == "__main__":
    app.run()

#!/usr/bin/env python3.8
from flask import Flask, Response
import flask
import time
import os


SECRET = os.environ["SECRET"]
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "5000"))

app = Flask(__name__)

balance = 0
hold_till = 0


@app.route('/check-allowed/activity')
def check_allowed_acitivity():
    if hold_till > time.time():
        return 'true'
    else:
        return 'false'


@app.route('/form/hold', methods=["GET", "POST"])
def form_hold():
    global balance
    global hold_till

    if flask.request.method == "POST":
        value = int(flask.request.form.get('value', 0)) * 60
        assert balance - value >= 0

        balance -= value

        now = int(time.time())
        if hold_till < now:
            hold_till = now

        hold_till += value

        return flask.redirect("")

    return f"""
    <p>Balance: {balance / 60}</p>
    <p>Hold left: {max(0, (hold_till - time.time()) / 60)} minutes</p>
    
    <form method=post>
        <p><input type=number name=value value="20" /></p>
        <p><input type=submit value=Hold></p>
    </form>
    """


@app.route('/form/add', methods=["GET", "POST"])
def form_add():
    global balance

    if flask.request.method == "POST":
        assert flask.request.form["secret"] == SECRET
        balance += int(flask.request.form.get("value", 0)) * 60
        return flask.redirect("")

    return f"""
    <p>Balance: {balance / 60}</p>
    
    <form method=post>
        <p><input placeholder=secret id=addsecret type=password name=secret /></p>
        <p><input type=number name=value value="10" /></p>
        <p><input type=submit value=Add></p>
    </form>
    
    <script>
        addsecret.onkeyup = e => localStorage.addsecret = addsecret.value
        addsecret.value = localStorage.addsecret
    </script>
    """


@app.route("/form/clear", methods=["GET", "POST"])
def form_clear():
    global hold_till
    global balance

    if flask.request.method == "POST":
        hold_till = balance = 0
        return flask.redirect("")

    return f"""
    <p>Balance: {balance / 60}</p>
    <p>Hold left: {max(0, (hold_till - time.time()) / 60)} minutes</p>

    <form method=post>
        <p><input type=submit value=CLEAR></p>
    </form>
    """


@app.route("/")
def main():
    return """
    <a href=/form/add>ADD</a>
    |
    <a href=/form/hold>HOLD</a>
    |
    <a href=/form/clear>CLEAR</a>
    """


app.run(host=HOST, port=PORT, debug=True)

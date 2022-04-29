from flask import Flask, send_file
from graph_maker import graph
import zipfile
import os
from score_maker import score_maker, test_bd

app = Flask(__name__)


@app.route("/")
def hello_world():
    file_name = graph()
    return send_file(file_name, mimetype="image/png")


@app.route("/score")
def get_score():
    score_maker()
    return send_file("scores-sample.csv", mimetype="file/csv")


@app.route("/bd")
def bd():
    list = test_bd()
    return f"{list}"

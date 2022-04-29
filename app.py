from flask import Flask, send_file
from graph_maker import graph
import zipfile
import os
from score_maker import score_maker

app = Flask(__name__)

if os.path.exists("oracleBasic/"):
    print("ja tem")
else:
    with zipfile.ZipFile("oracleBasic.zip", 'r') as zip_ref:
        zip_ref.extractall("")
    print("descompactado")
    os.remove("oracleBasic.zip")


@app.route("/")
def hello_world():
    file_name = graph()
    return send_file(file_name, mimetype="image/png")


@app.route("/score")
def get_score():
    score_maker()
    return send_file("scores-sample.csv", mimetype="file/csv")

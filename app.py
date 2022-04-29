from flask import Flask, send_file
from graph_maker import graph
import zipfile
import os

app = Flask(__name__)


@app.route("/")
def hello_world():
    file_name = graph()
    return send_file(file_name, mimetype="image/png")


@app.route("/unzip/")
def unzip_oracle():
    if os.path.exists("oracleBasic"):
        return "<b>Already unziped</b>"
    else:
        with zipfile.ZipFile("oracleBasic.zip", 'r') as zip_ref:
            zip_ref.extractall("")
        return "<b>Done, hopefully</b>"

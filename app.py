from flask import Flask, send_file, send_from_directory
from graph_maker import graph_one, graph_multiple
import zipfile
import os
from score_maker import score_maker, test_bd

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
    response.headers['Access-Control-Expose-Headers'] = '*'
    return response


@app.route("/")
def hello_world():
    #file_name = grap()
    #return send_file(file_name, mimetype="image/png")
    return "<h1> Hello World!!!</h1><br><b> Dev was here</b>"


@app.route("/graph/consumo/<cnpj>/")
def graph(cnpj):
    file_name = graph_one(cnpj)
    path = str(os.path.dirname(os.path.abspath(__file__))) + "/graphs/"
    print(path)
    return send_from_directory(path, file_name)


@app.route("/graph/consumo/<cnpj>/<format>/")
def graph_format(cnpj, format):
    file_name = graph_one(cnpj, format)
    path = str(os.path.dirname(os.path.abspath(__file__))) + "/graphs/"
    print(path)
    return send_from_directory(path, file_name)


@app.route("/graphs/consumo/<cnpj1>/<cnpj2>/")
def graph_double(cnpj1, cnpj2):
    file_name = graph_multiple(cnpj1, cnpj2)
    path = str(os.path.dirname(os.path.abspath(__file__))) + "/graphs/"
    print(path)
    return send_from_directory(path, file_name)


@app.route("/graphs/consumo/<cnpj1>/<cnpj2>/<format>/")
def graph_double_format(cnpj1, cnpj2, format):
    file_name = graph_multiple(cnpj1, cnpj2, format)
    path = str(os.path.dirname(os.path.abspath(__file__))) + "/graphs/"
    print(path)
    return send_from_directory(path, file_name)


@app.route("/score/")
def get_score():
    #score_maker()
    #return send_file("scores-sample.csv", mimetype="file/csv")
    return "<b>SORRY, NOT READY YET</b>"


@app.route("/bd/")
def bd():
    list = test_bd()
    return f"{list}"
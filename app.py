from flask import Flask, send_file
from graph_maker import graph_one, graph_multiple
import zipfile
import os
from score_maker import score_maker, test_bd

app = Flask(__name__)


@app.route("/")
def hello_world():
    #file_name = grap()
    #return send_file(file_name, mimetype="image/png")
    return "<h1> Hello World!!!</h1><br><b> Dev was here</b>"


@app.route("/graph/consumo/<cnpj>")
def graph(cnpj):
    file_name = graph_one(cnpj)
    return send_file(file_name, mimetype="image/png")


@app.route("/graph/consumo/<cnpj>/<format>")
def graph_format(cnpj, format):
    file_name = graph_one(cnpj, format)
    return send_file(file_name, mimetype="file/pdf")


@app.route("/graphs/consumo/<cnpj1>/<cnpj2>")
def graph_double(cnpj1, cnpj2):
    file_name = graph_multiple(cnpj1, cnpj2)
    return send_file(file_name, mimetype="image/png")


@app.route("/graphs/consumo/<cnpj1>/<cnpj2>/<format>")
def graph_double_format(cnpj1, cnpj2, format):
    file_name = graph_multiple(cnpj1, cnpj2, format)
    return send_file(file_name, mimetype="file/pdf")



@app.route("/score")
def get_score():
    #score_maker()
    #return send_file("scores-sample.csv", mimetype="file/csv")
    return "<b>SORRY, NOT READY YET</b>"


@app.route("/bd")
def bd():
    list = test_bd()
    return f"{list}"

import pandas
import matplotlib.pyplot as plt

import zipfile
import os
import requests
import json


def graph_multiple(cnpj1, cnpj2, format="png"):
    r1 = requests.get(f"http://localhost:8080/consumo/lista-consumo-empresa/{cnpj1}")
    r2 = requests.get(f"http://localhost:8080/consumo/lista-consumo-empresa/{cnpj2}")
    data1 = r1.json()
    data2 = r2.json()
    if len(data2) > len(data1):
        old_data1 = data1
        data1 = data2
        data2 = old_data1
    for i in range(len(data1)):
        data1[i]["mesReferencia"] = data1[i]["mesReferencia"][:7]
    for i in range(len(data2)):
        data2[i]["mesReferencia"] = data2[i]["mesReferencia"][:7]
    result = pandas.DataFrame(data1)
    result = result.rename(columns={"quantidadeConsumo": f"CNPJ: {cnpj1}", "mesReferencia": "Mês"})
    result = result.set_index("Mês")
    ax = result.plot(color="blue")
    result = pandas.DataFrame(data2)
    result = result.rename(columns={"quantidadeConsumo": f"CNPJ: {cnpj2}", "mesReferencia": "Mês"})
    fig = result.plot(ax=ax, color="green").get_figure()
    if not os.path.exists("graphs"):
        os.mkdir("graphs")
    file_name = f"graphs/consumo-empresas-{cnpj1}-{cnpj2}.{format.lower()}"
    fig.savefig(file_name)
    return file_name


    # data1 = transform_data("export (1).csv", "blue")
    # data2 = transform_data("export (2).csv", "red")
    # print(data1["df"])
    # for i in data2["df"]:
    #     data1["df"].append(i)
    #
    # print(data1["df"])
    #
    # #fig = data1["df"].plot(x="", y=data1["cnpj"], kind="line", figsize=(5, 4)).get_figure()
    #
    # result = {"data": [data1["df"], data2["df"]], "month": [1, 2, 3, 4, 5, 6]}
    # result = pandas.DataFrame(data1["df"], columns=["colors", "y", "x"])
    # result = result.pivot(index="x", columns="colors", values="y")
    # #fig = result.plot(x="data", y="month", kind="line").get_figure()
    # fig = result.plot(color=result.columns).get_figure()
    #
    #
    # #plt.show()
    # name = f"consumos-{data1['cnpj']}.png"
    # fig.savefig(name)
    # return name


# No momento recebe csv porque é teste. Mudar porque irá receber um dict
def transform_data(csv, color="blue"):
    # Pega os dados e ordena de uma forma que eu quero
    data = pandas.read_csv(csv)
    print(data)
    print(type(data))
    dict = []
    consumos = []
    cnpj = ""
    for i in data.iterrows():
        dict.append({"": i[1][0][:7], i[1][1]: i[1][2]})
        cnpj = i[1][1]
        consumos.append([cnpj, i[1][2], i[1][0][:7]])
    df = pandas.DataFrame(dict)
    df.to_csv(f"consumo-{cnpj}.csv", ";", index=False)
    # Retorna um dict com uma lista dos consumos[cnpj, consumo, mes], o valor do cnpj e a cor
    return {"df": consumos, "cnpj": cnpj, "color": color}


def transform(data, color="blue"):
    # Pega os dados e ordena de uma forma que eu quero
    print(data)
    print(type(data))
    dict = []
    consumos = []
    cnpj = ""
    for i in data:
        dict.append({"": i[1][0][:7], i[1][1]: i[1][2]})
        cnpj = i[1][1]
        consumos.append([cnpj, i[1][2], i[1][0][:7]])
    df = pandas.DataFrame(dict)
    df.to_csv(f"consumo-{cnpj}.csv", ";", index=False)
    # Retorna um dict com uma lista dos consumos[cnpj, consumo, mes], o valor do cnpj e a cor
    return {"df": consumos, "cnpj": cnpj, "color": color}


def graph_one(cnpj=11924000193, format="png"):
    # Pega os dados utilizando endpoint do spring
    r = requests.get(f"http://localhost:8080/consumo/lista-consumo-empresa/{cnpj}")
    print(r.json()[0])
    data = r.json()
    #data = r.json()[0]
    # Transformar os dados da request em df
    # do stuff here. Bim, Bam, Boom!

    # Usando dados do csv de exemplo
    #test_dict = transform_data("export (1).csv", "green")
    # A ordem que utilizo é:
    # DataFrame( lista de dicts, columns=[ nome da linha no grafico, nome de referencia pro values, nome do eixo X]
    for i in range(len(data)):
        data[i]["mesReferencia"] = data[i]["mesReferencia"][:7]
    result = pandas.DataFrame(data)
    result = result.rename(columns={"quantidadeConsumo": f"CNPJ: {cnpj}", "mesReferencia": "Mês"})
    result = result.set_index("Mês")
    print(result)
    # pivot( eixo X, eixo Y, nome de referencia usado acima)
    fig = result.plot().get_figure()
    print(result)
    #fig = result.plot(color="blue").get_figure()
    if not os.path.exists("graphs"):
        os.mkdir("graphs")
    file_name = f"consumo-empresa-{cnpj}.{format.lower()}"
    fig.savefig(f"graphs/{file_name}")
    return file_name


if __name__ == '__main__':
    #graph(11924000193)
    #graph_one()
    graph_multiple(11924000193, 97554065000110)

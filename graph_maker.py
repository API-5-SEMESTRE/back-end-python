import pandas
import matplotlib.pyplot as plt

import zipfile
import os
import requests

def graph_multiple(cnpj):
    r = requests.get(f"http://localhost:8080/consumo/consumo-por-cnpj/{cnpj}")
    print(r.json())
    data1 = transform_data("export (1).csv", "blue")
    data2 = transform_data("export (2).csv", "red")
    print(data1["df"])
    for i in data2["df"]:
        data1["df"].append(i)

    print(data1["df"])

    #fig = data1["df"].plot(x="", y=data1["cnpj"], kind="line", figsize=(5, 4)).get_figure()

    result = {"data": [data1["df"], data2["df"]], "month": [1, 2, 3, 4, 5, 6]}
    result = pandas.DataFrame(data1["df"], columns=["colors", "y", "x"])
    result = result.pivot(index="x", columns="colors", values="y")
    #fig = result.plot(x="data", y="month", kind="line").get_figure()
    fig = result.plot(color=result.columns).get_figure()


    #plt.show()
    name = f"consumos-{data1['cnpj']}.png"
    fig.savefig(name)
    return name


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


def graph_one(cnpj=11924000193, format="png"):
    # Pega os dados utilizando endpoint do spring
    #r = requests.get(f"http://localhost:8080/consumo/consumo-por-cnpj/{cnpj}")
    #print(r.json())
    #data = r.json()[0]
    # Transformar os dados da request em df
    # do stuff here. Bim, Bam, Boom!

    # Usando dados do csv de exemplo
    test_dict = transform_data("export (1).csv", "green")
    # A ordem que utilizo é:
    # DataFrame( lista de dicts, columns=[ nome da linha no grafico, nome de referencia pro values, nome do eixo X]
    result = pandas.DataFrame(test_dict["df"], columns=["Consumo - CNPJ", "consumo", "Periodo"])
    # pivot( eixo X, eixo Y, nome de referencia usado acima)
    result = result.pivot(index="Periodo", columns="Consumo - CNPJ", values="consumo")
    fig = result.plot(color=test_dict["color"]).get_figure()
    file_name = f"graphs/test-{cnpj}.{format.lower()}"
    fig.savefig(file_name)
    return file_name


if __name__ == '__main__':
    #graph(11924000193)
    graph_one(format="pdf")

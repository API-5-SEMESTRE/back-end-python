import pandas
import matplotlib.pyplot as plt

import zipfile
import os

def graph():
    data1 = get("export (1).csv", "blue")
    data2 = get("export (2).csv", "red")
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

def get(csv, color):
    data = pandas.read_csv(csv)
    print(data)
    print(type(data))
    dict = []
    con = []
    cnpj = ""
    for i in data.iterrows():
        dict.append({"": i[1][0][:7], i[1][1]: i[1][2]})
        cnpj = i[1][1]
        con.append([color, i[1][2], i[1][0][:7]])
    df = pandas.DataFrame(dict)
    df.to_csv(f"consumo-{cnpj}.csv", ";", index=False)
    return {"df": con, "cnpj": cnpj}


def graph_one_consumo(cnpj):
    pass
    # do stuff here


if __name__ == '__main__':
    graph()
    if os.path.exists("oracleBasic/"):
        print("ja tem")
    else:
        with zipfile.ZipFile("oracleBasic.zip", 'r') as zip_ref:
            zip_ref.extractall("")
        print("descompactado")

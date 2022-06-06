import sklearn
from sklearn import linear_model
import pandas
import numpy
import cx_Oracle
import os


def linear_regression():
    data = pandas.read_csv("prepared_data.csv", sep=";")
    X = numpy.array(data[["origem", "cnae_id", "regiao", "estado", "media_score",
                          "30/09/2021 00:00", "31/10/2021 00:00", "30/11/2021 00:00", "31/12/2021 00:00",
                          "31/01/2022 00:00"]])
    y = numpy.array(data[["28/02/2022 00:00"]])
    model = linear_model.LinearRegression()
    model.fit(X, y)
    predictions = model.predict(data[["origem", "cnae_id", "regiao", "estado", "media_score",
                                      "30/09/2021 00:00", "31/10/2021 00:00", "30/11/2021 00:00", "31/12/2021 00:00",
                                      "31/01/2022 00:00"]])
    scores = []
    for item in numpy.array(data["total_score"]):
        scores.append(int(item))
    counter = 1
    new_consumos = []
    for i in predictions:
        i = int(i)
        i = prediction_adjuster(i, scores[counter - 1])
        counter += 1
        print(f"POS[{counter}] -> {i}")
        new_consumos.append(i)
    data["31/03/2022 00:00"] = new_consumos
    data.to_csv("predicted_consumo.csv", sep=";")


def prediction_adjuster(value, score):
    value = value * (score * 0.002)
    if value > 3500:
        value = value - (score * 1.5)
    elif value < 1200:
        value = value - (score * 1.5)
    if value < 0:
        value = 0
    return int(value)


def column_change(data_frame):
    data_to_append = pandas.read_csv("scores-sample.csv", sep=";")
    print(data_to_append)
    estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR",
               "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",]
    regions = ["sudeste", "nordeste", "sul", "centro-oeste", "norte"]
    origem = ["SPC", "CONCORRENTE", "LIVRE"]
    print(estados)
    data = data_to_append.to_dict("records")
    for item in data:
        print(item)
        print(item["estado"])
        print(estados.index("AC"))
        try:
            print(estados.index("AC"))
            item["origem"] = origem.index(item["origem"])
            item["estado"] = estados.index(item["estado"])
            item["regiao"] = regions.index(item["regiao"].lower())
        except:
            pass
        print(item)

    df = pandas.DataFrame(data)
    df.to_csv("prepared_data.csv", sep=";", index=False)
    return "a"


def make_csv():
    db202203301935_low = '(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.sa-saopaulo-1.oraclecloud.com))(connect_data=(service_name=g5a8d282e2d63db_db202203301935_low.adb.oraclecloud.com))(security=(ssl_server_cert_dn="CN=adb.sa-saopaulo-1.oraclecloud.com, OU=Oracle ADB SAOPAULO, O=Oracle Corporation, L=Redwood City, ST=California, C=US")))'
    cx_Oracle.init_oracle_client(lib_dir=os.path.dirname(os.path.abspath(__file__)) + "/oracleBasic")
    connection = cx_Oracle.connect(user="ADMIN", password="BDrelacional5", dsn="db202203301935_low", encoding="utf8",
                                   nencoding="utf8")
    cursor = connection.cursor()
    c = cursor.execute(
        "SELECT C.CONS_MESREF, C.EMP_CNPJ, C.CONS_CONSUMO, E.CNAE_ID, E.EMP_ORIGEM, CI.CID_REG_IBGE, CI.CID_SIGLA_ESTADO FROM CONSUMO C INNER JOIN EMPRESA E ON E.EMP_CNPJ = C.EMP_CNPJ INNER JOIN CIDADE CI ON E.CID_ID = CI.CID_ID INNER JOIN CNAE CN ON CN.CNAE_ID = E.CNAE_ID ORDER BY C.EMP_CNPJ, C.CONS_MESREF")
    query_list = []
    for i in c:
        query_list.append(i)
    data = []
    for i in query_list:
        data.append({"CNPJ": data[1], "CNAE_ID": data[3], "EMP_ORIGEM": "a"})


if __name__ == '__main__':
    # column_change("a")
    linear_regression()

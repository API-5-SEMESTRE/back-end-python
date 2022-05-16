import json

import pandas
import matplotlib.pyplot as plt
import cx_Oracle
import os
from time import time
import time
from random import randint
import json


#ToDo analisar consumo, tipooo, bastante em pouco tempo é mt bom
#ToDo pegar os dados do consumo e verificar o cnpj pra ver o cnae

client = False
db202203301935_low = '(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.sa-saopaulo-1.oraclecloud.com))(connect_data=(service_name=g5a8d282e2d63db_db202203301935_low.adb.oraclecloud.com))(security=(ssl_server_cert_dn="CN=adb.sa-saopaulo-1.oraclecloud.com, OU=Oracle ADB SAOPAULO, O=Oracle Corporation, L=Redwood City, ST=California, C=US")))'


def init_client():
    cx_Oracle.init_oracle_client(lib_dir=os.path.dirname(os.path.abspath(__file__)) + "/oracleBasic")
    global client
    client = True


def analyse_consumo(consumo_separated, region):
    regions = ["sudeste", "nordeste", "sul", "centro-oeste", "norte"]
    region_multiplier = regions.index(region.lower()) + 1
    score = []
    multiplier = 0.20 + region_multiplier * 0.011
    size = len(consumo_separated)
    # Números inventandos, eu queria limitar as variaveis desse "score" pro maximo ser 4 e o mínimo 0.3
    # Se for num "streak" de coisas ruins (menos q o mes passado e valor mt baixo) é punido baseado no consumo da vez
    # Streak alto eleva baseado no consumo da vez. Assim achei q ficou mais dinamico e mais interessante
    for valor in consumo_separated:
        if sum(score) > 60:
            print(f"Score high! {sum(score)}")
            multiplier = 0.20 + region_multiplier * 0.005
        if consumo_separated.index(valor) == 0:
            pass
        else:
            if valor >= consumo_separated[consumo_separated.index(valor) - 1] * 1.15:
                score.append(2.7)
                if valor >= 2300:
                    score.append(3.7 + valor * 0.005 + region_multiplier * 2.5)
                elif valor >= 1400:
                    score.append(1.7)
                elif valor >= 800:
                    score.append(0.7 + region_multiplier - 3)
                else:
                    score.append(0.4 - valor * 0.007 + (region_multiplier * 0.4 - 1.7))
            elif valor <= consumo_separated[consumo_separated.index(valor) - 1] * 0.75:
                score.append(1)
                if valor >= 2300:
                    score.append(2.7 + valor * 0.005 + region_multiplier * 2.5)
                elif valor >= 1400:
                    score.append(1.5)
                elif valor >= 800:
                    score.append(0.7 + region_multiplier - 3)
                else:
                    score.append(0.4 - valor * 0.007 + (region_multiplier * 0.4 - 1.7))
            else:
                score.append(1.5)
                if valor >= 2300:
                    score.append(2.7 + valor * 0.005 + region_multiplier * 2.5)
                elif valor >= 1400:
                    score.append(1.5)
                elif valor >= 800:
                    score.append(0.7 + region_multiplier - 3)
                else:
                    score.append(0.3 - valor * 0.007 + (region_multiplier * 0.4 - 1.7))
    # Faz uma média desse "score" e do consumo pra gerar um score final.
    # Vendo quem tem mais scorefinal da pra conferir se tem outras empresas de ramos semelhantes do concorrente ou livre
    #print(f"soma {(sum(score) / size) * 20} -- consumos {(sum(consumo_separated) / size) * multiplier}")
    final_score = (sum(score) / size) * 20 + (sum(consumo_separated) / size) * multiplier
    if final_score > 1000:
        final_score = 1000
    return [int(final_score), int((sum(score) / size) * 20)]


def score_maker():
    print("start")
    start = time.time()

    global client
    if not client:
        init_client()
    global db202203301935_low

    connection = cx_Oracle.connect(user="ADMIN", password="BDrelacional5", dsn="db202203301935_low")
    print(cx_Oracle.version)
    cursor = connection.cursor()

    # Pega os dados do consumo baseado
    # c = cursor.execute("SELECT * FROM consumo c INNER JOIN empresa e ON e.emp_cnpj = c.emp_cnpj WHERE e.emp_origem = 'CONCORRENTE'")
    # conc = []
    # for i in c:
    #     conc.append(i)

    #1500 empresas do consumo_table e conc, cada


    #c = cursor.execute("SELECT * FROM consumo c INNER JOIN empresa e ON e.emp_cnpj = c.emp_cnpj ORDER BY c.emp_cnpj, c.cons_mesref")
    c = cursor.execute("SELECT C.CONS_MESREF, C.EMP_CNPJ, C.CONS_CONSUMO, E.CNAE_ID, E.EMP_ORIGEM, CI.CID_REG_IBGE FROM CONSUMO C INNER JOIN EMPRESA E ON E.EMP_CNPJ = C.EMP_CNPJ INNER JOIN CIDADE CI ON E.CID_ID = CI.CID_ID ORDER BY C.EMP_CNPJ, C.CONS_MESREF")
    consumo_table = []
    for i in c:
        consumo_table.append(i)
        print(i)
    #print(consumo_table)

    plot = []
    consumo = []
    score = []
    for data in consumo_table:
        if consumo_table.index(data) + 1 == len(consumo_table):
            #print(data[2])
            consumo.append(data[2])
            #print(f"TOTAL DO CLIENTE {data[1]} - {sum(consumo)}")
            sc = analyse_consumo(consumo, data[5])
            #print(f"SCORE: {sc}\n-------------------")
            score.append({"total_consumo": sum(consumo), "media_consumo": int(sum(consumo) / len(consumo)), "total_score": sc[0], "media_score": sc[1], "consumos": consumo, "cnpj": data[1], "origem": data[4], "regiao": data[5]})
            consumo = []
        else:
            if data[1] == consumo_table[consumo_table.index(data) + 1][1]:
                #print(data[2])
                consumo.append(data[2])
            else:
                #print(data[2])
                consumo.append(data[2])
                #print(f"TOTAL DO CLIENTE {data[1]} - {sum(consumo)}")
                sc = analyse_consumo(consumo, data[5])
                #print(f"SCORE: {sc}\n-------------------")
                score.append({"total_consumo": sum(consumo), "media_consumo": int(sum(consumo)/len(consumo)), "total_score": sc[0], "media_score": sc[1], "consumos": consumo, "cnpj": data[1], "origem": data[4], "regiao": data[5]})
                consumo = []

    print(len(score))
    for i in score:
        pass
        #print(i)


    # c = cursor.execute("SELECT * FROM cidade")
    # for i in c:
    #     print(i)


    df = pandas.DataFrame(score)
    df.to_csv("scores-sample.csv", index=False, columns=["origem", "cnpj", "regiao", "media_consumo", "total_consumo", "media_score", "total_score"], sep=";")


    cursor.close()
    connection.close()

    end = time.time()
    print(f"finish\nTime: {end - start}")


def test_bd():
    global client
    if not client:
        init_client()
    global db202203301935_low
    connection = cx_Oracle.connect(user="ADMIN", password="BDrelacional5", dsn="db202203301935_low")
    print(cx_Oracle.version)
    cursor = connection.cursor()
    c = cursor.execute("SELECT * FROM cidade FETCH FIRST 20 ROWS ONLY")
    list = []
    for i in c:
        print(i)
        list.append(i)
    return list


def test_with_json():
    f = open("export2.json")
    json_ = json.load(f)
    consumo = []
    score = []
    regiao = []
    for data in json_:
        if json_.index(data) + 1 == len(json_):
            consumo.append(data["cons_consumo"])
            sc = analyse_consumo(consumo)
            score.append({"total_consumo": sum(consumo), "media_consumo": int(sum(consumo) / len(consumo)),
                          "total_score": sc[0], "media_score": sc[1],
                          "consumos": consumo, "cnpj": data["emp_cnpj"],
                          "origem": data["emp_origem"], "regiao": data["cid_reg_ibge"]})
            consumo = []
        else:
            if data["emp_cnpj"] == json_[json_.index(data) + 1]["emp_cnpj"]:
                consumo.append(data["cons_consumo"])
            else:
                consumo.append(data["cons_consumo"])
                sc = analyse_consumo(consumo)
                if sc[0] > 00:
                    regiao.append({"regiao": data["cid_reg_ibge"], "score": sc[0]})
                score.append({"total_consumo": sum(consumo), "media_consumo": int(sum(consumo) / len(consumo)),
                          "total_score": sc[0], "media_score": sc[1],
                          "consumos": consumo, "cnpj": data["emp_cnpj"],
                          "origem": data["emp_origem"], "regiao": data["cid_reg_ibge"]})
                consumo = []

    centro = 0
    norte = 0
    nordeste = 0
    sul = 0
    sudeste = 0
    for i in regiao:
        if i["regiao"] == "CENTRO-OESTE":
            centro += 1
        elif i["regiao"] == "NORDESTE":
            nordeste += 1
        elif i["regiao"] == "NORTE":
            norte += 1
        elif i["regiao"] == "SUDESTE":
            sudeste += 1
        elif i["regiao"] == "SUL":
            sul += 1
    print(f"CENTRO-{centro}\nNORDESTE-{nordeste}\nNORTE-{norte}\nSUDESTE-{sudeste}\nSUL-{sul}")

    df = pandas.DataFrame(regiao)
    df.to_csv("regiao.csv", index=False, sep=";")

    # df = pandas.DataFrame(score)
    # df.to_csv("scores-sample.csv", index=False,
    #           columns=["origem", "cnpj", "media_consumo", "total_consumo", "media_score", "total_score", "regiao"], sep=";")

def consumo_regiao():
    global client
    if not client:
        init_client()
    global db202203301935_low

    connection = cx_Oracle.connect(user="ADMIN", password="BDrelacional5", dsn="db202203301935_low")
    print(cx_Oracle.version)
    cursor = connection.cursor()
    c = cursor.execute(
        "SELECT C.CONS_MESREF, C.EMP_CNPJ, C.CONS_CONSUMO, E.CNAE_ID, E.EMP_ORIGEM, CI.CID_REG_IBGE FROM CONSUMO C INNER JOIN EMPRESA E ON E.EMP_CNPJ = C.EMP_CNPJ INNER JOIN CIDADE CI ON E.CID_ID = CI.CID_ID ORDER BY C.EMP_CNPJ, C.CONS_MESREF")
    consumo_table = []
    for data in c:
        consumo_table.append(data)

    centro = 0
    centroc = 0
    norte = 0
    nortec = 0
    nordeste = 0
    nordestec = 0
    sul = 0
    sulc = 0
    sudeste = 0
    sudestec = 0
    for data in consumo_table:
        if data[2] < 250:
            if data[5] == "CENTRO-OESTE":
                centro += data[2]
                centroc += 1
            elif data[5] == "NORDESTE":
                nordeste += data[2]
                nordestec += 1
            elif data[5] == "NORTE":
                norte += data[2]
                nortec += 1
            elif data[5] == "SUDESTE":
                sudestec += 1
                sudeste += data[2]
            elif data[5] == "SUL":
                sul += data[2]
                sulc += 1
    print(f"CENTRO-{centro}\nNORDESTE-{nordeste}\nNORTE-{norte}\nSUDESTE-{sudeste}\nSUL-{sul}")
    print("-"*30)
    print(f"CENTRO-{centroc}\nNORDESTE-{nordestec}\nNORTE-{nortec}\nSUDESTE-{sudestec}\nSUL-{sulc}")





if __name__ == '__main__':
    #test_with_json()
    score_maker()
    #consumo_regiao()
    pass

from pymongo import MongoClient
from datetime import datetime, timedelta

def get_inicio_fim_mes(ano, mes):
    # Verificar se o ano é bissexto
    if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0):
        dias_mes = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        dias_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Definir a data de início do mês
    inicio_mes = datetime(ano, mes, 1)

    # Definir a data de fim do mês
    fim_mes = datetime(ano, mes, dias_mes[mes - 1], 23, 59, 59)

    return inicio_mes, fim_mes

client = MongoClient("mongodb+srv://administrador:administrador@economax.wa1uot6.mongodb.net/test")
db = client.Economax
collection = db.gastos
ano = 2023
mes = 6
inicio_mes, fim_mes = get_inicio_fim_mes(ano, mes)
query = {
    'data': {
        '$gte': inicio_mes.strftime("%Y-%m-%d %H:%M:%S"),
        '$lte': fim_mes.strftime("%Y-%m-%d %H:%M:%S")
    },
    'usuario_id': '645302f56527cb0c75783f89'
}

# # Buscar os documentos que correspondem à consulta
# result = collection.find(query)

# # Iterar sobre os documentos e imprimir os resultados
# for document in result:
#     print(document)

print(collection.count_documents(query))
from flask import Flask, jsonify, request
import pymongo
from bson import ObjectId
from datetime import datetime, timedelta
import pytz
import json

client = pymongo.MongoClient("mongodb+srv://administrador:administrador@cluster0.8vjnvh9.mongodb.net/test")
db = client['Economax']

def dataNow():
    fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')
    data_hora_atual_brasilia = datetime.now(fuso_horario_brasilia)
    data_hora_formatada = data_hora_atual_brasilia.strftime("%Y-%m-%d %H:%M:%S")
    return data_hora_formatada

def cadastro(user_crypt, password_crypt):    
    try:
        users = db.users
        if db.users.count_documents({'usuario': user_crypt, 'senha': password_crypt}) > 0:
            return {'Message': 'Usuário já existe!'}
        else:
            usuario = {
                "usuario": user_crypt,
                "senha": password_crypt,
            }
            user_id = users.insert_one(usuario).inserted_id
            
            return {'Message': 'Usuário cadastrado com sucesso!', 'id': str(user_id)}
    except Exception as ex:
        return {'Message': 'Ocorreu um erro ao inserir o usuário!', 'Descrição': str(ex)}

def login(username, password):
    try:
        users = db.users
        user = users.find_one({'usuario': username})
        if user and user['senha'] == password:
            return {'id_usuario': str(user['_id']),'Message': 'Usuário autenticado com sucesso!'}            
        else:
            return {'Message': 'Usuário ou senha incorretos!'}
    except Exception as ex:
        return {'Message': 'Um erro ocorreu!', 'Descrição': str(ex)}

def categorias_despesas_geral():
    try:
        categorias = db.categorias_despesas_geral.find()
        
        resposta = []
        
        for categoria in categorias:
            dicionario = {"id": str(categoria['_id']),"categoria": categoria['nome']}
            resposta.append(dicionario)

        return jsonify(resposta)
    except Exception as ex:
        return {'Message': 'Um erro ocorreu!', 'Descrição': str(ex)}

def categorias_rendimentos_geral():
    try:
        categorias = db.categorias_rendimentos_geral.find()
        
        resposta = []
        
        for categoria in categorias:
            dicionario = {"id": str(categoria['_id']),"categoria": categoria['nome']}
            resposta.append(dicionario)

        return jsonify(resposta)
    except Exception as ex:
        return {'Message': 'Um erro ocorreu!', 'Descrição': str(ex)}

def cadastro_categorias(nome_categoria, usuario_id):
    data_hora_formatada = dataNow()
    
    if db.categorias_despesas_geral.count_documents({'nome': nome_categoria}) > 0:
        return {'message': 'Categoria já está cadastrada!'}

    categoria = {'nome': nome_categoria, 'users_id': usuario_id, 'data': data_hora_formatada}
    categoria_id = db.categorias_despesas_geral.insert_one(categoria).inserted_id
    
    categoria_criada = db.categorias_despesas_geral.find_one({'_id': categoria_id}, {'_id': 1, 'nome': 1})
    return {'id': str(categoria_criada['_id']), 'categoria': categoria_criada['nome']}

def cadastro_categorias_rendimentos(nome_categoria, usuario_id):
    data_hora_formatada = dataNow()
    
    if db.categorias_rendimentos_geral.count_documents({'nome': nome_categoria}) > 0:
        return {'message': 'Categoria já está cadastrada!'}

    categoria = {'nome': nome_categoria, 'users_id': usuario_id, 'data': data_hora_formatada}
    categoria_id = db.categorias_rendimentos_geral.insert_one(categoria).inserted_id
    
    categoria_criada = db.categorias_rendimentos_geral.find_one({'_id': categoria_id}, {'_id': 1, 'nome': 1})
    return {'id': str(categoria_criada['_id']), 'categoria': categoria_criada['nome']}

def cadastro_categorias_usuario(id_usuario, categorias):
    try:
        cadastrar_categorias = db.cadastrar_categorias_usuario
        
        for categoria in categorias:
            categoria_id = categoria
            
            if cadastrar_categorias.count_documents({'users_id': id_usuario, 'categorias_id': categoria_id['id']}) == 0:
                nova_categoria = {
                    "users_id": id_usuario,
                    "categorias_id": categoria_id['id']
                }
                cadastrar_categorias.insert_one(nova_categoria)

        return {'message': 'Categorias inseridas com sucesso!'}
        
    except Exception as ex:
        return {'message': 'Um erro ocorreu!', 'descrição': str(ex)}
    
def cadastro_categorias_rendimentos_usuario(id_usuario, categorias):
    try:
        cadastrar_categorias = db.cadastro_categorias_rendimentos_usuario
        
        for categoria in categorias:
            categoria_id = categoria
            
            if cadastrar_categorias.count_documents({'users_id': id_usuario, 'categorias_id': categoria_id['id']}) == 0:
                nova_categoria = {
                    "users_id": id_usuario,
                    "categorias_id": categoria_id['id']
                }
                cadastrar_categorias.insert_one(nova_categoria)

        return {'message': 'Categorias inseridas com sucesso!'}
        
    except Exception as ex:
        return {'message': 'Um erro ocorreu!', 'descrição': str(ex)}
   
def busca_categorias_despesas_geral_usuario(user_id):
    categorias_usuario = db['cadastrar_categorias_usuario']
    categorias_geral = db['categorias_despesas_geral']

    categorias_user = categorias_usuario.find({'users_id': user_id})
    categorias = []
    for categoria in categorias_user:
        categoria_geral = categorias_geral.find_one({'_id': ObjectId(categoria['categorias_id'])})
        categorias.append({
            'id': str(categoria_geral['_id']),
            'categoria': categoria_geral['nome']
        })

    return jsonify(categorias)

def busca_categorias_rendimentos_geral_usuario(user_id):
    categorias_usuario = db['cadastro_categorias_rendimentos_usuario']
    categorias_geral = db['categorias_rendimentos_geral']

    categorias_user = categorias_usuario.find({'users_id': user_id})
    categorias = []
    for categoria in categorias_user:
        categoria_geral = categorias_geral.find_one({'_id': ObjectId(categoria['categorias_id'])})
        categorias.append({
            'id': str(categoria_geral['_id']),
            'categoria': categoria_geral['nome']
        })

    return jsonify(categorias)

def cadastro_gastos_usuario(registros_gastos, usuario_id):
    gastos = db.gastos    
    data_hora_formatada = dataNow()
    
    for registro in registros_gastos:
     
        categoria_id = registro['id_categoria'].lower()
        valor = registro['valor']
        descricao = registro['descricao']
        
        novo_gasto = {'categoria_despesa_id': categoria_id, 'usuario_id': usuario_id, 'valor': valor, 'descricao': descricao, 'data': data_hora_formatada}

        gasto_id = gastos.insert_one(novo_gasto)
        
    return {'message': 'Gastos inseridos com sucesso!'}
    
def ultimas_despesas_usuario(dias, users_id):
    gastos = db.gastos.find({'usuario_id': users_id})    
    resultado = []
    for gasto in gastos:
        categoria_id = gasto['categoria_despesa_id']
        categoria = db.categorias_despesas_geral.find_one({'_id': ObjectId(categoria_id)})
        resultado.append({
        'categoria': categoria['nome'],
        'valor': gasto['valor'].replace(',', ''),
        'data': gasto['data'],            
        'descricao': gasto.get('descricao', '')
        })
    
    if (dias==""):
        dias = 0
        data_atual = (datetime.now() - timedelta(days=int(dias))).replace(hour=0, minute=0, second=0)
        data_limite = data_atual.strftime("%Y-%m-01 00:00:00")
        data_limite = datetime.strptime(data_limite, '%Y-%m-%d %H:%M:%S')
    else:
        data_atual = datetime.now()
        data_limite = datetime(data_atual.year, data_atual.month, data_atual.day, 0, 0, 0) - timedelta(days=int(dias))
    
    lista_filtrada = []

    for item in resultado:
        data_item = datetime.strptime(item['data'], '%Y-%m-%d %H:%M:%S')
        if data_item >= data_limite:
            lista_filtrada.append(item)

    return jsonify(lista_filtrada)

def ultimas_despesas_usuario_mes_atual_sintetico(users_id):
    gastos = db.gastos.find({'usuario_id': users_id})
    resultado = []
    for gasto in gastos:
        categoria_id = gasto['categoria_despesa_id']
        categoria = db.categorias_despesas_geral.find_one({'_id': ObjectId(categoria_id)})
        resultado.append({
            'categoria': categoria['nome'],
            'valor': gasto['valor'].replace(',', '')            
        })

    return jsonify(resultado)

def gastos_categoria_usuario(usuario_id, dias):
    collection_gastos = db['gastos']
    collection_categorias = db['categorias_despesas_geral']

    if (dias == ""):
        dias = 0
        data_inicio = (datetime.now() - timedelta(days=int(dias))).replace(hour=0, minute=0, second=0)
        data_inicio_formatada = data_inicio.strftime("%Y-%m-01 00:00:00")
    else:
        data_inicio = (datetime.now() - timedelta(days=int(dias))).replace(hour=0, minute=0, second=0)
        data_inicio_formatada = data_inicio.strftime("%Y-%m-%d %H:%M:%S")

    query = {
        'usuario_id': usuario_id,
        'data': {'$gte': data_inicio_formatada}
    }

    result = collection_gastos.aggregate([
        {'$match': query},
        {'$group': {'_id': '$categoria_despesa_id', 'total': {'$sum': {'$toInt': '$valor'}}}}
    ])

    soma_gastos_por_categoria = {}
    for categoria in result:
        categoria_id = categoria['_id']
        total = categoria['total']
        nome_categoria = collection_categorias.find_one({'_id': ObjectId(categoria_id)})['nome']
        soma_gastos_por_categoria[nome_categoria] = total

    # Construindo o dicionário de resultados
    resultados = {}
    for categoria, total in soma_gastos_por_categoria.items():
        resultados[categoria] = total

    # Convertendo para JSON
    json_resultados = jsonify(resultados)

    # Exibindo o resultado JSON
    print(json_resultados)
    return json_resultados

def soma_total_gastos_por_usuario_por_dia(usuario_id, dias):
    collection = db['gastos']

    if (dias == ""):
        dias = 0
        data_inicio = (datetime.now() - timedelta(days=int(dias))).replace(hour=0, minute=0, second=0)
        data_inicio_formatada = data_inicio.strftime("%Y-%m-01 00:00:00")
    else:
        data_inicio = (datetime.now() - timedelta(days=int(dias))).replace(hour=0, minute=0, second=0)
        data_inicio_formatada = data_inicio.strftime("%Y-%m-%d %H:%M:%S")

    query = {
        'usuario_id': usuario_id,
        'data': {'$gte': data_inicio_formatada}
    }
    
    # Executando a consulta e calculando a soma dos gastos
    result = collection.aggregate([
        {'$match': query},
        {'$group': {'_id': None, 'total': {'$sum': {'$toInt': '$valor'}}}}
    ])

    # Obtendo o resultado da soma
    soma_gastos = next(result, {'total': 0})['total']

    data = {
    "Total": soma_gastos
    }
    
    json_data = jsonify(data)
    return json_data

# a = cadastro("Alexsander","1234")
# print(a)
# b = login("jheTeste","1234")
# print(b)
# c = cadastro_categorias("Uber",str(b['id_usuario']))
# print(c)
# try:
#     d = cadastro_categorias_usuario(str(b['id_usuario']),[str(c['id'])])
#     print(d)
# except:
#     pass
# try:
#     e = cadastro_gastos_usuario(str(c['id']),str(b['id_usuario']),"40,00",datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
#     print(e)
# except:
#     e = cadastro_gastos_usuario("6452bdf124f58c5f5ed55b89",str(b['id_usuario']),"40,00",datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
#     print(e)
# f = ultimas_despesas_usuario(1,str(b['id_usuario']))
# print(f)
# g = ultimas_despesas_usuario_mes_atual_sintetico(str(b['id_usuario']))
# print(g)

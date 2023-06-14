from flask import Flask, jsonify, request
import pymongo
from bson import ObjectId
from datetime import datetime, timedelta
import pytz
import json
import jwt

client = pymongo.MongoClient("mongodb+srv://administrador:administrador@economax.wa1uot6.mongodb.net/test")
db = client['Economax']

def get_inicio_fim_mes(ano, mes):
    if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0):
        dias_mes = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        dias_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    inicio_mes = datetime(ano, mes, 1)
    fim_mes = datetime(ano, mes, dias_mes[mes - 1], 23, 59, 59)
    return inicio_mes, fim_mes

def dataNow():
    fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')
    data_hora_atual_brasilia = datetime.now(fuso_horario_brasilia)
    data_hora_formatada = data_hora_atual_brasilia.strftime("%Y-%m-%d %H:%M:%S")
    return data_hora_formatada

def cadastro(user_login, user_crypt, password_crypt):    
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
            
            payload = {'id_usuario': str(user_id), 'usuario': user_login}
            jwt_token = jwt.encode(payload, "Economax", algorithm='HS256')
            
            return {'Message': 'Usuário cadastrado com sucesso!', 'jwt': jwt_token}
    except Exception as ex:
        return {'Message': 'Ocorreu um erro ao inserir o usuário!', 'Descrição': str(ex)}

def login(user_login, username, password):
    try:
        users = db.users
        user = users.find_one({'usuario': username})
        if user and user['senha'] == password:
            payload = {'id_usuario': str(user['_id']), 'usuario': user_login}
            jwt_token = jwt.encode(payload, "Economax", algorithm='HS256')
            return {'jwt': jwt_token,'Message': 'Usuário autenticado com sucesso!'}            
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
    
def cadastro_rendimentos_usuario(registros_gastos, usuario_id):
    gastos = db.rendimentos    
    data_hora_formatada = dataNow()
    
    for registro in registros_gastos:
     
        categoria_id = registro['id_categoria'].lower()
        valor = registro['valor']
        descricao = registro['descricao']
        
        novo_gasto = {'categoria_despesa_id': categoria_id, 'usuario_id': usuario_id, 'valor': valor, 'descricao': descricao, 'data': data_hora_formatada}

        gasto_id = gastos.insert_one(novo_gasto)
        
    return {'message': 'Rendimentos inseridos com sucesso!'}

def ultimas_despesas_usuario(mes, ano, users_id):
    inicio_mes, fim_mes = get_inicio_fim_mes(ano, mes)
    query = {
    'data': {
        '$gte': inicio_mes.strftime("%Y-%m-%d %H:%M:%S"),
        '$lte': fim_mes.strftime("%Y-%m-%d %H:%M:%S")
    },
    'usuario_id': users_id
    }
    result = db.gastos.find(query)
    gastos = sorted(result, key=lambda x: datetime.strptime(x['data'], "%Y-%m-%d %H:%M:%S"), reverse=True)
    
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
    # dias = 30000
    # if (dias==""):
    #     dias = 30000
    #     data_atual = (datetime.now() - timedelta(days=int(dias))).replace(hour=0, minute=0, second=0)
    #     data_limite = data_atual.strftime("%Y-%m-01 00:00:00")
    #     data_limite = datetime.strptime(data_limite, '%Y-%m-%d %H:%M:%S')
    # else:
    #     data_atual = datetime.now()
    #     data_limite = datetime(data_atual.year, data_atual.month, data_atual.day, 0, 0, 0) - timedelta(days=int(dias))
    
    # lista_filtrada = []

    # for item in resultado:
    #     data_item = datetime.strptime(item['data'], '%Y-%m-%d %H:%M:%S')
    #     if data_item >= data_limite:
    #         lista_filtrada.append(item)

    return jsonify(resultado)

def ultimas_rendimentos_usuario(mes, ano, users_id):
    inicio_mes, fim_mes = get_inicio_fim_mes(ano, mes)
    query = {
    'data': {
        '$gte': inicio_mes.strftime("%Y-%m-%d %H:%M:%S"),
        '$lte': fim_mes.strftime("%Y-%m-%d %H:%M:%S")
    },
    'usuario_id': users_id
    }
    result = db.rendimentos.find(query)
    rendimentos = sorted(result, key=lambda x: datetime.strptime(x['data'], "%Y-%m-%d %H:%M:%S"), reverse=True)
    resultado = []
    for rendimento in rendimentos:
        categoria_id = rendimento['categoria_despesa_id']
        categoria = db.categorias_rendimentos_geral.find_one({'_id': ObjectId(categoria_id)})
        resultado.append({
        'categoria': categoria['nome'],
        'valor': rendimento['valor'].replace(',', ''),
        'data': rendimento['data'],            
        'descricao': rendimento.get('descricao', '')
        })   
    
    return jsonify(resultado)

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

def ultimas_rendimentos_usuario_mes_atual_sintetico(users_id):
    gastos = db.rendimentos.find({'usuario_id': users_id})
    resultado = []
    for gasto in gastos:
        categoria_id = gasto['categoria_despesa_id']
        categoria = db.categorias_rendimentos_geral.find_one({'_id': ObjectId(categoria_id)})
        resultado.append({
            'categoria': categoria['nome'],
            'valor': gasto['valor'].replace(',', '')            
        })

    return jsonify(resultado)

def gastos_categoria_usuario(mes, ano, usuario_id):
    inicio_mes, fim_mes = get_inicio_fim_mes(ano, mes)
    
    collection_gastos = db['gastos']
    collection_categorias = db['categorias_despesas_geral']

    query = {
        'usuario_id': usuario_id,
        'data': {'$gte': inicio_mes.strftime("%Y-%m-%d %H:%M:%S")}
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

def rendimentos_categoria_usuario(mes, ano, usuario_id):
    inicio_mes, fim_mes = get_inicio_fim_mes(ano, mes)
    
    collection_gastos = db['rendimentos']
    collection_categorias = db['categorias_rendimentos_geral']

    query = {
        'usuario_id': usuario_id,
        'data': {'$gte': inicio_mes.strftime("%Y-%m-%d %H:%M:%S")}
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

def soma_total_gastos_por_usuario_por_dia(usuario_id):
    collection = db['gastos']
    data_hora_formatada = dataNow()
    data_hora_formatada = datetime.strptime(data_hora_formatada, '%Y-%m-%d %H:%M:%S')
    
    data_inicio = (data_hora_formatada - timedelta(days=int(0))).replace(hour=0, minute=0, second=0)
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

def soma_total_rendimentos_por_usuario_por_dia(usuario_id):
    collection = db['rendimentos']

    data_inicio = (datetime.now() - timedelta(days=int(0))).replace(hour=0, minute=0, second=0)
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

def cadastro_feedback(feedback, email):    
    try:
        feedbacks = db.feedback
        feedback_id = feedbacks.insert_one({
            "email": email,
            "feedback": feedback
        }).inserted_id
        return {'Message': 'feedback recebido com sucesso!', 'Id_feedback': str(feedback_id)}
    except Exception as ex:
        return {'Message': 'Ocorreu um erro ao enviar o feedback!', 'Descrição': str(ex)}
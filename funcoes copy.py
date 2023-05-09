import pymongo
from flask import Flask, jsonify, request
from bson import ObjectId
from datetime import datetime, timedelta

client = pymongo.MongoClient("mongodb+srv://administrador:administrador@economax.wa1uot6.mongodb.net/test")    
db = client['Economax']

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

def cadastro_categorias(nome_categoria, usuario_id):
    if db.categorias_despesas_geral.count_documents({'nome': nome_categoria}) > 0:
        return {'message': 'Categoria já está cadastrada!'}

    categoria = {'nome': nome_categoria, 'users_id': usuario_id, 'data': datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
    categoria_id = db.categorias_despesas_geral.insert_one(categoria).inserted_id
    
    categoria_criada = db.categorias_despesas_geral.find_one({'_id': categoria_id}, {'_id': 1, 'nome': 1})
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

def cadastro_gastos_usuario(registros_gastos, usuario_id):
    gastos = db.gastos
    
    for registro in registros_gastos:
     
        categoria_id = registro['id_categoria'].lower()
        valor = registro['valor']
        
        novo_gasto = {'categoria_despesa_id': categoria_id, 'usuario_id': usuario_id, 'valor': valor, 'data': datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

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
            'data': gasto['data']
        })
    
    data_atual = datetime.now()
    data_limite = datetime(data_atual.year, data_atual.month, data_atual.day, 0, 0, 0) - timedelta(days=int(dias))

    lista_filtrada = []
    for item in resultado:
        data_item = datetime.strptime(item['data'], '%d-%m-%Y %H:%M:%S')
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

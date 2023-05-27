from datetime import datetime
import os
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import logging
import AleCrypt
import funcoes

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def home():
    now = datetime.now()
    return jsonify({'datetime': now.strftime("%d-%m-%Y %H:%M:%S")})

#region Cadastro e login
@app.route('/cadastro', methods=['POST'])
def cadastro():
    user = request.json['usuario'].lower()
    user_crypt = AleCrypt.ale_encrypt(user, user)
    password = request.json['senha'].lower()
    password_crypt = AleCrypt.ale_encrypt(password, user)
    return funcoes.cadastro(user_crypt,password_crypt)

@app.route('/login', methods=['POST'])
def login():
    user = request.json['usuario'].lower()
    user_crypt = AleCrypt.ale_encrypt(user, user)
    password = request.json['senha'].lower()
    password_crypt = AleCrypt.ale_encrypt(password, user)    
    return funcoes.login(user_crypt,password_crypt)
#endregion

#region Categorias Despesas
@app.route('/categorias_despesas_geral', methods=['GET'])
def categorias_despesas_geral():  
    return funcoes.categorias_despesas_geral()
    
@app.route('/cadastro_categorias', methods=['POST'])
def cadastro_categorias():
    usuario_id = request.json['id_usuario'].lower()
    nome_categoria = request.json['categoria'].lower()
    return funcoes.cadastro_categorias(nome_categoria, usuario_id)

@app.route('/cadastro_categorias_usuario', methods=['POST'])
def cadastro_categorias_usuario():
    usuario_id = request.json['id_usuario'].lower()
    categorias = request.json['categorias']
    return funcoes.cadastro_categorias_usuario(usuario_id,categorias)
    
@app.route('/busca_categorias_despesas_geral_usuario', methods=['POST'])
def busca_categorias_despesas_geral_usuario():   
    user_id = request.json['id_usuario'].lower()
    return funcoes.busca_categorias_despesas_geral_usuario(user_id)
#endregion

#region Categorias Rendimentos
@app.route('/categorias_rendimentos_geral', methods=['GET'])
def categorias_rendimentos_geral():  
    return funcoes.categorias_rendimentos_geral()
    
@app.route('/cadastro_categorias_rendimentos', methods=['POST'])
def cadastro_categorias_rendimentos():
    usuario_id = request.json['id_usuario'].lower()
    nome_categoria = request.json['categoria'].lower()
    return funcoes.cadastro_categorias_rendimentos(nome_categoria, usuario_id)

@app.route('/cadastro_categorias_rendimentos_usuario', methods=['POST'])
def cadastro_categorias_rendimentos_usuario():
    usuario_id = request.json['id_usuario'].lower()
    categorias = request.json['categorias']
    return funcoes.cadastro_categorias_rendimentos_usuario(usuario_id,categorias)
    
@app.route('/busca_categorias_rendimentos_geral_usuario', methods=['POST'])
def busca_categorias_rendimentos_geral_usuario():   
    user_id = request.json['id_usuario'].lower()
    return funcoes.busca_categorias_rendimentos_geral_usuario(user_id)
#endregion

#region Relatórios
@app.route('/ultimas_despesas_usuario', methods=['POST'])
def ultimas_despesas_usuario():
    usuario_id = request.json['id_usuario'].lower()
    dias = request.json['dias']
    return funcoes.ultimas_despesas_usuario(dias, usuario_id)
    
@app.route('/ultimas_despesas_usuario_mes_atual_sintetico', methods=['POST'])
def ultimas_despesas_usuario_mes_atual_sintetico():
    usuario_id = request.json['id_usuario'].lower()
    return funcoes.ultimas_despesas_usuario_mes_atual_sintetico(usuario_id)

@app.route('/gastos_categoria_usuario', methods=['POST'])
def gastos_categoria_usuario():
    usuario_id = request.json['id_usuario'].lower()
    dias = request.json['dias']
    return funcoes.gastos_categoria_usuario(usuario_id,dias)

@app.route('/soma_total_gastos_por_usuario_por_dia', methods=['POST'])
def soma_total_gastos_por_usuario_por_dia():
    usuario_id = request.json['id_usuario'].lower()
    dias = request.json['dias']
    return funcoes.soma_total_gastos_por_usuario_por_dia(usuario_id,dias)
#endregion
    
#region Cadastro de valores
@app.route('/cadastro_gastos_usuario', methods=['POST'])
def cadastro_gastos_usuario():
    usuario_id = request.json['id_usuario'].lower()
    registros_gastos = request.json['gastos']
    return funcoes.cadastro_gastos_usuario(registros_gastos,usuario_id)

#endregion

if __name__ == '__main__':
    app.run()
from datetime import datetime
import os
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import logging
import AleCrypt
import funcoes
from flask_cors import CORS
import jwt

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
socketio = SocketIO(app)

CORS(app)

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
    return funcoes.cadastro(user, user_crypt,password_crypt)

@app.route('/login', methods=['POST'])
def login():
    user = request.json['usuario'].lower()
    user_crypt = AleCrypt.ale_encrypt(user, user)
    password = request.json['senha'].lower()
    password_crypt = AleCrypt.ale_encrypt(password, user)    
    return funcoes.login(user, user_crypt,password_crypt)
#endregion

#region Categorias Despesas
@app.route('/categorias_despesas_geral', methods=['GET'])
def categorias_despesas_geral():  
    return funcoes.categorias_despesas_geral()
    
@app.route('/cadastro_categorias', methods=['POST'])
def cadastro_categorias():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    nome_categoria = request.json['categoria'].lower()
    return funcoes.cadastro_categorias(nome_categoria, usuario_id)

@app.route('/cadastro_categorias_usuario', methods=['POST'])
def cadastro_categorias_usuario():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    categorias = request.json['categorias']
    return funcoes.cadastro_categorias_usuario(usuario_id,categorias)
    
@app.route('/busca_categorias_despesas_geral_usuario', methods=['POST'])
def busca_categorias_despesas_geral_usuario():   
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    user_id = payload['id_usuario']
    return funcoes.busca_categorias_despesas_geral_usuario(user_id)
#endregion

#region Categorias Rendimentos
@app.route('/categorias_rendimentos_geral', methods=['GET'])
def categorias_rendimentos_geral():  
    return funcoes.categorias_rendimentos_geral()
    
@app.route('/cadastro_categorias_rendimentos', methods=['POST'])
def cadastro_categorias_rendimentos():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    nome_categoria = request.json['categoria'].lower()
    return funcoes.cadastro_categorias_rendimentos(nome_categoria, usuario_id)

@app.route('/cadastro_categorias_rendimentos_usuario', methods=['POST'])
def cadastro_categorias_rendimentos_usuario():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    categorias = request.json['categorias']
    return funcoes.cadastro_categorias_rendimentos_usuario(usuario_id,categorias)
    
@app.route('/busca_categorias_rendimentos_geral_usuario', methods=['POST'])
def busca_categorias_rendimentos_geral_usuario():   
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    user_id = payload['id_usuario']
    return funcoes.busca_categorias_rendimentos_geral_usuario(user_id)
#endregion

#region Relatórios
# arrumado
@app.route('/ultimas_despesas_usuario', methods=['POST'])
def ultimas_despesas_usuario():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    mes = request.json['mes']
    ano = request.json['ano']
    return funcoes.ultimas_despesas_usuario(mes, ano, usuario_id)

# arrumado
@app.route('/ultimas_rendimentos_usuario', methods=['POST'])
def ultimas_rendimentos_usuario():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    mes = request.json['mes']
    ano = request.json['ano']
    return funcoes.ultimas_rendimentos_usuario(mes, ano, usuario_id)

# Rota morta mudada para ultimas_despesas_usuario
@app.route('/ultimas_despesas_usuario_mes_atual_sintetsico', methods=['POST'])
def ultimas_despesas_usuario_mes_atual_sintetico():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    return funcoes.ultimas_despesas_usuario_mes_atual_sintetico(usuario_id)

# Rota morta mudada para ultimas_rendimentos_usuario
@app.route('/ultimas_rendimentos_usuario_mes_atual_sintesatico', methods=['POST'])
def ultimas_rendimentos_usuario_mes_atual_sintetico():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    return funcoes.ultimas_rendimentos_usuario_mes_atual_sintetico(usuario_id)

# arrumado
@app.route('/gastos_categoria_usuario', methods=['POST'])
def gastos_categoria_usuario():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    mes = request.json['mes']
    ano = request.json['ano']
    return funcoes.gastos_categoria_usuario(mes, ano, usuario_id)

# arrumado
@app.route('/rendimentos_categoria_usuario', methods=['POST'])
def rendimentos_categoria_usuario():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    mes = request.json['mes']
    ano = request.json['ano']
    return funcoes.rendimentos_categoria_usuario(mes, ano, usuario_id)

# arrumado
@app.route('/soma_total_gastos_por_usuario_por_dia', methods=['POST'])
def soma_total_gastos_por_usuario_por_dia():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    return funcoes.soma_total_gastos_por_usuario_por_dia(usuario_id)

# arrumado
@app.route('/soma_total_rendimentos_por_usuario_por_dia', methods=['POST'])
def soma_total_rendimentos_por_usuario_por_dia():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    return funcoes.soma_total_rendimentos_por_usuario_por_dia(usuario_id)

#endregion
    
#region Cadastro de valores
@app.route('/cadastro_gastos_usuario', methods=['POST'])
def cadastro_gastos_usuario():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    registros_gastos = request.json['gastos']
    return funcoes.cadastro_gastos_usuario(registros_gastos,usuario_id)

@app.route('/cadastro_rendimentos_usuario', methods=['POST'])
def cadastro_rendimentos_usuario():
    payload = jwt.decode(request.json['jwt'], 'Economax', algorithms=['HS256'])
    usuario_id = payload['id_usuario']
    registros_gastos = request.json['rendimentos']
    return funcoes.cadastro_rendimentos_usuario(registros_gastos,usuario_id)

#endregion

#region Cadastro feedback
@app.route('/cadastro_feedback', methods=['POST'])
def cadastro_feedback():
    email = request.json['email']
    feedback = request.json['feedback']
    return funcoes.cadastro_feedback(feedback, email)
#endregion

if __name__ == '__main__':
    app.run()
import jwt

# Função para criar o JWT com usuário e senha
def codificar_jwt(usuario, senha, chave_secreta):
    payload = {'usuario': usuario, 'senha': senha}
    jwt_token = jwt.encode(payload, chave_secreta, algorithm='HS256')
    return jwt_token


# Função para decodificar o JWT e obter o usuário e a senha
def decodificar_jwt(jwt_token, chave_secreta):
    try:
        payload = jwt.decode(jwt_token, chave_secreta, algorithms=['HS256'])
        usuario = payload['usuario']
        senha = payload['senha']
        return usuario, senha
    except jwt.ExpiredSignatureError:
        # O JWT expirou
        return None, None
    except jwt.InvalidTokenError:
        # O JWT é inválido
        return None, None


# Exemplo de uso
chave_secreta = 'sua_chave_secreta_aqui'
usuario = 'exemplo_usuario'
senha = 'exemplo_senha'

# Cria o JWT com usuário e senha
jwt_token = codificar_jwt(usuario, senha, chave_secreta)
print('JWT gerado:', jwt_token)

# Decodifica o JWT e obtém o usuário e a senha
usuario_decodificado, senha_decodificada = decodificar_jwt(jwt_token, chave_secreta)
print('Usuário:', usuario_decodificado)
print('Senha:', senha_decodificada)

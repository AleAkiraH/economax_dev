import jwt

# Função para criar o JWT com usuário e senha
def codificar_jwt(usuario, chave_secreta):
    payload = {'usuario': usuario}
    jwt_token = jwt.encode(payload, chave_secreta, algorithm='HS256')
    return jwt_token


# Função para decodificar o JWT e obter o usuário e a senha
def decodificar_jwt(jwt_token, chave_secreta):
    try:
        payload = jwt.decode(jwt_token, chave_secreta, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # O JWT expirou
        return None, None
    except jwt.InvalidTokenError:
        # O JWT é inválido
        return None, None


# Exemplo de uso
chave_secreta = 'Alexsander'
userid = '6453cfea8f33516cd50542d4'

# Cria o JWT com usuário e senha
jwt_token = codificar_jwt(userid, chave_secreta)
print('JWT gerado:', jwt_token)

# Decodifica o JWT e obtém o usuário e a senha
payload = decodificar_jwt(jwt_token, chave_secreta)
print(payload)
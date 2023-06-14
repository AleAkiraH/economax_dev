import mysql.connector

# Configurações de conexão
host = 'sql213.infinityfree.com'  # Substitua pelo nome do servidor do banco de dados
database = 'if0_34418243_economax'  # Substitua pelo nome do banco de dados
user = 'if0_34418243'  # Substitua pelo nome de usuário do banco de dados
password = 'Kg0AMVJ28vFKs6A'  # Substitua pela senha do banco de dados

try:
    # Estabelecer conexão com o banco de dados
    connection = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    if connection.is_connected():
        print('Conexão estabelecida com sucesso!')
        # Aqui você pode realizar operações no banco de dados

except mysql.connector.Error as error:
    print('Falha ao conectar ao banco de dados:', error)

finally:
    if 'connection' in locals():
        connection.close()
        print('Conexão fechada.')

import requests
import schedule
import time

def fazer_requisicao():
    # URL da requisição
    url = 'https://economax.onrender.com/login'

    # Corpo da requisição
    data = {
        "usuario": "aleakirah",
        "senha": "14191712"
    }

    # Realiza a requisição
    response = requests.post(url, json=data)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        print('Requisição bem-sucedida!')
        # Registra o horário da requisição
        horario = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f'Requisição feita às {horario}')
    else:
        print('Erro na requisição.')
        # Registra o horário da requisição
        horario = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f'Requisição feita às {horario}')

# Agenda a execução da função a cada 4 minutos e 30 segundos
schedule.every(4).minutes.do(fazer_requisicao)
# schedule.every(10).seconds.do(fazer_requisicao)

executar_primeira_vez = True

while True:
    # Executa as tarefas agendadas
    schedule.run_pending()
    if (executar_primeira_vez):
        fazer_requisicao()
        executar_primeira_vez = False
    time.sleep(1)

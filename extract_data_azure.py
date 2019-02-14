# coding: utf-8
import urllib.request
import json
from ast import literal_eval

def get_data_api_ml_azure(temperatura):
    """
    Consumo de API do Azure Machine Learning
    Args: temperatura = temperatura em celsius para calculo
    Return: Response da API do tipo byte
    """
    # Preparando dict com variáveis para body
    data = {
        "Inputs": {
            "input1":
            [
                {
                    'Temperatura': str(temperatura)
                }
            ],
        }
    }
    # Preparando dados do body para consumo da API
    body = str.encode(json.dumps(data))
    # Atribuindo valores da url, chave de acesso da API e headers
    url = 'https://ussouthcentral.services.azureml.net/subscriptions/6e273f811bbd48fe870d6fe9187155e1/services/8116ce2309a64e2e95287513ca45dcb4/execute?api-version=2.0&format=swagger'
    api_key = 'v8tlTcwmjFs2G6jAGIvbx4JbfeVKw50bLZPmbQ1u7hzfb/SdmNj8G77+fE/E1180cY3ClAF6umuzaA6YvYm3zA=='
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    # Montando request da API com variáveis preparadas anteriormente
    req = urllib.request.Request(url, body, headers)

    # Fazendo consumo da API e retornando a função
    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return result

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read()))

def convert_fahrenheit_to_celsius(temperatura):
    """
    Converter grau fahrenheit para Celcius
    Args: temperatura = Grau em fahrenheit
    Returns: Grau celsius convertido
    """
    return (temperatura - 32) / 1.8

def break_alert(prob_quebra_maq):
    """
    Tranformar saída mais humanizada para tomada de decisão
    Args: prob_quebra_maq = Probabilidade de quebra da máquina
    Returns: Status da ação a ser tomada
    """
    if prob_quebra_maq < 0.40:
        status_quebra = 'Tranquilo'
    elif prob_quebra_maq < 0.75:
        status_quebra = 'Atenção'
    else:
        status_quebra = 'Requer atuação'

    return status_quebra

def main():
    """
    Função principal para receber dados do usuário e com ajustes para receber valor "resultado"
    Args: Nenhum
    Return: Print da variável resultado
    """
    # Recebendo dados do usuário
    while True:
        try:
            tipo_temp = input("Insira qual o tipo de temperatura (Celsius ou Fahrenheit): ")
            if not (tipo_temp == 'Celsius' or tipo_temp == 'Fahrenheit'):
                raise ValueError("Somente permitido inserir Celsius ou Fahrenheit")

            temperatura = int(input("Insira a temperatura (Somente número): "))
        except ValueError as e:
            print("Valor inválido:", e)
        else:
            break
    # Convertendo grau caso seja do tipo Fahrenheit
    if tipo_temp == 'Fahrenheit':
        temperatura = str(int(convert_fahrenheit_to_celsius(temperatura)))

    # Executando função para consumo da API
    data = get_data_api_ml_azure(temperatura)

    # Transformando byte em json para acesso a variável 'resultado'
    data = literal_eval(data.decode('utf8'))
    data = json.dumps(data, indent=4, sort_keys=True)
    data = json.loads(data)

    # Print da variável 'resultado' com 3 casas decimais
    prob_quebra_maq = round(float(data['Results']['output1'][0]['resultado']), 3)
    status_quebra = break_alert(prob_quebra_maq)
    print(status_quebra)
    input("Pressione ENTER para fechar")

# criar função que retorna string inteira para imprimir def break_alert():

if __name__ == '__main__':
    main()

import pandas as pd
import json

# Criar uma função que escreve um arquivo .json
def escrever_json(arq_json,dados):
    with open(arq_json, 'w', encoding='utf8') as f:
        json.dump(dados, f, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))

# Criar uma função que lê o arquivo .json
def ler_json(arq_json):
    with open(arq_json, 'r', encoding='utf8') as f:
        return json.load(f)

def chaves_json(arq_json,base):
    # Ler o arquivo .json e jogar na variável 'data'
    data = ler_json(arq_json)

    # Pegar as chaves de dentro de 'students' e jogar na variável 'keys'
    keys = data[base][0].keys()
    return keys

def valores_json(arq_json,base):
    # Ler o arquivo .json e jogar na variável 'data'
    data = ler_json(arq_json)

    # Pegar as chaves de dentro de 'students' e jogar na variável 'keys'
    values = data[base][0].values()
    return values

def tabela_json(arq_json,base,titulos_colunas):
    # Ler o arquivo .json e jogar na variável 'data'
    data = ler_json(arq_json)
    keys = chaves_json(arq_json,base)
    values = valores_json(arq_json,base)
    # # Finalmente, criar a tabela que você queria em um DataFrame
    df = pd.DataFrame(values, index=keys, columns=titulos_colunas)
    return df

def chave_valor_dicionario(dicionario):
    chaves = []
    valores = []
    for key,value in dicionario.items():
        chaves.append(key)
        valores.append(value)
    return chaves,valores
# # Exemplo  de um dicionário que virará um arquivo .json
# dict = {"students": [{"name": "Alan", "lastname": "Silva", "exam1": 50, "exam2": 80, "exam3": 91},
#     {"name": "Paula", "lastname": "Souza", "exam1": 95, "exam2": 98, "exam3": 99}]
#     }
# # Chamar a função escreve_jason()
# escrever_json(dict)

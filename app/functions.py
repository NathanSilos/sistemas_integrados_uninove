import requests as rs
import json

def api_login(username, password):

    resource = 'user'
    service = 'login'
    url = f"https://todolist-api.edsonmelo.com.br/api/{resource}/{service}/"

    payload = {
    "username": username,
    "password": password
    }

    headers = {'Content-type': 'application/json'}

    dados = rs.post(url, data=json.dumps(payload), headers=headers)

    dicionario = json.loads(dados.text)

    return dicionario

def cadastrar_usuario(payload):

    resource = 'user'
    service = 'new'
    url = f"https://todolist-api.edsonmelo.com.br/api/{resource}/{service}/"

    headers = {'Content-type': 'application/json'}

    dados = rs.post(url, data=json.dumps(payload), headers=headers)
    dicionario = json.loads(dados.text)

    return dicionario

def listar_tasks(acao ,user, token):

    resource = 'task'
    service = acao
    url = f"https://todolist-api.edsonmelo.com.br/api/{resource}/{service}/"

    payload = {
    "name": user
    }

    headers = {
        'Content-type': 'application/json', 
        "Authorization": token
        }

    dados = rs.post(url, data=json.dumps(payload), headers=headers)
    dicionario = json.loads(dados.text)

    if acao == 'search':
        if type(dicionario) == list:
            for linha in dicionario:
                if linha['realized'] == 1:
                    linha['realized'] = 'Concluída'
                else:
                    linha['realized'] = 'Em andamento'
        else:
            dicionario = None

    return dicionario

def concluir_task(id, name, token):
    resource = 'task'
    service = 'update'
    url = f"https://todolist-api.edsonmelo.com.br/api/{resource}/{service}/"

    payload = {
        "id": id,
        "name": name,
        "realized": 1
    }
    headers = {
        'Content-type': 'application/json', 
        "Authorization": token
        }

    dados = rs.put(url, data=json.dumps(payload), headers=headers)
    dicionario = json.loads(dados.text)

    return dicionario

def excluir_task(id, token):
    resource = 'task'
    service = 'delete'
    url = f"https://todolist-api.edsonmelo.com.br/api/{resource}/{service}/"

    payload = {"id": id}
    headers = {
            'Content-type': 'application/json', 
            "Authorization": token
    }

    dados = rs.delete(url, data=json.dumps(payload), headers=headers)
    dicionario = json.loads(dados.text)

    return dicionario

def edit_task(id, token):

    resource = 'task'
    service = 'edit'
    url = f"https://todolist-api.edsonmelo.com.br/api/{resource}/{service}/"

    payload = {"id": id}
    headers = {
            'Content-type': 'application/json', 
            "Authorization": token
    }

    dados = rs.delete(url, data=json.dumps(payload), headers=headers)
    dicionario = json.loads(dados.text)

    return dicionario
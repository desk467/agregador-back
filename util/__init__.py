from flask import request

def campos_presentes_na_requisicao(campos):
    campos = campos.split(' ')

    erros = []

    req = request.json if request.json else {}

    for campo in campos:
        if campo not in req:
            erros.append({'mensagem': 'Campo "{campo}" obrigatório.'.format(campo=campo)})
    
    if erros:
        return erros
    else:
        return []

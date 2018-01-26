import jwt
from flask import request, session
from app import app

from models.usuario import Usuario
from util.erro import gerar_erro_campo_obrigatorio


def campos_presentes_na_requisicao(campos):
    campos = campos.split(' ')

    erros = []

    req = request.form if request.form else {}

    for campo in campos:
        if campo not in req or len(req.get(campo)) == 0:
            erros.append(gerar_erro_campo_obrigatorio(campo))

    if erros:
        return erros
    else:
        return []


def usuario():
    return Usuario.get(Usuario.id == session['usuario']['id'])
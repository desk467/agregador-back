import jwt

from app import app

from flask import request, jsonify

from models import db
from models.usuario import Usuario, TipoUsuario
from models.professor import Professor
from models.estudante import Estudante
from models.instituicao import Instituicao

from playhouse.shortcuts import model_to_dict

from util import campos_presentes_na_requisicao

import hashlib


def senha_hasheada(senha):
    md5 = hashlib.md5()
    md5.update(senha.encode('utf-8'))

    return md5.digest()


@app.route('/login', methods=['POST'])
def login():
    erros = campos_presentes_na_requisicao('email senha')
    
    if erros: return jsonify(erros), 400

    email = request.json['email']
    senha = request.json['senha']

    try:
        usuario = Usuario.get(email=email)

        if usuario.hash_senha == senha_hasheada(senha):
            token = jwt.encode({'nome': usuario.nome, 'id': usuario.id }, app.secret_key, algorithm='HS256')

            return jsonify({'mensagem': 'Usuário logado com sucesso.', 'token': token.decode('utf-8') })
        else:
            return jsonify({'mensagem': 'Senha inválida.'}), 400

    except Usuario.DoesNotExist:
        return jsonify({'mensagem': 'Usuário não encontrado.'}), 404


def cadastrar_professor(usuario):
    nome_instituicao = request.json['nome_instituicao'] if 'nome_instituicao' in request.json else None

    if not nome_instituicao:
        return jsonify({'mensagem': 'Campo "nome_instituicao" obrigatório.'}), 400

    instituicao = Instituicao.select().where(
        Instituicao.nome % '%{}%'.format(nome_instituicao))
        
    if len(instituicao) == 0:
        instituicao = Instituicao.create(nome=nome_instituicao)

    Professor.create(usuario=usuario, instituicao=instituicao)

    return jsonify({'mensagem': 'Professor cadastrado com sucesso.'}), 200


def cadastrar_estudante(usuario):
    nome_instituicao = request.json['nome_instituicao'] if 'nome_instituicao' in request.json else None

    if not nome_instituicao:
        return jsonify({'mensagem': 'Campo "nome_instituicao" obrigatório.'}), 400

    try:
        instituicao = Instituicao.select().where(
            Instituicao.nome % '%{}%'.format(nome_instituicao))
    except Instituicao.DoesNotExist:
        instituicao = Instituicao.create(nome=nome_instituicao)

    Estudante.create(usuario=usuario, instituicao=instituicao)

    return jsonify({'mensagem': 'Estudante cadastrado com sucesso.'}), 200


cadastrar = {}
cadastrar[TipoUsuario.ESTUDANTE] = cadastrar_estudante
cadastrar[TipoUsuario.PROFESSOR] = cadastrar_professor


@app.route('/cadastro', methods=['POST'])
def cadastro():
    erros = campos_presentes_na_requisicao('nome email senha tipo_usuario')
    
    if erros: return jsonify(erros), 400

    nome = request.json['nome'] 
    email = request.json['email'] 
    senha = request.json['senha'] 
    tipo_usuario = request.json['tipo_usuario']

    try:
        tipo_usuario = TipoUsuario(tipo_usuario)
    except ValueError:
        return jsonify({'mensagem': 'Campo "tipo_usuario" inválido.'}), 400

    # Cadastrar usuário
    with db.atomic() as transacao:
        novo_usuario = Usuario.create(nome=nome, email=email,
                                      hash_senha=senha_hasheada(senha))

        # Criar professor ou aluno, dependendo do tipo_usuario
        try:
            resposta, codigo = cadastrar[tipo_usuario](novo_usuario)
            if codigo != 200:
                db.rollback()

            return resposta, codigo
        except Exception as e:
            db.rollback()

            return jsonify({'mensagem': 'Erro ao cadastrar usuário.'}), 500


@app.route('/esqueceu_senha')
def esqueceu_senha():
    pass


@app.route('/apagar_conta')
def apagar_conta():
    pass

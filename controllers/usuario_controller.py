from app import app

from flask import request, jsonify

from models import db
from models.usuario import Usuario, TipoUsuario
from models.professor import Professor
from models.estudante import Estudante
from models.instituicao import Instituicao

import hashlib


def senha_hasheada(senha):
    md5 = hashlib.md5()
    md5.update(senha.encode('utf-8'))

    return md5.digest()


@app.route('/login', methods=['POST'])
def login():
    email = request.json['email'] if 'email' in request.json else None
    senha = request.json['senha'] if 'senha' in request.json else None

    if not email:
        return jsonify({'mensagem': 'Campo "email" obrigatório.'}), 400

    if not senha:
        return jsonify({'mensagem': 'Campo "senha" obrigatório.'}), 400

    try:
        usuario = Usuario.get(email=email)

        if usuario.hash_senha == senha_hasheada(senha):
            return jsonify({'mensagem': 'Usuário logado com sucesso.', 'token': '123'})
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

    print(instituicao)
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
    nome = request.json['nome'] if 'nome' in request.json else None
    email = request.json['email'] if 'email' in request.json else None
    senha = request.json['senha'] if 'senha' in request.json else None
    tipo_usuario = request.json['tipo_usuario'] if 'tipo_usuario' in request.json else None

    if not nome:
        return jsonify({'mensagem': 'Campo "nome" obrigatório.'}), 400

    if not email:
        return jsonify({'mensagem': 'Campo "email" obrigatório.'}), 400

    if not senha:
        return jsonify({'mensagem': 'Campo "senha" obrigatório.'}), 400

    if not tipo_usuario:
        return jsonify({'mensagem': 'Campo "tipo_usuario" obrigatório.'}), 400

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
            print(e)
            db.rollback()

            return jsonify({'mensagem': 'Erro ao cadastrar usuário.'}), 500


@app.route('/esqueceu_senha')
def esqueceu_senha():
    pass


@app.route('/apagar_conta')
def apagar_conta():
    pass

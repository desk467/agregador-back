import jwt

from app import app

from flask import request, session, redirect, url_for, render_template, flash

from models import db
from models.usuario import Usuario, TipoUsuario
from models.professor import Professor
from models.estudante import Estudante
from models.disciplina import Disciplina
from models.estudante_disciplina import EstudanteDisciplina
from models.instituicao import Instituicao

from playhouse.shortcuts import model_to_dict

from models.disciplina import Disciplina

from util import campos_presentes_na_requisicao, usuario
from util.erro import Erro, gerar_erro_campo_invalido, gerar_erro_campo_obrigatorio
from util.professor import is_professor, disciplinas, injetar_professor
from util.estudante import is_estudante

from datetime import datetime

import hashlib


def senha_hasheada(senha):
    md5 = hashlib.md5()
    md5.update(senha.encode('utf-8'))

    return str(md5.digest())


@app.route('/')
def ir_para_inicio():
    return redirect(url_for('pagina_inicial'))


@app.route('/inicio')
def pagina_inicial():
    if is_professor(usuario()):
        professor = Professor.get(Professor.usuario == usuario())
        return render_template('usuario/index.html', disciplinas=disciplinas(professor))
    elif is_estudante(usuario()):
        estudante = Estudante.get(Estudante.usuario == usuario())
        disciplinas_disponiveis = [disciplina for disciplina in Disciplina.select().where(
            Disciplina.instituicao == estudante.instituicao)]

        disciplinas_assinadas = [disciplina for disciplina in Disciplina.select().join(
            EstudanteDisciplina).where(EstudanteDisciplina.estudante == estudante)]

        return render_template('usuario/index.html', estudante=estudante, disciplinas_disponiveis=disciplinas_disponiveis, disciplinas_assinadas=disciplinas_assinadas)
    else:
        return render_template('usuario/index.html')


@app.route('/login')
def pagina_login():
    if 'usuario' in session:
        return redirect(url_for('pagina_inicial'))

    return render_template('usuario/login.html')


@app.route('/login', methods=['POST'])
def login():
    erros = campos_presentes_na_requisicao('email senha')

    if erros:
        return render_template('usuario/login.html', erros=erros), 400

    email = request.form.get('email')
    senha = request.form.get('senha')

    try:
        usuario = Usuario.get(email=email)

        if usuario.hash_senha == senha_hasheada(senha):
            session['usuario'] = model_to_dict(usuario)

            flash(
                'Seja bem-vindo, {usuario}.'.format(usuario=usuario.nome.split()[0]))
            return redirect(url_for('pagina_inicial'))
        else:
            return render_template('usuario/login.html', erros=[Erro('Senha inválida.')]), 400

    except Usuario.DoesNotExist:
        return render_template('usuario/login.html', erros=[{'mensagem': 'Usuário não encontrado.'}]), 404


@app.route('/logout')
def deslogar():
    session.clear()
    return redirect(url_for('pagina_inicial'))


def cadastrar_professor(usuario):
    nome_instituicao = request.form['nome_instituicao'] if 'nome_instituicao' in request.form else None

    if not nome_instituicao:
        return gerar_erro_campo_obrigatorio("nome_instituicao"), 400

    instituicao = Instituicao.select().where(
        Instituicao.nome % nome_instituicao)

    if len(instituicao) == 0:
        instituicao = Instituicao.create(nome=nome_instituicao)

    Professor.create(usuario=usuario, instituicao=instituicao)

    return 'Professor cadastrado com sucesso.', 200


def cadastrar_estudante(usuario):
    nome_instituicao = request.form['nome_instituicao'] if 'nome_instituicao' in request.form else None

    if not nome_instituicao:
        return gerar_erro_campo_obrigatorio("nome_instituicao"), 400

    try:
        instituicao = Instituicao.get(
            Instituicao.nome % nome_instituicao)
    except Instituicao.DoesNotExist:
        instituicao = Instituicao.create(nome=nome_instituicao)

    Estudante.create(usuario=usuario, instituicao=instituicao)

    return 'Estudante cadastrado com sucesso.', 200


cadastrar = {}
cadastrar[TipoUsuario.ESTUDANTE] = cadastrar_estudante
cadastrar[TipoUsuario.PROFESSOR] = cadastrar_professor


@app.route('/cadastro')
def pagina_cadastro():
    if 'usuario' in session:
        return redirect(url_for('pagina_inicial'))

    return render_template('usuario/cadastro.html')


@app.route('/cadastro', methods=['POST'])
def cadastro():
    erros = campos_presentes_na_requisicao('nome email senha tipo_usuario')

    if erros:
        return render_template('usuario/cadastro.html', erros=erros), 400

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    tipo_usuario = int(request.form.get('tipo_usuario'))

    # Cadastrar usuário
    with db.atomic() as transacao:
        novo_usuario = Usuario.create(nome=nome, email=email, tipo_usuario=tipo_usuario,
                                      hash_senha=senha_hasheada(senha))

        # Criar professor ou aluno, dependendo do tipo_usuario
        try:
            resposta, codigo = cadastrar[TipoUsuario(
                tipo_usuario)](novo_usuario)
            if codigo != 200:
                db.rollback()

            flash(resposta)
            session['usuario'] = model_to_dict(novo_usuario)

            return redirect(url_for('pagina_inicial'))

        except Exception as e:
            db.rollback()
            print(e)
            flash(
                'Algo de errado aconteceu ao cadastrar o usuário. Por favor, tente mais tarde.')
            return render_template('usuario/cadastro.html'), 500

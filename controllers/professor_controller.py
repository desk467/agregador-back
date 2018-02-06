'''
professor_controller.py
-------------

Controller de professor
Conterá serviços de:
- CRUD de Disciplina
- CRUD de Atividade
'''

from flask import request, render_template, redirect, flash, url_for
from playhouse.shortcuts import model_to_dict
from app import app
from functools import wraps
from datetime import datetime

from models.professor import Professor
from models.disciplina import Disciplina
from models.atividade import Atividade
from util import usuario, campos_presentes_na_requisicao
from util.professor import injetar_professor, disciplinas


@app.route('/disciplina/criar')
def pagina_criar_disciplina():
    professor = Professor.get(Professor.usuario == usuario())
    instituicao = professor.instituicao.nome

    return render_template('professor/criar_disciplina.html', instituicao=instituicao)


@app.route('/disciplina/<id_disciplina>')
def pagina_disciplina(id_disciplina):

    try:
        disciplina = Disciplina.get(Disciplina.id == id_disciplina)
        atividades = [model_to_dict(atividade) for atividade in Atividade.select(
        ).where(Atividade.disciplina == disciplina)]

        return render_template('professor/pagina_disciplina.html', disciplina=model_to_dict(disciplina), atividades=atividades)
    except Disciplina.DoesNotExist:
        return render_template('erros/404.html'), 404


@app.route('/disciplinas')
@injetar_professor
def pagina_disciplinas(professor):
    return render_template('professor/pagina_disciplinas.html', disciplinas=disciplinas(professor))


@app.route('/disciplina/criar', methods=['POST'])
@injetar_professor
def criar_disciplina(professor):
    erros = campos_presentes_na_requisicao('nome descricao')

    if erros:
        return render_template('professor/criar_disciplina.html', erros=erros), 400

    nome = request.form.get('nome')
    descricao = request.form.get('descricao')

    disciplina = Disciplina.create(
        nome=nome, descricao=descricao, professor=professor, instituicao=professor.instituicao)

    flash('Disciplina {disciplina} criada com sucesso.'.format(
        disciplina=disciplina.nome))

    return redirect(url_for('pagina_disciplinas'))


@app.route('/disciplina/<id_disciplina>/atividade/criar')
def pagina_criar_atividade(id_disciplina):
    try:
        disciplina = Disciplina.get(Disciplina.id == id_disciplina)

        return render_template('disciplina/criar_atividade.html', disciplina=disciplina)
    except Disciplina.DoesNotExist:
        return render_template('erros/404.html'), 404


@app.route('/disciplina/<id_disciplina>/atividade/criar', methods=['POST'])
def criar_atividade(id_disciplina):
    erros = campos_presentes_na_requisicao('nome descricao data')

    if erros:
        return render_template('disciplina/criar_atividade.html', erros=erros), 400

    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    data = datetime.strptime(request.form.get('data'), '%d/%m/%Y')

    atividade = Atividade.create(
        nome=nome, descricao=descricao, data=data, disciplina_id=id_disciplina)

    flash('Atividade {atividade} criada com sucesso.'.format(
        atividade=atividade.nome))

    return redirect(url_for('pagina_disciplinas'))

@app.route('/atividade/<id_atividade>')
def pagina_atividade(id_atividade):
    try:
        atividade = Atividade.get(Atividade.id == id_atividade)
        atividade = model_to_dict(atividade)
        atividade['data'] = datetime.strftime(atividade['data'], '%d/%m/%Y')

        return render_template('disciplina/pagina_atividade.html', atividade=atividade)
    except Atividade.DoesNotExist:
        return render_template('erros/404.html'), 404
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

from models.professor import Professor
from models.disciplina import Disciplina
from util import usuario, campos_presentes_na_requisicao
from util.professor import injetar_professor, disciplinas


@app.route('/disciplina/criar')
def pagina_criar_disciplina():
    professor = Professor.get(Professor.usuario == usuario())
    instituicao = professor.instituicao.nome

    return render_template('professor/criar_disciplina.html', instituicao=instituicao)


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

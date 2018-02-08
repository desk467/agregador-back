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
from util.professor import injetar_professor, disciplinas, is_professor
from util.estudante import is_estudante, is_disciplina_assinada


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

        return render_template('professor/pagina_disciplina.html', disciplina=model_to_dict(disciplina), atividades=atividades, is_professor=is_professor(usuario()), is_estudante=is_estudante(usuario()), disciplina_assinada=is_disciplina_assinada(usuario(), id_disciplina))
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


@app.route('/disciplina/<id_disciplina>/excluir')
@injetar_professor
def excluir_disciplina(professor, id_disciplina):
    # Primeiro verificar se o usuário atual é o dono da disciplina
    # Se for, pode excluir
    # Se não, lança 400
    try:
        disciplina = Disciplina.get(Disciplina.id == id_disciplina)

        if disciplina.professor == professor:
            Atividade.delete().where(Atividade.disciplina == disciplina).execute()
            disciplina.delete_instance()

            flash('Disciplina <strong>{disciplina}</strong> removida com sucesso!'.format(
                disciplina=disciplina.nome))
            return redirect(url_for('pagina_disciplinas'))
        else:
            return render_template('/erros/401.html'), 401
    except Disciplina.DoesNotExist:
        return render_template('/erros/404.html'), 404


@app.route('/disciplina/<id_disciplina>/editar')
def pagina_editar_disciplina(id_disciplina):
    try:
        disciplina = Disciplina.get(Disciplina.id == id_disciplina)

        return render_template('professor/editar_disciplina.html', disciplina=disciplina)
    except Disciplina.DoesNotExist:
        return render_template('erros/404.html'), 404


@app.route('/disciplina/<id_disciplina>/editar', methods=['POST'])
@injetar_professor
def editar_disciplina(professor, id_disciplina):
    try:
        disciplina = Disciplina.get(Disciplina.id == id_disciplina)

        if disciplina.professor == professor:
            erros = campos_presentes_na_requisicao('nome descricao')

            if erros:
                return render_template('professor/editar_disciplina.html', erros=erros, disciplina=disciplina), 400

            nome = request.form.get('nome')
            descricao = request.form.get('descricao')

            disciplina.nome = nome
            disciplina.descricao = descricao

            disciplina.save()

            flash('Edição concluída com sucesso!')
            return redirect(url_for('pagina_disciplinas'))
        else:
            return render_template('erros/401.html'), 401
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

    flash('Atividade <strong>{atividade}</strong> criada com sucesso.'.format(
        atividade=atividade.nome))

    return redirect(url_for('pagina_disciplinas', id_disciplina=id_disciplina))


@app.route('/atividade/<id_atividade>')
def pagina_atividade(id_atividade):
    try:
        atividade = Atividade.get(Atividade.id == id_atividade)
        atividade = model_to_dict(atividade)
        atividade['data'] = datetime.strftime(atividade['data'], '%d/%m/%Y')

        return render_template('disciplina/pagina_atividade.html', atividade=atividade)
    except Atividade.DoesNotExist:
        return render_template('erros/404.html'), 404


@app.route('/atividade/<id_atividade>/editar')
def pagina_editar_atividade(id_atividade):
    try:
        atividade = Atividade.get(Atividade.id == id_atividade)
        atividade = model_to_dict(atividade)
        atividade['data'] = atividade['data'].strftime('%d/%m/%Y')

        return render_template('disciplina/editar_atividade.html', atividade=atividade)
    except Atividade.DoesNotExist:
        return render_template('erros/404.html'), 404


@app.route('/atividade/<id_atividade>/editar', methods=['POST'])
@injetar_professor
def editar_atividade(professor, id_atividade):
    try:
        atividade = Atividade.get(Atividade.id == id_atividade)

        if atividade.disciplina.professor == professor:
            erros = campos_presentes_na_requisicao('nome data descricao')

            if erros:
                return render_template('professor/editar_atividade.html', erros=erros, atividade=atividade), 400

            nome = request.form.get('nome')
            descricao = request.form.get('descricao')
            data = request.form.get('data')

            atividade.nome = nome
            atividade.descricao = descricao
            atividade.data = datetime.strptime(data, '%d/%m/%Y')

            atividade.save()

            flash('Edição concluída com sucesso!')
            return redirect(url_for('pagina_disciplina', id_disciplina=atividade.disciplina.id))
        else:
            return render_template('erros/401.html'), 401
    except atividade.DoesNotExist:
        return render_template('erros/404.html'), 404


@app.route('/atividade/<id_atividade>/excluir')
@injetar_professor
def excluir_atividade(professor, id_atividade):
    # Primeiro verificar se o usuário atual é o dono da atividade
    # Se for, pode excluir
    # Se não, lança 400

    try:
        atividade = Atividade.get(Atividade.id == id_atividade)

        if atividade.disciplina.professor == professor:
            atividade.delete_instance()
            flash('Atividade <strong>{atividade}</strong> removida com sucesso!'.format(
                atividade=atividade.nome))
            return redirect(url_for('pagina_disciplina', id_disciplina=atividade.disciplina.id))
        else:
            return render_template('/erros/401.html'), 401
    except Atividade.DoesNotExist:
        return render_template('/erros/404.html'), 404

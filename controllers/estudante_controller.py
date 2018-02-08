'''
estudante_controller.py
-------------

Controller de estudante
Conterá serviços de:
- Pesquisar disciplina
- Assinar disciplina
'''

from flask import render_template, flash, request, redirect, url_for
from models.disciplina import Disciplina
from models.estudante_disciplina import EstudanteDisciplina
from models.estudante import Estudante
from util.estudante import injetar_estudante

from app import app

@app.route('/pesquisar_disciplina')
def pesquisar_disciplina():
    chave_pesquisa = request.args.get('nome')

    disciplinas_encontradas = [d for d in Disciplina.select().where(Disciplina.nome ** '%{}%'.format(chave_pesquisa))]
    return render_template('usuario/pesquisa_disciplina.html', chave_pesquisa=chave_pesquisa, disciplinas_encontradas=disciplinas_encontradas)

@app.route('/assinar/<id_disciplina>')
@injetar_estudante
def assinar_disciplina(estudante, id_disciplina):
    try:
        disciplina = Disciplina.get(Disciplina.id == id_disciplina)

        EstudanteDisciplina.create(estudante=estudante, disciplina=disciplina)
        flash('Disciplina assinada.')
        return redirect(url_for('pagina_disciplina', id_disciplina=id_disciplina))

    except Disciplina.DoesNotExist:
        return render_template('erros/404.html'), 404
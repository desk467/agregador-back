'''
professor_controller.py
-------------

Controller de professor
Conterá serviços de:
- CRUD de Disciplina
- CRUD de Atividade
'''

from flask import jsonify
from playhouse.shortcuts import model_to_dict
from app import app
from functools import wraps

from models.professor import Professor
from models.disciplina import Disciplina
from util import usuario

# Decorators úteis para o controller


def injetar_professor(handler):
    '''
    professor_existe
    Verifica se o usuário atual existe como um professor
    '''
    def wrapper(*args, **kwargs):
        try:
            professor = Professor.get(Professor.usuario == usuario())
        except Professor.DoesNotExist:
            return jsonify({'mensagem': 'Professor não encontrado.'}), 404

        return handler(professor, *args, **kwargs)

    wrapper.__name__ = handler.__name__

    return wrapper


@app.route('/professor/info')
@injetar_professor
def get_professor(professor):
    return jsonify(model_to_dict(professor))


@app.route('/professor/disciplina')
@injetar_professor
def get_disciplinas(professor):
    disciplinas = Disciplina.select().where(Disciplina.professor == professor)

    return jsonify([model_to_dict(disciplina) for disciplina in disciplinas])

@app.route('/professor/disciplina')
@injetar_professor
def criar_disciplina(professor, methods=['POST']):
    return 'Ok'


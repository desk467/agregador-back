'''
Helpers de professor
'''
from playhouse.shortcuts import model_to_dict

from . import usuario
from models.professor import Professor
from models.disciplina import Disciplina


def is_professor(usuario):
    '''
    Retorna True se usuario é um professor.
    '''
    try:
        Professor.get(Professor.usuario == usuario)
        return True
    except Professor.DoesNotExist as ex:
        return False


def injetar_professor(handler):
    '''
    Verifica se o usuário atual existe como um professor
    Em caso positivo, retorna uma nova função que recebe o
    professor como parâmetro.
    '''
    def wrapper(*args, **kwargs):
        try:
            professor = Professor.get(Professor.usuario == usuario())
        except Professor.DoesNotExist:
            return 500

        return handler(professor, *args, **kwargs)

    wrapper.__name__ = handler.__name__

    return wrapper


def disciplinas(professor):
    return [model_to_dict(disciplina) for disciplina in Disciplina.select().where(Disciplina.professor == professor)]

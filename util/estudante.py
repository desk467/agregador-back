from models.estudante import Estudante
from models.estudante_disciplina import EstudanteDisciplina
from models.disciplina import Disciplina
from . import usuario

def is_estudante(usuario):
    '''
    Retorna True se usuario é um estudante.
    '''
    try:
        Estudante.get(Estudante.usuario == usuario)
        return True
    except Estudante.DoesNotExist as ex:
        return False

def is_disciplina_assinada(usuario, id_disciplina):
    '''
    Retorna True se uma disciplina foi assinada
    '''
    try:
        estudante = Estudante.get(Estudante.usuario == usuario)
        disciplina = Disciplina.get(Disciplina.id == id_disciplina)
        EstudanteDisciplina.get(EstudanteDisciplina.estudante == estudante, EstudanteDisciplina.disciplina == disciplina)

        return True
    except Estudante.DoesNotExist:
        return False
    except EstudanteDisciplina.DoesNotExist:
        return False

def injetar_estudante(handler):
    '''
    Verifica se o usuário atual existe como um estudante
    Em caso positivo, retorna uma nova função que recebe o
    estudante como parâmetro.
    '''
    def wrapper(*args, **kwargs):
        try:
            estudante = Estudante.get(Estudante.usuario == usuario())
        except Estudante.DoesNotExist:
            return 500

        return handler(estudante, *args, **kwargs)

    wrapper.__name__ = handler.__name__

    return wrapper
from models.estudante import Estudante

def is_estudante(usuario):
    '''
    Retorna True se usuario é um estudante.
    '''
    try:
        Estudante.get(Estudante.usuario == usuario)
        return True
    except Estudante.DoesNotExist as ex:
        return False

'''
estudante.py
------------

Model responsável por guardar todos os estudantes do serviço
Cada estudante está atrelado a uma entidade Usuário.
'''

from models import BaseModel
from models.instituicao import Instituicao
from models.usuario import Usuario
from peewee import CharField, ForeignKeyField


class Estudante(BaseModel):
    usuario = ForeignKeyField(Usuario)
    instituicao = ForeignKeyField(Instituicao)
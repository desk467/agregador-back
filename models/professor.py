'''
professor.py
------------

Model responsável por definir a entidade Professor.
Um professor está atrelado a um usuário do serviço.
'''

from models import BaseModel
from models.instituicao import Instituicao
from models.usuario import Usuario
from peewee import CharField, ForeignKeyField


class Professor(BaseModel):
    usuario = ForeignKeyField(Usuario)
    instituicao = ForeignKeyField(Instituicao)

    @property
    def disciplinas(self):
        return []

'''
disciplina.py
-------------

Model responsável por guardar todas as disciplinas
que foram registradas no site por professores, agrupadas por
instituição.
'''

from models import BaseModel
from models.instituicao import Instituicao
from models.usuario import Usuario
from peewee import CharField, ForeignKeyField, TextField


class Disciplina(BaseModel):
    usuario = ForeignKeyField(Usuario, related_name="administrador")
    nome = CharField()
    descricao = TextField()
    instituicao = ForeignKeyField(Instituicao)

    @property
    def alunos_inscritos():
        return []
    
    @property
    def atividades():
        return []
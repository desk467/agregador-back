'''
disciplina.py
-------------

Model responsável por guardar todas as disciplinas
que foram registradas no site por professores, agrupadas por
instituição.
'''

from models import BaseModel
from models.instituicao import Instituicao
from models.professor import Professor
from peewee import CharField, ForeignKeyField, TextField


class Disciplina(BaseModel):
    professor = ForeignKeyField(Professor, related_name="administrador")
    nome = CharField()
    descricao = TextField()
    instituicao = ForeignKeyField(Instituicao)

    @property
    def alunos_inscritos():
        return []
    
    @property
    def atividades():
        return []
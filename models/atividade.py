'''
atividade.py
------------

Model responsável por guardar todas as atividades
que foram criadas para uma disciplina.
'''

from models import BaseModel
from models.disciplina import Disciplina
from peewee import CharField, TextField, ForeignKeyField


class Atividade(BaseModel):
    disciplina = ForeignKeyField(Disciplina)

    nome = CharField()
    descricao = TextField()

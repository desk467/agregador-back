'''
usuario.py
----------

Entidade separada do conceito de estudante/professor
que servirá como entidade "logável" e capaz de efetuar
operações dentro do sistema.
'''
from enum import Enum

from models import BaseModel
from models.instituicao import Instituicao
from peewee import CharField, ForeignKeyField, IntegerField

TipoUsuario = Enum('TipoUsuario', 'PROFESSOR ESTUDANTE')

class Usuario(BaseModel):
    nome = CharField()
    tipo_usuario = IntegerField()
    email = CharField(max_length=100)
    hash_senha = CharField(max_length=128)
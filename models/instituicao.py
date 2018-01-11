'''
instituicao.py
--------------

Entidade responsável por guardar todas as instituições do serviço.
Cada instituição poderá ter uma página com todas as suas disciplinas,
professores e alunos cadastrados.
'''

from models import BaseModel
from peewee import CharField, TextField


class Instituicao(BaseModel):
    nome = CharField()
    descricao = TextField()

    @get
    def disciplinas(self):
        return []

    @get
    def alunos(self):
        return []

    @get
    def professores(self):
        return []

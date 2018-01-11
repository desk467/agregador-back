'''
estudante_disciplina.py
-------------------

Model responsável por guardar todas as incrições dos estudantes
em disciplinas.
'''

from models import BaseModel
from models.estudante import Estudante
from models.disciplina import Disciplina
from peewee import CharField, ForeignKeyField


class EstudanteDisciplina(BaseModel):
    estudante = ForeignKeyField(Estudante)
    disciplina = ForeignKeyField(Disciplina)

    @property
    def atividades(self):
        return []
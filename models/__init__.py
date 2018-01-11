import datetime
from peewee import SqliteDatabase
from peewee import Model
from peewee import DateTimeField, PrimaryKeyField

db = SqliteDatabase('agregador.db')

'''
BaseModel
Classe base de todos os models, que define alguns campos padrão
como id e data_criacao, bem como qual banco será utilizado
'''


class BaseModel(Model):
    id = PrimaryKeyField()
    data_criacao = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

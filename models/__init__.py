from peewee import *

db = SqliteDatabase('agregador.db')

class BaseModel:
    class Meta:
        database = db
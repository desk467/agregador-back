'''
server.py
------
Arquivo que faz o bootstrap da aplicação, isto é:
- Recupera a instância do servidor
- Registra as rotas
- Inicia o servidor
que será utilizada para registrar rotas e iniciar a aplicação.
'''

from app import app

# models

from models import db
from models.usuario import Usuario
from models.estudante import Estudante
from models.professor import Professor
from models.disciplina import Disciplina
from models.instituicao import Instituicao
from models.atividade import Atividade
from models.estudante_disciplina import EstudanteDisciplina

try:
    db.create_tables([
        Usuario,
        Estudante,
        Professor,
        Disciplina,
        Instituicao,
        Atividade,
        EstudanteDisciplina,
    ])
except:
    pass

# controllers

from controllers import professor_controller
from controllers import estudante_controller
from controllers import usuario_controller

if __name__ == '__main__':
    app.run(debug=True)

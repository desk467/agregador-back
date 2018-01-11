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

# controllers

from controllers import professor_controller
from controllers import estudante_controller
from controllers import usuario_controller

if __name__ == '__main__':
    app.run(debug=True)

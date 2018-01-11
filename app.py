'''
app.py
------
Arquivo que possui a instancia do servidor
que será utilizada para registrar rotas e iniciar a aplicação.
'''

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.secret_key = 'b7292HvYQridVgfT6bkCUJAVjmvjabrk'
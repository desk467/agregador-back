'''
app.py
------
Arquivo que possui a instancia do servidor
que será utilizada para registrar rotas e iniciar a aplicação.
'''

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.before_request
def verificar_json():
    if not request.json:
        return jsonify({'mensagem': 'Requisição inválida.'}), 400

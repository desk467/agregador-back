'''
app.py
------
Arquivo que possui a instancia do servidor
que será utilizada para registrar rotas e iniciar a aplicação.
'''

from flask import Flask, request, render_template

app = Flask(__name__)
app.secret_key = 'b7292HvYQridVgfT6bkCUJAVjmvjabrk'


@app.errorhandler(404)
def erro_404(e):
    return render_template('erros/404.html'), 404


@app.errorhandler(500)
def erro_500(e):
    print(e)
    return render_template('erros/500.html'), 500

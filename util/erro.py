class Erro:
    '''
    Classe padrão para a geração de erros que serão
    mostrados para os usuários da aplicação.
    '''

    def __init__(self, descricao, codigo=None):
        self._codigo = codigo
        self._descricao = descricao

    @property
    def mensagem(self):
        if self._codigo:
            return "{codigo} - {descricao}".format(codigo=self._codigo, descricao=self._descricao)
        else:
            return "{descricao}".format(descricao=self._descricao)

# Fábricas de erros

def gerar_erro_campo_obrigatorio(campo):
    return Erro(descricao='Campo <strong>{campo}</strong> obrigatório.'.format(campo=campo))


def gerar_erro_campo_invalido(campo):
    return Erro(descricao='Campo <strong>{campo}</strong> inválido.'.format(campo=campo))

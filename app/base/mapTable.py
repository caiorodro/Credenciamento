class mapUser(object):
    def __init__(self, ID_USER, NAME_USER, PASSWORD1, EMAIL, USER_ENABLED, KIND_OF_USER):
        self.ID_USER = ID_USER
        self.NAME_USER = NAME_USER
        self.PASSWORD1 = PASSWORD1
        self.EMAIL = EMAIL
        self.USER_ENABLED = USER_ENABLED
        self.KIND_OF_USER = KIND_OF_USER

class mapLogger(object):
    def __init__(self, ID_LOG, ID_USER, DATE_OF, MESSAGE1, LEVEL1, TRACE):
        self.ID_LOG = ID_LOG
        self.ID_USER = ID_USER
        self.DATE_OF = DATE_OF
        self.MESSAGE1 = MESSAGE1
        self.LEVEL1 = LEVEL1
        self.TRACE = TRACE

class mapEmpresaContratante(object):
    def __init__(self, ID_EMPRESA, RAZAO_SOCIAL, NOME_FANTASIA, CNPJ, IE, ENDERECO, NUMERO, COMPLEMENTO, CEP, MUNICIPIO, UF, EMAIL, TELEFONE, CONTATO):
        self.ID_EMPRESA = ID_EMPRESA
        self.RAZAO_SOCIAL = RAZAO_SOCIAL
        self.NOME_FANTASIA = NOME_FANTASIA
        self.CNPJ = CNPJ
        self.IE = IE
        self.ENDERECO = ENDERECO
        self.NUMERO = NUMERO
        self.COMPLEMENTO = COMPLEMENTO
        self.CEP = CEP
        self.MUNICIPIO = MUNICIPIO
        self.UF = UF
        self.EMAIL = EMAIL
        self.TELEFONE = TELEFONE
        self.CONTATO = CONTATO

class mapEvento(object):
    def __init__(self, ID_EVENTO, ID_EMPRESA, DATA_EVENTO, TITULO_EVENTO, OBSERVACAO):
        self.ID_EVENTO = ID_EVENTO
        self.ID_EMPRESA = ID_EMPRESA
        self.DATA_EVENTO = DATA_EVENTO
        self.TITULO_EVENTO = TITULO_EVENTO
        self.OBSERVACAO = OBSERVACAO

class mapConvidado(object):
    def __init__(self, ID_CONVIDADO, ID_EVENTO, NOME_CONVIDADO, CELULAR_CONVIDADO):
        self.ID_CONVIDADO = ID_CONVIDADO
        self.ID_EVENTO = ID_EVENTO
        self.NOME_CONVIDADO = NOME_CONVIDADO
        self.CELULAR_CONVIDADO = CELULAR_CONVIDADO

class mapCredenciamento(object):
    def __init__(self, ID_CREDENCIAMENTO, ID_EVENTO, ID_CONVIDADO, DATA_HORA, PRESENTE):
        self.ID_CREDENCIAMENTO = ID_CREDENCIAMENTO
        self.ID_EVENTO = ID_EVENTO
        self.ID_CONVIDADO = ID_CONVIDADO
        self.DATA_HORA = DATA_HORA
        self.PRESENTE = PRESENTE

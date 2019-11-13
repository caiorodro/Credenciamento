from datetime import datetime
import json
import os

from flask import Blueprint
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import redirect

from app.views.credenciamento import credenciamento
from app.base.mapTable import mapEvento, mapConvidado
from app.base.loggerNoSQL import loggerNoSQL

dataCredenciamento = Blueprint('dataCredenciamento', __name__)

@dataCredenciamento.route('/listCredenciamento', methods=['POST'])
def listCredenciamento():
    rec = json.loads(request.get_data())

    idUser = rec['idUser']
    keep = rec['keep']
    ID_EVENTO = rec['ID_EVENTO']

    user1 = credenciamento(keep, idUser)
    result = user1.testListOf(ID_EVENTO)
    del user1

    return result

@dataCredenciamento.route('/adicionaPresenca', methods=['POST'])
def adicionaPresenca():

    rec = json.loads(request.get_data())

    ID_EVENTO = rec['ID_EVENTO']
    ID_CONVIDADO = rec['ID_CONVIDADO']
    keep = rec['keep']
    idUser = rec['idUser']

    user1 = credenciamento(keep, idUser)
    result = user1.testAdicionaPresenca(ID_EVENTO, ID_CONVIDADO)

    del user1

    return result

@dataCredenciamento.route('/deletePresenca', methods=['POST'])
def deletePresenca():
    rec = json.loads(request.get_data())

    ID_CREDENCIAMENTO = rec['ID_CREDENCIAMENTO']

    keep = rec['keep']
    idUser = rec['idUser']

    user1 = credenciamento(keep, idUser)
    retorno = user1.testDeletePresenca(ID_CREDENCIAMENTO)

    del user1

    return retorno

@dataCredenciamento.route('/carregaEventoCredenciamento', methods=['POST'])
def carregaEventoCredenciamento():
    rec = json.loads(request.get_data())

    keep = rec['keep']
    idUser = rec['idUser']
    DATA = datetime.strptime(rec['DATA'], '%Y-%m-%d').date()

    user1 = credenciamento(keep, idUser)
    retorno = user1.testListComboEvento(DATA)

    del user1

    return retorno

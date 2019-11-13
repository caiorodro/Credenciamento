import os
from flask import Blueprint
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import redirect
from flask import url_for, jsonify
import json
from app.views.evento import evento
from app.base.mapTable import mapEvento, mapConvidado
from app.base.loggerNoSQL import loggerNoSQL
from datetime import datetime

dataEvento = Blueprint('dataEvento', __name__)

@dataEvento.route('/listEvento', methods=['POST'])
def listEvento():
    rec = json.loads(request.get_data())

    idUser = rec['idUser']

    user1 = evento(rec['keep'], idUser)
    
    result = user1.testListOf()

    del user1

    return result

@dataEvento.route('/getEvento', methods=['POST'])
def getEvento():

    rec = json.loads(request.get_data())

    ID_EVENTO = rec['ID_EVENTO']
    keep = rec['keep']
    idUser = rec['idUser']

    user1 = evento(keep, idUser)
    result = user1.testGet(ID_EVENTO)

    del user1

    return result

@dataEvento.route('/saveEvento', methods=['POST'])
def saveEvento():
    rec = json.loads(request.get_data())

    ID_EVENTO = rec['ID_EVENTO']
    DATA_EVENTO = datetime.strptime(rec['DATA_EVENTO'], '%d/%m/%Y %H:%M')
    TITULO_EVENTO = rec['TITULO_EVENTO']
    ID_EMPRESA = rec['ID_EMPRESA']
    OBSERVACAO = rec['OBSERVACOES']
    NOME_CONVIDADO = rec['NOME_CONVIDADO']
    CELULAR_CONVIDADO = rec['CELULAR_CONVIDADO']
    ID_CONVIDADO = rec['ID_CONVIDADO']

    keep = rec['keep']
    idUser = rec['idUser']

    rec = mapEvento(ID_EVENTO, ID_EMPRESA, DATA_EVENTO, TITULO_EVENTO, OBSERVACAO)
    recConvidado = mapConvidado(ID_CONVIDADO, ID_EVENTO, NOME_CONVIDADO, CELULAR_CONVIDADO)

    user1 = evento(keep, idUser)
    retorno = user1.testSave(rec, recConvidado)

    del user1

    return retorno

@dataEvento.route('/deleteEvento', methods=['POST'])
def deleteEvento():
    rec = json.loads(request.get_data())

    ID_EVENTO = rec['ID_EVENTO']
    keep = rec['keep']
    idUser = rec['idUser']

    user1 = evento(keep, idUser)
    user1.testDelete(ID_EVENTO)

    del user1

    return "Ok"

@dataEvento.route('/listEmpresas', methods=['POST'])
def listEmpresas():
    rec = json.loads(request.get_data())

    keep = rec['keep']
    idUser = rec['idUser']

    user1 = evento(keep, idUser)
    retorno = user1.listEmpresas()

    del user1

    return retorno

@dataEvento.route('/listConvidados', methods=['POST'])
def listConvidados():
    
    rec = json.loads(request.get_data())

    keep = rec['keep']
    idUser = rec['idUser']
    idEvento = rec['ID_EVENTO']

    user1 = evento(keep, idUser)
    retorno = user1.testListConvidados(idEvento)

    del user1

    return retorno

@dataEvento.route('/deleteConvidado', methods=['POST'])
def deleteConvidado():
    rec = json.loads(request.get_data())

    ID_CONVIDADO = rec['ID_CONVIDADO']
    keep = rec['keep']
    idUser = rec['idUser']

    user1 = evento(keep, idUser)
    user1.testDeleteConvidado(ID_CONVIDADO)

    del user1

    return "Ok"

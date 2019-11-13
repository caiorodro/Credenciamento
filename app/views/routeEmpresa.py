import os
from flask import Blueprint
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import redirect
from flask import url_for, jsonify
import json
from app.views.empresaContratante import empresaContratante
from app.base.mapTable import mapEmpresaContratante
from app.base.loggerNoSQL import loggerNoSQL

dataEmpresa = Blueprint('dataEmpresa', __name__)

@dataEmpresa.route('/listEmpresa', methods=['POST'])
def listEmpresa():
    rec = json.loads(request.get_data())

    idUser = rec['idUser']

    user1 = empresaContratante(rec['keep'], idUser)
    
    result = user1.testListOf()

    del user1

    return result

@dataEmpresa.route('/getEmpresa', methods=['POST'])
def getEmpresa():

    rec = json.loads(request.get_data())

    ID_EMPRESA = rec['ID_EMPRESA']
    keep = rec['keep']
    idUser = rec['idUser']

    user1 = empresaContratante(keep, idUser)
    result = user1.testGetEmpresa(ID_EMPRESA)

    del user1

    return result

@dataEmpresa.route('/saveEmpresa', methods=['POST'])
def saveEmpresa():
    rec = json.loads(request.get_data())

    ID_EMPRESA = rec['ID_EMPRESA']
    RAZAO_SOCIAL = rec['RAZAO_SOCIAL']
    NOME_FANTASIA = rec['NOME_FANTASIA']
    CNPJ = rec['CNPJ']
    IE = rec['IE']
    ENDERECO = rec['ENDERECO']
    NUMERO = rec['NUMERO']
    COMPLEMENTO = rec['COMPLEMENTO']
    CEP = rec['CEP']
    MUNICIPIO = rec['MUNICIPIO']
    UF = rec['UF']
    EMAIL = rec['EMAIL']
    TELEFONE = rec['TELEFONE']
    CONTATO = rec['CONTATO']

    keep = rec['keep']
    idUser = rec['idUser']

    table = mapEmpresaContratante(ID_EMPRESA, RAZAO_SOCIAL, NOME_FANTASIA, CNPJ, IE, ENDERECO, NUMERO, COMPLEMENTO, CEP, 
        MUNICIPIO, UF, EMAIL, TELEFONE, CONTATO)

    user1 = empresaContratante(keep, idUser)
    retorno = user1.testSave(table)

    del user1

    return retorno

@dataEmpresa.route('/deleteEmpresa', methods=['POST'])
def deleteEmpresa():
    rec = json.loads(request.get_data())

    ID_EMPRESA = rec['ID_EMPRESA']
    keep = rec['keep']
    idUser = rec['idUser']

    user1 = empresaContratante(keep, idUser)
    user1.testDelete(ID_EMPRESA)

    del user1

    return "Ok"
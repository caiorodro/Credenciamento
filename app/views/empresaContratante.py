import json
from flask import jsonify 
import app.base.QModel as ctx 
from app.base.QBase import qBase
from app.base.mapTable import mapEmpresaContratante
import unittest
from app.base.loggerNoSQL import kindOfLog
from app.base.loggerMySQL import loggerMySQL
import traceback

class empresaContratante(unittest.TestCase):

    def __init__(self, keep=None, idUser=None):
        self.qBase = qBase(keep)
        self.__loggerMySQL = loggerMySQL(keep, idUser)
        self.__listOf = []
        self.__idUser = idUser
        self.__rec = None
        self.__email = ''

    def listEmpresa(self, name=None, email=None):
        btnEdit = '<button class="btn btn-primary waves-effect waves-light" onclick="editEmpresa({});" title="Editar"><i class="ti-pencil"></i></button>'
        btnDelete = '<button class="btn btn-danger waves-effect waves-light" onclick="deleteEmpresa({});" title="Deletar"><i class="ti-trash"></i></button>'

        table = ctx.mapEmpresaContratante

        select1 = ctx.session.query(
            table.ID_EMPRESA,
            table.NOME_FANTASIA,
            table.UF,
            table.CONTATO,
            table.TELEFONE
            ).order_by(table.NOME_FANTASIA)

        select1 = select1.all()

        [(self.__listOf.append((
            row.NOME_FANTASIA,
            row.UF,
            row.CONTATO,
            row.TELEFONE,
            btnEdit.format(str(row.ID_EMPRESA)), 
            btnDelete.format(str(row.ID_EMPRESA))))) for row in select1]

        return len(self.__listOf)

    def saveEmpresa(self, empresa=mapEmpresaContratante):

        try:
            cmd = None

            if empresa.ID_EMPRESA > 0:

                cmd = ctx.tb_empresa_contratante.update().values(
                    RAZAO_SOCIAL = empresa.RAZAO_SOCIAL.upper(),
                    NOME_FANTASIA = empresa.NOME_FANTASIA.upper(),
                    CNPJ = empresa.CNPJ.upper(),
                    IE = empresa.IE.upper(),
                    ENDERECO = empresa.ENDERECO.upper(),
                    NUMERO = empresa.NUMERO.upper(),
                    COMPLEMENTO = empresa.COMPLEMENTO.upper(),
                    CEP = empresa.CEP.upper(),
                    MUNICIPIO = empresa.MUNICIPIO.upper(),
                    UF = empresa.UF.upper(),
                    EMAIL = empresa.EMAIL.lower(),
                    TELEFONE = empresa.TELEFONE.upper(),
                    CONTATO = empresa.CONTATO.upper()
                    ).where(ctx.mapEmpresaContratante.ID_EMPRESA == empresa.ID_EMPRESA)

            elif empresa.ID_EMPRESA == 0:

                cmd = ctx.tb_empresa_contratante.insert().values(
                    RAZAO_SOCIAL = empresa.RAZAO_SOCIAL.upper(),
                    NOME_FANTASIA = empresa.NOME_FANTASIA.upper(),
                    CNPJ = empresa.CNPJ.upper(),
                    IE = empresa.IE.upper(),
                    ENDERECO = empresa.ENDERECO.upper(),
                    NUMERO = empresa.NUMERO.upper(),
                    COMPLEMENTO = empresa.COMPLEMENTO.upper(),
                    CEP = empresa.CEP.upper(),
                    MUNICIPIO = empresa.MUNICIPIO.upper(),
                    UF = empresa.UF.upper(),
                    EMAIL = empresa.EMAIL.lower(),
                    TELEFONE = empresa.TELEFONE.upper(),
                    CONTATO = empresa.CONTATO.upper())

            ctx.session.execute(cmd)
            ctx.session.commit()

            return True
        except Exception as ex:
            self.__loggerMySQL.testInsertLog(ex.args[0], kindOfLog.ERROR(), traceback.format_exc())

            return False

    def deleteEmpresa(self, ID_EMPRESA):

        try:
            q = ctx.session.query(ctx.mapEmpresaContratante).filter(ctx.mapEmpresaContratante.ID_EMPRESA == ID_EMPRESA)

            if not ctx.session.query(q.exists()).scalar():
                raise Exception('Empresa não encontrado')

            del1 = ctx.tb_empresa_contratante.delete().where(ctx.mapEmpresaContratante.ID_EMPRESA == ID_EMPRESA)

            ctx.session.execute(del1)
            ctx.session.commit()

            return True
        except Exception as ex:
            _message = ex.args[0]
            self.__loggerMySQL.testInsertLog(_message, kindOfLog.ERROR(), traceback.format_exc())

            return False

    def getEmpresa(self, ID_EMPRESA):
        table = ctx.mapEmpresaContratante

        select1 = ctx.session.query(
            table.ID_EMPRESA,
            table.RAZAO_SOCIAL,
            table.NOME_FANTASIA,
            table.CNPJ,
            table.IE,
            table.ENDERECO,
            table.NUMERO,
            table.COMPLEMENTO,
            table.CEP,
            table.MUNICIPIO,
            table.UF,
            table.EMAIL,
            table.TELEFONE,
            table.CONTATO).filter(table.ID_EMPRESA == ID_EMPRESA).all()

        self.__rec = self.qBase.toDict(select1)

        return True

    def testListOf(self, name=None, email=None):
        try:
            self.assertGreater(self.listEmpresa(), 0)
            return self.qBase.toJson(self.__listOf)

        except AssertionError as ae:
            self.__loggerMySQL.testInsertLog(ae.args[0], kindOfLog.INFO(), traceback.format_exc())

            return self.qBase.toJson(self.__listOf)

    def testSave(self, empresa=mapEmpresaContratante):
        try:
            self.assertTrue(self.saveEmpresa(empresa))
            
            self.__loggerMySQL.testInsertLog('Ok', kindOfLog.INFO(), 'Insert Ok')

            return self.qBase.toJsonRoute("Ok", 200)
        except AssertionError as ae:
            _message = ae.args[0]
            self.__loggerMySQL.testInsertLog(_message, kindOfLog.ERROR(), traceback.format_exc())

            return self.qBase.toJsonRoute(_message, 500)

    def testDelete(self, idEmpresa):
        try:
            self.assertTrue(self.deleteEmpresa(idEmpresa))

            return self.qBase.toJsonRoute("Ok", 200)
        except AssertionError:
            _message = "There is a problem on delete this company. Look at the logs"

            return self.qBase.toJsonRoute(_message, 500)

    def testGetEmpresa(self, ID_EMPRESA):
        try:
            self.assertTrue(self.getEmpresa(ID_EMPRESA))

            return self.qBase.toJsonRoute(str(self.__rec), 200)
        except AssertionError:
            _message = "There is a problem to delete this company. Look at the logs"

            return self.qBase.toJsonRoute(_message, 500)

    def close(self):
        try:
            ctx.conn.close()
        except:
            pass

    def __del__(self):
        self.close()

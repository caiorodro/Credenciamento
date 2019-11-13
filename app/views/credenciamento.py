from datetime import datetime
import json

from flask import jsonify
import traceback
import unittest

import app.base.QModel as ctx
from app.base.QBase import qBase
from app.base.mapTable import mapCredenciamento, mapEvento, mapConvidado
from app.base.loggerNoSQL import kindOfLog
from app.base.loggerMySQL import loggerMySQL

class credenciamento(unittest.TestCase):

    def __init__(self, keep=None, idUser=None):
        self.qBase = qBase(keep)
        self.__loggerMySQL = loggerMySQL(keep, idUser)
        self.__listOf = []
        self.__idUser = idUser
        self.__rec = None
        self.__email = ''

    def listEvento(self, ID_EVENTO):

        table = ctx.mapConvidado

        select1 = ctx.session.query(
            table.ID_CONVIDADO,
            table.ID_EVENTO,
            ctx.mapEvento.DATA_EVENTO,
            ctx.mapEvento.TITULO_EVENTO,
            table.NOME_CONVIDADO)\
            .filter(table.ID_EVENTO == ID_EVENTO)\
            .join(ctx.mapEvento, ctx.mapEvento.ID_EVENTO == table.ID_EVENTO)\
            .order_by(table.NOME_CONVIDADO)

        def checkIt(ID_EVENTO, ID_CONVIDADO):
            presente = ctx.session.query(
                ctx.mapCredenciamento.ID_CREDENCIAMENTO)\
                    .filter(ctx.mapCredenciamento.ID_CONVIDADO == ID_CONVIDADO)

            ID_CREDENCIAMENTO = 0
            
            for row in presente.all():
                ID_CREDENCIAMENTO = row.ID_CREDENCIAMENTO

            btnPresente = '<button class="btn btn-purple waves-effect waves-light" onclick="adicionaPresenca({}, {});" title="Confirmar presença"><i class="mdi mdi-account-check"></i></button>'
            btnAusente = '<button class="btn btn-danger waves-effect waves-light" onclick="deletePresenca({});" title="Deletar presença"><i class="mdi mdi-account-remove"></i></button>'

            btn = btnPresente.format(str(ID_EVENTO), str(ID_CONVIDADO)) if ID_CREDENCIAMENTO == 0 else \
                btnAusente.format(str(ID_CREDENCIAMENTO))

            return (ID_CREDENCIAMENTO, btn)

        for row in select1.all():
            ctrls = checkIt(row.ID_EVENTO, row.ID_CONVIDADO)

            self.__listOf.append((
                row.TITULO_EVENTO,
                row.DATA_EVENTO.strftime('%d/%m/%Y %H:%M'),
                row.NOME_CONVIDADO,
                'Sim' if ctrls[0] > 0 else 'Não',
                ctrls[1]))

        return len(self.__listOf)

    def adicionaPresenca(self, ID_EVENTO, ID_CONVIDADO):

        try:

            table = ctx.mapCredenciamento

            q = ctx.session.query(table).filter(table.ID_CONVIDADO == ID_CONVIDADO and table.ID_EVENTO == ID_EVENTO)

            if not ctx.session.query(q.exists()).scalar():

                cmd = ctx.tb_credenciamento.insert().values(
                    DATA_HORA = datetime.now(),
                    ID_EVENTO = ID_EVENTO,
                    ID_CONVIDADO = ID_CONVIDADO,
                    PRESENTE = 1)

                ctx.session.execute(cmd)
                ctx.session.commit()

            return True
        except Exception as ex:
            self.__loggerMySQL.testInsertLog(ex.args[0], kindOfLog.ERROR(), traceback.format_exc())

            return False

    def deletePresenca(self, ID_CREDENCIAMENTO):

        try:
            q = ctx.session.query(ctx.mapCredenciamento).filter(ctx.mapCredenciamento.ID_CREDENCIAMENTO == ID_CREDENCIAMENTO)

            if not ctx.session.query(q.exists()).scalar():
                raise Exception('Registro não encontrado')

            del1 = ctx.tb_credenciamento.delete().where(ctx.mapCredenciamento.ID_CREDENCIAMENTO == ID_CREDENCIAMENTO)

            ctx.session.execute(del1)
            ctx.session.commit()

            return True
        except Exception as ex:
            _message = ex.args[0]
            self.__loggerMySQL.testInsertLog(_message, kindOfLog.ERROR(), traceback.format_exc())

            return False

    def listComboEvento(self, DATA):
        table = ctx.mapEvento

        query = ctx.session.query(
            table.ID_EVENTO,
            table.TITULO_EVENTO,
            table.DATA_EVENTO
        ).filter(table.DATA_EVENTO >= DATA)\
            .order_by(table.DATA_EVENTO)

        retorno = []

        [retorno.append({
            "ID_EVENTO": row.ID_EVENTO, "TITULO_EVENTO": 
                ''.join((row.TITULO_EVENTO, ' - ', row.DATA_EVENTO.strftime('%d/%m/%Y %H:%M')))
        }) for row in query]

        self.__listOf = retorno

        return True

    def testListOf(self, ID_EVENTO):
        try:
            self.assertGreater(self.listEvento(ID_EVENTO), 0)
            return self.qBase.toJson(self.__listOf)

        except AssertionError as ae:
            self.__loggerMySQL.testInsertLog(ae.args[0], kindOfLog.INFO(), traceback.format_exc())

            return self.qBase.toJson(self.__listOf)

    def testAdicionaPresenca(self, ID_EVENTO, ID_CONVIDADO):
        try:
            self.assertTrue(self.adicionaPresenca(ID_EVENTO, ID_CONVIDADO))

            self.__loggerMySQL.testInsertLog('Ok', kindOfLog.INFO(), 'Insert Ok')

            return self.qBase.toJsonRoute("Ok", 200)
        except AssertionError as ae:
            _message = ae.args[0]
            self.__loggerMySQL.testInsertLog(_message, kindOfLog.ERROR(), traceback.format_exc())

            return self.qBase.toJsonRoute(_message, 500)

    def testDeletePresenca(self, ID_CREDENCIAMENTO):
        try:
            self.assertTrue(self.deletePresenca(ID_CREDENCIAMENTO))

            return self.qBase.toJsonRoute("Ok", 200)
        except AssertionError:
            _message = "There is a problem on delete this credentials. Look at the logs"

            return self.qBase.toJsonRoute(_message, 500)

    def testListComboEvento(self, DATA):
        try:
            self.assertTrue(self.listComboEvento(DATA))

            return self.qBase.toJsonRoute(self.__listOf, 200)
        except AssertionError as ae:
            _error = ae.args[0]
            _message = f"There is a problem to load Event combo data. Look at the logs {_error}"

            self.__loggerMySQL.testInsertLog(_message, kindOfLog.ERROR(), traceback.format_exc())

            return self.qBase.toJsonRoute(_message, 500)

    def __del__(self):
        pass

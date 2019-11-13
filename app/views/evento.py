import json
import unittest
import traceback

from flask import jsonify 
from sqlalchemy import func

import app.base.QModel as ctx 
from app.base.QBase import qBase
from app.base.mapTable import mapEvento, mapConvidado
from app.base.loggerNoSQL import kindOfLog
from app.base.loggerMySQL import loggerMySQL

class evento(unittest.TestCase):

    def __init__(self, keep=None, idUser=None):
        self.qBase = qBase(keep)
        self.__loggerMySQL = loggerMySQL(keep, idUser)
        self.__listOf = []
        self.__idUser = idUser
        self.__rec = None
        self.__email = ''
        self.__ID_EVENTO = 0

    def listEvento(self, name=None, email=None):
        btnEdit = '<button class="btn btn-primary waves-effect waves-light" onclick="editEvento({});" title="Editar"><i class="ti-pencil"></i></button>'
        btnDelete = '<button class="btn btn-danger waves-effect waves-light" onclick="deleteEvento({});" title="Deletar"><i class="ti-trash"></i></button>'

        table = ctx.mapEvento

        select1 = ctx.session.query(
            table.ID_EVENTO,
            table.ID_EMPRESA,
            ctx.mapEmpresaContratante.NOME_FANTASIA,
            table.DATA_EVENTO,
            table.TITULO_EVENTO,
            table.OBSERVACAO)\
             .join(ctx.mapEmpresaContratante, ctx.mapEmpresaContratante.ID_EMPRESA == table.ID_EMPRESA)\
             .order_by(table.DATA_EVENTO)

        def getRowCount(idEvento):
            rowCount = ctx.session.query(ctx.mapConvidado.ID_EVENTO, func.count(ctx.mapConvidado.ID_CONVIDADO))\
                .filter(ctx.mapConvidado.ID_EVENTO == idEvento).group_by(ctx.mapConvidado.ID_EVENTO).all()

            return rowCount[0][1] if len(rowCount) > 0 else 0

        [(self.__listOf.append((
            row.DATA_EVENTO.strftime('%d/%m/%Y %H:%M'),
            row.NOME_FANTASIA,
            row.TITULO_EVENTO,
            getRowCount(row.ID_EVENTO),
            btnEdit.format(str(row.ID_EVENTO)),
            btnDelete.format(str(row.ID_EVENTO))))) for row in select1.all()]

        return len(self.__listOf)

    def saveEvento(self, evento=mapEvento, convidado=mapConvidado):

        try:
            cmd = None

            if evento.ID_EVENTO > 0:

                cmd = ctx.tb_evento.update().values(
                    DATA_EVENTO = evento.DATA_EVENTO,
                    TITULO_EVENTO = evento.TITULO_EVENTO.upper(),
                    ID_EMPRESA = evento.ID_EMPRESA,
                    OBSERVACAO = evento.OBSERVACAO
                    ).where(ctx.mapEvento.ID_EVENTO == evento.ID_EVENTO)

                ctx.session.execute(cmd)

            elif evento.ID_EVENTO == 0:
                cmd = ctx.tb_evento.insert().values(
                    DATA_EVENTO = evento.DATA_EVENTO,
                    TITULO_EVENTO = evento.TITULO_EVENTO.upper(),
                    ID_EMPRESA = evento.ID_EMPRESA,
                    OBSERVACAO = evento.OBSERVACAO)

                inserted = ctx.session.execute(cmd)

                evento.ID_EVENTO = inserted.inserted_primary_key[0]

            if len(convidado.NOME_CONVIDADO) > 0:
                if convidado.ID_CONVIDADO == 0 :
                    cmd1 = ctx.tb_convidado.insert().values(
                        ID_EVENTO = evento.ID_EVENTO,
                        NOME_CONVIDADO = convidado.NOME_CONVIDADO,
                        CELULAR_CONVIDADO = convidado.CELULAR_CONVIDADO
                    )
                elif convidado.ID_CONVIDADO > 0:
                    cmd1 = ctx.tb_convidado.update().values(
                        NOME_CONVIDADO = convidado.NOME_CONVIDADO,
                        CELULAR_CONVIDADO = convidado.CELULAR_CONVIDADO
                    ).where(ctx.mapConvidado.ID_CONVIDADO == convidado.ID_CONVIDADO)

            ctx.session.execute(cmd1)
            ctx.session.commit()

            self.__ID_EVENTO = evento.ID_EVENTO

            return True
        except Exception as ex:
            self.__loggerMySQL.testInsertLog(ex.args[0], kindOfLog.ERROR(), traceback.format_exc())

            return False

    def deleteEvento(self, ID_EVENTO):

        try:
            q = ctx.session.query(ctx.mapEvento).filter(ctx.mapEvento.ID_EVENTO == ID_EVENTO)

            if not ctx.session.query(q.exists()).scalar():
                raise Exception('Evento não encontrado')

            del1 = ctx.tb_evento.delete().where(ctx.mapEvento.ID_EVENTO == ID_EVENTO)

            ctx.session.execute(del1)
            ctx.session.commit()

            return True
        except Exception as ex:
            _message = ex.args[0]
            self.__loggerMySQL.testInsertLog(_message, kindOfLog.ERROR(), traceback.format_exc())

            return False

    def getEvento(self, ID_EVENTO):
        table = ctx.mapEvento

        select1 = ctx.session.query(
            table.ID_EVENTO,
            table.DATA_EVENTO,
            table.TITULO_EVENTO,
            table.ID_EMPRESA,
            table.OBSERVACAO).filter(table.ID_EVENTO == ID_EVENTO).all()

        self.__rec = self.qBase.toDict(select1)

        self.__rec[0]['DATA_EVENTO'] = self.__rec[0]['DATA_EVENTO'].strftime('%Y-%m-%d %H:%M')

        return True

    def listEmpresas(self):
        table = ctx.mapEmpresaContratante

        query = ctx.session.query(
            table.ID_EMPRESA,
            table.NOME_FANTASIA
        ).order_by(table.NOME_FANTASIA)

        retorno = []

        [retorno.append({
            "ID_EMPRESA": row.ID_EMPRESA, "NOME_FANTASIA": row.NOME_FANTASIA
        }) for row in query]

        return self.qBase.toJsonRoute(retorno, 200)

    def listConvidados(self, ID_EVENTO):
        btnEdit = '<button class="btn btn-primary waves-effect waves-light" title="Editar"><i class="ti-pencil"></i></button>'
        btnDelete = '<button class="btn btn-danger waves-effect waves-light" onclick="deleteConvidado({});" title="Deletar"><i class="ti-trash"></i></button>'

        table = ctx.mapConvidado

        query = ctx.session.query(
            table.ID_CONVIDADO,
            table.NOME_CONVIDADO,
            table.CELULAR_CONVIDADO
        ).filter(ctx.mapConvidado.ID_EVENTO == ID_EVENTO).order_by(table.NOME_CONVIDADO)

        [(
            self.__listOf.append((
                row.ID_CONVIDADO,
                row.NOME_CONVIDADO,
                row.CELULAR_CONVIDADO,
                btnEdit,
                btnDelete.format(str(row.ID_CONVIDADO))))) for row in query]

        return True

    def deleteConvidado(self, ID_CONVIDADO):

        try:
            q = ctx.session.query(ctx.mapConvidado).filter(ctx.mapConvidado.ID_CONVIDADO == ID_CONVIDADO)

            if not ctx.session.query(q.exists()).scalar():
                raise Exception('Convidado(a) não encontrado(a)')

            del1 = ctx.tb_convidado.delete().where(ctx.mapConvidado.ID_CONVIDADO == ID_CONVIDADO)

            ctx.session.execute(del1)
            ctx.session.commit()

            return True
        except Exception as ex:
            _message = ex.args[0]
            self.__loggerMySQL.testInsertLog(_message, kindOfLog.ERROR(), traceback.format_exc())

            return False

    def testListOf(self, name=None, email=None):
        try:
            self.assertGreater(self.listEvento(), 0)
            return self.qBase.toJson(self.__listOf)

        except AssertionError as ae:
            self.__loggerMySQL.testInsertLog(ae.args[0], kindOfLog.INFO(), traceback.format_exc())

            return self.qBase.toJson(self.__listOf)

    def testSave(self, evento=mapEvento, convidado=mapConvidado):
        try:
            self.assertTrue(self.saveEvento(evento, convidado))

            self.__loggerMySQL.testInsertLog('Ok', kindOfLog.INFO(), 'Insert Ok')

            return self.qBase.toJsonRoute(str(self.__ID_EVENTO), 200)

        except AssertionError as ae:
            _message = ae.args[0]
            self.__loggerMySQL.testInsertLog(_message, kindOfLog.ERROR(), traceback.format_exc())

            return self.qBase.toJsonRoute(_message, 500)

    def testDelete(self, idEvento):
        try:
            self.assertTrue(self.deleteEvento(idEvento))

            return self.qBase.toJsonRoute("Ok", 200)
        except AssertionError:
            _message = "There is a problem on delete this event. Look at the logs"

            return self.qBase.toJsonRoute(_message, 500)

    def testDeleteConvidado(self, idConvidado):
        try:
            self.assertTrue(self.deleteConvidado(idConvidado))

            return self.qBase.toJsonRoute("Ok", 200)
        except AssertionError:
            _message = "There is a problem on delete this guest. Look at the logs"

            return self.qBase.toJsonRoute(_message, 500)

    def testGet(self, ID_EVENTO):
        try:
            self.assertTrue(self.getEvento(ID_EVENTO))

            return self.qBase.toJsonRoute(str(self.__rec), 200)
        except AssertionError:
            _message = "There is a problem to delete this event. Look at the logs"

            return self.qBase.toJsonRoute(_message, 500)

    def testListConvidados(self, ID_EVENTO):
        try:
            self.assertTrue(self.listConvidados(ID_EVENTO))
            
            return self.qBase.toJson(self.__listOf)
        except AssertionError:
            _message = "There is a problem to delete this event. Look at the logs"

            return self.qBase.toJsonRoute(_message, 500)

    def close(self):
        try:
            ctx.conn.close()
        except:
            pass

    def __del__(self):
        self.close()

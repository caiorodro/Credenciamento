from datetime import datetime
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

class dashBoard(unittest.TestCase):

    def __init__(self, keep=None, idUser=None):
        self.qBase = qBase(keep)
        self.__loggerMySQL = loggerMySQL(keep, idUser)
        self.__dataChart = ''   

    def chartPeopleByEvents(self, fromDate):
        try:
            table = ctx.mapEvento

            query = ctx.session.query(
                table.ID_EVENTO,
                table.TITULO_EVENTO,
                table.DATA_EVENTO
            ).filter(table.DATA_EVENTO >= datetime.strptime(fromDate, '%d/%m/%Y'))

            tableCredenciamento = ctx.mapCredenciamento
            tableConvidado = ctx.mapConvidado

            retorno = "['Evento', 'Presentes', 'Ausentes', { role: 'annotation' }]"

            for item in query.all():
                presentes = ctx.session.query(tableCredenciamento.ID_EVENTO).filter(tableCredenciamento.ID_EVENTO == item.ID_EVENTO).count()
                ausentes = ctx.session.query(tableConvidado.ID_EVENTO).filter(tableConvidado.ID_EVENTO == item.ID_EVENTO).count() - presentes

                retorno += ",[{}, {}, {}, '']".format("'" + item.TITULO_EVENTO + "'", str(presentes), str(ausentes))

            self.__dataChart = "[{}]".format(retorno)

            return True
        except Exception as ex:
            self.__loggerMySQL.insertLog(ex.args[0], kindOfLog.ERROR(), traceback.format_exc())

            return False

    def testchartPeopleByEvents(self, fromDate):
        try:
            self.assertTrue(self.chartPeopleByEvents(fromDate))

            return self.qBase.toJsonRoute(self.__dataChart, 200)
        except AssertionError:
            _message = "There is a problem to load data chart. Look at the logs"

            return self.qBase.toJsonRoute(_message, 500)




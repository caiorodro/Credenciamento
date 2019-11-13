from datetime import datetime
from enum import Enum
import requests
import unittest

import traceback

import app.base.QModel as ctx 
from app.base.QBase import qBase
from app.base.mapTable import mapLogger

class loggerMySQL(unittest.TestCase):

    def __init__(self, keep=None, idUser=None):
        """
        Class that write and read logging on any kind info or error of the application
        """
        self.qBase = qBase(keep)
        self.__idUser = idUser
        self.__listOfLogs = None

    def insertLog(self, message, kind, trace):
        """
        Create a new log info or error and insert on database
        """

        cmd = ctx.tb_logger.insert().values(
            ID_LOG = 0,
            ID_USER = self.__idUser,
            DATE_OF = datetime.now(),
            MESSAGE1 = message,
            LEVEL1 = kind,
            TRACE = trace)

        ctx.session.execute(cmd)
        ctx.session.commit()

        return True

    def listLogs(self, data, start, limit):
        """
        Creates a filtered list of collextion logs

        Return: returns a length of records found
        """
        
        btnView = '<button class="btn btn-default waves-effect waves-light btn-sm m-b-5" onclick="viewLog({});" title="Visualizar log"><i class="dripicons-article"></i></button>'

        tbl = ctx.mapLogger

        select1 = ctx.session.query(
            tbl.ID_LOG,
            tbl.ID_USER,
            tbl.DATE_OF,
            tbl.MESSAGE1,
            tbl.LEVEL1,
            tbl.TRACE).order_by(tbl.DATE_OF)

        select1 = select1.filter(tbl.DATE_OF >= data)

        select1 = select1.all()

        [(self.__listOfLogs.append((row.ID_LOG,
            row.ID_USER,
            row.DATE_OF,
            row.MESSAGE1,
            row.LEVEL1,
            row.TRACE,
            btnView.format(str(row.ID_USER))))) for row in select1]

        return len(self.__listOfLogs)

    def testListLogs(self, data, start, limit):
        """
        Tests the list of logs

        Return: returns the listOfLogs filled list 
        """

        try:
            self.assertGreater(self.listLogs(data, start, limit), 0)
        except AssertionError:
            pass

        return self.qBase.toJsonRoute(self.__listOfLogs, 200)

    def testInsertLog(self, message, kind, trace):
        """
        Tests the list of logs

        Return: returns the listOfLogs filled list 
        """

        try:
            self.assertTrue(self.insertLog(message, kind, trace))
        except AssertionError:
            pass
import os
from flask import Blueprint
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import redirect
from flask import url_for, jsonify
import json
from app.views.dashBoard import dashBoard
from app.base.loggerNoSQL import loggerNoSQL

dataDashBoard = Blueprint('dataDashBoard', __name__)

@dataDashBoard.route('/chartPeopleByEvents', methods=['POST'])
def chartPeopleByEvents():
    rec = json.loads(request.get_data())

    idUser = rec['idUser']
    dateFrom = rec['dateFrom']

    user1 = dashBoard(rec['keep'], idUser)
    
    result = user1.testchartPeopleByEvents(dateFrom)

    del user1

    return result

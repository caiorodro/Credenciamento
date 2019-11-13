import os
from flask import Blueprint
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import redirect
from flask import url_for
from flask import jsonify
import json
from app.base.mapTable import mapUser

cwd = os.getcwd()

dataTemplate = Blueprint('dataTemplate', __name__)

@dataTemplate.route('/app/templates/scripts/<path:path>')
def send_scripts(path):
    return send_from_directory('app/templates/scripts', path)

@dataTemplate.route('/app/templates/css/<path:path>')
def send_css(path):
    return send_from_directory('app/templates/css', path)

@dataTemplate.route('/app/csv/<path:filename>', methods=['GET', 'POST'])
def downloadCSV(filename):
    uploads = '/'.join((cwd, 'app/csv/'))
    return send_from_directory(directory=uploads, filename=filename)

@dataTemplate.route('/app/templates/assets/<path:path>')
def send_assets(path):
    return send_from_directory('app/templates/assets', path)

@dataTemplate.route('/app/templates/assets/images/<path:path>')
def send_assets_images(path):
    return send_from_directory('app/templates/assets/images', path)

@dataTemplate.route('/app/templates/images/<path:path>')
def send_images(path):
    return send_from_directory('app/templates/images', path)

@dataTemplate.route('/app/templates/dist/<path:path>')
def send_dist(path):
    return send_from_directory('app/templates/dist', path)

@dataTemplate.route("/")
def hello():
    return render_template('index.html')

@dataTemplate.route("/panel")
def panel():
    return render_template('painel.html')

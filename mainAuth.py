from flask import Flask
from app.views.routeUser import dataUser
from app.views.routeEmpresa import dataEmpresa
from app.views.routeTemplates import dataTemplate
from app.views.routeEvento import dataEvento
from app.views.routeCredenciamento import dataCredenciamento
from app.views.routeDashboard import dataDashBoard

import os

cwd = os.getcwd()

templates = '/'.join((cwd, 'app/templates/'))
app = Flask(__name__, template_folder=templates, static_url_path="")

packs = [dataUser, dataTemplate, dataEmpresa, dataEvento, dataCredenciamento, dataDashBoard]

[app.register_blueprint(pack) for pack in packs]

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, use_reloader=True)

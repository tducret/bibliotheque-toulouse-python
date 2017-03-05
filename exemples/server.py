# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import Response
import bibliothequetoulouse as bib


app = Flask(__name__)


# https://api.fakecompany.com/v1/search?q=running+paid
# https://api.fakecompany.com/v1/rechercher?q=victor+hugo
# https://api.fakecompany.com/v1/rechercher?auteur=victor+hugo&titre=les+miserables

@app.route('/')
def home():
    return 'Accueil'

@app.route('/rechercher', methods=['GET'])
def rechercher():
    print request.args.get('auteur')
    print request.args.get('titre')
    resultats = bib.rechercher(titre=request.args.get('titre'),
                       auteur=request.args.get('auteur'),
                       dispo_uniquement=True)
    
    resp = Response(str(resultats), status=200, mimetype='application/json')
    
    return resp

if __name__ == '__main__':
    app.run()

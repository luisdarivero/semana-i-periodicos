#!/usr/bin/env python3
#encoding: UTF-8
#pip install Flask
from flask import Flask, render_template, Markup, jsonify, request
#Clase que maneja objetos tipo JSON
import json
#Clase
from seleniumApp import SeleniumManager


application = Flask(__name__)

@application.route("/")
def main():
    diccionario = {"Status" : "Success"}
    resp = jsonify(diccionario)
    resp.status_code = 200
    return resp

@application.route("/get_urls_eluniversal")
def get_urls_eluniversal():
    try:
        sm = SeleniumManager()
        liga = sm.ligaBusquedaUniversal("policia muerto")
        sm.abrir(liga)
        urlList = sm.getLinks()
        sm.exit()
        contador = 0
        listaURLs = []
        for url in urlList:
            listaURLs.append({"url":url})
            contador += 1;
        diccionario = {"elementos" : str(contador), "urls" : listaURLs}
        resp = jsonify(diccionario)
        resp.status_code = 200
        return resp
    except Exception as e:
        diccionario = {"status" : "error", "ErrorName" : str(e)}
        resp = jsonify(diccionario)
        resp.status_code = 500
        return resp

if __name__ == '__main__':
    application.run(debug=True, host = '0.0.0.0', port = 80)


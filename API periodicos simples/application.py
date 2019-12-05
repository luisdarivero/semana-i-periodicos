#encoding: UTF-8
#pip install Flask
from flask import Flask, render_template, Markup, jsonify, request
#pip install flask-cors
from flask_cors import CORS
#Clase que maneja objetos tipo JSON
import json
#Clase
from NewspaperScrapper import NewspaperScrapper

from news_checker import News_checker

from podio import Podio

#mail sender=========================================
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(message, subject):
    # create message object instance
    msg = MIMEMultipart()
    # setup the parameters of the message
    password = "O23KSDLCXMA_yocullar"
    msg['From'] = "luisdaniel@ocullar.com"
    msg['To'] = "luisdarivero.s@gmail.com"
    msg['Subject'] = subject
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

    #mail sender=========================================


application = Flask(__name__)
CORS(application,resources={r"*": {"origins": "*"}})

@application.route('/podio/hook',methods = ['GET', 'POST'])
def podiohook():
    try:

        type = request.form['type']
        hookid = request.form['hook_id']
        code = request.form['code']
        podioError = None
        if(type == "hook.verify"):
            try:
                podio = Podio()
                podio.validateHook(hookid, code)
            except Exception as e:
                try:
                    podioError = json.loads(str(e).encode("utf-8"))
                except:
                    podioError = str(e)

        dictionary = {
            "type" : type,
            "hookid" : hookid,
            "code":code,
            "podioError":podioError
        }

        emailResponse  = json.dumps(dictionary)
        sendMail(str(emailResponse),"podio Mail")

        diccionario = {"Status" : "Success"}
        resp = jsonify(diccionario)
        resp.status_code = 200

        return resp
    except Exception as e:
        dictionary = {
            "Status" : "Error",
            "error": str(e),
            "data": str(request.form)
        }
        emailResponse  = json.dumps(dictionary)
        sendMail(str(emailResponse),"podio Mail")
        
        resp = jsonify(dictionary)
        resp.status_code = 200
        return resp

@application.route("/")
def main():
    diccionario = {"Status" : "Success"}
    resp = jsonify(diccionario)
    resp.status_code = 200
    return resp

@application.route("/get_urls_lajornada")
def get_urls_lajornada():
    try:
        np = NewspaperScrapper()
        urlList =  np.get_urls_lajornada()
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
        diccionario = {"success": False, "error" : str(e)}
        resp = jsonify(diccionario)
        resp.status_code = 500
        return resp

@application.route("/get_urls_milenio")
def get_urls_milenio():
    try:
        np = NewspaperScrapper()
        urlList =  np.get_urls_milenio()
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
        diccionario = {"success": False, "error" : str(e)}
        resp = jsonify(diccionario)
        resp.status_code = 500
        return resp

@application.route("/get_urls_heraldo_recent")
def get_urls_heraldo_recent():
    try:
        np = NewspaperScrapper()
        urlList =  np.get_urls_heraldo_recent()
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
        diccionario = {"success": False, "error" : str(e)}
        resp = jsonify(diccionario)
        resp.status_code = 500
        return resp

@application.route("/get_urls_lajornadaoriente_recent")
def get_urls_lajornadaoriente_recent():
    try:
        np = NewspaperScrapper()
        urlList =  np.get_urls_lajornadaoriente_recent()
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
        diccionario = {"success": False, "error" : str(e)}
        resp = jsonify(diccionario)
        resp.status_code = 500
        return resp

@application.route('/news_checker', methods=['POST']) #GET requests will be blocked
def news_checker():
    try:
        content = request.stream.read().decode('utf-8')
        content = json.loads(content)
        url = content["url"]
        date = content["date"]
        text = content["text"]
        periodico = content["newspaper"]
        print(text)
        checker = News_checker()
        response = checker.azureTextAnalyze(url,date,periodico,text)
        diccionario = {"success" : response}
        resp = jsonify(diccionario)
        resp.status_code = 200
        return resp
    except Exception as e:
        diccionario = {"success": False, "error" : str(e)}
        resp = jsonify(diccionario)
        resp.status_code = 500
        return resp

if __name__ == '__main__':
    application.run()

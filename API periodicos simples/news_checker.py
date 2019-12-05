# -*- coding: utf-8 -*-
import requests
import json
from pymongo import MongoClient

class News_checker:
    lst_palabras_tristes = ["muere","mueren","murió","murieron", "asesinó","asesinaron","asesinado","asesinando",
    "policía","policías","federales","estatales","municipales","fallece","fallecen","falleció", "falleciendo",
    "fallecieron","fallecido","ejecutan","ejecutó","ejecutaron","ejecutado","ejecutando","dispara","disparan",
    "disparó","dispararon","disparado","disparando","agente","patrulla","arma","pistola","operativo","sangre",
    "tiroteo","muere","cadáver","cuerpo","custodio","balazos","balazo","balacera","lesionados","balaceando",
    "tirador","tiró","tiraron","tirando","vida","perdió","perdieron","policiaco","policial","fuerza","fuerzas",
    "uniformados","guardia","ministerio","seguridad","violento","enfrentamiento","armado","oficial","calibre",
    "cartucho","cartuchos","rifle","ametralladora","ametralladoras","rafaguiada","rafaguiado","acribillada",
    "acribillado","acribillados ","fusilado","fusilada","homicidio","asesinato","muerte","muertos","armas",
    "armados","comando","federal","estatal","municipal","agentes","fiscal","balas","fiscalía"]
    subscription_key = 'a11e611aced646abaea980f652ab0b6c'
    endpoint = 'https://semanai2019money.cognitiveservices.azure.com/'
    keyphrase_url = endpoint + "/text/analytics/v2.1/keyphrases"
    entities_url = endpoint + "/text/analytics/v2.1/entities"
    sentiment_url = endpoint + "/text/analytics/v2.1/sentiment"
    def azureTextAnalyze(self,url,fecha,periodico,texto):
        #key words
        documents = {"documents": [{"id": "1", "language": "es","text": texto}]}
        headers_keyWords = {"Ocp-Apim-Subscription-Key": News_checker.subscription_key}
        response = requests.post(News_checker.keyphrase_url, headers=headers_keyWords, json=documents)
        key_phrases = response.content
        data_key_words = json.loads(key_phrases)
        lst_key_words=[]
        for item in data_key_words["documents"]:
            for phrase in item["keyPhrases"]:
                for word in phrase.split():
                    lst_key_words.append(word.lower())
        lst_ok_key_words=[]
        for word in lst_key_words:
            if word in News_checker.lst_palabras_tristes and not word in lst_ok_key_words:
                lst_ok_key_words.append(word)
        if len(lst_ok_key_words) <= 5:
            return False

        #entities
        headers_entities = {"Ocp-Apim-Subscription-Key": News_checker.subscription_key}
        response = requests.post(News_checker.entities_url, headers=headers_entities, json=documents)
        entities = response.content
        data_entities = json.loads(entities)

        lst_entities = []
        for doc in data_entities["documents"]:
            for entit in doc["entities"]:
                if entit["type"] == "Location":
                    lst_entities.append(entit["name"])
        try:
            client = MongoClient("mongodb+srv://ericgomez:eric.gomez@cec-mtckf.mongodb.net/test?retryWrites=true&w=majority")
            db = client["CEC"]
            collection = db["news"]
            mydict = { "url": str(url), "date": fecha, "newspaper":periodico , "textcontent": texto,"keyWords":lst_ok_key_words,"locations":lst_entities}
            collection.insert_one(mydict)
        except Exception:
            return False
        else:
            return True

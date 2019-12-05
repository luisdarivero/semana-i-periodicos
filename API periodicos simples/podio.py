from references import References
import requests
import json
import traceback

#implementar errores https://realpython.com/python-requests/

class Podio:

    token = None
    data = None
    appID = None

    #constructor de la clase
    def __init__(self):
        try:
            self.data = References()
            self.token = {
                "Authorization" : "Bearer " + self.getToken()

            }
            self.appID = self.data.references["testAPP_ID"]
        except Exception as e:
            response = self.processError(e, traceback.format_exc(),"Error al ejecutar la función __init__()")
            raise Exception(response)


    #genera un token nuevo
    def getToken(self):
        try:
            result = requests.post(
                self.data.references["podioLoginURL"],
                data=self.data.credencialesTokenAsUser
            )
            content =  result.content.decode("utf-8")
            data = json.loads(content)
            if result.status_code != 200:
                raise Exception(self.badStatusCode(result.status_code,data))
            return data["access_token"]
        except Exception as e:
            response = self.processError(e, traceback.format_exc(),"Error al ejecutar la función getToken()")
            raise Exception(response)

    def validateHook(self, hook_id, code):
        try:
            url = self.data.references["apiBaseUrl"]
            url += self.data.apiCalls["validateHook"]
            url = url.replace("{hook_id}",hook_id)
            body = {
                "code" : code
            }
            result = requests.post(
                url,
                headers=self.token,
                json=body
            )
            if result.status_code != 200:
                raise Exception(self.badStatusCode(result.status_code,data))
            return data

        except Exception as e:
            response = self.processError(e, traceback.format_exc(),"Error al ejecutar la función validateHook()")
            raise Exception(response)

    #obtiene info de la app
    def getApp(self):
        url = self.data.references["apiBaseUrl"]
        url += self.data.apiCalls["getApp"]
        url = url.replace("{app_id}",self.appID)
        result = requests.get(
            url,
            headers=self.token
        )
        content =  result.content.decode("utf-8")
        data = json.loads(content)
        return data

    #obtiene el conteo de items de la app
    def getItemCount(self):
        url = self.data.references["apiBaseUrl"]
        url += self.data.apiCalls["getItemCount"]
        url = url.replace("{app_id}",self.appID)
        result = requests.get(
            url,
            headers=self.token
        )
        content =  result.content.decode("utf-8")
        data = json.loads(content)
        return data["count"]

    #Obtiene todos los items de una aplicación
    def filterItems(self):
        url = self.data.references["apiBaseUrl"]
        url += self.data.apiCalls["filterItems"]
        url+="/?fields=items.view(micro).fields(files.view(micro),file_count,external_id,fields.view(micro))"
        url = url.replace("{app_id}",self.appID)
        body = {
            "limit" : min(50,self.getItemCount())
            #"offset": 1

        }
        result = requests.post(
            url,
            headers=self.token,
            json=body
        )
        print(result.status_code)
        content =  result.content.decode("utf-8")
        data = json.loads(content)
        return data

    def fileStringWrite(self, cadena): #cadena = result.content
        archivo = "podio/stringResult.json"
        f=open(archivo, 'w')
        f.write(cadena)
        f.close()

    #Procesa un error para debolverlo en formato string json
    def processError(self, error, traceback, description):
        jsonFormatError = None
        try:
            jsonFormatError = json.loads(str(error).encode("utf-8"))
        except:
            jsonFormatError = str(error)
        response  = {
            "Error" : jsonFormatError,
            "Type: " : str(type(error).__name__),
            "Description": description,
            "traceback": traceback
        }

        response = json.dumps(response)
        return(str(response))

    #genera un string con el estatus de error
    def badStatusCode(self, status_code, jsonResponse):
        return ("response_code = " + str(status_code) + ", response:" + str(jsonResponse))

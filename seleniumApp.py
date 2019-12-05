
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class SeleniumManager:
    driver = None
    periodicos = {
        #"universal": "file:///C:/Users/Luis%20Da/Documents/9o%20Semestre/semana%20i/index.html"
        "universal": "https://www.eluniversal.com.mx/"
    }
    def __init__(self):
        #self.driver=webdriver.Firefox(executable_path=r"C:/Users/Luis Da/Documents/9o Semestre/semana i/geckodriver.exe")
        self.driver = webdriver.PhantomJS(executable_path=r"phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
    def abrir(self, liga):
        self.driver.get(liga)
    def ligaBusquedaUniversal(self,busqueda):
        return (self.periodicos["universal"] + "buscar/" + busqueda)
    def exit(self):
        self.driver.close()
        self.driver.quit()
    def getLinks(self):
        frames = self.driver.find_elements_by_tag_name("iframe")
        self.driver.switch_to.frame(frames[0])
        lista = []
        for x in range(20):
            time.sleep(0.25)
            links = self.driver.find_elements_by_class_name('marcoimagen')
            for link in links:
                lista.append(link.get_attribute("href"))
            nextContent = self.driver.find_element_by_class_name('Siguiente')
            nextContent.click()
        #print(lista)
        return lista
    def escribirArchivo(self,archivo, cadena):
        f=open(archivo, 'w', encoding="utf-8")
        f.write(cadena)
        f.close()


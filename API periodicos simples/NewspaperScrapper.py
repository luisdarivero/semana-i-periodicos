import requests
import re


class NewspaperScrapper:

    def get_urls_lajornada(self):
        urls_result = set()
        urls_source = [
            "https://www.jornada.com.mx/ultimas/capital/",
            "https://www.jornada.com.mx/ultimas/estados/"
        ]

        pattern = re.compile('href="https://www[.]jornada[.]com[.]mx/ultimas.*[.]html')

        for url in urls_source:
            html_string = requests.get(url).text
            for match in pattern.findall(html_string):
                urls_result.add(match.replace('href="', ""))

        urls_result = list(urls_result)
        urls_result.sort()
        return urls_result


    def get_urls_milenio(self):
        urls_result = set()
        urls_source = [
            "https://www.milenio.com/policia",
            "https://www.milenio.com/estado-de-mexico",
            "https://www.milenio.com/jalisco",
            "https://www.milenio.com/laguna",
            "https://www.milenio.com/cdmx",
            "https://www.milenio.com/hidalgo",
            "https://www.milenio.com/puebla",
            "https://www.milenio.com/tamaulipas",
            "https://www.milenio.com/monterrey"
            "https://www.milenio.com/leon"
        ]

        pattern = re.compile('href="/policia/.*">')

        for url in urls_source:
            html_string = requests.get(url).text
            for match in pattern.findall(html_string):
                urls_result.add("https://www.milenio.com" + match.replace('href="', '').replace('">', ''))

        urls_result = list(urls_result)
        urls_result.sort()
        return urls_result


    def get_urls_heraldo(self, num_pages):
        urls_result = set()
        urls_source_estado = [
            "https://heraldodemexico.com.mx/seccion/estados/"
        ]
        urls_source_cdmx = [
            "https://heraldodemexico.com.mx/seccion/cdmx/"
        ]

        for i in range(1, num_pages):
            urls_source_estado.append(urls_source_estado[0] + "pagina/" + str(i))
            urls_source_cdmx.append(urls_source_cdmx[0] + "pagina/" + str(i))

        pattern_estado = re.compile('href="https://heraldodemexico[.]com[.]mx/estados/.*?"')

        for url in urls_source_estado:
            html_string = requests.get(url).text
            for match in pattern_estado.findall(html_string):
                urls_result.add(match.replace('href="', '').replace('"', ''))

        pattern_cdmx = re.compile('href="https://heraldodemexico[.]com[.]mx/cdmx/.*?"')

        for url in urls_source_cdmx:
            html_string = requests.get(url).text
            for match in pattern_cdmx.findall(html_string):
                urls_result.add(match.replace('href="', '').replace('"', ''))

        urls_result = list(urls_result)
        urls_result.sort()
        return urls_result


    def get_urls_heraldo_recent(self):
        return self.get_urls_heraldo(10)


    def get_urls_heraldo_historico(self):
        return self.get_urls_heraldo(1000)


    def get_urls_lajornadaoriente(self, num_pages):
        urls_result = set()
        urls_source_estado = [
            "https://www.lajornadadeoriente.com.mx/categorias/noticias/estado/"
        ]
        urls_source_justicia = [
            "https://www.lajornadadeoriente.com.mx/categorias/noticias/sociedad_y_justicia/"
        ]

        for i in range(1, num_pages):
            urls_source_estado.append(urls_source_estado[0] + "page/" + str(i))
            urls_source_justicia.append(urls_source_justicia[0] + "page/" + str(i))

        pattern = re.compile('href="https://www.lajornadadeoriente[.]com[.]mx/puebla/.*?"')

        for url in urls_source_estado:
            html_string = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}).text
            for match in pattern.findall(html_string):
                urls_result.add(match.replace('href="', '').replace('"', ''))

        for url in urls_source_justicia:
            html_string = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}).text
            for match in pattern.findall(html_string):
                urls_result.add(match.replace('href="', '').replace('"', ''))

        urls_result = list(urls_result)
        urls_result.sort()
        return urls_result


    def get_urls_lajornadaoriente_recent(self):
        return self.get_urls_lajornadaoriente(10)


    def get_urls_lajornadaoriente_historico(self):
        return self.get_urls_lajornadaoriente(900)


if __name__ == '__main__':

    np = NewspaperScrapper()

    for url in np.get_urls_lajornada():
        print(url)

    for url in np.get_urls_milenio():
        print(url)

    for url in np.get_urls_heraldo_recent():
        print(url)

    for url in np.get_urls_lajornadaoriente_recent():
        print(url)

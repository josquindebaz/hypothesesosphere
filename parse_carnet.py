import urllib.request
import re
import json

url = "https://socioargu.hypotheses.org/5306"

class parsepage(object):
    def __init__(self, url):
        self.getcarnet(url)
        print (url, "recupere")
        self.recupmeta() 
        """TODO decoupe, recupere tous les urls
        separe carnets, images et autres liens
        genere log json avec toutes ces infos si c'est un post et pas un autre type d'entree
        ajoute non presentes a la liste des pages a parser"""

    def getcarnet(self, url):
        with urllib.request.urlopen(url) as response:
            html = response.read()
            self.html = html.decode('utf-8')

    def recupmeta(self, html=None):
        """TODO recupérer taille, date """
        if not (html): 
            html = self.html
        if re.search('time class="entry-date" datetime=', html):
            print ('date : ',  re.findall('time class="entry-date" datetime="([\d-]*)T\S*">', html) )
            print ('size : ', len(html))
            return 1
        else:
            print ("not a post")
            return 0

    def decoupe_main(self, html=None):
        if not (html): 
            html = self.html
        main = re.split('<div id="main" class="wrapper">', html)[1]
        self.main = re.split('</div><!-- #main .wrapper -->', main)[0]
        #networks_button = re.split('<ul class="soc">', without_footer)
        #without_footer = networks_button[0] + re.split("</ul>", networks_button[1], 1)[1]

    def recup_urls(self, html=None):
        if not (html): 
            html = self.main

        urls = re.findall('https?://(\S*)["\']', html) 

        urls = map(lambda x: re.sub('/$', '', x), urls)
        urls = map(lambda x: re.split('#', x)[0], urls)
        self.urls = list (set (urls))
        print ( len(self.urls) )

    def recup_urls_carnet(self, urls=None):
        """TODO separe tous les liens qui sont des carnets des autres"""
        if not (urls): 
            urls = self.urls
        for i in urls:
            if re.search("^\w*.hypotheses.org", i): 
                print (i)
    
    def recup_img(self, urls=None):
        """TODO recup images du post"""
        pass



parsepage(url)

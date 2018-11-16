#!/usr/bin/python3
# -*- coding: utf-8 -*-
#import urllib.request
from bs4 import BeautifulSoup
import re
import json

class parsepage(object):
    def __init__(self, html):
        post = self.recupmeta(html) 

        soup = BeautifulSoup(html, "lxml")
        content = soup.find(id='page')

        post['id'] = soup.find(property='og:url')['content']

        #Get all urls
        post['urls'] = self.recup_urls(content)    
        #TODO remove social media, wordpress

        #Get images
        post['imgs'] = self.recup_img(content)

        #json for log
        js = json.dumps(post)
        print(js)

        #Get all links to X.hypotheses.org
        #to_follow = filter(self.is_carnet, urls)

        """
        #Get carnets from urls
        self.recup_names_carnets (filter(self.is_carnet, urls))
        """
           

        """TODO 
        separe carnets, images et autres liens
        genere log json avec toutes ces infos si c'est un post et pas un autre type d'entree
        ajoute non presentes a la liste des pages a parser"""

    def recupmeta(self, html):
        """ If it's a post, get date and size, Else return False """
        if re.search('time class="entry-date" datetime=', html):
            md = {'date' : re.findall('time class="entry-date" datetime="([\d-]*)T\S*">', html)[0] } 
            md['size'] = len(html)
            return md 
        else:
            print ("not a post")
            return False 

    def recup_names_carnets(self, urls):
        """ Get Carnet Names from url"""
        L = map( lambda x: re.search("^(\w*).hypotheses.org", x).group(1), urls)
        return list(set(L))
    
    def recup_img(self, soup):
        """Get images with hard src"""
        list_img = []
        for img in soup.find_all('img'):
            list_img.extend(re.findall("http\S*", str(img)))
        return list(set(list_img))

    def recup_urls(self, soup):
        """Get urls fom <a """
        list_url = []
        for url in soup.find_all('a', href=True):
            href = url['href']
            href = re.sub("https?://(www.)?", "", href) 
            href = re.sub("(#.*|/$)", "", href)
            if (href):
                list_url.append(href)
        return list(set(list_url))


if __name__ == '__main__' :
    #url = "https://socioargu.hypotheses.org/5306"
    with open('test.html', 'r') as F:
        B = F.read()
        parsepage(B)

# -*- encoding: utf-8 -*-
#josquin debaz 26 septembre 2018


"""TODO
log pages faites
log a faire, y injecter le seed -exclus
faire le suivant de la liste, recup infos si post, recup urls carnet manquante, les injecter si pas exclus

descripteur carnet :
liste tailles + médiane (=> nb post)
liste nb images total et mediane par post
premier et dernier post

synthese images
classement sources
classement images
histoire d'une image ?

matrice croisée des liens d'un carnet vers les autres
"""




import urllib.request
import re

###CONFIG###
link_for_seed = "http://www.openedition.org/?page=coverage&pubtype=carnet"
force_update_seed = 0

def get_links(html):
    liste = []
    while re.search('https?://', html): 
        html = re.split('https?://', html, 1) 
        fragment =  re.split('[\'" <]', html[1], 1) 
        liste.append('http://%s'%fragment[0])
        html = fragment[1]
    return list(set(liste))

def get_links_from_body(url):
    #url = re.sub("http://http://", "http://", url)
    print ("Opening %s" % url)

    with urllib.request.urlopen(url) as buf:
        page = buf.read()
        #try :
        #    page = re.split("<body", page, 1)[1]
        #    page = re.split('<div id="footer">', page)[0]
        return get_links(page)
        #except :
        #    print( "split problem with %s" % url)
        #    return []

def get_carnets_from_seed(url):
    seed = get_links_from_body(url)
    print("Got %d carnet(s) on  %s" % (len(seed), url))

get_carnets_from_seed(link_for_seed)


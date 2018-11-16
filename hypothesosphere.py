# -*- encoding: utf-8 -*-
#josquin debaz 16 novembre


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
from bs4 import BeautifulSoup
import os

###CONFIG###
link_for_seed = "http://www.openedition.org/?page=coverage&pubtype=carnet"
force_update_seed = 0
todo = "todo.dat"

def get_links(soup):
    """Get urls fom <a """
    list_url = []
    for url in soup.find_all('a', href=True):
        href = url['href']
        href = re.sub("https?://(www.)?", "", href) 
        href = re.sub("(#.*|/$)", "", href)
        if (href):
            list_url.append(href)
    return list(set(list_url))

def is_carnet(url): 
    return re.search("^\w*.hypotheses.org", url) 

def ReadUrl(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'gsprbot (Contact:debaz@ehess.fr)')
    with urllib.request.urlopen(req) as buf:
        page = buf.read()
    return page
 
def get_carnets_from_seed(url):
    html = ReadUrl(url)
    soup = BeautifulSoup(html, "lxml")
    urls = get_links(soup)
    return [url for url in urls if is_carnet(url)]

if __name__ == '__main__' :
    if (not os.path.isfile(todo)) or (force_update_seed):
        seed = get_carnets_from_seed(link_for_seed)
        print("Found %d carnet(s) on  %s" % (len(seed), link_for_seed))
        with open(todo, "w") as todofile:
            todofile.writelines(line + '\n' for line in seed)
            


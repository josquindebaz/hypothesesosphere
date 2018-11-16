# -*- encoding: utf-8 -*-
#josquin debaz 16 novembre


"""TODO
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
agent = 'gsprbot (Contact:debaz@ehess.fr)'
link_for_seed = "http://www.openedition.org/?page=coverage&pubtype=carnet"
force_update_seed = 1
todo = "todo.dat"
done = "done.dat"
exclude = [
    #"socioargu.hypotheses.org",
    ]

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
    """Open an url with declarative header"""
    global agent
    req = urllib.request.Request(url)
    req.add_header('User-Agent', agent) 
    with urllib.request.urlopen(req) as buf:
        page = buf.read()
        page = page.decode('utf-8')
    return page
 
def get_carnets_from_seed(url):
    html = ReadUrl(url)
    soup = BeautifulSoup(html, "lxml")
    urls = get_links(soup)
    return [url for url in urls if is_carnet(url)]

class logs(object):
    def __init__(self, todofile, donefile):
        self.todofile = todofile
        self.donefile = donefile
        
    def save_todo(self, seed):
        with open(self.todofile, "w") as F:
            F.writelines(line + '\n' for line in seed)

    def get_todo(self):
        with open(self.todofile, 'r') as F:
            b = F.read()
            return re.split('\n', b)[:-1]
 
    def add_done(self, url):
        with open(self.donefile, "a") as F:
            F.write(url+"\n")

    def get_done(self):
        if (os.path.isfile(self.donefile)):
            with open(self.donefile, 'r') as F:
                b = F.read()
                return re.split('\n', b)[:-1]
        else:
            return []

if __name__ == '__main__' :
    Logs = logs(todo, done)
    if (not os.path.isfile(todo)) or (force_update_seed):
        seed = get_carnets_from_seed(link_for_seed)
        seed = [url for url in seed if url not in exclude]
        print("Found %d carnet(s) on  %s" % (len(seed), link_for_seed))
        Logs.save_todo(seed)

    done =Logs.get_done() 
    seed = Logs.get_todo()
    while(seed):
        billet = seed.pop(0) 
        """Parse le billet"""
        """Recupere urls carnets"""
        """ajoute todo ceux qui n'y sont pas et ne sont pas dans done ni exclus"""

        """ajoute billet a done"""
        done.append(billet)
        Logs.add_done(billet)
        print (len(done), "done", len(seed), "to do")
    
            


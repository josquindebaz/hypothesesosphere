# -*- encoding: utf-8 -*-
#josquin debaz 23 novembre


"""TODO
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
import json
import time
import sys

###CONFIG###
agent = 'gsprbot (Contact:debaz@ehess.fr)'
init_time = 0 
end_time = 7 
link_for_seed = "http://www.openedition.org/?page=coverage&pubtype=carnet"
force_update_seed = 0
force_redo = 0
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

def name_carnet(url):
    """ Get Carnet Name from url"""
    return re.search("^(\w*).hypotheses.org", url).group(1)

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
    """Log files and lists for todo and done urls"""
    def __init__(self, todofile, donefile):
        self.todofile = todofile
        self.donefile = donefile
        self.done_list = []
        self.todo_list = []
        
    def save_todo(self, todo):
        with open(self.todofile, "w") as F:
            F.writelines(line + '\n' for line in todo)

    def get_todo(self):
        with open(self.todofile, 'r') as F:
            b = F.read()
            self.todo_list = re.split('\n', b)[:-1]
 
    def add_done(self, url):
        self.done_list.append(url)
        with open(self.donefile, "a") as F:
            F.write(url+"\n")

    def get_done(self):
        if (os.path.isfile(self.donefile)):
            with open(self.donefile, 'r') as F:
                b = F.read()
                self.done_list = re.split('\n', b)[:-1]
        else:
            self.done_list = []

    def reset_done(self):
        if (os.path.isfile(self.donefile)):
            open(self.donefile, "w") 

class links_logs(object):
    """Log links from a carnet to others"""
    def __init__(self, rep="links"):
        self.rep = rep
        self.links = []

    def f_carnet(self, carnet):
        return os.path.join(self.rep, carnet + ".dat")
    
    def get_links(self, carnet):
        print(carnet)
        path = self.f_carnet(carnet)
        if (os.path.isfile(path)):
            with open(path, 'r') as F:
                b = F.read()
                self.links = re.split('\n', b)[:-1]
        else:
            self.links = []

    def add_link(self, carnet, receiver):
        self.links.append(receiver)
        path = self.f_carnet(carnet)
        with open(path, "a") as F:
            F.write(receiver+"\n")

class posts_logs(object):
    """Log post contents"""
    def __init__(self, rep="posts"):
        self.rep = rep

    def f_carnet(self, carnet):
        return os.path.join(self.rep, carnet + ".json")
    
    def add_post(self, carnet, json):
        path = self.f_carnet(carnet)
        with open(path, "a") as F:
            F.write(json+"\n")

class parsepage(object):
    def __init__(self, html):
        soup = BeautifulSoup(html, "lxml")

        """Get all urls"""
        URLS = get_links(soup)
        URLS = self.remove_wordpress(URLS)
        self.carnets = [url for url in URLS if is_carnet(url)] 

        self.post = self.recupmeta(html) 
        if (self.post):
            content = soup.find(id='page')
            self.post['id'] = soup.find(property='og:url')['content']
            #Get all urls
            self.post['urls'] = get_links(content)    
            #Get images
            self.post['imgs'] = self.recup_img(content)

            #json for log
            self.js = json.dumps(self.post)

    def remove_wordpress(self, urls):
        l = []
        for url in urls:
            if re.search("\.php$", url):
                if not re.search("wp-login.php$", url):
                    print('url')
            elif re.search("\.\w{1,}$", url):
                if re.search("\.org$", url):
                    l.append(url)
            else:
                l.append(url)
        return l

    def recupmeta(self, html):
        """ If it's a post, get date and size, Else return False """
        if (len(re.findall('time class="entry-date" datetime=', html)) == 1):
            md = {'date' : re.findall('time class="entry-date" datetime="([\d-]*)T\S*">', html)[0] } 
            md['size'] = len(html)
            return md 
        else:
            return False 

    def recup_img(self, soup):
        """Get images with hard src"""
        list_img = []
        for img in soup.find_all('img'):
            list_img.extend(re.findall("http\S*", str(img)))
        return list(set(list_img))


if __name__ == '__main__' :
    #if time is correct we process
    H = int(time.strftime('%H'))
    if (not (H >= init_time) and (H <= end_time)):
        sys.exit("Not in scheduled time")

    start_time = time.time()

    #Initiate log files
    Logs = logs(todo, done)

    #Get a first list to crawl
    if (not os.path.isfile(todo)) or (force_update_seed):
        seed = get_carnets_from_seed(link_for_seed)
        seed = [url for url in seed if url not in exclude]
        print("Found %d carnet(s) on  %s" % (len(seed), link_for_seed))
        Logs.save_todo(seed)
    Logs.get_todo()

    #Get the done list
    if (force_redo):
       Logs.reset_done() 
    else:
       Logs.get_done() 

    #Initiate links and posts data files
    Links = links_logs()
    Posts = posts_logs()

    while(Logs.todo_list):
        billet = Logs.todo_list.pop() 
        print(billet)
        name = name_carnet(billet)

        #add page to done
        Logs.add_done(billet)

        #get links known for the carnet
        Links.get_links(name)
        
        #open and read url
        html = ReadUrl("https://" + billet) 
        #Parse page
        parse = parsepage(html)

        #if post, save content data in posts/name.json
        if (parse.post):
            Posts.add_post(name, parse.js)

        #for every carnet found in urls
        for url in parse.carnets: 
            #append if needed the receiving carnet to links/name.dat
            receiver = name_carnet(url)
            if (receiver not in Links.links) and (receiver != name):
                Links.add_link(name, receiver)

            #If url if not in todo, nor in done and excludes
            if ((url not in Logs.done_list) 
                    and (url not in Logs.todo_list) 
                    and (url not in exclude)): 
                Logs.todo_list.append(url)
                
        #save todo list in todo log file
        Logs.save_todo(Logs.todo_list)

        print("--- %s seconds ---" % (time.time() - start_time), len(Logs.done_list), "done", len(Logs.todo_list), "to do")
    
        #if time is over we stop
        if (not (H >= init_time) and (H <= end_time)):
            sys.exit("Not in scheduled time")

        


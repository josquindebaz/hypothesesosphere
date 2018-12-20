#!/usr/bin/python3
#josquin debaz 20/12/2018
import glob
import re

carnets = {}
for f in glob.glob("links/*.dat"):
    with open(f, 'r') as d:
        b = d.read()
        l = re.split("\n", b)[:-1]
        carnets[re.search("links/(\S*)\.dat", f).group(1)] = l

l_carnets = list(carnets.keys())

with open('h.net', 'w') as h:
    content = "*Vertices %d\n" % (len(carnets))
    for i, c in enumerate(l_carnets):
        content += "%s %s\n" % (i+1, c)
    
    content += "*edgeslist\n"
    for k, v in carnets.items():
        n = l_carnets.index(k)+1
        try:
            content += "%s %s\n" %(n, " ".join( [str(l_carnets.index(el)+1) for el in v] ) ) 
        except:
            pass
            
            


    h.write(content)

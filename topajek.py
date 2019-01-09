#!/usr/bin/python3
#Josquin Debaz 07/01/2019
#Licence GPL3
import glob
import re

#output
out = "nets/hypothesosphere.net"

#for each filename.dat in links directory
#put in carnets[filename] the list of links it contents
carnets = {}
for f in glob.glob("links/*.dat"):
    with open(f, 'r') as d:
        b = d.read()
        carnets[ re.search("links/(\S*)\.dat", f).group(1) ] = \
            re.split("\n", b)[:-1]

#fix the order by creating the list of filename/carnets
l_carnets = list(carnets.keys())

with open(out, 'w') as h:
    #Indicate the number of nodes
    #List each carnet with its number
    content = "*Vertices %d\n" % (len(carnets))
    content += "".join(["%d %s\n" % (i+1, carnet) \
        for i, carnet in enumerate(l_carnets)])
    
    #Insert linked carnet number for each carnet number
    content += "*edgeslist\n"
    for k, v in carnets.items():
        #remove non-listed carnets
        vindices = [l_carnets.index(x)+1 for x in v if x in l_carnets]
        if (len(vindices) > 0):
            content += "%s" % (l_carnets.index(k)+1)
            for el in vindices:
                content += " %d" % el
            content += "\n" 

    h.write(content)

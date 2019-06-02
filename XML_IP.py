import os
from lxml import etree
import socket
from itertools import zip_longest
import csv
import sys

#not this one...
#file_to_open = os.path.join("template.xml")

file_to_open =os.path.join(sys.path[0], 'template.xml')

f = open(file_to_open)
print(file_to_open)

#Set up some lists
addresses=[]
names = []
rows = [addresses,names]

#import the file
tree = etree.parse(f)

root = tree.getroot()
#confirm load
print(root.attrib)

#grab that IP
for tcp in tree.xpath("//address"):
    print (tcp.attrib)
    x = tcp.attrib["addr"]
    print (x)
    addresses.append(x)

#confirm it worked.
print(addresses)

for y in addresses:
    print(y)
    #Attempt get host, writes line - Failed if it didnt work.
    try:
        host_name = socket.gethostbyaddr(y)
        a = host_name[0]
        names.append(a)
        print(a)
        print(host_name)
    except:
        names.append("Failed")
        pass


#debug
print(names)
print("rows")
print(rows)


#write a CSV
export_data = zip_longest(*rows, fillvalue = '')
with open('the_ip.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(("IP", "Name"))
    wr.writerows(export_data)
myfile.close()
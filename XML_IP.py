import os
from lxml import etree
import socket
from itertools import zip_longest
import csv
import sys

cwd = os.getcwd()
files= os.listdir(cwd)


#Set up some lists
xmls =[]
#for outupt CSV
addresses=[]
names = []
input_filename =[]
rows = [addresses,names,input_filename]


#loads XML files from directory into list.
for file in files:
    if file.endswith(".xml"):
        xmls.append(file)
        #print (file)

print ("\033[0;35;0m" +"Found these XML's : " +str (xmls) +"\033[0;0m")

for xml in xmls:
    #import the file
    try:
        file_to_open = os.path.join(sys.path[0], xml)
        f = open(file_to_open)
        print("\033[0;32;0m" +"Opening this file and loading to list:  " + str(file_to_open) +"\033[0;0m" )
        tree = etree.parse(f)
        root = tree.getroot()
        #confirm load
        #print(root.attrib)

        # grab that IP
        for tcp in tree.xpath("//address"):
            input_filename.append(xml)
            #print (tcp.attrib)
            x = tcp.attrib["addr"]
            #print (x)
            addresses.append(x)
    except:
        #skipping broken files and showing an arror.
        print("\x1b[1;31;40m" +str(xml) +" Skipped due to error in file \033[0;0m")
        pass





    #confirm it worked.
#print("The addresses are: " +str(addresses))


#Name lookup with sockets
for y in addresses:
    print(y)
    #Attempt get host, writes line - Failed if it didnt work.
    try:
        host_name = socket.gethostbyaddr(y)
        a = host_name[0]
        names.append(a)
        print(a)
        #print(host_name)
    except:
        names.append("Failed")
        pass


#debug
# print(names)
# print("rows")
# print(rows)


#write a CSV
print("")
print ("Exporting a CSV")
export_data = zip_longest(*rows, fillvalue = '')
with open('the_ip.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(("IP", "Name", "Input filename"))
    wr.writerows(export_data)
    print("Export complete")
myfile.close()
# This program serves as an interface with the bulk
# uploader program. It allows one to specify a directory
# containing multiple osm files and have them all uploaded at
# once. Please use this program carefully and reach a
# a community consensus before massive imports.
# ~ingalls

import os
import shutil

print "OSM Multi-Uploader v0.1"
print "Please make sure that you know what you are doing..."
print "Directory (Press enter for current)"
fileLoc = raw_input(":")

if fileLoc <> "": 
	os.chdir(fileLoc) #change to user specified directory

print "Username"
username = raw_input(":")

print "Password"
password = raw_input(":")

print "Changeset Comment"
comment = raw_input(":")

print "\n\n\n"
print "Username: " + username
print "Password: " + password
print "Comment: " + comment

print "\nAre you sure you wish to continue?"
check = raw_input("type 'yes' to continue \n:")
if check != "yes":
	exit()

print "Go get a beer. This will take awhile!"

osmList = list() #Declares variable

for files in os.listdir("."): #Gets a list of osm files
    if files.endswith(".osm"):
        osmList.append(files) #Store files in list
listNum = len(osmList) #returns number of osm files
listNum = listNum - 1 #Fixes for 0th element

while listNum >= 0:
    print "---Converting: " + osmList[listNum] + "---"
    os.system("python3 osm2change.py " + osmList[listNum])
    newFile = osmList[listNum].replace(".osm", ".osc")

    fileSize = int(os.path.getsize(newFile) * 0.000976562) #gets size in B, converts to kB, rounds to int.
    splitNumber = fileSize / 200 #Will split into 200kB bits - NEEDS DISCUSSION
    if splitNumber > 1:
        print "---Splitting: " + newFile + " into " + str(splitNumber) + " parts---"
        os.system("python3 split.py " + newFile + " " + str(splitNumber))
        os.rename(newFile, newFile + ".old")
	
    listNum = listNum - 1

splitList = list()

for files in os.listdir("."): #Regenerate list of osc files with newly generated splits
    if files.endswith(".osc"):
        splitList.append(files) #Store files in list
listNum = len(splitList) #returns number of osm files
listNum = listNum - 1 #Fixes for 0th element

while listNum >= 0:
	#TODO Add diff code here
	#Since I now have the basic split support this must be added before ANY uploads can take place
	#otherwise they will break. More info on wiki
	
	print "---Uploading: " + splitList[listNum] + "---"
        # os.system("python3 upload.py -u " + username + " -p " + password + " -m \"" + comment + "\" -t -c yes " + splitList[listNum] )
        listNum = listNum - 1 
        

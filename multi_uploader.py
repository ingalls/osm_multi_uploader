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

# TODO poll array to find out how many files are to be uploaded and inform user.
print "\nAre you sure you wish to continue?"
check = raw_input("type 'yes' to continue \n:")
if check != "yes":
	exit()

fileList = list() #Declares variable

for files in os.listdir("."): #Gets a list of osm files
    if files.endswith(".osm"):
        fileList.append(files) #Store files in list
listNum = len(fileList) #returns number of osm files
listNum = listNum - 1 #Fixes for 0th element

while listNum >= 0:
	print "--- Converting: " + fileList[listNum] + "---"
	os.system("python3 osm2change.py " + fileList[listNum])
	newFile = fileList[listNum].replace(".osm", ".osc")
	
	fileSize = int(os.path.getsize(newFile) * 0.000976562) #gets size in B, converts to kB, rounds to int.
	splitNumber = fileSize / 200 #Will split into 200kB bits - NEEDS DISCUSSION
	
	print "---Splitting: " + newFile + " into " + splitNumber + " parts---"
	os.system("python3 split.py " + newFile + " " + splitNumber
	os.rename(newFile, newFile + ".old")
	
	listNum = listNum - 1

for files in os.listdir("."): #Regenerate list of osc files with newly generated splits
    if files.endswith(".osc"):
        fileList.append(files) #Store files in list
listNum = len(fileList) #returns number of osm files
listNum = listNum - 1 #Fixes for 0th element

while listNum >= 0:
	#TODO Add diff code here
	#Since I now have the basic split support this must be added before ANY uploads can take place
	#otherwise they will break. More info on wiki
	
	print "---Uploading: " + fileList[listNum] + "---"
        # os.system("python3 upload.py -u " + username + " -p " + password + " -m \"" + comment + "\" -t -c yes " + fileList[listNum] )
        listNum = listNum - 1 
        
        
        

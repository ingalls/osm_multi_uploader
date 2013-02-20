#LISCENSE
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#INTRODUCTION
# This program serves as an interface with the bulk
# uploader program. It allows one to specify a directory
# containing multiple osm files and have them all uploaded at
# once. Please use this program carefully and reach a
# a community consensus before massive imports.
# ~ingalls

#REQUIREMENTS
# Python2
# Python3
# Perl

import os
import shutil
import sys


rootLoc = os.getcwd()
version = "0.2"
fileLoc = ""
username = ""
password = ""
comment = ""
num = 0

if len(sys.argv) == 0:
	print "OSM MultiUploader"
	print "-----"
	print "-u <username>"
	print "-p <password>"
	print "-c <changeset comment>"
	print "-d <upload> "
	print "-----"
	print "-m (Prompt for values)"
	sys.exit(1)
	
print "OSM Multi-Uploader " + version

#if sys.argv !contains "-m"
while num < len(sys.argv)-2:
	num += 1
	arg = sys.argv[num]
	if arg == "-u":
		num += 1
		username = sys.argv[num]
	elif arg == "-p":
		num += 1
		password =sys.argv[num]
	elif arg == "-d":
		num += 1
		fileLoc = sys.argv[num]
	elif arg == "-c":
		num += 1
		comment = sys.argv[num]

if fileLoc == "":
	print "Enter Directory (Press enter for current)"
	fileLoc = raw_input(":")

if username == "":
	print "Enter Username"
	username = raw_input(":")

if password == "":
	print "Enter Password"
	password = raw_input(":")

if comment == "":
	print "Enter Changeset Comment"
	comment = raw_input(":")

if fileLoc <> ".":
	fileLoc = rootLoc + fileLoc
else:
	fileLoc = rootLoc

print "\n\n\n"
print "Username: " + username
print "Password: " + password
print "Comment: " + comment

print "\nAre you sure you wish to continue?"
check = raw_input("type 'yes' to continue \n:")
if check != "yes":
	exit()

print "Go get a beer. I've got this now!"

#Creates various directories used during the upload
if not os.path.exists(rootLoc + "/conversions"): #stores osc files
    os.makedirs(rootLoc + "/conversions")
if not os.path.exists(rootLoc + "/splits"): #stores split files
    os.makedirs(rootLoc + "/splits")
if not os.path.exists(rootLoc + "/completed"): #stores sucessfully uploaded splits
    os.makedirs(rootLoc + "/completed") 

osmList = list() #stores list of osm files to be split
splits = list()

for files in os.listdir(fileLoc): #Gets a list of osm files
    if files.endswith(".osm"):
        osmList.append(files) #Store files in list
listNum = len(osmList) #returns number of osm files
listNum = listNum - 1 #Fixes for 0th element

while listNum >= 0:
    print "---Converting: " + fileLoc + "/" + osmList[listNum] + "---"
    os.system("python3 osm2change.py " + fileLoc + "/" + osmList[listNum])
    newFile = osmList[listNum].replace(".osm", ".osc")
    print "   Moving to /conversions"
    os.rename(fileLoc + "/" + newFile, rootLoc + "/conversions/" + newFile)
    newFile = rootLoc + "/conversions/" + newFile

    print "---Sorting: " + newFile + "---"
    os.system("python smarter-sort.py " + newFile)
    os.rename(newFile, newFile + ".old")
    newFile = newFile.replace(".osc","-sorted.osc")

    fileSize = int(os.path.getsize(newFile) * 0.000976562) #gets size in B, converts to kB, rounds to int.
    splitNumber = fileSize / 200 #Will split into 200kB bits
    if splitNumber > 1:
        print "---Splitting: " + newFile + " into " + str(splitNumber) + " parts---"
        os.system("python3 split.py " + newFile + " " + str(splitNumber))
        os.rename(newFile, newFile + ".old")
	
    for files in os.listdir(rootLoc + "/conversions"): #Regenerate list of osc files with newly generated splits
        if files.endswith(".osc"):
            splits.append(files) #Store files in list
    listNumber = len(splits) #returns number of osm files
    listNumber -= 1 #Fixes for 0th element

    while listNumber >= 0:
        os.rename(rootLoc + "/conversions/" + splits[listNumber] , rootLoc + "/splits/" + splits[listNumber])
        listNumber -= 1
	        
    listNum -= 1

splitList = list()

for files in os.listdir(rootLoc + "/splits"): #Gets a list of osm files
    if files.endswith(".osc"):
        splitList.append(files) #Store files in list
listNum = len(splitList) #returns number of osm files
listNum = listNum - 1 #Fixes for 0th element
fileNum = listNum

diffList = list()



while listNum >= 0:
	
    print "---Uploading: " + rootLoc + "/splits/" + splitList[listNum] + "---"
    os.system("python3 upload.py -u " + username + " -p " + password + " -m \"" + comment + "\" -t -c yes " + rootLoc + "/splits/" + splitList[listNum] )
    listNum -= 1
    
    del diffList[:]
    for files in os.listdir(rootLoc + "/splits"): #Gets a list of osm files
        if files.endswith(".diff.xml"):
            diffList.append(files) #Store files in list
    diffNum = len(diffList) #returns number of osm files
    diffNum = diffNum - 1 #Fixes for 0th element
    
    while diffNum >= 0:
        while fileNum >=0:
            os.system("python diffpatch.py " + diffList[diffNum] + " " + splitList[fileNum])
            fileNum -= 1
        diffNum -= 1
        

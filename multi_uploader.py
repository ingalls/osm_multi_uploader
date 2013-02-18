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

if fileLoc <> "" and fileLoc <> ".":
	fileLoc = rootLoc + fileLoc
	os.chdir(fileLoc) #change to user specified directory
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

osmList = list() #stores list of osm files to be split

for files in os.listdir("."): #Gets a list of osm files
    if files.endswith(".osm"):
        osmList.append(files) #Store files in list
listNum = len(osmList) #returns number of osm files
listNum = listNum - 1 #Fixes for 0th element

while listNum >= 0:
    print "---Converting: " + osmList[listNum] + "---"
    os.system("python3 osm2change.py " + osmList[listNum])
    newFile = osmList[listNum].replace(".osm", ".osc")

    print "---Sorting: " + newFile + "---"
    os.system("python smarter-sort.py " + newFile)
    os.rename(newFile, newFile + ".old")
    newFile = newFile.replace(".osc","-sorted.osc")

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
        

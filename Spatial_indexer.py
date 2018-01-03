# Copyright, Jack Andersen - Wisecloud.dk
#-*- coding: utf-8 -*-
#import site-packages, modules and set enviroment, glob can ensure unicode caracters Æ Ø Å is kept
import os, time, datetime, arcpy, os
from arcpy import env

#initialize variables.
extList = ["shp"]
mappaths = []
#counters for number of shapefiles processed and skipped.
count = 0
filecount = 0
fileskipcount = 0

#directory where files are located, this dir is searched for the shapefiles to be indexed.
targetDir = u"F:\GISdata\ArcGIS\Kursusmateriale"
#print a timestamp for the start of the scipt.
print "|" + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') + " Starting...|"+"\n"
#walking through folder and subfolders, finding shapefiles.
for root, dirs, files in os.walk(targetDir):
    for filename in files:
       #splits all filenames, checks the suffic againt the extList variable.
        splitFilename = filename.split(".")
        if splitFilename[-1] in extList:
            #merge the split filename again
            fullpath = os.path.join(root, filename)
            #counter for files in dirs.
            count = count + 1
            #appends the merged shp filename and path to the mappath list.
            mappaths.append(fullpath)

#print count of shapefiles found.
print "found " + str(count) + " files." + "\n"

# Create a spatial index for each shapefile.
#sort the list of datasources
for map in sorted(mappaths):
   try:
    arcpy.AddSpatialIndex_management(map, "")
    print map + " index created!"
    filecount = filecount + 1
    
   except Exception: 
    pass
    print "Something went wrong with " + map +" skipping file" + "\n"
    fileskipcount = fileskipcount + 1

#print summary of files indexed and a timestamp
print "\n" + str(filecount) + " file(s) where indexed!"
print "\n" + str(fileskipcount) + " file(s) where skipped!"
print "\n" + "|" + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') + " all spatial indexes was succesfully created! |"+"\n"

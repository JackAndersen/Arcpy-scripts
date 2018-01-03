# Copyright, Jack Andersen - Wisecloud.dk
#-*- coding: utf-8 -*-
#import site-packages, modules and set enviroment, glob can ensure unicode caracters Æ Ø Å is kept
import arcpy, os, shutil, glob
#from os.path import isfile

#Initialize variables.
extList = ["lyr"]
mappaths = []
ignorefiles = ("*.ecw", "*.", "*.001", "*.2", "*._gdb", "*._timestamps", "*.adf", "*.aid", "*.aih", "*.ain", "*.alg", "*.ant", "*.apr", "*.asc", "*.atx", "*.aux", "*.avi", "*.avl", "*.avx", "*.bak", "*.bas", "*.bat", "*.bck", "*.bil", "*.bin", "*.bmp", "*.cab", "*.cache", "*.cal", "*.cdf", "*.cfg", "*.chm", "*.clr", "*.cmd", "*.cnt", "*.conf", "*.config", "*.cpg", "*.cs", "*.csh", "*.csproj", "*.css", "*.csv", "*.dat", "*.db", "*.dbf", "*.dbf#", "*.dbg", "*.def", "*.dem", "*.dgn", "*.dir", "*.dll", "*.doc", "*.docx", "*.dot", "*.ds_store", "*.dsn", "*.ecw2", "*.eps", "*.ers", "*.esriaddin", "*.esriaddinx", "*.eww", "*.exe", "*.exp", "*.ffs", "*.fix", "*.fme", "*.fmelic", "*.fmw", "*.freelist", "*.gdbindexes", "*.gdbtabidx", "*.gdbtable", "*.gdbtablx", "*.ged", "*.gfs", "*.gid", "*.gif", "*.gl", "*.gml", "*.grd", "*.gst", "*.gz", "*.hdr", "*.hlp", "*.htm", "*.html", "*.ico", "*.id", "*.img", "*.ind", "*.inf", "*.ini", "*.ini_old", "*.iso", "*.it", "*.iwz", "*.ixs", "*.jar", "*.jgw", "*.jpg", "*.js", "*.kms", "*.komprimeret", "*.kor", "*.lcn", "*.ldb", "*.lic", "*.lis", "*.lng", "*.lnk", "*.loc", "*.lock", "*.log", "*.lox", "*.lst", "*.lut", "*.magik", "*.manifest", "*.map", "*.mb", "*.mbx", "*.mbx_old", "*.mdb", "*.mdb#", "*.mid", "*.mif", "*.mig", "*.mlm", "*.mnu", "*.msg", "*.msi", "*.msp", "*.mwcore", "*.mws", "*.mxd", "*.mxd_old", "*.mxs", "*.mxt", "*.nit", "*.nls", "*.odb", "*.old", "*.oldwor", "*.ovr", "*.par", "*.pdb", "*.pdf", "*.pl", "*.pm", "*.png", "*.ppt", "*.prj", "*.properties", "*.py", "*.qix", "*.qpj", "*.qry", "*.rar", "*.reg", "*.repx", "*.resources", "*.resx", "*.rrd", "*.rtf", "*.sbn", "*.sbnold", "*.sbx", "*.sbxold", "*.scc", "*.sde", "*.sh", "*.shp", "*.shx", "*.sln", "*.so", "*.spx", "*.style", "*.suo", "*.swf", "*.tab", "*.tat", "*.tbx", "*.tda", "*.tfw", "*.tgz", "*.thm", "*.tif", "*.tin", "*.tlb", "*.tlog", "*.tma", "*.tmp", "*.ttf", "*.txt", "*.txx", "*.url", "*.user", "*.vba", "*.vbs", "*.wkt", "*.wmf", "*.wor", "*.x32", "*.xls", "*.xlsx", "*.xml", "*.xsd", "*.xsl", "*.zip"))  #write all files to be excluded from the backup
 

#Directories and search parameters, change these:
targetDir = u"F:\GISdata\Raster" #directory where files are located, this dir is searched for the old LYRS ie after a drive update from M:\ to F:\, write F:\
oldPath = "M:\\" #the old part of the directory that needs updating (FROM)
newPath = "F:\\" #the new part that the file should be updated to (TO)

print "Batch update of .lyr files is started for: " + targetDir + "\n"

#Every file is backed up in a subfolder named _BK therefore this is first created if it doesn't exist already.
#python versions < 3 does not support ignoring everything but value in list, therefore i have to ignore all known files except lyr files. There are other more elegant solutions, but this works... (ignorefiles)
if not os.path.exists(targetDir + "\_BK"):
               print "No Backup is found, " + targetDir + "\_BK is created..."
               shutil.copytree(targetDir, targetDir + "\_BK\\", ignore=shutil.ignore_patterns(ignorefiles)
               print "Backup Completed! \n"
elif os.path.exists(targetDir + "\_BK"):
                  print "Updates Backup in, " + targetDir + "\_BK..."  
                  os.system('rmdir /S /Q \"{}\"'.format(targetDir + "\_BK"))
                  shutil.copytree(targetDir, targetDir + "\_BK\\", shutil.ignore_patterns(ignorefiles)
				  print "Backup Completed! \n"

#Loop through each LYR in the folder and write paths to a list
for root, dirs, files in os.walk(targetDir):
    for filename in files:
	    #splits all filenames, checks the suffic againt the extList variable.
        splitFilename = filename.split(".")
        if splitFilename[-1] in extList:
		    #merge the split filename again
            fullpath = os.path.join(root, filename)
			#appends the merged shp filename and path to the mappath list.
            mappaths.append(fullpath)
			#if there is an existing _BK folder in the dirs, i have to exclude/remove them.
            if "_BK" in dirs:
               dirs.remove("_BK")

#I could use try and catch exeptions, but this works fine and it skips the files not working...
for maps in mappaths:
   lyr = arcpy.mapping.Layer(maps)
   #If some stuff is true, then continue and start replacing the sources otherwise print a statement, and continue...
   for layer in arcpy.mapping.ListLayers(lyr):
       if layer.supports("DATASOURCE"):
            if oldPath in layer.dataSource:
               if ".shp" or ".gdb" in layer.dataSource:
                  print "\n Layer: " + layer.name + "\n old data source: " + layer.dataSource
                  layer.findAndReplaceWorkspacePath(oldPath, newPath, False)
                  print " New data source: " + layer.dataSource
                  lyr.saveACopy(maps)
                  print " .lyr saved at:   " + maps + "\n"
            else:
               print "No changes are needed to " + maps #comment out this print statement if debugging is not neccesary, this ensures that all paths are printed incl. those that are not changed (if the IF statement is not true)

print "\n Done updating files!"

#ERROR messages help:
#layer.name does not equal filename
#The error: "ValueError: Layer: Unexpected error" is caused by a lyr file not pointing to a designated file in the first place. ie missing a shp file reference. Open the last mentioned file in the python view and check the datasource manually.
#CreateObject Layer invalid data source, fails because there is a .lyr file that is broken somewhere after the last opened file

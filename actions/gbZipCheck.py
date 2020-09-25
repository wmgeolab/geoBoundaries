import os
import sys
import zipfile
import subprocess

#For testing
try:
    working = os.environ['GITHUB_WORKSPACE']
except:
    working = "/home/dan/git/gbRelease"
print("Python WD: " + working)  

#For testing
try:
    changedFiles = os.environ['changes'].strip('][').split(',')
except:
    changedFiles = ['.github/workflows/gbPush.yml', 'sourceData/gbOpen/ARE_ADM1.zip', 'sourceData/gbOpen/QAT_ADM0.zip']

print("Python changedFiles: " + str(changedFiles))


#Check that zip files exist in the request
zips = list(filter(lambda x: x[-4:] == '.zip', changedFiles))

zipFailures = 0
zipSuccess = 0
zipTotal = 0

if(len(zips) > 0):
    print("Modified zip files found.  Downloading and checking validity.")
    print("")
    zipTotal = zipTotal + 1
    for z in zips:
        checkFail = 0
        print("")
        print("Downloading: " + z)
        try:
            os.remove(working + "/" + z)
        except:
            pass
        try:
            dl = os.system('git lfs pull --include=\"' + z +'\"')
        except:
            print("No file on LFS to retrieve.  Continuing.")
        print("File Check (" + str(zipTotal) + " of " + str(len(zips)) + "): " + z)
        bZip = zipfile.ZipFile(working + "/" + z)
        if("meta.txt" in bZip.namelist()):
            print("Metadata file exists in " + z)
        else:
            print("CRITICAL ERROR: Metadata file does not exist in " + z)
            checkFail = 1
        
        geojson = list(filter(lambda x: x[-4:] == '.geojson', bZip.namelist()))
        shp = list(filter(lambda x: x[-4:] == '.shp', bZip.namelist()))
        allShps = geojson + shp 
        if(len(allShps) == 1):
            if(len(shp) == 1):
                print("Shapefile (*.shp) found. Checking if all required files are present.")
                if(len(list(filter(lambda x: x[-4:] == '.shx', bZip.namelist()))) != 1):
                    print("CRITICAL ERROR: A valid *.shp requires a *.shx (index) file. None was found in " + z)
                    checkFail = 1
                else:
                    print(".shx found.")
                if(len(list(filter(lambda x: x[-4:] == '.dbf', bZip.namelist()))) != 1):
                    print("CRITICAL ERROR: A valid *.shp requires a *.dbf (index) file. None was found in " + z)
                    checkFail = 1
                else:
                    print(".dbf found.")
                if(len(list(filter(lambda x: x[-4:] == '.prj', bZip.namelist()))) != 1):
                    print("CRITICAL ERROR: A valid *.shp requires a *.prj (index) file. None was found in " + z)
                    checkFail = 1
                else:
                    print(".prj found.")

            if(len(geojson) == 1):
                print("geoJSON found.")

        if(len(allShps) == 0):
            print("CRITICAL ERROR: No *.shp or *.geojson found for " + z)
            checkFail = 1
        if(len(allShps) > 1):
            print("CRITICAL ERROR: More than one geometry file (*.shp, *.geojson) was found for " + z)
            checkFail = 1
        
        if(checkFail == 1):
            zipFailures = zipFailures + 1
            print("CRITICAL ERROR: Zipfile validity checks failed for " + z + ".  Check the log to see what is wrong.")
        else:
            zipSuccess = zipSuccess + 1
            print("Zipfile validity checks passed for " + z)

    print("")
    print("====================")
    print("All zip validity checks complete.")
    print("Successes: " + str(zipSuccess))
    print("Failures: " + str(zipFailures))
    if(zipFailures > 0):
        sys.exit("CRITICAL ERROR: At least one Metadata check failed; check the log to see what's wrong.")

else:
    print("No modified zip files found.")
    sys.exit("Error: No zip files found!")

import os
import sys
import zipfile
import subprocess
import pandas as pd
import geopandas

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
anyFail = 0

if(len(zips) > 0):
    print("Modified zip files found.  Checking shape data validity.")
    print("")
    
    for z in zips:
        zipTotal = zipTotal + 1
        req = {}
        opt = {}

        opt["bndName"] = 0
        opt["nameExample"] = ""
        opt["nameCount"] = 0
        opt["bndISO"] = 0
        opt["isoExample"] = ""
        opt["isoCount"] = 0
        
        req["topology"] = 0
        req["proj"] = 0


        checkFail = 0
        print("")
        print("--------------------------------")
        print("Downloading: " + z)
        try:
            os.remove(working + "/" + z)
        except:
            pass
        try:
            dl = os.system('git lfs pull --include=\"' + z +'\"')
        except:
            print("No file on LFS to retrieve.  Continuing.")
        print("Data Check (" + str(zipTotal) + " of " + str(len(zips)) + "): " + z)
        bZip = zipfile.ZipFile(working + "/" + z)

        #Extract the zipfiles contents
        bZip.extractall()

        geojson = list(filter(lambda x: x[-4:] == '.geojson', bZip.namelist()))
        shp = list(filter(lambda x: x[-4:] == '.shp', bZip.namelist()))
        allShps = geojson + shp

        if(len(allShps) == 1):
            if(len(shp) == 1):
                print("Shapefile (*.shp) found. Attempting to load.")
                try:
                    dta = geopandas.read_file(shp[0])
                except:
                    print("CRITICAL ERROR: The shape file provided failed to load. Make sure all required files are included (i.e., *.shx).")
                    checkFail = 1

            if(len(geojson) == 1):
                print("geoJSON (*.geojson) found. Attempting to load.")
                try:
                    dta = geopandas.read_file(geojson[0])
                except:
                    print("CRITICAL ERROR: The geoJSON provided failed to load.")
                    checkFail = 1
            
            
            nameC = set(['Name', 'name', 'NAME', 'shapeName', 'shapename', 'SHAPENAME']) 
            nameCol = list(nameC & set(dta.columns))
            if(len(nameCol) == 1):
                print("")
                print("Column for name detected: " + str(nameCol[0]))
                nameExample = dta[str(nameCol[0])][0]
                nameValues = (dta[dta[str(nameCol[0])].str.contains('.*', regex=True)][str(nameCol[0])]).count()
                print("Total number of names detected: " + str(nameValues))
                print("Example of first name detected: " + str(nameExample))
                opt["bndName"] = 1
                opt["nameExample"] = nameExample
                opt["nameCount"] = nameValues
            else:
                print("WARN: No column for boundary names found.  This is not required.")

            nameC = set(['ISO', 'ISO_code', 'ISO_Code', 'iso', 'shapeISO', 'shapeiso', 'shape_iso']) 
            nameCol = list(nameC & set(dta.columns))
            if(len(nameCol) == 1):
                print("")
                print("Column for boundary ISO detected: " + str(nameCol[0]))
                nameExample = dta[str(nameCol[0])][0]
                nameValues = (dta[dta[str(nameCol[0])].str.contains('.*', regex=True)][str(nameCol[0])]).count()
                print("Total number of boundary ISOs detected: " + str(nameValues))
                print("Example of first boundary ISO detected: " + str(nameExample))
                opt["bndISO"] = 1
                opt["isoExample"] = nameExample
                opt["isoCount"] = nameValues

                if(len(opt["isoExample"]) < 3):
                    print("WARN: While a boundary ISO code column exists with data, the data appears to be invalid and would not be used in a release.  Please ensure the ISO codes follow ISO 3166-2, or the appropriate equivalent standard.")

            else:
                print("WARN: No column for boundary ISOs found.  This is not required.")
            
            for index, row in dta.iterrows():
                validBounds = 1
                validGeom = 1
                warnBuffer = 0
                xmin = row["geometry"].bounds[0]
                ymin = row["geometry"].bounds[1]
                xmax = row["geometry"].bounds[2]
                ymax = row["geometry"].bounds[3]
                tol = 1e-12
                valid = ((xmin >= -180-tol) and (xmax <= 180+tol) and (ymin >= -90-tol) and (ymax <= 90+tol))
                if not valid:
                    checkFail = 1
                    validBounds = 0
                    #print("")
                    #print("CRITICAL ERROR: The bounds of the shapefile appear to be in another castle (i.e., not on the planet earth).  This is frequently indicative of a projection error (we expect EPSG 4326).")
                    #print("Here are the bounds we found: " + str(row["geometry"].bounds))
                if(not row["geometry"].is_valid):
                    if(not row["geometry"].buffer(0).is_valid):
                        checkFail = 1
                        validGeom = 0
                        print("CRITICAL ERROR: At least one polygon is invalid and cannot be corrected.")
                        print("Here is what we know: " + str(row))
                    else:
                        warnBuffer = 1
                        checkFail = 1
                        print("CRITICAL ERROR: At least one polygon is invalid; automatically correcting with shapely buffer(0) clears this error, but it needs to be visually examined.")
                        print("Here is what we know: " + str(row))
                else:
                    req["topology"] = 1

            if(validBounds == 1):
                print("")
                print("All shape geometries are within valid bounds.")
            else:
                print("")
                print("CRITICAL ERROR: At least one geometry had bounds indicating it existed off the planet earth.  This is generally indicative of a projection error.")
            
            if(validGeom == 1):
                print("")
                print("All shape geometries have valid topology.")

            if(warnBuffer == 1):
                print("")
                checkFail = 1
                print("CRITICAL ERROR: At least one polygon was invalid, but could be cleared by shapely buffer(0).  It needs to be visually examined when possible.")


            if(dta.crs == "epsg:4326"):
                print("Projection confirmed as " + str(dta.crs))
                req["proj"] = 1
            else:
                print("The projection must be EPSG 4326.  The file proposed has a projection of: " + str(dta.crs))
                checkFail = 1
                

        if(len(allShps) == 0):
            print("CRITICAL ERROR: No *.shp or *.geojson found for " + z)
            checkFail = 1
            
        if(len(allShps) > 1):
            print("CRITICAL ERROR: More than one geometry file (*.shp, *.geojson) was found for " + z)
            checkFail = 1
                    

        print("")
        print("Data checks complete for " + z)
        print("")
        print("----------------------------")
        print("      OPTIONAL TESTS        ")
        print("----------------------------")
        for i in opt:
            if(opt[i] == 1 or len(str(opt[i]))>1 or isinstance(opt[i], str) or opt[i]>0):
                print('%-20s%-12s' % (i, "PASSED"))
            else:
                print('%-20s%-12s' % (i, "FAILED"))
        print("")
        print("----------------------------")
        print("      REQUIRED TESTS        ")
        print("----------------------------")
        for i in req:
            if(req[i] == 1 or len(str(req[i]))>1 or isinstance(req[i], str) or req[i]>0):
                print('%-20s%-12s' % (i, "PASSED"))
            else:
                print('%-20s%-12s' % (i, "FAILED"))
        print("==========================")
            
            
        
        
        
        if(checkFail == 1):
            zipFailures = zipFailures + 1
            anyFail = 1
            
        else:
            zipSuccess = zipSuccess + 1
            print("Data checks passed for " + z)

    print("")
    print("====================")
    print("All data checks complete.")
    print("Successes: " + str(zipSuccess))
    print("Failures: " + str(zipFailures))
    
    if(zipFailures > 0):
        sys.exit("CRITICAL ERROR: At least one data check failed; check the log to see what's wrong.")

else:
    print("No modified zip files found.")
    sys.exit("Error: No zip files found!")

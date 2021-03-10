import os
import pandas as pd
import json
import requests
import requests_cache
import geopandas
import io

requests_cache.install_cache(os.path.expanduser("~") + "/tmp/cache")

#Build ADM0 datasets
directory = os.path.expanduser("~") + "/git/geoBoundaries/ancillaryData/gdOpen/sourceData/ADM0/"
dd = []
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        vD = {}
        vD["STATUS"] = "PASS"
        fD = {}
        fD["FILE"] = filename
        fD["STATUS"] = "PASS"
        
        print("Parsing " +  os.path.join(directory, filename))
        for l in open(os.path.join(directory, filename), 'r'):
            try:
                key = l.replace("http://","").replace("https://","").split(':', 1)[0].strip("\n")
                val = l.replace("http://","").replace("https://","").split(':', 1)[1].strip("\n")
            except:
                key = "NA"
                val = "NA"
            
            if(key != "NA"):
                vD[key] = val

        #Check if mandatory fields are filled.
        #Note checking for field validity yet.
        errors = []
        warns = []
        
        if((("Metadata for" in vD) and
            ("Full Variable Name" in vD) and
            ("Data Definition" in vD) and
            ("Units" in vD) and
            ("Data Representative Of Year(s)" in vD) and
            ("geoBoundary Shapefile Dataset API Link" in vD) and
            ("Each row ID is defined by" in vD) and
            ("Data Processing Methodology" in vD) and 
            ("Data Collection Methodology (or link to documentation)" in vD) and
            (("Source 1" in vD) or ("Source 2" in vD)) and
            ("License" in vD) and
            ("License Source" in vD) and
            ("Link to Source Data" in vD) and
            ("Tag(s)" in vD) and
            ("Other Notes" in vD))):
            
            print("All required fields exist.  Checking validity.")
        
        else:
            errors.append("Not all required fields exist.  Even if they are left blank, all required fields must be present in the metadata file.\n\r")
            fD["STATUS"] = "FAIL"

    
        
        if(len(str(vD["Metadata for"]).strip()) <= 10 and len(str(vD["Metadata for"]).strip()) > 0):
            fD["VARNAME"] = vD["Metadata for"].upper()
        else:
            errors.append("Metadata variable name is invalid.  Must be 10 characters or less.\n\r")
            fD["STATUS"] = "FAIL"
            fD["VARNAME"] = "ERROR"
            
        
        if(not len(str(vD["Full Variable Name"])) > 5):
            errors.append("Full variable name must be at least 5 characters long.\n\r")
            fD["STATUS"] = "FAIL"
            fD["fullName"] = "ERROR"
        else:
            fD["fullName"] = vD["Full Variable Name"]

        if(not len(str(vD["Data Definition"])) > 5):
            errors.append("No data definition was detected.\n\r")
            fD["STATUS"] = "FAIL"
            fD["dataDefinition"] = "ERROR"
        else:
            fD["dataDefinition"] = vD["Data Definition"]
        
        if(not len(str(vD["Units"])) > 3):
            errors.append("No units were detected.  Units must be at least 3 characters long - i.e., use 'Celsius', not 'C' - to prevent ambiguity.\n\r")
            fD["STATUS"] = "FAIL"
            fD["Units"] = "ERROR"
        else:
            fD["Units"] = vD["Units"]

        if(not len(str(vD["Data Representative Of Year(s)"])) > 3):
            errors.append("Must specify either a single year or range of years in format YYYY or YYYY-YYYY.\n\r")
            fD["STATUS"] = "FAIL"
            fD["Years"] = "ERROR"
        else:
            fD["Years"] = vD["Data Representative Of Year(s)"]
        
        if(not len(str(vD["geoBoundary Shapefile Dataset API Link"])) > 3):
            errors.append("Specify the geoBoundary API URL - i.e., https://www.geoboundaries.org/gbRequest.html?ISO=GLB&VER=3_0_0&ADM=ADM0.\n\r")
            fD["STATUS"] = "FAIL"
            fD["geoBoundary"] = "ERROR"
            fD["GROUP"] = ""
            fD["REGION"] = ""
            fd["VER"] = ""
        else:
            fD["geoBoundary"] = vD["geoBoundary Shapefile Dataset API Link"]
            fD["REGION"] = [i for i in fD["geoBoundary"].split("?")[1].split("&") if i.startswith("ISO")][0].split("=")[1]
            fD["GROUP"] = [i for i in fD["geoBoundary"].split("?")[1].split("&") if i.startswith("ADM")][0].split("=")[1]
            fD["VER"] = [i for i in fD["geoBoundary"].split("?")[1].split("&") if i.startswith("VER")][0].split("=")[1]
        
        if(not len(str(vD["Data Processing Methodology"])) > 3):
            errors.append("Please provide at least one sentence describing any data processing you conducted on this data (even if it was simply retrieval).\n\r")
            fD["STATUS"] = "FAIL"
            fD["dataProcessingMethod"] = "ERROR"
        else:
            fD["dataProcessingMethod"] = vD["Data Processing Methodology"]


        if(not len(str(vD["Data Collection Methodology (or link to documentation)"])) > 3):
            warns.append("Please provide at least one sentence describing how the data was collected, or who collected it.  A link to a description also works.  This is an optional field.).\n\r")
            fD["dataCollectionMethod"] = "ERROR"
        else:
            fD["dataCollectionMethod"] = vD["Data Collection Methodology (or link to documentation)"]
            

        if(not len(str(vD["Each row ID is defined by"])) > 3):
            warns.append("Tell us what each row in the database is (i.e., ISO code or other linking code).  This is an optional field..\n\r")
            fD["rowDef"] = "ERROR"
        else:
            fD["rowDef"] = vD["Each row ID is defined by"]
            
        if((not len(str(vD["Source 1"])) > 3) and (not len(str(vD["Source 2"])) > 3)):
            errors.append("At least one source must be specified.")
            fD["STATUS"] = "FAIL"
            fD["Source_1"] = "ERROR"
            fD["Source_2"] = "ERROR"
        else:
            fD["Source_1"] = vD["Source 1"]
            fD["Source_2"] = vD["Source 2"]
        
        if((not len(str(vD["License"])) > 3) or (not len(str(vD["License Source"])) > 3)):
            errors.append("Both a license and license source for the data must be specified.")
            fD["STATUS"] = "FAIL"
            fD["License"] = "ERROR"
            fD["licenseSource"] = "ERROR"
        else:
            fD["License"] = vD["License"]
            fD["licenseSource"] = vD["License Source"]

        if(not len(str(vD["Tag(s)"])) > 3):
            warns.append("Specify at least one tag.  This is optional; untagged elements will be added to a generic 'All data' Tag.")
            fD["Tags"] = "ERROR"
        else:
            fD["Tags"] = vD["Tag(s)"]

        #Load the data and do diagnostics.
        dataCSV = filename.replace("meta","").replace(".txt",".csv")
        df = pd.read_csv(directory + dataCSV)
        
        if(len(df) < 2):
            errors.append("It doesn't appear that you have any data in your CSV file.")
            fD["STATUS"] = "FAIL"
            fD["DATACHECK"] = "ERROR. No data found"
        else:
            fD["DATACHECK"] = "PASS"
            
            if((df["Value"].isna().sum() / len(df)) > 0.5):
                errors.append("ERROR. More than fifty percent of your data is missing an observation.  We can't accept this dataset right now.")
                fD["STATUS"] = "FAIL"
                fD["DATACHECK"] = "Missing at least fifty percent of data; not accepted."
            
            if((df["Value"].isna().sum() / len(df)) > 0.1):
                warns.append("PASS. Note that more than 10 percent of your data is missing an observation.  While it's accepted in this version of gD, it won't be in the future.")
                fD["DATACHECK"] = "More than 10 percent of data is missing an observation.  Accepted in this version of gD, but it won't be in the future."


        fD["CRITICALERRORS"] = errors
        fD["WARNINGS"] = warns

        #If everything passed, build the geoJson with the joined data.
        if(fD["STATUS"] == "PASS"):
            call = "https://" + fD["geoBoundary"].strip()
            r = requests.get(call)
            dlPath = r.json()[0]['gjDownloadURL']
            print("Downloading geoJSON from " + dlPath)
            t = requests.get(dlPath)
            gdf = geopandas.read_file(io.BytesIO(t.content))
            #print(gdf.head())
            joined = gdf.merge(df, left_on="shapeISO", right_on="ID")
            joined = joined.rename(columns={"Value" : fD["VARNAME"].strip()})
            joined.to_file(os.path.expanduser("~") + "/git/geoBoundaries/ancillaryData/gdOpen/buildData/" + fD["VARNAME"] + ".geojson", driver="GeoJSON")

        dd.append(fD)
    else:
        continue

#print(dd)
import csv
keys = dd[0].keys()
with open("gdBuildResults.csv", "w") as f:
    writer = csv.DictWriter(f, keys, delimiter="|")
    writer.writeheader()
    writer.writerows(dd)
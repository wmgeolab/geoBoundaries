import requests
import pandas as pd

df = pd.read_csv("/home/dan/git/gbRelease/ancillaryData/ingestScripts/ADM0.csv", index_col=0, header=[0,1], skiprows=[0,3,4], dtype=str)

lookup = pd.read_csv("/home/dan/git/gbRelease/ancillaryData/ingestScripts/ADM0.csv", index_col=0, header=[0,1], skiprows=[0], nrows=2)

valid = []
for i in range(0, len(df.columns)):
    #First element of data in each case
    if(df.columns[i][1] == "Value"):
        validSet = {}
        validSet["Name"] = df.columns[i][0]
        print("======================================================\n")
        print("Conducting metadata check for " + str(df.columns[i][0]) + "\n")

        try:
            if((int(lookup[df.columns[i][0]]["Year Represented"][0]) > 1500) and (int(lookup[df.columns[i][0]]["Year Represented"][0]) < 2500)):
                validSet["startYear"] = lookup[df.columns[i][0]]["Year Represented"][0]
                validSet["endYear"] = lookup[df.columns[i][0]]["Year Represented"][0]
                print("YEAR(S) REPRESENTED: PASS")
            else:
                print("Year field for " + str (df.columns[i][0]) + " is invalid!\n")
                validSet["startYear"] = False
                validSet["endYear"] = False
        except:
            #Range of Years
            try:
                yearSplit = str(lookup[df.columns[i][0]]["Year Represented"][0]).split("-")
                if(int(yearSplit[0]) > 1500 and int(yearSplit[0]) < 2500):
                    if(int(yearSplit[1]) > 1500 and int(yearSplit[1]) < 2500):
                        validSet["startYear"] = yearSplit[0]
                        validSet["endYear"] = yearSplit[1]
                    
                    else:
                        print("It looks like you're trying to specify a range of years.  This must be in YYYY-YYYY format.")
                        print("Raw Format Detected: " + str(lookup[df.columns[i][0]]["Year Represented"][0]))
                        print("Parsed Format: " + str(yearSplit))
                        validSet["startYear"] = False
                        validSet["endYear"] = False
                else:
                    print("It looks like you're trying to specify a range of years.  This must be in YYYY-YYYY format.")
                    validSet["startYear"] = False
                    validSet["endYear"] = False
            except:
                print("Invalid year specified for this ingest script.")
                validSet["startYear"] = False
                validSet["endYear"] = False

        try:
            if(len(lookup[df.columns[i][0]]["Source"][0]) > 1):
                validSet["source"] = lookup[df.columns[i][0]]["Source"][0]
                print("SOURCE:              PASS")
        
            else:
                print("Source field for " + str(df.columns[i][0]) + " is invalid!\n")
                validSet["source"] = False
        except:
            print("Source field could not be parsed for " + str(df.columns[i][0])+ ".\n")
        

        #Try to find URL
        try:
            if('http' in lookup[df.columns[i][0]]["Other Notes"][1]):
                validSet["url"] = lookup[df.columns[i][0]]["Other Notes"][1]
            else:
                print("No valid URL detected.")
                validSet["url"] = False
        except:
            print("No valid URL detected.")
            validSet["url"] = False

        #Detect Tags
        validSet["tags"] = []
        try:
            validSet["tags"].append(lookup[df.columns[i][0]]["Value"][1])
        except:
            print("No tag 1 found.")
        try:
            validSet["tags"].append(lookup[df.columns[i][0]]["Year Represented"][1])
        except:
            print("No tag 2 found.")


        valid.append(validSet)


keys = valid[0].keys()
import os
import csv
with open(os.path.expanduser("~") + "/tmp/ancillaryData/gdTranslate_metaDataChecks.csv", "w") as f:
    writer = csv.DictWriter(f, keys)
    writer.writeheader()
    writer.writerows(valid)


#Create folders and data structures.
#Only doing this for a subset that we have 10-char names for, for now.
metaCrosswalk = {}
metaCrosswalk["Maternal Mortality Rate"] = "MATMORRATE"
metaCrosswalk["Proportion of Population with Access to Electricity"] = "PERPOPELEC"


for i in range(0, len(valid)):
    try:
        varName = metaCrosswalk[valid[i]["Name"]]
        crosswalk = True
    except:
        print("No crosswalk exists for this variable.")
        crosswalk = False
    
    if(crosswalk == True):
        fname = "meta" + varName + ".txt"

        metaC = "geoDesc (www.geodesc.org) Ancillary Variables Metadata File \n"
        metaC = metaC +  "==============================================================\n"
        metaC = metaC +  "Metadata for: " + varName + "\n"
        metaC = metaC +  "Full Variable Name: " + valid[i]["Name"] + "\n"
        metaC = metaC +  "==============================================================\n"
        metaC = metaC +  "\n"
        metaC = metaC +  "Data Definition: \n"
        metaC = metaC +  "Units: \n"
        metaC = metaC +  "Data Representative Of Year(s): " + str(valid[i]["startYear"])[:-2] + "-" + str(valid[i]["endYear"])[:-2] + "\n"
        metaC = metaC +  "Each row in the dataset is representative of: " + "ADM0\n" 
        metaC = metaC +  "Each row ID is defined by: " + "ISO 3166-1 alpha-3\n"
        metaC = metaC +  "Data Processing Methodology: \n"
        
        metaC = metaC +  "Data Collection Methodology (or link to documentation): \n"
        
        metaC = metaC +  "Source 1: " + str(valid[i]["source"]) + "\n"
        metaC = metaC +  "Source 2: " + "\n"

        metaC = metaC +  "License: \n" 
        metaC = metaC +  "License Source: \n"
        metaC = metaC +  "Link to Source Data: " + str(valid[i]["url"]) + "\n"

        metaC = metaC + "Tag(s): "
        for j in range(0, len(valid[i]["tags"])-1):
            metaC = metaC +  str(valid[i]["tags"][j]) + ","
        metaC = metaC[:-1] + "\n"

        metaC = metaC +  "Other Notes: \n" 

        with open(os.path.expanduser("~") + "/git/gbRelease/ancillaryData/gdOpen/ADM0/" + fname, "w+") as f:
            f.write(metaC)

        #Write out the data for this variable.
        csvName = os.path.expanduser("~") + "/git/gbRelease/ancillaryData/gdOpen/ADM0/" + varName + ".csv"
        df[valid[i]["Name"]]["Value"].to_csv(csvName, index_label="ID", header=["Value"])
        
        


    
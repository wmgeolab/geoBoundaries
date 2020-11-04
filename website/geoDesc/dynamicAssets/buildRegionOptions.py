import pandas as pd
import os 

#Going to act as if we're using gbAuthoritative to identify 
#Boundaries - will need to swithc to gbOpen for production.
#Will also need to peg this to a specific release each time.

b = pd.read_csv(os.path.realpath("../../../ancillaryData/gdOpen/scripts/geoDataIngest/gdBuildResults.csv"), delimiter="|")

cL = pd.read_csv(os.path.realpath("../../../releaseData/gbOpen/gbOpen_metaData.csv"))

iso = pd.read_csv("https://raw.githubusercontent.com/wmgeolab/geoBoundaryBot/master/dta/iso_3166_1_alpha_3.csv", encoding="latin1")

#export const data = [{ id: 1, title: 'DatasetA', year: 'Test' },
#            {id:2, title:"DatasetB", year:'test2'}
#];

buildData = []
buildData.append("export const data = [")

buildConst = []
buildConst.append("export const regionOptions = [")
    

for index, row in b.iterrows():
    rowLabel = "NONE"
    if((row['STATUS'] == "PASS")):
        if(row["REGION"] == "GLB"):
            if(row["GROUP"] == "ADM0"):
                rowLabel = "Global / ADM0 (Countries)"
            if(row["GROUP"] == "ADM1"):
                rowLabel = "Global / ADM1 (States or Equivalent)"
            if(row["GROUP"] == "ADM2"):
                rowLabel = "Global / ADM2 (Districts or Equivalent)"
        else:
            #NEED TO ADD CANONICAL LOOKUP HERE.  
            print(cL["boundaryISO"])
            print(row["REGION"])
            print(cL.loc[cL["boundaryISO"] == row["REGION"]])

            canon = cL.loc[(cL["boundaryISO"] == row["REGION"]) & (cL["boundaryType"] == row["GROUP"])]["boundaryCanonical"].values[0].strip()
            rowLabel = str(iso.loc[iso["Alpha-3code"] == row["REGION"]]["Country"].values[0]).strip() + " / " + str(row["GROUP"]).strip() + " (" + canon + ")"

        buildData.append('{ boundID:"' + row["REGION"] + "_" + row["GROUP"] + '", varID:"' + row["VARNAME"].strip() + '", title:"' + row["fullName"].strip() + '", units:"' + row["Units"].strip() + '", source:"' + row["Source_1"].strip()  + '"},')

    if(rowLabel != "NONE"):
        buildConst.append('{ code:"' + row["REGION"].strip() + "_" + row["GROUP"].strip() + '", label: "' + rowLabel + '"},')

    

buildConst[-1] = buildConst[-1][:-1]
buildConst.append("];")

buildData[-1] = buildData[-1][:-1]
buildData.append("];")

#Remove any duplicates
buildConst = list(dict.fromkeys(buildConst))

with open('regionOptions.js', "w") as f:
    for i in buildConst:
        f.write("%s\n" % i)

with open('regionData.js', "w") as f:
    for i in buildData:
        f.write("%s\n" % i)

print(buildConst)
print(buildData)


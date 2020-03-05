#8 Generate relevant statistics for release and save htem to the release_dta.js (license counts, etc).
#Note this stage of the build is NOT automatic,
#As it will update the front-end of the website.
import json
import os
import pandas as pd

def releaseDta(buildID, version):
  metaData = pd.read_csv("./release/" + buildID + "/" + buildID + ".csv")
  #metaZip = "./release/" + buildID + "/" + buildID + ".zip"

  

  shpCnt = 0
  #Calculate total number of shapes
  #Commented out after first run for builds,
  #As it takes a while and I haven't written this properly yet!
  #2_0_0 - 351819
  #for i, row in metaData.iterrows():
  #  jsonPath = "./release/" + row["downloadURL"][31:][:-8] + ".geojson"
  #  jsonObj = open(jsonPath)
  #  cnt = json.load(jsonObj)
  #  shpCnt = shpCnt + len(cnt['features'])
  #  print(shpCnt)
  
  # print(shpCnt)
  
  totalBounds = metaData.shape[0]
  totalCountries = metaData["boundaryISO"].nunique()
  totalADM1 = metaData.groupby("boundaryType").count()["boundaryID"]["ADM1"]
  totalADM2 = metaData.groupby("boundaryType").count()["boundaryID"]["ADM2"]
  totalADM3 = metaData.groupby("boundaryType").count()["boundaryID"]["ADM3"]
  totalADM4 = metaData.groupby("boundaryType").count()["boundaryID"]["ADM4"]
  totalADM5 = metaData.groupby("boundaryType").count()["boundaryID"]["ADM5"]
  
  adm1_prog = int(round((totalADM1 / totalCountries) * 100, 0))
  adm2_prog = int(round((totalADM2 / totalCountries) * 100, 0))
  adm3_prog = int(round((totalADM3 / totalCountries) * 100, 0))
  
  #fullDLsize = round((os.path.getsize(metaZip) / 1000000000), 1)
  
  #Calculate full size of all ADM1 for Publication
  size = 0
  for index, row in metaData.iterrows():
    if(row["boundaryType"] == "ADM1"):
      print(row)
      size = size + os.path.getsize("./release/" + buildID + "/" + row["boundaryISO"] + "/ADM1/geoBoundaries-2_0_0-" + row["boundaryISO"] + "-ADM1-shp.zip")
    
  print(size)
  URL = "https://www.geoboundaries.org/data/" + buildID + "/" + buildID + ".zip"
  
  #rDest = "./tmp/release_dta.js"
  #rD = open(rDest, "w")
  #rD.write("var data = {\n")
  #rD.write('MRV: "' + version + '",\n')
  #rD.write('IS: "' + str(351819) + '",\n')
  #rD.write('ADM1PROG: "' + str(adm1_prog) + '%",\n')
  #rD.write('ADM2PROG: "' + str(adm2_prog) + '%",\n')
  #rD.write('ADM3PROG: "' + str(adm3_prog) + '%",\n')
  #rD.write('FULLDLSIZE: "' + str(fullDLsize) + '",\n')
  #rD.write('DLLINK: "' + str(URL) + '"\n')
  #rD.write('}')
  #rD.close()
  
  #Print to screen the license information
  print(metaData.groupby("boundaryLicense").count())
  

  

  
releaseDta("geoBoundaries-2_0_0", "2.0.0")
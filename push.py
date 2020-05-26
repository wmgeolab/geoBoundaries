#Script to push new major / minor release of geoBoundaries
import pandas as pd
from os.path import expanduser
import glob
import os
import fiona
home = expanduser("~")

#Specify Version this release will be:
geoBoundariesVersion = "3_0_0"

#Can use this script to push core or ancillary products.
#Accepts a list
#HPSCU - High Precision Single Country Unstadardized (HPSCU)
#HPSCGS - High Precision Single Country Globally Standardized (HPSCGS)
#CGAZ - Contigious Global Administrative Zones
#SSCU - Simplified Single Country Unstandardized 
#SSCGS - Simplified Single Country Globally Standardized
pushType = ["HPSCU", "HPSCGS", "SSCU", "SSCGS"]



#Create CITATION_AND_USE.txt
citeUsePath = (home + "/gbRelease/gbReleaseData/CITATION-AND-USE-geoBoundaries-" + version + ".txt")
citUse = open(citeUsePath, "w")
citUse.write("====================================================\n")
citUse.write("Citation of the geoBoundaries Data Product\n")
citUse.write("====================================================\n")
citUse.write("geoBoundaries Version " + version.replace("_",".") + "\n")
citUse.write("www.geoboundaries.org \n")
citUse.write("geolab.wm.edu \n")
citUse.write("The geoBoundaries database is made available in a \n")
citUse.write("variety of software formats to support GIS software \n")
citUse.write("programs.  Contrasted to other administrative \n")
citUse.write("boundary datasets, geoBoundaries is an open product: \n")
citUse.write("all boundaries are open and redistributable, and are \n")
citUse.write("released alongside extensive metadata and license \n")
citUse.write("information to help inform end users. \n")
citUse.write("We update geoBoundaries on a yearly cycle, \n")
citUse.write("with new versions in or around August of each calendar \n")
citUse.write("year; old versions remain accessible at www.geoboundaries.org. \n")
citUse.write("The only requirement to use this data is to, with any use, provide\n")
citUse.write("information on the authors (us), a link to geoboundaries.org or \n")
citUse.write("our academic citation, and the version of geoBoundaries used. \n")
citUse.write("Example citations for the current version of GeoBoundaries are:  \n")
citUse.write(" \n")
citUse.write("+++++ General Use Citation +++++\n")
citUse.write("Please include the term 'geoBoundaries v. "+ version.replace("_",".") +  "' with a link to")
citUse.write("https://www.geoboundaries.org\n")
citUse.write(" \n")
citUse.write("+++++ Academic Use Citation +++++++++++\n")
citUse.write("Runfola D, Anderson A, Baier H, Crittenden M, Dowker E, Fuhrig S, et al. (2020) \n")
citUse.write("geoBoundaries: A global database of political administrative boundaries. \n")
citUse.write("PLoS ONE 15(4): e0231866. https://doi.org/10.1371/journal.pone.0231866. \n")
citUse.write("\n")
citUse.write("Users using individual boundary files from geoBoundaries should additionally\n")
citUse.write("ensure that they are citing the sources provided in the metadata for each file.\n")
citUse.write(" \n")
citUse.write("====================================================\n")
citUse.write("Column Definitions\n")
citUse.write("====================================================\n")
citUse.write("boundaryID - A unique ID created for every boundary in the geoBoundaries database by concatenating ISO 3166-1 3 letter country code, boundary level, geoBoundaries version, and an incrementing ID.\n")
citUse.write("boundaryISO -  The ISO 3166-1 3-letter country codes for each boundary.\n")
citUse.write("boundaryYear - The year for which a boundary is representative.\n")
citUse.write("boundaryType - The type of boundary defined (i.e., ADM0 is equivalent to a country border; ADM1 a state.  Levels below ADM1 can vary in definition by country.)\n")
citUse.write("boundarySource-K - The name of the Kth source for the boundary definition used (with most boundaries having two identified sources).\n")
citUse.write("boundaryLicense - The specific license the data is released under.\n")
citUse.write("licenseDetail - Any details necessary for the interpretation or use of the license noted.\n")
citUse.write("licenseSource - A resolvable URL (checked at the time of data release) declaring the license under which a data product is made available.\n")
citUse.write("boundarySourceURL -  A resolvable URL (checked at the time of data release) from which source data was retrieved.\n")
citUse.write("boundaryUpdate - A date encoded following ISO 8601 (Year-Month-Date) describing the last date this boundary was updated, for use in programmatic updating based on new releases.\n")
citUse.write("downloadURL - A URL from which the geoBoundary can be downloaded.\n")
citUse.write("shapeID - The boundary ID, followed by the letter `B' and a unique integer for each shape which is a member of that boundary.\n")
citUse.write("shapeName - The identified name for a given shape.  'None' if not identified.\n")
citUse.write("shapeGroup - The country or similar organizational group that a shape belongs to, in ISO 3166-1 where relevant.\n")
citUse.write("shapeType - The type of boundary represented by the shape.\n")
citUse.write("shapeISO - ISO codes for individual administrative districts, where available.  Where possible, these conform to ISO 3166-2, but this is not guaranteed in all cases. 'None' if not identified.\n")
citUse.write(" \n")
citUse.write("====================================================\n")
citUse.write("Reporting Issues or Errors\n")
citUse.write("====================================================\n")
citUse.write("We track issues associated with the geoBoundaries dataset publically,\n")
citUse.write("and any individual can contribute comments through our github repository:\n")
citUse.write("https://github.com/wmgeolab/gbRelease\n")
citUse.write(" \n")
citUse.write("Thank you for citing your use of geoBoundaries and reporting any issues you find -\n")
citUse.write("as a non-profit academic project, your citations are what keeps geoBoundaries alive.\n")
citUse.write("-Dan Runfola (dan@danrunfola.com)")
citUse.close()
#HPSCU - High Precision Single Country Unstadardized (HPSCU)
#HPSCGS - High Precision Single Country Globally Standardized (HPSCGS)
#CGAZ - Contigious Global Administrative Zones
#SSCU - Simplified Single Country Unstandardized 
#SSCGS - Simplified Single Country Globally Standardized

class releaseCandidateBoundary:
  def __init__(self,gbMeta, geoBoundariesVersion, home):
    self.iso = str(gbMeta["boundaryISO"])
    self.adm = str(gbMeta["boundaryType"])
    self.home = str(home)
    self.version = str(geoBoundariesVersion)
    self.allMeta = gbMeta
  
  def geoLog(self, errorType, errorMessage):
    folderPath = self.home + "/gbRelease/gbRelease/buildLogs/" + self.version + "/"
    if not os.path.exists(folderPath):
      os.makedirs(folderPath)
    filePath = folderPath + errorType + ".txt"
    while True:
      try:
        with open(filePath, 'a') as f:
          f.write(errorMessage + "\n")
      except:
        break
      
      else:
        return 0  
      
  def HPSCU(self):
    outDirectory = self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/"
    inShape = (self.home + "/gbRelease/gbRawData/current/" + self.iso + "/" + self.adm + 
               "/shapeFixes/" + self.iso + "_" + self.adm + "_" +
               "fixedInternalTopology.shp")
    try:
      shpFile = fiona.open(inShape)
    except:
      geoLog("CRITICAL", (self.iso + "|" self.adm + "Shape failed to open."))
    
    #Build the shapefile zip.
    #Requires first editing shapefile attributes (updating version names)
    #Then second creating the zip

    fID = 0
    for elem in shpFile:
      fID = fID + 1
      elem["properties"]["shapeID"] = (self.iso + "-" + self.adm + "-" + self.version + "-B" + str(fID))

    #Create a geojson
    geojson = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/" +
               "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + ".geojson")
  
    #For uniformity, we'll store all our geoJSONs as multipolygons,
    #even though it's unnecessary for many.
    shpFile.schema["geometry"] = "MultiPolygon"

    kwargs = {"COORDINATE_PRECISION":7}
    with fiona.open(geojson, 'w', driver="GeoJSON", 
                schema=shpFile.schema,
                encoding='utf-8',
                crs=fiona.crs.from_epsg(4326), **kwargs) as write_geojson:

      for feature in shpFile:
        if(feature["geometry"]["type"] == "MultiPolygon"):
          write_geojson.write(feature)
        else:
          multiFeature = feature
          multiFeature['geometry'] = geom.mapping(geom.MultiPolygon([shape(feature["geometry"])]))
          write_geojson.write(multiFeature)
    
    #Create a json and textfile of metadata
    json_txt = self.allMeta
    jsonOut = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/"
               "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + "-metaData.json")
    json_txt.to_json(jsonOut)
  
    csvOutpath = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/"
               "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + "-metaData.txt")
    json_txt.to_csv(csvOutpath, index=True, header=False, sep=' ')
    
    #Create a shapefile
    shapefilePath = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/" +
               "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + ".shp")
  
    with fiona.open(shapefilePath, 'w', driver="ESRI Shapefile", 
                  schema=shpFile.schema,
                 encoding='utf-8',
                 crs=fiona.crs.from_epsg(4326), **kwargs) as write_shp:

      for feature in shpFile:
        if(feature["geometry"]["type"] == "MultiPolygon"):
          write_shp.write(feature)
        else:
          multiFeature = feature
          multiFeature['geometry'] = geom.mapping(geom.MultiPolygon([shape(feature["geometry"])]))
          write_shp.write(multiFeature)
   
    
    dirToZip = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/")
    
    shutil.make_archive(base_name = self.home + "/gbRelease/tmp/geoBoundaries-" + version,
                          format="zip",
                          root_dir = dirToZip)    
      
def pushRelease(pushType, geoBoundariesVersion, metaDataRow, home):
  #Let's not talk about this.
  while True:              
    try:
      if (not os.path.isdir((home + '/gbRelease/gbReleaseData/' + releaseType + '/' + 
                             row["boundaryISO"] + "/"))):
        os.mkdir((home + '/gbRelease/gbReleaseData/' + releaseType + '/' + 
                             row["boundaryISO"] + "/"))
        if not os.path.isdir((home + '/gbRelease/gbReleaseData/' + releaseType + '/' + 
                             row["boundaryISO"] + "/")):
          os.mkdir((home + '/gbRelease/gbReleaseData/' + releaseType + '/' + 
                             row["boundaryISO"] + "/" + row["boundaryType"] + '/'))
    except:
      pass
    else:
      break

      
      

allMeta = glob.glob((home + "/gbRelease/gbRawData/metadata/"))
latestMeta = max(allMeta, key=os.path.getctime)
nightlyVersion = str(latestMeta).split(".")[0]
metaData = pd.read_csv(("./gbRawData/current/geoBoundaries-" + nightlyVersion + ".csv"))


#Confirm the release we're using for the push doesn't have any
#Critical errors remaining.  If so, kill this job.
if(not os.path.isfile(os.path.join((home + "/gbRelease/buildLogs/" + 
                                    nightlyVersion + "/"), "CRITICAL.txt"))):
  #Update the version in the metadata (not a nightly)
  bndCnt = 0
  for i, row in metaData.iterrows():
    bndCnt = bndCnt + 1
    metaData.at[i,'boundaryID'] = (metaData["boundaryISO"] + "-" + 
                                 metaData["boundaryADM"] + "-" 
                                 + geoBoundariesVersion + "-G" + str(bndCnt))
    
  metaData.to_csv((home + "/gbReleaseData/geoBoundaries-" + geoBoundariesVersion + ".csv"), index=False)

  #Create root, country and hierarchy folders if they do not exist.
  #Copy metadata into the root of each, as it is identical across
  #ancillary releases.
  
  for releaseType in pushType:
    if(not os.path.isdir(home + "/gbReleaseData/" + releaseType + "/")):
      os.mkdir(home + "/gbReleaseData/" + releaseType + "/")
      shutil.copyfile((home + "/gbReleaseData/geoBoundaries-" + geoBoundariesVersion + ".csv"),
                      (home + "/gbReleaseData/" + releaseType + "/geoBoundaries-" + geoBoundariesVersion + ".csv"))
  
  #Launch the ships:
  with parallel_backend("loky", inner_max_num_threads=1):
  (Parallel(n_jobs=-2, verbose=100)
   (delayed(pushRelease)
    (pushType, geoBoundariesVersion, metaData.iloc[i], home) 
    for i in range(len(metaData))))
      




      

      
else:
  print("You cannot push this build, as it still has critical errors.")
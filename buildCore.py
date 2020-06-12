import os
import pandas as pd
from datetime import datetime
import glob
from collections import Counter
from joblib import Parallel, delayed, parallel_backend
from os.path import expanduser
import re
import requests
from pathlib import Path
import ciso8601
import zipfile
import time
import shutil
import fiona
import shapely
import subprocess
import shapely
import shapely.geometry
from collections import OrderedDict
home = expanduser("~")
userKey = os.environ.get('USER')

def geoLog(timestamp, errorType, errorMessage):
  folderPath = home + "/gbRelease/buildLogs/" + timestamp + "/"
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


    
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
#Core Class
###################################################
###################################################
###################################################
###################################################
###################################################

class geoBoundary:
  "Class with helper functions to build geoBoundaries releases."
  #import classImports.geoLog as geoLog
  #import classImports.preProcessing as preProcessing
  def __init__(self,gbMeta, nightlyVersion, home):
    self.iso = str(gbMeta["Processed File Name"])[:3]
    self.adm = str(gbMeta["Processed File Name"])[4:8]
    self.source1 = str(gbMeta["Source 1"])
    self.source2 = str(gbMeta["Source 2"])
    self.version = str(nightlyVersion)
    self.license = str(gbMeta["License"])
    self.home = home
    self.gDriveURL = str(gbMeta["gDriveID"])
    try:
      self.year = str(int(gbMeta["Year"]))
    except:
      self.year = "None"
      self.geoLog("WARN", ("ISO " + self.iso + " | " + self.adm +
                   " does not have a valid year."))
    self.lastUpdate = str(gbMeta["Last Updated Date"])
  
  def geoLog(self, errorType, errorMessage):
    folderPath = self.home + "/gbRelease/buildLogs/" + self.version + "/"
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
    
  def metaCheck(self):
    self.metaFail = False
    #ISO Valid Check
    validISOList = pd.read_csv(self.home + "/gbRelease/gbRawData/ISO_0_Standards/ISO_3166_1_Alpha_3.csv", encoding="ISO-8859-1")  
    if(not self.iso in validISOList["Alpha-3code"].values):
      self.geoLog("CRITICAL", ("ISO " +
                               self.iso + " is invalid."))
      self.metaFail = True
    
    #Boundary Type Valid Check
    if(not self.adm in 
       ["ADM0", "ADM1", "ADM2", "ADM3", "ADM4", "ADM5"]):
      self.geoLog("CRITICAL", ("ADM " +
                               self.adm + " is invalid."))
      self.metaFail = True
    
    #Source Exists Check
    if((len(self.source1) < 1) and (len(self.source2) < 1)):
      self.geoLog("CRITICAL", ("ISO " + self.iso + " | " + self.adm +
                               " does not have a valid source for the file origination."))
      self.metaFail = True
  
    #License Valid Type Check
    licenses = list(
    pd.read_csv(self.home + "/gbRelease/gbRawData/gbLicenses.txt", 
      header=None)[0])
    if(not (self.license in licenses)):
        self.geoLog("CRITICAL",("ISO " + self.iso + " | " + self.adm +
                               " does not have a valid license."))
        self.metaFail = True
  
  def checkForUpdatesDownload(self, previousCSV):
    self.retrieveFail = False
    self.metaChange = False
    #Check if the metadata has changed since the last version
    previousCSV = previousCSV[(previousCSV["boundaryISO"] == self.iso) & 
                (previousCSV["boundaryType"] == self.adm)]
    
    
    if(len(previousCSV) == 1):
      if(str(previousCSV["boundaryYear"]) != self.year):
        self.metaChange = True

      if(str(previousCSV["boundarySource-1"]) != self.source1):
        self.metaChange = True

      if(str(previousCSV["boundarySource-2"]) != self.source2):
        self.metaChange = True

      if(str(previousCSV["boundaryLicense"]) != self.license):
        self.metaChange = True
        
    else:
      self.geoLog("INFO",("ISO " + self.iso + " | " + self.adm +
                               " was not in the last release, so cannot be compared for changes."))
    
    
    #Check if the file on google drive is different than what
    #we have local
    self.remoteFileDiff = True
    
    #expected path to zip
    zipDir = home + "/gbRelease/gbRawData/currentZips/"
    self.zipPath = zipDir + self.iso + "_" + self.adm + ".zip"
    
    if(not os.path.isfile(os.path.join(zipDir, (self.iso + "_" + self.adm + ".zip")))):
      self.remoteFileDiff = True
      self.geoLog("INFO",("ISO " + self.iso + " | " + self.adm +
                               " did not have a local file copy. Downloading."))
    
    else:
      rCloneCall = (home + "/libs/rclone -v --drive-impersonate " +
                    userKey + " check remote:releaseCandidates/"+
                    "gbReleaseCandidate_current/" + self.adm + "/" +
                    self.iso + "_" + self.adm + ".zip " + zipDir)
                    
      process = subprocess.Popen([rCloneCall], shell=True, 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      process.wait()
      output, error = process.communicate()

      if(("0 differences found" in str(error)) and os.path.isfile(os.path.join(zipDir, (self.iso + "_" + self.adm + ".zip")))):
        #We already have a matching file, so we can skip this download.
        self.remoteFileDiff = False
        
    if((self.metaChange == True) and (self.remoteFileDiff == False)):
      self.geoLog("WARN",("ISO " + self.iso + " | " + self.adm +
                               " Metadata changed, but the file did not."))
    
    if((self.metaChange == False) and (self.remoteFileDiff == True)):
      self.geoLog("WARN",("ISO " + self.iso + " | " + self.adm +
                               " File changed, but the metadata did not."))
      
    if(self.remoteFileDiff == True):
      self.geoLog("INFO",("ISO " + self.iso + " | " + self.adm +
                               " Downloading new copy from remote."))
    
      rCloneCall = (home + "/libs/rclone -v --drive-impersonate " +
                    userKey + " copy remote:releaseCandidates/"+
                    "gbReleaseCandidate_current/" + self.adm + "/" +
                    self.iso + "_" + self.adm + ".zip " + zipDir)
                    
      dlProcess = subprocess.Popen([rCloneCall], shell=True)
      dlProcess.wait()
      
      if((dlProcess.returncode != 0) or (not os.path.isfile(os.path.join(zipDir, (self.iso + "_" + self.adm + ".zip"))))):
        self.geoLog("CRITICAL",("ISO " + self.iso + " | " + self.adm +
                               " did not have a local file copy, and the download failed."))
        self.retrieveFail = True
        return False
    
    rawUnzipTarget = (self.home + "/gbRelease/gbRawData/current/" + 
                             self.iso + "/" + self.adm + "/")
    if(((self.retrieveFail == False) and (self.remoteFileDiff == True)) or (not os.path.isdir(rawUnzipTarget))):
      #Delete any old data and unzip the new data

      if(not os.path.isdir((self.home + "/gbRelease/gbRawData/current/" + 
                             self.iso + "/"))):
        while True:
          try:
            os.mkdir((self.home + "/gbRelease/gbRawData/current/" + 
                             self.iso + "/"))
          except:
            pass

          else:
            break
      
      if(os.path.isdir(rawUnzipTarget)):
        shutil.rmtree(rawUnzipTarget)
        os.mkdir(rawUnzipTarget)
      if(not os.path.isdir(rawUnzipTarget)):
        os.mkdir(rawUnzipTarget)
      
      try:
        with zipfile.ZipFile(self.zipPath, "r") as zipObj:
          zipObj.extractall(rawUnzipTarget)
      except:
        self.geoLog("CRITICAL", ("ISO " + self.iso + " | " + self.adm + ": had an invalid zip file."))
        self.retrieveFail = True
        return False


  def shapeCheckBuild(self):
    self.shapeFail = False
    #Basic geometry checks
    #Only do these if the file hasn't already been processed.
    correctHome = (self.home + 
                 "/gbRelease/gbRawData/current/" + 
                 self.iso + "/" + self.adm + "/shapeFixes/")
    corrected_shp = (self.home + 
                 "/gbRelease/gbRawData/current/" + 
                 self.iso + "/" + self.adm + "/shapeFixes/" + 
                 self.iso + "_" + self.adm + "_fixedInternalTopology.shp")

    shpPath = (self.home + 
                 "/gbRelease/gbRawData/current/" + 
                 self.iso + "/" + self.adm + "/" +
                 self.iso + "_" + self.adm + ".shp")
    if(not os.path.isdir(correctHome)):
      os.mkdir(correctHome)
      
    if(not os.path.isfile(os.path.join(correctHome, (self.iso + "_" + self.adm + "_fixedInternalTopology.shp")))):
      try:
        shpFile = fiona.open(shpPath)
      except:
        self.geoLog("CRITICAL", ("ISO " + self.iso + " | " + self.adm + ": had an invalid shapefile."))
        self.shapeFail = True
        return 0 


      if(not shpFile.crs['init'] == "epsg:4326"):
        self.geoLog("CRITICAL", ("ISO " + self.iso + " | " + self.adm + ": had an invalid projection."))
        self.shapeFail = True
        return 0 

      xmin = shpFile.bounds[0]
      ymin = shpFile.bounds[1]
      xmax = shpFile.bounds[2]
      ymax = shpFile.bounds[3]
      tol = 1e-12
      valid = ((xmin >= -180-tol) and (xmax <= 180+tol) and (ymin >= -90-tol) and (ymax <= 90+tol))
      if not valid:
        self.geoLog("CRITICAL", ("ISO " + self.iso + " | " + self.adm + ": bounds were in another castle."))
        self.shapeFail = True
        return 0

      #Shapefile Topology checks  
      valid = True
      error = None

      fixed = []
      for feature in shpFile:
        try:
          raw_shape = shapely.geometry.shape(feature['geometry'])
          valid = raw_shape.is_valid
        except:
          self.geoLog("CRITICAL", ("ISO " + self.iso + " | " + self.adm + ": At least one feature is topologically invalid and cannot be fixed automatically."))
          self.shapeFail = True
          return 0
        if valid:
          fixed.append(feature)
        if not valid:
          fixed_shape = raw_shape.buffer(0)
          fix_valid = fixed_shape.is_valid
          if fix_valid and error is None:
            self.geoLog("WARN", ("ISO " + self.iso + " | " + self.adm + ": At least one feature had a minor topological issue, fixed by shapely buffer=0."))
            feature["geometry"] = shapely.geometry.mapping(fixed_shape)
            fixed.append(feature)
          elif not fix_valid:
            if error is not None:
              self.geoLog("CRITICAL", ("ISO " + self.iso + " | " + self.adm + ":CRITICAL ERROR: An error in the geometry of the file " + shpPath + " exists that we could not automatically fix."))
              self.shapeFail = True
              return 0
            else:
              self.geoLog("CRITICAL", ("ISO " + self.iso + " | " + self.adm + "CRITICAL ERROR: A really bad error in the geometry of the file" + shpPath + "exists that we could not automatically fix."))
              self.shapeFail = True
              return 0
      try:
        #Attribute schema checks and fixes
        #Only doing these in case of a file update.
        schema = shpFile.schema.copy()

        #First, identify which of the existing columns represent:
        validNameColumns = ['Name', 'name', 'NAME']
        validISOcolumns = ['ISO', 'ISO_code', 'ISO_Code', 'iso']
        dictName = None
        dictISO = None

        for attribute in list(schema['properties'].items()):
          if(attribute[0] in validNameColumns):
            dictName = attribute[0]
          if(attribute[0] in validISOcolumns):
            dictISO = attribute[0]

        if(dictName == None):
          self.geoLog("WARN", ("ISO " + self.iso + " | " + self.adm + ": No name information was found in a validly named column for: " + shpPath))
          schema["properties"]["shapeName"] = 'str:254'
        else:
          #Rename our name field to the schema field.
          schema["properties"] = OrderedDict([('shapeName', v) if k==dictName else (k,v) for k,v in schema["properties"].items()])


        if(dictISO == None):
          self.geoLog("WARN", ("ISO " + self.iso + " | " + self.adm + ": No ISO information was found in a validly named column for: " + shpPath))
          schema["properties"]["shapeISO"] = 'str:10'
        else:
          schema["properties"] = OrderedDict([('shapeISO', v) if k==dictISO else (k,v) for k,v in schema["properties"].items()])

        #remove invalid elements
        for attribute in list (schema['properties'].items()):
          if(attribute[0] not in ["shapeISO", "shapeName"]):
            schema['properties'].pop(attribute[0])

        #Add additional schema elements 
        schema["properties"]["shapeID"] = 'str:10'
        schema["properties"]["shapeGroup"] = 'str:50'
        schema["properties"]["shapeType"] = 'str:10'

        #Repeat for ordered dicts representing each feature.
        year = self.year
        featureID = 0
        for elem in fixed:
          featureID = featureID + 1
          if(dictName == None):
            elem["properties"]["shapeName"] = 'None'
          else:
            elem["properties"] = OrderedDict([('shapeName', v) if k==dictName else (k,v) for k,v in elem["properties"].items()])

          if(dictISO == None):
            elem["properties"]["shapeISO"] = 'None'
          else:
            elem["properties"] = OrderedDict([('shapeISO', v) if k==dictISO else (k,v) for k,v in elem["properties"].items()])

            #remove invalid elements
          for attribute in list (elem['properties'].items()):
            if(attribute[0] not in ["shapeISO", "shapeName"]):
              elem['properties'].pop(attribute[0])  

          elem["properties"]["shapeID"] = (self.iso + "-" + self.adm + "-" + self.version + '-B' + str(featureID))
          elem["properties"]["shapeGroup"] = self.iso
          elem["properties"]["shapeType"] = self.adm
      except:
        self.geoLog("CRITICAL", ("ISO " + self.iso + " | " + self.adm + ": schema could not be corrected."))
        self.shapeFail = True
        return 0

      #Update the original file with a corrected version:
      try:
        with fiona.open(corrected_shp, 'w', 'ESRI Shapefile', schema, shpFile.crs) as output:
          for elem in fixed:
            output.write(elem)
      except:
        self.geoLog("CRITICAL", ("ISO " + self.iso + " | " + self.adm + ": update did not write correctly."))
        self.shapeFail = True
        
def gbBuild (nightlyVersion, gbMeta, home, previousCSV):
  try:
    boundary = geoBoundary(gbMeta, nightlyVersion, home)
  except ValueError as e:
    geoLog(nightlyVersion, "CRITICAL", "A boundary failed to initialize.  Here is what we know: " + str(e) + "\n" + str(gbMeta))
    return 0
  
  boundary.metaCheck()
  if(boundary.metaFail):
    return 0
  
  boundary.checkForUpdatesDownload(previousCSV)
  if(boundary.retrieveFail):
    return 0
  
  boundary.shapeCheckBuild()
  
  
  
  
#Remove the last iteration to ensure a full file check
if(os.path.isdir(home + "/gbRelease/gbRawData/current/")):
  shutil.rmtree(home + "/gbRelease/gbRawData/current/")
  os.mkdir(home + "/gbRelease/gbRawData/current/")


#Grab the most recent geoBoundaries metadata
sheet = "https://docs.google.com/spreadsheets/d/1SJSpZxgM4rKw9Qb8tj7qtL2G6E3GKLrJL0s-QyTIYIU/edit?usp=sharing"
csv = sheet.replace('/edit?usp=sharing', '/export?format=csv')
currentCSV = pd.read_csv(csv)

#Grab the last pushed build to create delta
#Identify the most recent version of geoBoundaries
r = requests.get("https://www.geoboundaries.org/gbRequest.html?ISO=USA&ADM=ADM0")
lastVersion = (re.search("[0-9]_[0-9]_[0-9]", r.json()[0]
                     ['boundaryID'])[0])
previousCSV = pd.read_csv("https://www.geoboundaries.org/data/geoBoundaries-" +
           lastVersion + "/geoBoundaries-" + lastVersion + ".csv")

#Define build timestamp (version ID)
nightlyVersion = str(round(datetime.timestamp(datetime.now()),0))[:-2]

#Save the current version
currentCSV.to_csv("./gbRelease/gbRawData/metadata/" + nightlyVersion + ".csv")

#Critical error if there are any duplicates (same ISO and ADM level)
criticalDuplicate = currentCSV["Processed File Name"].value_counts() > 1
if(len(criticalDuplicate[criticalDuplicate > 1]) > 0):
  geoLog(nightlyVersion, "CRITICAL", 
         "There is at least one duplicate ISO code / ADM level combination.")
  
#Critical error if there are any duplicate google drive links
criticalDuplicate = currentCSV["gDriveID"].value_counts() > 1
if(len(criticalDuplicate[criticalDuplicate > 1]) > 0):
  geoLog(nightlyVersion, "CRITICAL", 
         "There is at least one duplicate Google Drive link.")

#Check if any boundaries have been added or removed vs. the last recorded metadata.
#Flag these in the logs if so, with a WARN tag.
prevCases = previousCSV["boundaryISO"] + "_" + previousCSV["boundaryType"] + ".zip"

caseCounts = pd.DataFrame.from_dict(
  Counter(prevCases.tolist() + 
          currentCSV["Processed File Name"].tolist()), orient= "index")

caseCounts = caseCounts[caseCounts[0] != 2]
if(len(caseCounts) > 0):
  geoLog(nightlyVersion, "WARN", "NEW OR REMOVED: \n" + caseCounts.to_string())

#Begin high precision single country build for each country.
with parallel_backend("loky", inner_max_num_threads=1):
  (Parallel(n_jobs=-2, verbose=100)
   (delayed(gbBuild)
    (nightlyVersion, currentCSV.iloc[i], home, previousCSV) 
    for i in range(len(currentCSV))))

############################################################
############################################################
#Metadata Standardization for Release
def metaStandardization(metaData, version):  
  metaData["boundaryID"] = "ERROR"
  metaData["boundaryISO"] = "ERROR"
  metaData["boundaryYear"] = "ERROR"
  metaData["boundaryType"] = "ERROR"
  metaData["boundarySource-1"] = "ERROR"
  metaData["boundarySource-2"] = "ERROR"
  metaData["boundaryLicense"] = "ERROR"
  metaData["licenseDetail"] = "ERROR"
  metaData["licenseSource"] = "ERROR"
  metaData["boundarySourceURL"] = "ERROR"
  metaData["boundaryUpdate"] = "ERROR"
  metaData["downloadURL"] = "ERROR"
  
  bndCnt = 0
  for i, row in metaData.iterrows():
    bndCnt = bndCnt + 1
    rowISO = row["Processed File Name"][:3]
    rowADM = row["Boundary Level"].replace(" ","")
    rowGroup = ["boundaryGroup"]
    
    #Create unique ID for each row
    metaData.at[i,'boundaryID'] = rowISO + "-" + rowADM + "-" + version + "-G" + str(bndCnt)
    
    #Save ISO for each row
    metaData.at[i, 'boundaryISO'] = rowISO
    
    #Save Year
    metaData.at[i, "boundaryYear"] = row["Year"]
    
    #Save Type
    metaData.at[i, "boundaryType"] = rowADM
    
    #Save sources
    metaData.at[i, "boundarySource-1"] = row["Source 1"]
    metaData.at[i, "boundarySource-2"] = row["Source 2"]
    
    #License
    metaData.at[i, "boundaryLicense"] = row["License"]
    
    #License Detail
    metaData.at[i, "licenseDetail"] = row["License Detail"]
    
    #License Source
    metaData.at[i, "licenseSource"] = row["License Source"]
    
    #Boundary Source URL
    metaData.at[i, "boundarySourceURL"] = row["Link to Source Data"]
    

    if(not str(row["Last Updated Date"]).find("-") == -1):
      metaData.at[i, "boundaryUpdate"] = str(pd.to_datetime(row["Last Updated Date"], format='%Y-%m-%d', errors="coerce").date())
    else:
      metaData.at[i, "boundaryUpdate"] = str(pd.to_datetime('today', format='%Y-%m-%d', errors='ignore').date())
    
    #Download URL
    fullURL = "https://geoboundaries.org/data/geoBoundaries-" + version + "/" + rowISO + "/" + rowADM + "/"
    fullFile = "geoBoundaries-" + version + "-" + rowISO + "-" + rowADM + "-all.zip"
    metaData.at[i, "downloadURL"] = fullURL + fullFile
      
  cleanMeta = metaData[["boundaryID", "boundaryISO", "boundaryYear", "boundaryType",
                         "boundarySource-1", "boundarySource-2", "boundaryLicense", "licenseDetail",
                         "licenseSource", "boundarySourceURL", "boundaryUpdate", "downloadURL"]]

  
  #Generate the final CSV for the package.
  cleanMeta.to_csv(home + "/gbRelease/gbRawData/current/geoBoundaries-" + version + ".csv", index=False)

try:
  metaStandardization(currentCSV, nightlyVersion)
except:
  geoLog(nightlyVersion, "CRITICAL", "The metadata build failed.")





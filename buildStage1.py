########
#Build Stage 1 for geoBoundaries
#This stage extracts files into the appropriate folder structure,
#confirms the structure of those folders,
#and validates the files themselves.
#Small topology fixes are done in this section as well.
########


#import multiprocessing
import pandas as pd
import zipfile
import shutil
import importlib
import os
import fiona
import shapely
import datetime
import shapely.geometry
from collections import OrderedDict
from pandarallel import pandarallel
import sys

#Using the following hierarchy:
#geoBoundaries-2-0-0_init
###JPN
####ADM0
####ADM1

def buildLogger(logID, dta):
  if os.path.exists(logID):
      append_write = 'a' # append if already exists
  else:
      append_write = 'w' # make a new file if not

  #Hedge against disaster.
  if(len(logID) > 5):
    logger = open(logID,append_write)
    logger.write(dta + '\n')
    logger.close()


def shapeChecks(buildID):
  success_log = ("./build_logs/success/" + buildID + "_shapeCheckOutputs" + ".txt")
  
  if(os.path.isfile(success_log)):
    print("++ Shape Checks have already been completed for this release. Skipping.")
    return(0)
  
  logID = ("./build_logs/" + buildID + "_shapeCheckOutputs_" + str(datetime.datetime.timestamp(datetime.datetime.now())) + ".txt")
  metaData_folder = "./releaseCandidateRaw/" + buildID + "/metadata/"
  metaFiles = [f for f in os.listdir(metaData_folder) if os.path.isfile(os.path.join(metaData_folder, f))]
  metaData = pd.read_excel(metaData_folder + metaFiles[0])
    
  #Create root, country and hierarchy folders if they do not exist:
  if(not os.path.isdir("./releaseCandidateInit/" + buildID + "/")):
    os.mkdir("./releaseCandidateInit/" + buildID + "/")
  
  for row in metaData.iterrows():
    if(not os.path.isdir("./releaseCandidateInit/" + buildID +"/" + row[1][0][:3])):
      os.mkdir("./releaseCandidateInit/" + buildID +"/" + row[1][0][:3])
    
    groupCode = row[1][3].replace(" ","")
    
    if(not os.path.isdir("./releaseCandidateInit/" + buildID +"/" + row[1][0][:3] + "/" + groupCode + "/")):
      os.mkdir("./releaseCandidateInit/" + buildID +"/" + row[1][0][:3] + "/" + groupCode + "/")
    
  print("++ Shape file checks commencing.")
  
  
  metaData["logID"] = logID
  metaData["jobID"] = buildID

  pandarallel.initialize(use_memory_fs = False)
  
  metaData.parallel_apply(boundaryAnalysis, axis=1)
  
  #Check if anything failed with a critical error that would prevent building..:
  if(os.path.isfile(logID)):
    with open(logID) as file:
      for line in file:
        if "CRITICAL" in line:
          matchedLine = line
          sys.exit("At least one critical error existed in the shapefile checks. Please check the log at " + logID)

  else:
    #No errors, create a blank log.
    with open(logID, 'a'):
      os.utime(logID, None)
    
  #Build succeeded.  Save the output log.
  shutil.copyfile(logID, success_log)
  
def boundaryAnalysis(bdDta):
  
  #Parallelized part:
  logID = bdDta["logID"]
  ISO = bdDta["Processed File Name"][:3]
  
  groupCode = bdDta["Boundary Level"].replace(" ","")
  buildID = bdDta["jobID"]
  
  #Skip countries that have already finished:
  if(os.path.isfile("./releaseCandidateInit/" + buildID + "/" + ISO + "/" + groupCode + "/" + ISO + "_" + groupCode + "_fixedInternalTopology.shp")):
    print("Boundary already processed, skipping: " + ISO + groupCode)
    return("Already done!")
  
  print(ISO)
  print(groupCode)
     
  boundaryPath = "./releaseCandidateInit/" + buildID + "/" + ISO + "/" + groupCode + "/"
  zipPath = "./releaseCandidateRaw/" + buildID + "/" + groupCode + "/" + ISO + "_" + groupCode + ".zip"
  
  #Unzip the data into the appropriate folder.
  try:
    with zipfile.ZipFile(zipPath) as zipObj:
      zipObj.extractall(boundaryPath)
  except:
      print("CRITICAL ERROR: Zipfile " + boundaryPath + " failed to extract.")
      buildLogger(logID, "CRITICAL ERROR: Zipfile " + boundaryPath + " failed to extract.")
      return("Failed")

  #Open the shapefile
  try:
    shpPath = "./releaseCandidateInit/" + buildID + "/" + ISO + "/" + groupCode + "/" + ISO + "_" + groupCode + ".shp"
    shpFile = fiona.open(shpPath)
  except:
    print("CRITICAL ERROR: Shapefile " + shpPath + " failed to open.")
    buildLogger(logID, "CRITICAL ERROR: Zipfile " + boundaryPath + " failed to extract.")
    return("Failed")
  
  if(not shpFile.crs['init'] == "epsg:4326"):
    buildLogger(logID, "CRITICAL ERROR: Shapefile " + shpPath + " has an incorrect projection.")
    return("Failed")

  xmin = shpFile.bounds[0]
  ymin = shpFile.bounds[1]
  xmax = shpFile.bounds[2]
  ymax = shpFile.bounds[3]
  tol = 1e-12
  valid = ((xmin >= -180-tol) and (xmax <= 180+tol) and (ymin >= -90-tol) and (ymax <= 90+tol))
  if not valid:
    buildLogger(logID, "CRITICAL ERROR: Bounds appear to be in another castle for shape:" + shpPath)
    return("Failed")

  
  #Topology checks  
  valid = True
  error = None
  
  fixed = []
  for feature in shpFile:
    raw_shape = shapely.geometry.shape(feature['geometry'])
    valid = raw_shape.is_valid
    if valid:
      fixed.append(feature)
    if not valid:
      fixed_shape = raw_shape.buffer(0)
      fix_valid = fixed_shape.is_valid
      if fix_valid and error is None:
        buildLogger(logID, "INFO: The shapefile " + shpPath + " has a minor topology error, which was corrected with a shapely buffer = 0.")
        feature["geometry"] = shapely.geometry.mapping(fixed_shape)
        fixed.append(feature)
      elif not fix_valid:
        if error is not None:
          buildLogger(logID, "CRITICAL ERROR: An error in the geometry of the file " + shpPath + " exists that we could not automatically fix.")
          return("Failed")
        else:
          buildLogger(logID, "CRITICAL ERROR: A really bad error in the geometry of the file" + shpPath + "exists that we could not automatically fix.")
          return("Failed")
#  
  #Attribute schema checks and fixes
  schema = shpFile.schema.copy()
  
  #First, identify which of the existing columns represent:
  validNameColumns = ['Name', 'name', 'NAME']
  validISOcolumns = ['ISO', 'ISO_code', 'ISO_Code', 'iso']
  dictName = None
  dictISO = None
  #shapeName
  #shapeISO
  #Both are optional columns, so may not exist.
  for attribute in list(schema['properties'].items()):
    if(attribute[0] in validNameColumns):
      dictName = attribute[0]
    if(attribute[0] in validISOcolumns):
      dictISO = attribute[0]
      
  if(dictName == None):
    buildLogger(logID, "INFO: No name information was found in a validly named column for: " + shpPath)
    schema["properties"]["shapeName"] = 'str:254'
  else:
    #Rename our name field to the schema field.
    schema["properties"] = OrderedDict([('shapeName', v) if k==dictName else (k,v) for k,v in schema["properties"].items()])
    
    
  if(dictISO == None):
    buildLogger(logID, "INFO: No ISO information was found in a validly named column for: " + shpPath)
    schema["properties"]["shapeISO"] = 'str:10'
  else:
    schema["properties"] = OrderedDict([('shapeISO', v) if k==dictISO else (k,v) for k,v in schema["properties"].items()])
  
  #remove invalid elements
  for attribute in list (schema['properties'].items()):
    if(attribute[0] not in ["shapeISO", "shapeName"]):
      schema['properties'].pop(attribute[0])
  
  #Add additional schema elements (test)
  schema["properties"]["shapeID"] = 'str:10'
  schema["properties"]["shapeGroup"] = 'str:50'
  schema["properties"]["shapeType"] = 'str:10'
  
  #Repeat for ordered dicts representing each feature.
  year = bdDta["Year"]
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
    
    elem["properties"]["shapeID"] = (ISO + "-" + groupCode + "-" + buildID.split('_', 1)[1] + '-B' + str(featureID))
    elem["properties"]["shapeGroup"] = ISO
    elem["properties"]["shapeType"] = groupCode
  
  #Update the original file with a corrected version:
  corrected_shp = "./releaseCandidateInit/" + buildID + "/" + ISO + "/" + groupCode + "/" + ISO + "_" + groupCode + "_fixedInternalTopology.shp"
  with fiona.open(corrected_shp, 'w', 'ESRI Shapefile', schema, shpFile.crs) as output:
    for elem in fixed:
      output.write(elem)
  
  print("Job Finished: " + ISO + "-" + groupCode)
  
if __name__ == "__main__": 
  import buildMain
  importlib.reload(buildMain)
  buildMain.geoBoundaries_build("gbReleaseCandidate_2_0_0_0")
  
import pandas as pd
import os
import shutil
import importlib
from pandarallel import pandarallel
import zipfile
import fiona
import fiona.crs
import json
import shapely.wkt
import shapely.geometry as geom
from shapely.geometry import shape

def buildFiles(buildID, minor):
  if(minor == True):
    version = buildID.split('_', 1)[1]
    buildID = buildID[:-1] + "0"

    
  metaData = pd.read_csv("./releaseCandidateInit/" + buildID + "/" + buildID + ".csv")
  base_path = "./release/"
  release_base = "./release/geoBoundaries-" + version + "/"
  
  return 0
  
  
  #Create root, country and hierarchy folders if they do not exist:
  if(not os.path.isdir("./release/geoBoundaries-" + version + "/")):
    os.mkdir("./release/geoBoundaries-" + version + "/")
  
  for i, row in metaData.iterrows():
    if(not os.path.isdir("./release/geoBoundaries-" + version + "/" + row["boundaryISO"])):
      os.mkdir("./release/geoBoundaries-" + version + "/" + row["boundaryISO"])
        
    if(not os.path.isdir("./release/geoBoundaries-" + version + "/" + row["boundaryISO"] + "/" + row["boundaryType"])):
      os.mkdir("./release/geoBoundaries-" + version + "/" + row["boundaryISO"] + "/" + row["boundaryType"])
  
  #Copy the final metaData file over to the release structure.
  shutil.copyfile("./releaseCandidateInit/" + buildID + "/" + buildID + ".csv", 
         "./release/geoBoundaries-" + version + "/geoBoundaries-" + version + ".csv")
  
  
  #Create CITATION_AND_USE.txt
  citeUsePath = "./tmp/CITATION-AND-USE-geoBoundaries-" + version + ".txt"
  citUse = open(citeUsePath, "w")
  citUse.write("====================================================\n")
  citUse.write("Citation of the geoBoundaries Data Product\n")
  citUse.write("====================================================\n")
  citUse.write("geoBoundaries Version " + version + "\n")
  citUse.write("www.geoboundaries.org \n")
  citUse.write("geolab.wm.edu \n")
  citUse.write("The GeoBoundaries database is made available in a \n")
  citUse.write("variety of software formats to support GIS software \n")
  citUse.write("programs.  Contrasting to other administrative \n")
  citUse.write("boundary datasets, geoBoundaries is an open product: \n")
  citUse.write("all boundaries are open and redistributable, and are \n")
  citUse.write("released alongside extensive metadata and license \n")
  citUse.write("information to help inform end users. \n")
  citUse.write("We update GeoBoundaries on a yearly cycle, \n")
  citUse.write("with new versions in August of each calendar \n")
  citUse.write("year; old versions remain accessible through this website. \n")
  citUse.write("information on the authors (us), this website, \n")
  citUse.write("and the version of GeoBoundaries used. \n")
  citUse.write("Example citations for the current version of GeoBoundaries are:  \n")
  citUse.write(" \n")
  citUse.write("+++++ Short Form Citation +++++\n")
  citUse.write("Runfola, D. et al. 2020. GeoBoundaries Database of Global Administrative\n")
  citUse.write("Boundaries version " + version + ". http://www.geoboundaries.org\n")
  citUse.write(" \n")
  citUse.write("+++++ Full Citation +++++++++++\n")
  citUse.write("Runfola, D., Anderson, A., Crittenden, M., Dowker, E., Fuhrig, S.,\n")
  citUse.write("Grimsley, G., Layko, R., Melville, G., Mulder, M., Oberman, R.,\n")
  citUse.write("Panganiban, J., Peck, A., Seitz, L., Shea, S., Slevin, H., Youngerman, R.\n")
  citUse.write("and Hobbs, L. 2020. GeoBoundaries Database of Global Administrative Boundaries\n")
  citUse.write("version " + version + ". http://www.geoboundaries.org.\n")
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
  citUse.write("https://github.com/wmgeolab/geoBoundaries_build\n")
  citUse.write(" \n")
  citUse.write("+++++ Policy on Contested Boundaries +++++\n")
  citUse.write("All decisions on what data to include into this database \n")
  citUse.write("are made on the basis of the best available data - i.e.,\n")
  citUse.write("if there are two competing shapefiles representing administrative\n")
  citUse.write("zones for a single country, we will take the one\n")
  citUse.write("with the most geographic precision.  All representations\n")
  citUse.write("of zones are up to the data source, and do not represent the\n")
  citUse.write("views or opinions of the geoBoundaries team.\n")
  citUse.write("Further, geoBoundaries does not ensure cross-country topology,\n")
  citUse.write("so in the case of contested boundaries, it is possible for two\n")
  citUse.write("shapefiles to overlap with one another.\n")
  citUse.write(" \n")
  citUse.write("Thank you for citing your use of geoBoundaries and reporting any issues you find -\n")
  citUse.write("as a non-profit academic project, your citations are what keeps geoBoundaries alive.")
  citUse.write("Dan Runfola (dan@danrunfola.com)")
  citUse.close()
  
  pandarallel.initialize(use_memory_fs = False)#, nb_workers = 1 )
  
  metaData["release_base"] = release_base
  metaData["version"] = version
  metaData["buildID"] = buildID
  
  metaData.parallel_apply(pBuild,axis=1)
  print("++ ISO paths and ADM level zip files have been created.")
  
  #Create the "all" ISO zips
  allISOs = os.listdir(release_base)
  
  pdaISOs = pd.DataFrame(allISOs)
  
  pdaISOs["release_base"] = release_base
  pdaISOs["version"] = version
  pdaISOs["buildID"] = buildID
    
  pdaISOs.parallel_apply(allISOzip, axis=1)
  print("++ ISO level 'all' zip files have been created (with all ADMs).")
  
  if(os.path.isfile("./release/geoBoundaries-" + version + "/geoBoundaries-" + version + ".zip")):
    #print("Final rollup zip is complete for " + iso[0] + ". Skipping.")
    pass
  
  else:
    #Final mega-zip
    zipdir("./release/geoBoundaries-" + version +"/",
          "./release/geoBoundaries-" + version + "/geoBoundaries-" + version + ".zip",
          includeDirInZip=False,
          citeUsePath = citeUsePath)
  
def allISOzip(iso):
  #check if this ISO is already done or not
  buildID = iso["buildID"]
  release_base = iso["release_base"]
  version = iso["version"]
  citeUsePath = "./tmp/CITATION-AND-USE-geoBoundaries-" + version + ".txt"
  isoZipPath = "./release/geoBoundaries-" + version + "/" + iso[0] + "/geoBoundaries-" + version + "-" + iso[0] + ".zip"
  
  if(os.path.isfile(isoZipPath)):
    #print("Final rollup zip is complete for " + iso[0] + ". Skipping.")
    pass
  
  else:
    dir_name = "./release/geoBoundaries-" + version + "/" + iso[0] 
    if(os.path.isfile(dir_name)):
      #print("Metadata CSV and similar files are not zipped into ADM top-level zips; skipping.")
      pass
    else:
      zipdir(dir_name, isoZipPath, citeUsePath = citeUsePath)

    
def zipdir(dirPath=None, zipFilePath=None, includeDirInZip=False, citeUsePath=False):
  if not zipFilePath:
    zipFilePath = dirPath + ".zip"
  if not os.path.isdir(dirPath):
    raise OSError("dirPath argument must point to a directory. "
            "'%s' does not." % dirPath)
  parentDir, dirToZip = os.path.split(dirPath)
    
  def trimPath(path):
    archivePath = path.replace(parentDir, "", 1)
    if parentDir:
      archivePath = archivePath.replace(os.path.sep, "", 1)
    if not includeDirInZip:
      archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
    return os.path.normcase(archivePath)

  outFile = zipfile.ZipFile(zipFilePath, "w",compression=zipfile.ZIP_DEFLATED)
  for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
    for fileName in fileNames:
      if(not fileName == zipFilePath.split("/")[-1]):
        filePath = os.path.join(archiveDirPath, fileName)
        outFile.write(filePath, trimPath(filePath))
  
  outFile.write(citeUsePath, os.path.basename(citeUsePath))
  outFile.close()
    
def pBuild(row):  
  #identify root directory
  buildID = row["buildID"]
  release_base = row["release_base"]
  version = row["version"]
  citeUsePath = "./tmp/CITATION-AND-USE-geoBoundaries-" + version + ".txt"
  
  rowDir = release_base + row["boundaryISO"] + "/" + row["boundaryType"] + "/"
  sourceDir = "./releaseCandidateInit/" + buildID + "/" + row["boundaryISO"] + "/" + row["boundaryType"] + "/"
  allZipPath = rowDir + "geoBoundaries-" + version + "-" + row["boundaryISO"] + "-" + row["boundaryType"] + "-all.zip"
  
  #Check if this row has already been completed.
  if(os.path.isfile(allZipPath)):
    #print("++ All final files have been built for file " + allZipPath + ".  Skipping.")
    return(0)
  
  
  #Create a geojson
  shp = sourceDir + row["boundaryISO"] + "_" + row["boundaryType"] + "_fixedInternalTopology.shp"
  
  srcShp = fiona.open(shp, 'r')
  geojson = rowDir + "geoBoundaries-" + version + "-" + row["boundaryISO"] + "-" + row["boundaryType"] + ".geojson"
  
  #For uniformity, we'll store all our geoJSONs as multipolygons,
  #even though it's unnecessary for many.
  srcShp.schema["geometry"] = "MultiPolygon"

  with fiona.open(geojson, 'w', driver="GeoJSON", 
                  schema=srcShp.schema,
                 encoding='utf-8',
                 crs=fiona.crs.from_epsg(4326)) as write_geojson:

    for feature in srcShp:
      if(feature["geometry"]["type"] == "MultiPolygon"):
        write_geojson.write(feature)
      else:
        multiFeature = feature
        multiFeature['geometry'] = geom.mapping(geom.MultiPolygon([shape(feature["geometry"])]))
        write_geojson.write(multiFeature)
      
  #Create a json and textfile of metadata
  json_txt = row.drop(['release_base', 'version', 'buildID'])
  jsonOut = rowDir + "geoBoundaries-" + version + "-" + row["boundaryISO"] + "-" + row["boundaryType"] + "-metaData.json"
  json_txt.to_json(jsonOut)
  
  csvOutpath = rowDir + "geoBoundaries-" + version + "-" + row["boundaryISO"] + "-" + row["boundaryType"] + "-metaData.txt"
  json_txt.to_csv(csvOutpath, index=True, header=False, sep=' ')
  
  #Create shapefile zip
  files_to_zip = [sourceDir + row["boundaryISO"] + "_" + row["boundaryType"] + "_fixedInternalTopology.shp",
                  sourceDir + row["boundaryISO"] + "_" + row["boundaryType"] + "_fixedInternalTopology.cpg",
                  sourceDir + row["boundaryISO"] + "_" + row["boundaryType"] + "_fixedInternalTopology.dbf",
                  sourceDir + row["boundaryISO"] + "_" + row["boundaryType"] + "_fixedInternalTopology.prj",
                  sourceDir + row["boundaryISO"] + "_" + row["boundaryType"] + "_fixedInternalTopology.shx"]
    
  #Rename each file to the final format
  fNames = []
  for f in files_to_zip:
    fName = (sourceDir + "geoBoundaries-" + version + "-" +
                     row["boundaryISO"] + "-" + row["boundaryType"] 
                     + "." + f.split(".")[2])
    fNames.append(fName)
    shutil.copyfile(f,fName)
  
  fNames.append(str("./tmp/CITATION-AND-USE-geoBoundaries-" + version + ".txt"))
  fNames.append(csvOutpath)
  
  #Create the shapefile zip, including a copy of the citation and use.
  zipShpFl = rowDir + "geoBoundaries-" + version + "-" + row["boundaryISO"] + "-" + row["boundaryType"] + "-shp.zip"
  with zipfile.ZipFile(zipShpFl, 'w') as shpZip:
    for f in fNames:
      shpZip.write(f, compress_type=zipfile.ZIP_DEFLATED)
    for zip_info in shpZip.infolist():
        if zip_info.filename[-1] == '/':
            continue
        zip_info.filename = os.path.basename(zip_info.filename)
  
  print("Zipping everything into a top-level zip.  This may take a while.")
  #Create the "all" zip
  allFilesToZip = [zipShpFl, geojson, jsonOut, csvOutpath, citeUsePath]
  
  with zipfile.ZipFile(allZipPath, 'w') as allZip:
    for f in allFilesToZip:
      allZip.write(f, compress_type=zipfile.ZIP_DEFLATED)
    for zip_info in allZip.infolist():
        if zip_info.filename[-1] == '/':
            continue
        zip_info.filename = os.path.basename(zip_info.filename)
 
  
  print("++ Final overall release zip created. Dataset production complete.")
  
  

  
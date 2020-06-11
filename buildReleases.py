#Script to build new major / minor release of geoBoundaries
import pandas as pd
from os.path import expanduser
import glob
import os
import fiona
import fiona.crs
import shapely.geometry as geom
from shapely.geometry import shape, mapping, MultiPolygon
from joblib import Parallel, delayed, parallel_backend
import shutil
import subprocess
import zipfile
import json
import sys
import topojson
from matplotlib import pyplot as plt
from shapely.geometry import asShape
from itertools import chain
import pickle
import geojson
from osgeo import ogr
from geojson import Feature, Point, FeatureCollection, Polygon
home = expanduser("~")

#Specify Version this release will be:
geoBoundariesVersion = "development"

#Can use this script to build core or ancillary products.
#Accepts a list
#HPSCU - High Precision Single Country Unstadardized (HPSCU)
#CGAZ - Contigious Global Administrative Zones
#GSB does both  Simplified Single Country Globally Standardized (SSCGS )
#and High Precision Single Country Globally Standardized (HPSCGS)
#SSCU - Simplified Single Country Unstandardized 
builds = ["HPSCU", "SSCU", "GSB", "CGAZ"]


if (not os.path.isdir(home + '/gbRelease/tmp/')):
            os.mkdir(home + '/gbRelease/tmp/')
          
#Create CITATION_AND_USE.txt
citeUsePath = (home + "/gbRelease/tmp/CITATION-AND-USE-geoBoundaries-" + geoBoundariesVersion + ".txt")
citUse = open(citeUsePath, "w")
citUse.write("====================================================\n")
citUse.write("Citation of the geoBoundaries Data Product\n")
citUse.write("====================================================\n")
citUse.write("geoBoundaries Version " + geoBoundariesVersion.replace("_",".") + "\n")
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
citUse.write("Please include the term 'geoBoundaries v. "+ geoBoundariesVersion.replace("_",".") +  "' with a link to")
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

#Helper functions for conversion from topojson to geojson
#Hacked together from https://github.com/perrygeo/topo2geojson
def topoCoordinates(arcs, topology_arcs, scale=None, translate=None):
    """Return GeoJSON coordinates for the sequence(s) of arcs.
    
    The arcs parameter may be a sequence of ints, each the index of a
    coordinate sequence within topology_arcs
    within the entire topology -- describing a line string, a sequence of 
    such sequences -- describing a polygon, or a sequence of polygon arcs.
    
    The topology_arcs parameter is a list of the shared, absolute or
    delta-encoded arcs in the dataset.

    The scale and translate parameters are used to convert from delta-encoded
    to absolute coordinates. They are 2-tuples and are usually provided by
    a TopoJSON dataset. 
    """
    if isinstance(arcs[0], int):
        coords = [
            list(
                rel2abs(
                    topology_arcs[arc if arc >= 0 else ~arc],
                    scale, 
                    translate )
                 )[::arc >= 0 or -1][i > 0:] \
            for i, arc in enumerate(arcs) ]
        return list(chain.from_iterable(coords))
    elif isinstance(arcs[0], (list, tuple)):
        return list(
            topoCoordinates(arc, topology_arcs, scale, translate) for arc in arcs)
    else:
        raise ValueError("Invalid input %s", arcs)
        
def rel2abs(arc, scale=None, translate=None):
    """Yields absolute coordinate tuples from a delta-encoded arc.

    If either the scale or translate parameter evaluate to False, yield the
    arc coordinates with no transformation."""
    if scale and translate:
        a, b = 0, 0
        for ax, bx in arc:
            a += ax
            b += bx
            yield scale[0]*a + translate[0], scale[1]*b + translate[1]
    else:
        for x, y in arc:
            yield x, y
            
def topoGeometry(obj, topology_arcs, scale=None, translate=None):
    """Converts a topology object to a geometry object.
    
    The topology object is a dict with 'type' and 'arcs' items, such as
    {'type': "LineString", 'arcs': [0, 1, 2]}.

    See the coordinates() function for a description of the other three
    parameters.
    """
    return {
        "type": obj['type'], 
        "coordinates": topoCoordinates(
            obj['arcs'], topology_arcs, scale, translate )}
  
def topo2geojson(topojson_path, geojson_path):
  with open(topojson_path, 'r') as fh:
    f = fh.read()
    topology = json.loads(f)

  # file can be renamed, the first 'object' is more reliable
  layername = 'data' 

  features = topology['objects'][layername]['geometries']

  with open(geojson_path, 'w') as dest:
      fc = {'type': "FeatureCollection", 'features': []}

      for id, tf in enumerate(features):
          f = {'id': id, 'type': "Feature"}
          f['properties'] = tf['properties'].copy()

          geommap = topoGeometry(tf, topology['arcs'])
          geom = asShape(geommap).buffer(0)
          assert geom.is_valid
          f['geometry'] = geom.__geo_interface__

          fc['features'].append(f) 

      dest.write(json.dumps(fc))
  return fc


###################################
###################################
###################################
###Main Class

class releaseCandidateBoundary:
  def __init__(self,gbMeta, geoBoundariesVersion, home):
    self.iso = str(gbMeta["boundaryISO"])
    self.adm = str(gbMeta["boundaryType"])
    self.home = str(home)
    self.version = str(geoBoundariesVersion)
    self.allMeta = gbMeta
    self.BuildComplete_HPSCU = False
    self.BuildComplete_SSCU = False
    self.ID = str(gbMeta["boundaryID"])
  
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
  
  def geoMeta(self, release):
    prefix = "geoBoundaries" + release + "-"
    if(release == "HPSCU"):
      prefix = "geoBoundaries-"
    
    metaInfo = self.allMeta
    jsonOut = (self.home + "/gbRelease/gbReleaseData/" + release + "/" + self.iso + "/" + self.adm + "/" +
               prefix + self.version + "-" + self.iso + "-" + self.adm + "-metaData.json")
    metaInfo.to_json(jsonOut)
  
    csvOutpath = (self.home + "/gbRelease/gbReleaseData/" + release + "/" + self.iso + "/" + self.adm + "/" +
               prefix + self.version + "-" + self.iso + "-" + self.adm + "-metaData.txt")
    metaInfo.to_csv(csvOutpath, index=True, header=False, sep=' ')
    
  def geoViz(self, inputFile, outputFile, release):
    outputTitle = "High Precision Unstd"
    if(release == "SSCU"):
      inputTitle = "High Precision Unstd."
      outputTitle = "Simplified Unstd."
    if(release == "HPSCGS"):
      inputTitle = "High Precision Unstd."
      outputTitle = "High Precision Std."
    if(release == "SSCGS"):
      inputTitle = "Simplified Unstd"
      outputTitle = "Simplified Std"
    
    prefix = "geoBoundariesPreview" + release + "-"
    if(release == "HPSCU"):
      prefix = "geoBoundariesPreview-"
    
    with open(inputFile, 'r') as j:
      inputGeom = json.load(j)

    fig = plt.clf()
    fig = plt.figure(1, figsize=(10,5), dpi=300)
    axs = fig.add_subplot(121)

    inputSize = round(sys.getsizeof(str(inputGeom)) / 1000000,3)

    axs.set_title("geoBoundaries " + self.version.replace("_",".") + 
                  "\n" + self.iso + " " + self.adm + " " + 
                  '\n' + inputTitle + " " + str(inputSize) + "MB")

    #Accounting for Multipolygon Boundaries
    for boundary in inputGeom["features"]:
      if(boundary["geometry"]['type'] == "MultiPolygon"):
        polys = list(shape(boundary["geometry"]))
        for poly in polys:
          xs, ys = poly.exterior.xy    
          axs.fill(xs, ys, alpha=0.5, fc='red', ec='black')
      else:
        xs, ys = shape(boundary["geometry"]).exterior.xy    
        axs.fill(xs, ys, alpha=0.5, fc='red', ec='black')

    axsb = fig.add_subplot(122)
    
    with open(outputFile, 'r') as i:
      outputGeom = json.load(i)
      
    outputSize = round(sys.getsizeof(str(outputGeom)) / 1000000,3)

    axsb.set_title("geoBoundaries " + self.version.replace("_",".") + 
                  "\n" + self.iso + " " + self.adm + " " + 
                  '\n' + outputTitle + " " + str(outputSize) + "MB")

    #Accounting for Multipolygon Boundaries
    for boundary in outputGeom["features"]:
      if(boundary["geometry"]['type'] == "MultiPolygon"):
        polys = list(shape(boundary["geometry"]))
        for poly in polys:
          xs, ys = poly.exterior.xy    
          axsb.fill(xs, ys, alpha=0.5, fc='red', ec='black')
      else:
        xs, ys = shape(boundary["geometry"]).exterior.xy    
        axsb.fill(xs, ys, alpha=0.5, fc='red', ec='black')

    outgeoPNG = (self.home + "/gbRelease/gbReleaseData/" + release + "/" + self.iso + "/" + self.adm + "/" +
             prefix + self.version + "-" + self.iso + "-" + self.adm + ".png")
    fig.savefig(outgeoPNG, bbox_inches='tight')   
      
  def buildFullZip(self, release):
    prefix = "geoBoundaries" + release + "-"
    if(release == "HPSCU"):
      prefix = "geoBoundaries-"
    
    dirToZip = (self.home + "/gbRelease/gbReleaseData/" + release + "/" + self.iso + "/" + self.adm + "/")
    zipTarget = (self.home + "/gbRelease/tmp/" + prefix + self.version + "-" + self.iso + "-" + self.adm + "-all")
    shutil.make_archive(base_name = zipTarget,
                          format="zip",
                          root_dir = dirToZip)
    
    #Append citation and use doc
    citePath = (self.home + "/gbRelease/tmp/CITATION-AND-USE-geoBoundaries-" + self.version + ".txt")
    zipAppend = zipfile.ZipFile(zipTarget + ".zip", 'a')
    zipAppend.write(citePath, os.path.basename(citePath))
    zipAppend.close()
      
    shutil.move(zipTarget + ".zip", 
                 dirToZip)
  
  def HPSCU(self):
    self.BuildComplete_HPSCU = False
    jsonOUT = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/" +
               "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + ".geojson")
    topoOUT = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/" +
               "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + ".topojson") 
    shpOUT = (self.home + "/gbRelease/tmp/hpscuTemp" + self.iso + self.adm + "/")
    finalZipPath = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/" + "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + "-all.zip")
    
    if(os.path.isfile(finalZipPath)):
      buildTimeStamp = os.path.getmtime(finalZipPath) 
      zipDownloadTimeStamp = os.path.getmtime(self.home + "/gbRelease/gbRawData/currentZips/" + self.iso + "_" + self.adm + ".zip")
      if((buildTimeStamp - zipDownloadTimeStamp) > 0):
        self.BuildComplete_HPSCU = True
        return 0
      else:
        self.geoLog("INFO", (self.iso + "|" + self.adm + " HPSCU build starting."))
        shutil.rmtree((self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/"))
        os.mkdir((self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/"))
    
    outDirectory = self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/"
    inShape = (self.home + "/gbRelease/gbRawData/current/" + self.iso + "/" + self.adm + 
               "/shapeFixes/" + self.iso + "_" + self.adm + "_" +
               "fixedInternalTopology.shp")
    try:
      shpFile = fiona.open(inShape)
    except:
      self.geoLog("CRITICAL", (self.iso + "|" + self.adm + "Shape failed to open."))
    
    #For uniformity, we'll store all our geoJSONs as multipolygons,
    #even though it's unnecessary for many.  
    shpFile.schema["geometry"] = "MultiPolygon"
    fid = 0
    kwargs = {"COORDINATE_PRECISION":7}
    with fiona.open(jsonOUT, 'w', driver="GeoJSON", 
                schema=shpFile.schema,
                encoding='utf-8',
                crs=fiona.crs.from_epsg(4326), **kwargs) as write_geojson:

      for feature in shpFile:
        fid = fid + 1
        feature["properties"]["shapeID"] = (self.iso + "-" + self.adm + "-" + self.version + "-B" + str(fid)) 
        if(feature["geometry"]["type"] == "MultiPolygon"):
          write_geojson.write(feature)
        else:
          multiFeature = feature
          multiFeature['geometry'] = geom.mapping(geom.MultiPolygon([shape(feature["geometry"])]))
          write_geojson.write(multiFeature)
    
    self.geoMeta("HPSCU")
    
    #Create a temp folder to hold the shapefile
    if(os.path.isdir(shpOUT)):
      shutil.rmtree(shpOUT) 
      os.mkdir(shpOUT)
    else:
      os.mkdir(shpOUT)
    
    try:
      mapShaperWriteShape = (self.home + "/node_modules/mapshaper/bin/mapshaper-xl " + inShape +
                             " -o format=shapefile " + shpOUT +
                             " -o format=topojson " + topoOUT) 
      os.system(mapShaperWriteShape)
    except:
      self.geoLog("CRITICAL", (self.iso + "|" + self.adm + " Shapefile write failed."))
    
    try:
      #Zip the shapefile and output it to the final folder
      shutil.make_archive(
        base_name = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/" +
               "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + "-shp"),
        format="zip",
        root_dir = shpOUT)
      shutil.rmtree(shpOUT) 
    except:
      self.geoLog("CRITICAL", (self.iso + "|" + self.adm + " Shapefile zipfile build failed."))
    
                    
    #Matplotlib Viz - one off for HPSCU
    with open(jsonOUT, 'r') as j:
      geoBoundary = json.load(j)
    fig = plt.clf()
    fig = plt.figure(1, figsize=(10,5), dpi=300)
    axs = fig.add_subplot(111)

    mbpost = round(sys.getsizeof(str(geoBoundary)) / 1000000,3)

    axs.set_title("geoBoundaries " + self.version.replace("_",".") + "\n" + self.iso + " " + self.adm + " " + 'High Precision Unstandardized ' + str(mbpost) + "MB")

    #Accounting for Multipolygon Boundaries
    for boundary in geoBoundary["features"]:
      if(boundary["geometry"]['type'] == "MultiPolygon"):
        polys = list(shape(boundary["geometry"]))
        for poly in polys:
          xs, ys = poly.exterior.xy    
          axs.fill(xs, ys, alpha=0.5, fc='red', ec='black')
      else:
        xs, ys = shape(boundary["geometry"]).exterior.xy    
        axs.fill(xs, ys, alpha=0.5, fc='red', ec='black')

    outgeoPNG = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/"
             "geoBoundariesPreview-" + self.version + "-" + self.iso + "-" + self.adm + ".png")
    fig.savefig(outgeoPNG, bbox_inches='tight')
    
    self.buildFullZip("HPSCU")
    
    self.BuildComplete_HPSCU = True
#################################
#################################
##### SSCU Build (Simplified Unstandardized)
#################################
#################################

  def SSCU(self):
    #Simplified single country release
    self.BuildComplete_SSCU = False
    finalZipPath = (self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/" + "geoBoundariesSSCU-" + self.version + "-" + self.iso + "-" + self.adm + "-all.zip")
    toposimp = "25%"
  
    if(os.path.isfile(finalZipPath)):
      buildTimeStamp = os.path.getmtime(finalZipPath) 
      zipDownloadTimeStamp = os.path.getmtime(self.home + "/gbRelease/gbRawData/currentZips/" + self.iso + "_" + self.adm + ".zip")
      if(buildTimeStamp - zipDownloadTimeStamp > 0):
        self.BuildComplete_SSCU = True
        return 0
      else:
        self.geoLog("INFO", (self.iso + "|" + self.adm + " SSCU build starting."))
        shutil.rmtree((self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/"))
        os.mkdir((self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/"))
    
    sB = self.allMeta.copy()
    sB["simplificationRate"] = toposimp
    outDirectory = self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/"
    inShape = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + 
               self.adm + "/" + "geoBoundaries-" + self.version + "-" + 
               self.iso + "-" + self.adm + ".geojson")
    outJSON = outDirectory + "geoBoundariesSSCU-" + self.version + "-" + self.iso + "-" + self.adm + ".geojson"
    outTOPO = outDirectory + "geoBoundariesSSCU-" + self.version + "-" + self.iso + "-" + self.adm + ".topojson"
    outSHP = (self.home + "/gbRelease/tmp/simp_" + self.iso + self.adm + "/" +
               "geoBoundariesSSCU-" + self.version + "-" + self.iso + "-" + self.adm + ".shp")

    if(os.path.isdir((self.home + "/gbRelease/tmp/simp_" + self.iso + self.adm + "/"))):
      shutil.rmtree((self.home + "/gbRelease/tmp/simp_" + self.iso + self.adm + "/")) 
      os.mkdir((self.home + "/gbRelease/tmp/simp_" + self.iso + self.adm + "/"))
    else:
      os.mkdir((self.home + "/gbRelease/tmp/simp_" + self.iso + self.adm + "/"))
      
    try:
      mapShaperSimplify = (self.home + "/node_modules/mapshaper/bin/mapshaper-xl " + inShape +
                             " -simplify keep-shapes percentage=" + toposimp + 
                             " -o format=geojson " + outJSON + 
                             " -o format=topojson " + outTOPO +
                             " -o format=shapefile " + outSHP) 
      os.system(mapShaperSimplify)
    except:
      self.geoLog("CRITICAL", (self.iso + "|" + self.adm + " Simplification Failed."))
    
    try:
      shutil.make_archive(
        base_name = (self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/" +
                     "geoBoundariesSSCU" + self.version + "-" + self.iso + "-" + self.adm + "-shp"),
        format="zip",
        root_dir = (self.home + "/gbRelease/tmp/simp_" + self.iso + self.adm + "/"))
    except:
      self.geoLog("CRITICAL", (self.iso + "|" + self.adm + " Simplification SHP zip build failed."))
    
      
    self.geoMeta("SSCU")
    
    self.geoViz(inShape, outJSON, "SSCU")
    
    self.buildFullZip("SSCU")

    self.BuildComplete_SSCU = True
    
#################################
#################################
##### Globally Standardized Builds
##### Includes 
##### High Precision Single Country Globally Standardized (HPSCGS)
##### Simplified Single Country Globally Standardized (SSCGS )
#################################
################################# 
  def GSB(self):
    count = 0
    notIncludedGSB = ["NIU", "PSE"]
    if(not self.iso in notIncludedGSB):
    
      for buildType in ["HPSCGS", "SSCGS"]:
        finalZipPath = (self.home + "/gbRelease/gbReleaseData/" + buildType + "/" + self.iso + "/" + self.adm + "/geoBoundaries" + buildType + "-" + self.version + "-" + self.iso + "-" + self.adm + "-all.zip")
        outDirectory = self.home + "/gbRelease/gbReleaseData/"+ buildType + "/" + self.iso + "/" + self.adm + "/"
        outJSON = outDirectory + "geoBoundaries" + buildType + "-" + self.version + "-" + self.iso + "-" + self.adm + ".geojson"
        outTOPO = outDirectory + "geoBoundaries" + buildType + "-" + self.version + "-" + self.iso + "-" + self.adm + ".topojson"
        outSHPTemp = (self.home + "/gbRelease/tmp/" + buildType + self.iso + self.adm + "/" +
                 "geoboundaries" + buildType + "-" + self.version + "-" + self.iso + "-" + self.adm + ".shp")
        outSHP = outDirectory + "geoBoundaries" + buildType + "-" + self.version + "-" + self.iso + "-" + self.adm + "-shp"
        clipPath = self.home + "/gbRelease/gbRawData/ISO_0_Standards/USDoS/" + self.iso + ".topojson"
        cleanClipPath = self.home + "/gbRelease/gbRawData/ISO_0_Standards/USDoS/" + self.iso + self.adm + "_clean.topojson"
        
        
        
        if(buildType == "HPSCGS"):
          inGeom = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + 
                 self.adm + "/" + "geoBoundaries-" + self.version + "-" + 
                 self.iso + "-" + self.adm + ".topojson") 
          inGeoJson = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + 
                 self.adm + "/" + "geoBoundaries-" + self.version + "-" + 
                 self.iso + "-" + self.adm + ".geojson") 

        if(buildType == "SSCGS"):
          inGeom = (self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + 
                 self.adm + "/" + "geoBoundariesSSCU-" + self.version + "-" + 
                 self.iso + "-" + self.adm + ".topojson") 
          inGeoJson = (self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + 
                 self.adm + "/" + "geoBoundariesSSCU-" + self.version + "-" + 
                 self.iso + "-" + self.adm + ".geojson") 

        if(not os.path.isdir((self.home + "/gbRelease/tmp/" + buildType + self.iso + self.adm + "/" ))):
           os.mkdir((self.home + "/gbRelease/tmp/" + buildType + self.iso + self.adm + "/" ))

        if not os.path.isdir((self.home + "/gbRelease/gbReleaseData/SSCGS/" + self.iso + "/" + self.adm + "/")):
          os.mkdir((self.home + "/gbRelease/gbReleaseData/SSCGS/" + self.iso + "/" + self.adm + "/"))
            
        if(os.path.isfile(finalZipPath)):
          buildTimeStamp = os.path.getmtime(finalZipPath) 
          zipDownloadTimeStamp = os.path.getmtime(self.home + "/gbRelease/gbRawData/currentZips/" + self.iso + "_" + self.adm + ".zip")
          if(buildTimeStamp - zipDownloadTimeStamp > 0):
            count = count + 1
            if(count == 2):
              self.BuildComplete_GSB = True
              return 0
            else:
              continue
          else:
            self.geoLog("INFO", (self.iso + "|" + self.adm + " " + buildType + " build started.")) 
            shutil.rmtree((self.home + "/gbRelease/gbReleaseData/" + buildType + "/" + self.iso + "/" + self.adm + "/"))
            os.mkdir((self.home + "/gbRelease/gbReleaseData/" + buildType + "/" + self.iso + "/" + self.adm + "/"))
        
        #Need to simplify ISO0 to same standard as other
        #Simplified products in simplify case.
        if(buildType == "SSCGS"):
          mapShaperClip = (self.home + "/node_modules/mapshaper/bin/mapshaper-xl" +
                                 " -i name=data " + clipPath  + 
                                 " -dissolve2 " +
                                 " -o format=topojson " + cleanClipPath)
          process = subprocess.Popen([mapShaperClip], shell=True, 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          process.wait()
          output, error = process.communicate()
        
        else:
          mapShaperClip = (self.home + "/node_modules/mapshaper/bin/mapshaper-xl" +
                                 " -i name=data " + clipPath  +  
                                 " -dissolve2 " +
                                 " -o format=topojson " + cleanClipPath)
          process = subprocess.Popen([mapShaperClip], shell=True, 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          process.wait()
          output, error = process.communicate()

                     
        mapShaperErase = (home + "/node_modules/mapshaper/bin/mapshaper-xl" +
                               " -i " + inGeom + 
                               " -clip " + cleanClipPath +
                               " -o format=geojson " + outJSON + 
                               " -o format=topojson " + outTOPO +
                               " -o format=shapefile " + outSHPTemp) 
        process = subprocess.Popen([mapShaperErase], shell=True, 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        
        
        process.wait()
        output, error = process.communicate()

        try:
          shutil.make_archive(
            base_name = (outSHP),
            format="zip",
            root_dir = (self.home + "/gbRelease/tmp/" + buildType + self.iso + self.adm + "/"))
        except:
          self.geoLog("CRITICAL", (self.iso + "|" + self.adm + " Clip SHP zip build failed."))


        self.geoMeta(buildType)

        self.geoViz(inGeoJson, outJSON, buildType)

        self.buildFullZip(buildType)
        
def buildRelease(builds, geoBoundariesVersion, metaDataRow, home):
  #Let's not talk about this.
  for releaseType in builds:
    if(releaseType != 'GSB'):
      while True:
        try:
          if (not os.path.isdir((home + '/gbRelease/gbReleaseData/' + releaseType + '/' + 
                               metaDataRow["boundaryISO"] + "/"))):
            os.mkdir((home + '/gbRelease/gbReleaseData/' + releaseType + '/' + 
                               metaDataRow["boundaryISO"] + "/"))
          if (not os.path.isdir((home + '/gbRelease/gbReleaseData/' + releaseType + '/' + 
                               metaDataRow["boundaryISO"] + "/" + metaDataRow["boundaryType"] + '/'))):
              os.mkdir((home + '/gbRelease/gbReleaseData/' + releaseType + '/' + 
                               metaDataRow["boundaryISO"] + "/" + metaDataRow["boundaryType"] + '/'))
        except:
          pass
        else:
          break
        
  #Initialize the boundary object
  boundary = releaseCandidateBoundary(metaDataRow, geoBoundariesVersion, home)

  if("HPSCU" in builds):
    try:
      boundary.HPSCU()
    except:
      boundary.geoLog("CRITICAL", (boundary.iso + "|" + boundary.adm + " - HPSCU build failed."))
  
  if((boundary.BuildComplete_HPSCU == True) and ("SSCU" in builds)):
    try:
      boundary.SSCU()
    except:
      boundary.geoLog("CRITICAL", (boundary.iso + "|" + boundary.adm + " - SSCU build failed."))
  
  elif((boundary.BuildComplete_HPSCU != True) and ("SSCU" in builds)):
    boundary.geoLog("CRITICAL", (boundary.iso + "|" + boundary.adm + " Cannot build SSCU product without HPSCU completion."))
  
  #NOTE: Both standardized products are built in GSB.
  #We do both standardized products at once for the sake of effeciency.
  if((boundary.BuildComplete_HPSCU == True) and ("GSB" in builds)):
    try:
      boundary.GSB()
    except:
      boundary.geoLog("CRITICAL", (boundary.iso + "|" + boundary.adm + " - GSB build failed."))
  
  elif((boundary.BuildComplete_HPSCU != True) and ("GSB" in builds)):
    boundary.geoLog("CRITICAL", (boundary.iso + "|" + boundary.adm + " Cannot build GSB product without HPSCU completion."))
    
    
  
allMeta = glob.glob((home + "/gbRelease/gbRawData/metadata/*"))
latestMeta = max(allMeta, key=os.path.getctime)
nightlyVersion = str(latestMeta).split("/")[-1].split(".")[0]
metaData = pd.read_csv((home + "/gbRelease/gbRawData/current/geoBoundaries-" + nightlyVersion + ".csv"))

#Wipe the old version, init dev log
if(os.path.isdir(os.path.join((home + "/gbRelease/buildLogs/" + nightlyVersion + "/")))):
  shutil.rmtree((os.path.join((home + "/gbRelease/buildLogs/" + nightlyVersion + "/"))))
  os.mkdir((home + "/gbRelease/buildLogs/" + nightlyVersion + "/"))
  
if(os.path.isdir(os.path.join(home + "/gbRelease/gbReleaseData/"))):
  shutil.rmtree(os.path.join(home + "/gbRelease/gbReleaseData/"))
  os.mkdir(os.path.join(home + "/gbRelease/gbReleaseData/"))
  


#Confirm the release we're using for the build doesn't have any
#Critical errors remaining.  If so, kill this job.
if(not os.path.isfile(os.path.join((home + "/gbRelease/buildLogs/" + 
                                    nightlyVersion + "/"), "CRITICAL.txt"))):
  #Update the version in the metadata (not a nightly)
  bndCnt = 0
  for i, row in metaData.iterrows():
    bndCnt = bndCnt + 1
    metaData.at[i,'boundaryID'] = (metaData["boundaryISO"][i] + "-" + 
                                 metaData["boundaryType"][i] + "-" 
                                 + geoBoundariesVersion + "-G" + str(bndCnt))
    metaData.at[i,'downloadURL'] = ("https://geoboundaries.org/data/geoBoundaries-" +
                                    geoBoundariesVersion + "/" + metaData["boundaryISO"][i] +
                                    "/" + metaData["boundaryType"][i] + "/geoBoundaries-" +
                                    geoBoundariesVersion + "-" + metaData["boundaryISO"][i] + 
                                    "-" + metaData["boundaryType"][i] + "-all.zip")
       
  metaData.to_csv((home + "/gbRelease/gbReleaseData/geoBoundaries-" + geoBoundariesVersion + ".csv"), index=False)

  #Create root, country and hierarchy folders if they do not exist.
  #Copy metadata into the root of each, as it is identical across
  #ancillary releases.
  if("GSB" in builds):
    builds.append("SSCGS")
    builds.append("HPSCGS")
  
  for releaseType in builds:
    if(releaseType != "GSB"):
      if(not os.path.isdir(home + "/gbRelease/gbReleaseData/" + releaseType + "/")):
        os.mkdir(home + "/gbRelease/gbReleaseData/" + releaseType + "/")
      
      shutil.copyfile((home + "/gbRelease/gbReleaseData/geoBoundaries-" + geoBoundariesVersion + ".csv"),
                        (home + "/gbRelease/gbReleaseData/" + releaseType + "/geoBoundaries-" + geoBoundariesVersion + ".csv"))
  
  #Build the globally standardized geoJSONs for any source boundary ISO0
  #We intend to standardize with.  For now, this is just US DoS, retrieved from:
  #http://geonode.state.gov/geoserver/wfs?srsName=EPSG%3A4326&typename=geonode%3AGlobal_LSIB_Polygons_Detailed&outputFormat=json&version=1.0.0&service=WFS&request=GetFeature
  #Filename local: usDoSLSIB_Mar2020.geojson
  if("CGAZ" in builds):
    isoStdDir = home + "/gbRelease/gbRawData/ISO_0_Standards/USDoS/"
    isoStdData = home + "/gbRelease/gbRawData/ISO_0_Standards/usDoSLSIB_Mar2020.geojson"
    isoJSONOUT = isoStdDir + "USDoS_ISOstd.geojson"
    if(not os.path.isdir(isoStdDir)):
      os.mkdir(isoStdDir)



    with open(isoStdData) as f:
      globalDta = json.load(f)

    isoCSV = pd.read_csv(home + "/gbRelease/gbRawData/ISO_0_Standards/ISO_3166_1_Alpha_3.csv")
    isoCSV["matchCountryCSV"] = isoCSV["Country"].str.upper().replace(" ","")
    allSourceISOs = []
    #Messy cleanup of the DoS Boundary.
    #Will eventually move this pipeline elsewhere.
    for i in range(0, len(globalDta['features'])):
      #Country name cleanup & Contested Areas
      #Goal here is to reconstruct US political worldview
      #as closely as is possible.
      #In cases where the US has no official stance,
      #We base attribution on country population (i.e,)
      #The country that is contesting that has the larger pop
      #gets the territory.
      #This is obviously not a perfect system, and discussion is welcomed.
      #Over time, we hope to add additional "World View" products.
      disp = 0
      if("(disp)" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        print("DISP")
        print(globalDta['features'][i]['properties']['COUNTRY_NA'])
        disp = 1
      #Abyei - Status unclear; US view appears to be it is a part of Sudan
      #Pending ratification of UNIFA changes?
      if("Abyei" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Sudan"
      
      #No official US stance found on Aksai Chin; India pop is estimated
      #to be slightly higher as of this writing.
      if("Aksai" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "India"
      if("CH-IN" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "India"
      if("Demchok" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "India"
      
      #No evidence of US taking a stance, going with Croatia.
      if("Dragonja" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Croatia"
      
      #China is bigger than Bhutan, no evidence of a US stance
      if("Dramana" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "China"
      
      #Adding Gaza to Israel to replicate US view
      if("Gaza" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Israel"  
      if("West Bank" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Israel"  

        
      #Brazil larger; no sign of US stance
      if("Brasilera" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Brazil"
      
      #India bigger than Nepal; no sign of US stance
      if("Kalapani" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "India"
  
      #No sign of US stance
      if("Koualou" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Burkina Faso"
      
      #No sign of US stance Japan / South Korea
      if("Liancourt" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Japan"
      
      #No Man's Land - ascribing to Israel, as US put Israel embassy here.
      #Unclear if this should count as official stance or not, open for discussion.
      if("No Man's Land" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Israel"
        print("NOMAN")
      #Chinese Island Dispute - China is occupying, US has no formal 
      if("Paracel" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "China"
      #Chinese Island Dispute - China is occupying, US has no formal 
      if("Senkakus" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "China"
      if("Spratly" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "China"
   
      #Looks like Saudi Arabia owns this now, but a bit unclear.
      if("Sanafir & Tiran" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Saudi Arabia"     
        print("SANAFIR")
      #Morocco / West Sahara
      if("Western Sahara" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Morocco"

      
      #Kashmir
      if("Siachen-Saltoro" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "India"

      if(disp == 1):
        
        print(globalDta['features'][i]['properties']['COUNTRY_NA'])
        print("DISPEND")
        
      if("(UK)" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "United Kingdom"

      if("(US)" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "United States"

      if("(Aus)" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Australia"

      if("Greenland (Den)" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Greenland"

      if("(Den)" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Denmark"

      if("(Fr)" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "France"

      if("(Ch)" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "China"

      if("(Nor)" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Norway"

      if("(NZ)" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "New Zealand"

      if("Netherlands [Caribbean]" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Netherlands"

      if("(Neth)" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Netherlands"

      if("Portugal [" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Portugal"

      if("Spain [" in globalDta['features'][i]['properties']['COUNTRY_NA']):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = "Spain"

      #Match ISO    

      country = globalDta['features'][i]['properties']['COUNTRY_NA'].upper().replace(" ","")
      easyMatches = isoCSV[isoCSV["matchCountryCSV"] == country]
      if(len(easyMatches) == 1):
        globalDta['features'][i]['properties']['COUNTRY_NA'] = easyMatches.reset_index()["Alpha-3code"][0]
        allSourceISOs.append(globalDta['features'][i]['properties']['COUNTRY_NA'])
      else:
        country = globalDta['features'][i]['properties']['COUNTRY_NA']
        globalDta['features'][i]['properties']['COUNTRY_NA'] = (country + " No ISO Match")
        #Manual adjustments:
        if(country == "Antigua & Barbuda"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "ATG"
        if(country == "Bahamas, The"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "BHS"
        if(country == "Bosnia & Herzegovina"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "BIH"
        if(country == "Congo, Dem Rep of the"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "COD"
        if(country == "Congo, Rep of the"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "COG"
        if(country == "Cabo Verde"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "CPV"
        if(country == "Cote d'Ivoire"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "CIV"
        if(country == "Central African Rep"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "CAF"
        if(country == "Czechia"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "CZE"
        if(country == "Gambia, The"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "GMB"
        if(country == "Iran"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "IRN"
        if(country == "Korea, North"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "PRK"
        if(country == "Korea, South"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "KOR"
        if(country == "Laos"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "LAO"
        if(country == "Macedonia"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "MKD"
        if(country == "Marshall Is"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "MHL"
        if(country == "Micronesia, Fed States of"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "FSM"
        if(country == "Moldova"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "MDA"
        if(country == "Sao Tome & Principe"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "STP"
        if(country == "Solomon Is"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "SLB"
        if(country == "St Kitts & Nevis"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "KNA"
        if(country == "St Lucia"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "LCA"
        if(country == "St Vincent & the Grenadines"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "VCT"
        if(country == "Syria"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "SYR"
        if(country == "Tanzania"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "TZA"
        if(country == "Vatican City"):
          globalDta['features'][i]['properties']['COUNTRY_NA'] = "VAT"
        
        allSourceISOs.append(globalDta['features'][i]['properties']['COUNTRY_NA'])
    
    
    if(not os.path.isfile(isoJSONOUT)):
      with open(isoJSONOUT, 'w') as f:
        json.dump(globalDta, f)
    print(allSourceISOs)
    #sys.exit()

    for iso in allSourceISOs:
      ##NEED TO UPDATE AND PARALLELIZE THIS
      #CURRENTLY WILL NOT AUTO-UPDATE ADM0 BOUNDARIES
      #IF CHANGES ARE MADE OR NEW PRODUCTS BUILT
      if(not ('(disp)' in iso)):
        outTOPO = isoStdDir + iso + ".topojson"
        if(not os.path.isfile(outTOPO)):

          mapShaperISO = (home + "/node_modules/mapshaper/bin/mapshaper-xl " + isoJSONOUT +
                             " -filter '" + '"' + iso + '"' +
                             ".indexOf(COUNTRY_NA) > -1' -o " + outTOPO)
          os.system(mapShaperISO)
       
  
  #Launch the ships:
  with parallel_backend("loky", inner_max_num_threads=1):
    (Parallel(n_jobs=-2, verbose=100)
     (delayed(buildRelease)
      (builds, geoBoundariesVersion, metaData.iloc[i], home) 
      for i in range(len(metaData))))
else:
  print("You cannot create this build, as it still has critical errors.")
  sys.exit()
  
#CGAZ
def buildCGAZ_ADM(iso):
  if(not os.path.isdir(home + "/gbRelease/gbReleaseData/CGAZ/")):
      os.mkdir(home + "/gbRelease/gbReleaseData/CGAZ/")
      os.mkdir(home + "/gbRelease/gbReleaseData/CGAZ/" + iso + "/")
      os.mkdir(home + "/gbRelease/gbReleaseData/CGAZ/" + iso + "/ADM1/")
      os.mkdir(home + "/gbRelease/gbReleaseData/CGAZ/" + iso + "/ADM2/") 
      
  inTOPOADM2 = (home + "/gbRelease/gbReleaseData/SSCGS/" + iso +
            "/ADM2/geoBoundariesSSCGS-" + geoBoundariesVersion +
            "-" + iso + "-" + "ADM2.topojson")
  inTOPOADM1 = (home + "/gbRelease/gbReleaseData/SSCGS/" + iso +
            "/ADM1/geoBoundariesSSCGS-" + geoBoundariesVersion +
            "-" + iso + "-" + "ADM1.topojson")
  inTOPOADM0 = (home + "/gbRelease/gbReleaseData/SSCGS/" + iso +
            "/ADM0/geoBoundariesSSCGS-" + geoBoundariesVersion +
            "-" + iso + "-" + "ADM0.topojson")
  
  outTMPTopoA = (home + "/gbRelease/tmp/CGAZ_" + iso + "adm2Temp.topojson")
  outTMPTopoB = (home + "/gbRelease/tmp/CGAZ_" + iso + "adm2TempB.topojson")
  outTMPTopoC = (home + "/gbRelease/tmp/CGAZ_" + iso + "adm2TempC.topojson")
  ADM2OUT = home + "/gbRelease/gbReleaseData/CGAZ/" + iso + "/ADM2/" + iso + "_ADM2.topojson"
  ADM1OUT = home + "/gbRelease/gbReleaseData/CGAZ/" + iso + "/ADM1/" + iso + "_ADM1.topojson"
  ADM0OUT = home + "/gbRelease/gbReleaseData/CGAZ/" + iso + "/ADM0/" + iso + "_ADM0.topojson"

  if(os.path.isfile(inTOPOADM2)):
    mapShaperJoinADM1 = (home + "/node_modules/mapshaper/bin/mapshaper-xl " + inTOPOADM2 +
                                 " -join "+ inTOPOADM1 +
                                 " fields=shapeID" + 
                                 " prefix=ADM1_" + 
                                 " point-method" +
                                 " -o format=topojson " + outTMPTopoA)
    
    
    process = subprocess.Popen([mapShaperJoinADM1], shell=True, 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    output, error = process.communicate()
    print(str(error) + mapShaperJoinADM1)

    mapShaperJoinADM0 = (home + "/node_modules/mapshaper/bin/mapshaper-xl " + outTMPTopoA +
                               " -join "+ inTOPOADM0 +
                               " fields=shapeID" + 
                               " prefix=ADM0_" + 
                               " point-method" +
                               " -o format=topojson " + outTMPTopoB)

    process = subprocess.Popen([mapShaperJoinADM0], shell=True, 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    output, error = process.communicate()
    print(str(error) + mapShaperJoinADM0)

    mapShaperFullHierarcy = (home + "/node_modules/mapshaper/bin/mapshaper-xl " + outTMPTopoB +
                               " -each 'ADMHIERARCHY=shapeID.concat(" + '"|"' +").concat(ADM1_shapeID).concat(" + '"|"' +").concat(ADM0_shapeID)'"
                               " -o format=topojson " + ADM2OUT)
    
    process = subprocess.Popen([mapShaperFullHierarcy], shell=True, 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    output, error = process.communicate()
    print(str(error) + mapShaperFullHierarcy)
    
  if(os.path.isfile(inTOPOADM1)):
    #Repeat for ADM1
    mapShaperJoinADM1_ADM0 = (home + "/node_modules/mapshaper/bin/mapshaper-xl " + inTOPOADM1 +
                                 " -join "+ inTOPOADM0 +
                                 " fields=shapeID" + 
                                 " prefix=ADM0_" + 
                                 " point-method" +
                                 " -o format=topojson " + outTMPTopoA)

    process = subprocess.Popen([mapShaperJoinADM1_ADM0], shell=True, 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    output, error = process.communicate()
    print(str(error) + str(mapShaperJoinADM1_ADM0))
    
    mapShaperFullHierarcy = (home + "/node_modules/mapshaper/bin/mapshaper-xl " + outTMPTopoA +
                                 " -each 'ADMHIERARCHY=shapeID.concat(" + '"|"' +").concat(ADM0_shapeID)'"
                                 " -o format=topojson " + ADM1OUT)
    
    process = subprocess.Popen([mapShaperFullHierarcy], shell=True, 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    output, error = process.communicate()
    print(str(error) + str(mapShaperFullHierarcy))
    
  #Copy the ADM0s over
  if(os.path.isfile(inTOPOADM0)):
    mapShaperCopyADM0 = (home + "/node_modules/mapshaper/bin/mapshaper-xl " + inTOPOADM0 +
                           " -o format=topojson " + ADM0OUT)

    process = subprocess.Popen([mapShaperCopyADM0], shell=True, 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    output, error = process.communicate()
    print(str(error) + str(mapShaperCopyADM0))
  
  
if("CGAZ" in builds):
  with parallel_backend("loky", inner_max_num_threads=1):
    (Parallel(n_jobs=-2, verbose=100)
     (delayed(buildCGAZ_ADM)
      (list(set(allSourceISOs))[i]) 
      for i in range(len(list(set(allSourceISOs))))))
  
  adm1str = (home + "/node_modules/mapshaper/bin/mapshaper-xl 40gb " +
             "-i ")
  adm2str = (home + "/node_modules/mapshaper/bin/mapshaper-xl 40gb " +
             "-i ")
  adm0str = (home + "/node_modules/mapshaper/bin/mapshaper-xl 40gb " +
             "-i ")
  adm1renameLayers = "id1"
  adm2renameLayers = "id1"
  adm0renameLayers = "id1"
  count = 1
  if(not os.path.isdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/"))):
     os.mkdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/"))
  if(not os.path.isdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM0/"))):
     os.mkdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM0/"))
  if(not os.path.isdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM1/"))):
     os.mkdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM1/"))
  if(not os.path.isdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM2/"))):
     os.mkdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM2/"))     

  for iso in list(set(allSourceISOs)):
    count = count + 1
    if(os.path.isfile((home + "/gbRelease/gbReleaseData/CGAZ/" + iso + "/ADM1/" + iso + "_ADM1.topojson"))):
      adm1str = adm1str + (home + "/gbRelease/gbReleaseData/CGAZ/" + iso + "/ADM1/" + iso + "_ADM1.topojson ")
    if(os.path.isfile((home + "/gbRelease/gbReleaseData/CGAZ/" + iso + "/ADM2/" + iso + "_ADM2.topojson"))):
      adm2str = adm2str + (home + "/gbRelease/gbReleaseData/CGAZ/" + iso + "/ADM2/" + iso + "_ADM2.topojson ")
    if(os.path.isfile((home + "/gbRelease/gbReleaseData/CGAZ/" + iso + "/ADM0/" + iso + "_ADM0.topojson"))):
      adm0str = adm0str + (home + "/gbRelease/gbReleaseData/CGAZ/" + iso + "/ADM0/" + iso + "_ADM0.topojson ")
  
  #Here we go! Loop this for four different simplification levels.
  simplify = ["100", "75", "50", "25", "10"]
  
  for ratio in simplify:
    if(not os.path.isdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM1/simplifyRatio_" + ratio))):
      os.mkdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM1/simplifyRatio_" + ratio)) 
      os.mkdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM1/simplifyRatio_" + ratio + "/shp/"))  
    if(not os.path.isdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM2/simplifyRatio_" + ratio))):
      os.mkdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM2/simplifyRatio_" + ratio))  
      os.mkdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM2/simplifyRatio_" + ratio + "/shp/"))  
    if(not os.path.isdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM0/simplifyRatio_" + ratio))):
      os.mkdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM0/simplifyRatio_" + ratio))  
      os.mkdir((home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM0/simplifyRatio_" + ratio + "/shp/"))  
  
    mapShaperFullADM1 = (adm1str + 
                       " combine-files -merge-layers force" +
                       " name=globalADM1" +
                       " -clean gap-fill-area=10000km2 keep-shapes" +
                       " -simplify weighted " + ratio + "% keep-shapes" +
                       " -o format=topojson " + (home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM1/simplifyRatio_"+ratio+"/geoBoundariesCGAZ_ADM1.topojson") +
                       " -o format=geojson " + (home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM1/simplifyRatio_"+ratio+"/geoBoundariesCGAZ_ADM1.geojson") +
                       " -o format=shapefile " + (home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM1/simplifyRatio_"+ratio+"/shp/geoBoundariesCGAZ_ADM1.shp")       
                      )
  
    os.system(mapShaperFullADM1)
  
    mapShaperFullADM0 = (adm0str + 
                       " combine-files -merge-layers force" +
                       " name=globalADM0" +
                       " -clean gap-fill-area=10000km2 keep-shapes" +
                       " -simplify weighted " + ratio + "% keep-shapes" +
                       " -o format=topojson " + (home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM0/simplifyRatio_"+ratio+"/geoBoundariesCGAZ_ADM0.topojson") +
                       " -o format=geojson " + (home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM0/simplifyRatio_"+ratio+"/geoBoundariesCGAZ_ADM0.geojson") +
                       " -o format=shapefile " + (home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM0/simplifyRatio_"+ratio+"/shp/geoBoundariesCGAZ_ADM0.shp")       
                      )
  
    os.system(mapShaperFullADM0)
  
    mapShaperFullADM2 = (adm2str + 
                       " combine-files -merge-layers force" +
                       " name=globalADM2" +
                       " -clean gap-fill-area=10000km2 keep-shapes" +
                       " -simplify weighted " + ratio + "% keep-shapes" +
                       " -o format=topojson " + (home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM2/simplifyRatio_"+ratio+"/geoBoundariesCGAZ_ADM2.topojson") +
                       " -o format=geojson " + (home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM2/simplifyRatio_"+ratio+"/geoBoundariesCGAZ_ADM2.geojson") +
                       " -o format=shapefile " + (home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ADM2/simplifyRatio_"+ratio+"/shp/geoBoundariesCGAZ_ADM2.shp")       
                      )
  
    os.system(mapShaperFullADM2)
  
shutil.rmtree(home + "/gbRelease/tmp/") 
      

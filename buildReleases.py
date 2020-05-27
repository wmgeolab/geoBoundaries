#Script to build new major / minor release of geoBoundaries
import pandas as pd
from os.path import expanduser
import glob
import os
import fiona
import fiona.crs
import shapely.geometry as geom
from shapely.geometry import shape
from joblib import Parallel, delayed, parallel_backend
import shutil
import zipfile
import json
import sys
import topojson
from matplotlib import pyplot as plt
from shapely.geometry import asShape
from itertools import chain
from geojson import Feature, Point, FeatureCollection, Polygon
home = expanduser("~")

#Specify Version this release will be:
geoBoundariesVersion = "3_0_0"

#Can use this script to build core or ancillary products.
#Accepts a list
#HPSCU - High Precision Single Country Unstadardized (HPSCU)
#CGAZ - Contigious Global Administrative Zones
#GSB does both  Simplified Single Country Globally Standardized (SSCGS )
#and High Precision Single Country Globally Standardized (HPSCGS)
#SSCU - Simplified Single Country Unstandardized 
buildType = ["HPSCU", "HPSCGS", "SSCU", "SSCGS"]



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
      
  def HPSCU(self):
    self.BuildComplete_HPSCU = False
    #Check if a file already exists and if the current zip file was downloaded
    #on a date *later than* our most recent build.
    #If so, we need to rebuild everything.
    #Otherwise, we can skip.
    finalZipPath = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/" + "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + "-all.zip")
    
    if(os.path.isfile(finalZipPath)):
      buildTimeStamp = os.path.getmtime(finalZipPath) 
      zipDownloadTimeStamp = os.path.getmtime(self.home + "/gbRelease/gbRawData/currentZips/" + self.iso + "_" + self.adm + ".zip")
      if(buildTimeStamp - zipDownloadTimeStamp > 0):
        self.BuildComplete_HPSCU = True
        self.geoLog("WARN", (self.iso + "|" + self.adm + " HPSCU build skipped - already had most recent version."))
        return 0
      else:
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
    
    #Build the geometry files...
  
    #Create a geojson
    geojson = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/" +
               "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + ".geojson")
  
    #For uniformity, we'll store all our geoJSONs as multipolygons,
    #even though it's unnecessary for many.
  
    shpFile.schema["geometry"] = "MultiPolygon"
    fid = 0
    kwargs = {"COORDINATE_PRECISION":7}
    with fiona.open(geojson, 'w', driver="GeoJSON", 
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
    
    #Create a json and textfile of metadata
    json_txt = self.allMeta
    jsonOut = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/"
               "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + "-metaData.json")
    json_txt.to_json(jsonOut)
  
    csvOutpath = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/"
               "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + "-metaData.txt")
    json_txt.to_csv(csvOutpath, index=True, header=False, sep=' ')
    
    #Create a temp folder to hold the shapefile
    if(os.path.isdir((self.home + "/gbRelease/tmp/" + self.iso + self.adm + "/"))):
      shutil.rmtree((self.home + "/gbRelease/tmp/" + self.iso + self.adm + "/")) 
      os.mkdir((self.home + "/gbRelease/tmp/" + self.iso + self.adm + "/"))
    else:
      os.mkdir((self.home + "/gbRelease/tmp/" + self.iso + self.adm + "/"))
    
    fid = 0
    shapefilePath = (self.home + "/gbRelease/tmp/" + self.iso + self.adm + "/" +
               "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + ".shp")
  
    with fiona.open(shapefilePath, 'w', driver="ESRI Shapefile", 
                  schema=shpFile.schema,
                 encoding='utf-8',
                 crs=fiona.crs.from_epsg(4326), **kwargs) as write_shp:

      for feature in shpFile:
        fid = fid + 1
        feature["properties"]["shapeID"] = (self.iso + "-" + self.adm + "-" + self.version + "-B" + str(fid)) 
        
        if(feature["geometry"]["type"] == "MultiPolygon"):
          write_shp.write(feature)
        else:
          multiFeature = feature
          multiFeature['geometry'] = geom.mapping(geom.MultiPolygon([shape(feature["geometry"])]))
          write_shp.write(multiFeature)
   
    #Zip the shapefile and output it to the final folder
    shutil.make_archive(
      base_name = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/" +
               "geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + "-shp"),
      format="zip",
      root_dir = (self.home + "/gbRelease/tmp/" + self.iso + self.adm + "/")
  )
                    
    #Matplotlib Visualization
    with open(geojson, 'r') as j:
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
    
    dirToZip = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + self.adm + "/")
    zipTarget = (self.home + "/gbRelease/tmp/geoBoundaries-" + self.version + "-" + self.iso + "-" + self.adm + "-all")
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
    
    

    self.BuildComplete_HPSCU = True
#################################
#################################
##### SSCU Build (Simplified Unstandardized)
#################################
#################################

  def SSCU(self):
    #Simplified single country release
    self.BuildComplete_SSCU = False
    finalZipPath = (self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/" + "geoBoundariesSimplified-" + self.version + "-" + self.iso + "-" + self.adm + "-all.zip")
    
    if(os.path.isfile(finalZipPath)):
      buildTimeStamp = os.path.getmtime(finalZipPath) 
      zipDownloadTimeStamp = os.path.getmtime(self.home + "/gbRelease/gbRawData/currentZips/" + self.iso + "_" + self.adm + ".zip")
      if(buildTimeStamp - zipDownloadTimeStamp > 0):
        self.BuildComplete_SSCU = True
        self.geoLog("WARN", (self.iso + "|" + self.adm + " SSCU build skipped - already had most recent version."))
        return 0
      else:
        shutil.rmtree((self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/"))
        os.mkdir((self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/"))
    
    
    outDirectory = self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/"
    inShape = (self.home + "/gbRelease/gbReleaseData/HPSCU/" + self.iso + "/" + 
               self.adm + "/" + "geoBoundaries-" + self.version + "-" + 
               self.iso + "-" + self.adm + ".geojson")
    outJSON = outDirectory + "geoBoundariesSimplified-" + self.version + "-" + self.iso + "-" + self.adm + ".geojson"
    
    #Check if the raw file is small already.
    #If so, we don't want to simplify further.
    #"Small" is arbitrarily defined as 100kb or smaller
    #(Roughly)
    with open(inShape, 'r') as j:
      geoBoundary = json.load(j)

    origSize = sys.getsizeof(str(geoBoundary))
    
    if(origSize <= 10000):
      with open(outgeoJSON, 'w') as f:
        json.dump(geoBoundary, f)
        self.BuildComplete_SSCU = True
        self.geoLog("WARN", (self.iso + "|" + self.adm + " File size already below threshold; no simplification applied."))
        return 0
    
    #Else, apply simplification.
    #First, identify the level of simplification
    #Based on the area of features.
    #We'll refine this algorithm over releases. Fairly coarse right now.
    else:    
      minA = 9999999999999999
      for boundary in geoBoundary["features"]:
        if(boundary["geometry"]['type'] == "MultiPolygon"):
          polys = list(shape(boundary["geometry"]))
          for poly in polys:
            mA = poly.area
            if(mA < minA):
              minA = mA
        else:
          mA = shape(boundary["geometry"]).area
          if(mA < minA):
            minA = mA
      
      toposimp = min(0.01, max(((10*minA) + 0.001), .00000000001))
      
      uniqueTMP = self.home + "/gbRelease/tmp/" + self.version + self.iso + self.adm + ".topo" 
      
      #Make a temporary copy of the metadata
      #We'll include the simplification rate there for these builds.
      sB = self.allMeta.copy()
      
      sB["simplificationRate"] = toposimp
      
      try:
        with open(uniqueTMP, 'w') as outfile:
          topo = topojson.Topology(FeatureCollection(geoBoundary['features']), 
                      prequantize=False,
                      presimplify=False,
                      toposimplify=toposimp, 
                      simplify_with='shapely', 
                      simplify_algorithm='dp', 
                      winding_order='CW_CCW').to_json()
          json.dump(json.loads(topo), outfile)
      except:
        self.geoLog("CRITICAL", (self.iso + "|" + self.adm + " Simplification Failed."))
         
      try:
        geoJSON = topo2geojson(uniqueTMP, outJSON)
      except:
        self.geoLog("CRITICAL", (self.iso + "|" + self.adm + " Topojson conversion to geoJSON Failed."))
        
      
      shapefilePath = (self.home + "/gbRelease/tmp/simp_" + self.iso + self.adm + "/" +
               "geoBoundariesSimplified-" + self.version + "-" + self.iso + "-" + self.adm + ".shp")
  
      try:
        schemaSource = fiona.open((self.home + "/gbRelease/gbRawData/current/" + self.iso + "/" + self.adm + 
               "/shapeFixes/" + self.iso + "_" + self.adm + "_" +
               "fixedInternalTopology.shp"))
      except:
        self.geoLog("CRITICAL", (self.iso + "|" + self.adm + "Shape failed to open."))
    
      if(os.path.isdir((self.home + "/gbRelease/tmp/simp_" + self.iso + self.adm + "/"))):
        shutil.rmtree((self.home + "/gbRelease/tmp/simp_" + self.iso + self.adm + "/")) 
        os.mkdir((self.home + "/gbRelease/tmp/simp_" + self.iso + self.adm + "/"))
      else:
        os.mkdir((self.home + "/gbRelease/tmp/simp_" + self.iso + self.adm + "/"))
    
      #Build shapefile:
      kwargs = {"COORDINATE_PRECISION":7}
      with fiona.open(shapefilePath, 'w', driver="ESRI Shapefile", 
                 schema=schemaSource.schema,
                 encoding='utf-8',
                 crs=fiona.crs.from_epsg(4326), **kwargs) as write_shp:

        for feature in geoJSON["features"]:
          if(feature["geometry"]["type"] == "MultiPolygon"):
            write_shp.write(feature)
          else:
            multiFeature = feature
            multiFeature['geometry'] = geom.mapping(geom.MultiPolygon([shape(feature["geometry"])]))
            write_shp.write(multiFeature)
      
      shutil.make_archive(
        base_name = (self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/" +
                     "geoBoundariesSimplified-" + self.version + "-" + self.iso + "-" + self.adm + "-shp"),
        format="zip",
        root_dir = (self.home + "/gbRelease/tmp/simp_" + self.iso + self.adm + "/"))
      
      #Build metadata
      json_txt = sB
      jsonOut = (self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/"
               "geoBoundariesSimplified-" + self.version + "-" + self.iso + "-" + self.adm + "-metaData.json")
      json_txt.to_json(jsonOut)
  
      csvOutpath = (self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/"
               "geoBoundariesSimplified-" + self.version + "-" + self.iso + "-" + self.adm + "-metaData.txt")
      json_txt.to_csv(csvOutpath, index=True, header=False, sep=' ')
      
      #Make visualization
      #geoBoundary - pre
      #geoJSON - post
      simplegeoBoundary = geoJSON
      #Matplotlib Visualization
      fig = plt.clf()
      fig = plt.figure(1, figsize=(10,5), dpi=300)
      axs = fig.add_subplot(121)

      mbpost = round(sys.getsizeof(str(simplegeoBoundary)) / 1000000,3)

      axs.set_title("geoBoundaries " + self.version.replace("_",".") + "\n" + self.iso + " " + self.adm + " " + '\nPost Simplification ' + str(mbpost) + "MB")

      #Accounting for Multipolygon Boundaries
      for boundary in simplegeoBoundary["features"]:
        if(boundary["geometry"]['type'] == "MultiPolygon"):
          polys = list(shape(boundary["geometry"]))
          for poly in polys:
            xs, ys = poly.exterior.xy    
            axs.fill(xs, ys, alpha=0.5, fc='red', ec='black')
        else:
          xs, ys = shape(boundary["geometry"]).exterior.xy    
          axs.fill(xs, ys, alpha=0.5, fc='red', ec='black')

      axsb = fig.add_subplot(122)

      mbpre = round(sys.getsizeof(str(geoBoundary)) / 1000000,3)

      axsb.set_title("geoBoundaries " + self.version.replace("_",".") + "\n" + self.iso + " " + self.adm + " " + '\nOriginal '  + str(mbpre) + "MB")

      #Accounting for Multipolygon Boundaries
      for boundary in geoBoundary["features"]:
        if(boundary["geometry"]['type'] == "MultiPolygon"):
          polys = list(shape(boundary["geometry"]))
          for poly in polys:
            xs, ys = poly.exterior.xy    
            axsb.fill(xs, ys, alpha=0.5, fc='red', ec='black')
        else:
          xs, ys = shape(boundary["geometry"]).exterior.xy    
          axsb.fill(xs, ys, alpha=0.5, fc='red', ec='black')

      outgeoPNG = (self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/"
               "geoBoundariesPreviewSimplified-" + self.version + "-" + self.iso + "-" + self.adm + ".png")
      fig.savefig(outgeoPNG, bbox_inches='tight')
      
      #Build final zip
      dirToZip = (self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/")
      zipTarget = (self.home + "/gbRelease/tmp/geoBoundariesSimplified-" + self.version + "-" + self.iso + "-" + self.adm + "-all")
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
    #Simplified single country release
    self.BuildComplete_SSCU = False
    finalZipPath = (self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/" + "geoBoundariesSimplified-" + self.version + "-" + self.iso + "-" + self.adm + "-all.zip")
    
    if(os.path.isfile(finalZipPath)):
      buildTimeStamp = os.path.getmtime(finalZipPath) 
      zipDownloadTimeStamp = os.path.getmtime(self.home + "/gbRelease/gbRawData/currentZips/" + self.iso + "_" + self.adm + ".zip")
      if(buildTimeStamp - zipDownloadTimeStamp > 0):
        self.BuildComplete_SSCU = True
        self.geoLog("WARN", (self.iso + "|" + self.adm + " SSCU build skipped - already had most recent version."))
        return 0
      else:
        shutil.rmtree((self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/"))
        os.mkdir((self.home + "/gbRelease/gbReleaseData/SSCU/" + self.iso + "/" + self.adm + "/"))
    
        
def buildRelease(buildType, geoBoundariesVersion, metaDataRow, home):
  #Let's not talk about this.
  for releaseType in buildType:
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

  if("HPSCU" in buildType):
    try:
      boundary.HPSCU()
    except:
      boundary.geoLog("CRITICAL", (boundary.iso + "|" + boundary.adm + " - HPSCU build failed."))
  
  if((boundary.BuildComplete_HPSCU == True) and ("SSCU" in buildType)):
    try:
      boundary.SSCU()
    except:
      boundary.geoLog("CRITICAL", (boundary.iso + "|" + boundary.adm + " - SSCU build failed."))
  
  elif((boundary.BuildComplete_HPSCU != True) and ("SSCU" in buildType)):
    boundary.geoLog("CRITICAL", (boundary.iso + "|" + boundary.adm + " Cannot build SSCU product without HPSCU completion."))
  
  #NOTE: Both standardized products are built in GSB.
  #We do both standardized products at once for the sake of effeciency.
  if((boundary.BuildComplete_HPSCU == True) and ("GSB" in buildType)):
    try:
      boundary.GSB()
    except:
      boundary.geoLog("CRITICAL", (boundary.iso + "|" + boundary.adm + " - GSB build failed."))
  
  elif((boundary.BuildComplete_HPSCU != True) and ("GSB" in buildType)):
    boundary.geoLog("CRITICAL", (boundary.iso + "|" + boundary.adm + " Cannot build GSB product without HPSCU completion."))
    
    
                    
               
               ##REMEMBER AT THE END: GO BACK AND BUILD THE ISO LEVEL ZIPS!!!   
      

allMeta = glob.glob((home + "/gbRelease/gbRawData/metadata/*"))
latestMeta = max(allMeta, key=os.path.getctime)
nightlyVersion = str(latestMeta).split("/")[-1].split(".")[0]
metaData = pd.read_csv((home + "/gbRelease/gbRawData/current/geoBoundaries-" + nightlyVersion + ".csv"))


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
  
  for releaseType in buildType:
    if(not os.path.isdir(home + "/gbRelease/gbReleaseData/" + releaseType + "/")):
      os.mkdir(home + "/gbRelease/gbReleaseData/" + releaseType + "/")
      shutil.copyfile((home + "/gbRelease/gbReleaseData/geoBoundaries-" + geoBoundariesVersion + ".csv"),
                      (home + "/gbRelease/gbReleaseData/" + releaseType + "/geoBoundaries-" + geoBoundariesVersion + ".csv"))
  
  #Launch the ships:
  with parallel_backend("loky", inner_max_num_threads=1):
    (Parallel(n_jobs=-2, verbose=100)
     (delayed(buildRelease)
      (buildType, geoBoundariesVersion, metaData.iloc[i], home) 
      for i in range(len(metaData))))
  

      
else:
  print("You cannot create this build, as it still has critical errors.")
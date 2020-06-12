import geojson
from os.path import expanduser

home = expanduser("~")
version = "development"

ratio = ["10", "25", "50", "75", "100"]
level = ["ADM0", "ADM1", "ADM2"]
counts = []
for l in level:
  for r in ratio:
    path = home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/"+l+"/simplifyRatio_" + r + "/geoBoundariesCGAZ_" +l+".geojson"
    with open(path, 'r', encoding="ISO-8859-1") as j:
      temp = j.read()
    
    geoBoundaries = geojson.loads(temp)
    counts.append([l, r, len(geoBoundaries['features'])])
    
    #ADM2 Expectation:
    #114673 ADM2 True
    #3332 ADM1 True
    #200 ADM0 True
    #ADM0 - we drop two - ["NIU", "PSE"] - not recognized by US for standard
    

#Compare ADM2 Ireland 2 for differences between products as a check
I = {}
I['CGAZ'] = home + "/gbRelease/gbReleaseData/CGAZ/IRL/ADM2/IRL_ADM2.topojson"
I['SSCU'] = home + "/gbRelease/gbReleaseData/SSCU/IRL/ADM2/geoBoundariesSSCU-"+version+"-IRL-ADM2.geojson"
I['SSCGS'] = home + "/gbRelease/gbReleaseData/SSCGS/IRL/ADM2/geoBoundariesSSCGS-"+version+"-IRL-ADM2.geojson"
I['HPSCU'] = home + "/gbRelease/gbReleaseData/HPSCU/IRL/ADM2/geoBoundaries-"+version+"-IRL-ADM2.geojson"
I['HPSCGS'] = home + "/gbRelease/gbReleaseData/HPSCGS/IRL/ADM2/geoBoundariesHPSCGS-"+version+"-IRL-ADM2.geojson"

productCounts = []

for i in I:
  with open(I[i], 'r', encoding="ISO-8859-1") as j:
    temp = j.read()
  
  geoBoundaries = geojson.loads(temp)
  
  if(i == "CGAZ"):
    productCounts.append([i, len(geoBoundaries['objects']['geoBoundaries-development-IRL-ADM2']['geometries'])])
  else:
    productCounts.append([i, len(geoBoundaries['features'])])
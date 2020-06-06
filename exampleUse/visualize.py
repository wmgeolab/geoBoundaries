import json
import requests
from matplotlib import pyplot as plt
from shapely.geometry import shape

r = requests.get("https://www.geoboundaries.org/gbRequest.html?ISO=EGY&ADM=ADM1")
dlPath = r.json()[0]['gjDownloadURL']
geoBoundary = requests.get(dlPath).json()

#Matplotlib Visualization
fig = plt.figure(1, figsize=(5,5), dpi=90)
axs = fig.add_subplot(111)
axs.set_title('Example Visualization')

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

fig.savefig("example.png")
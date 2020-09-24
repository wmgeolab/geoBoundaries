import json
import requests

r = requests.get("https://www.geoboundaries.org/gbRequest.html?ISO=EGY&ADM=ADM1")
dlPath = r.json()[0]['gjDownloadURL']
geoBoundary = requests.get(dlPath).json()


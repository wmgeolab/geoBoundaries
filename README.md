# geoBoundaries

![](https://www.geoboundaries.org/images/pic11.jpg)
Built by the community and William & Mary [geoLab](http://geolab.wm.edu/) since 2017, the geoBoundaries Global Database of Political Administrative Boundaries Database is an online, open license resource of boundaries (i.e., state, county) for every country in the world. We currently track 199 total entities, including all 195 UN member states, Greenland, Taiwan, Niue, and Kosovo. All boundaries are available to view or download in common file formats, including shapefiles; the only requirement for use is [acknowledgement](https://www.geoboundaries.org/index.html#citation). The most up-to-date information about geoBoundaries can be found at www.geoboundaries.org.

# Getting Involved
We welcome contributions to the geoBoundaries dataset.  Involvement can take many forms: assistance identifying errors in the database, contributing boundary files, or even contributing code for our build or website scripts.  To get started, you could:
- [Report Boundary Errors](https://github.com/wmgeolab/geoBoundaries/issues/new?assignees=&labels=&template=boundary-errata.md&title=%5BBOUNDARY+ERRATA%5D): While we try to ensure geoBoundaries is as error-free as possible, we are currently tracking around 300 million vertices across hundreds-of-thousands of geometries - there are bound to be issues!  We very much welcome any reports of errors across the database.
- [Contribute Boundaries](https://github.com/wmgeolab/geoBoundaries/blob/main/CONTRIBUTING.md): We carefully curate all boundaries that are submitted to the database, and have a very active community.  Join us in the fun!  We try to keep things simple for everyone, requiring only a zipfile upload. 
- [Fix Known Issues](https://github.com/wmgeolab/geoBoundaries/issues): We have a number of known issues with the database, and always welcome contributions that might fix any of these.  
- [Help with the Python Code](https://github.com/wmgeolab/geoBoundaryBot): We always welcome contributions to our codebase that improve the efficiency of our processing, or introduce new types of checks to automatically prevent errors.  Our code includes a number of different pieces, such as the www.geoboundaries.org website, API, the geoBoundaryBot (responds to PRs), and our formal build scripts.


# File Access

We provide three different mechanisms to download geoBoundaries data: a web-based GUI, HTML file access on GitHub (for archival versions), and an API. Releases come in both unsimplified ("HPSCU") and simplified ("SSCU") releases, and include a global composite of ADM0, ADM1, and ADM2 with gaps filled between borders ("CGAZ").  

_HPSCU_  - High Precision Single Country Unstandardized. The premier geoBoundaries release, representing the highest precision files available for every country in the world. Every country is represented as that country represents itself, so (for example) two countries may overlap in the case of contested boundaries.

_SSCU_  - Simplified Single Country Unstandardized. A simplified version of every file available for every country in the world, using the HPSCU product as a base. 

_CGAZ_  - Comprehensive Global Administrative Zones. A global composite of the SSCU ADM0, ADM1 and ADM2, clipped to international boundaries (US Department of State), with gaps filled between borders.  Also available at higher levels of simplification.

## Manual Data Retrieval & Archival Access

Since geoBoundaries 3.0, file access has been standardized on the github platform. To download a file from any release, you can navigate to our [releases page](https://github.com/wmgeolab/geoBoundaries/releases/), and choose the release you are interested in retrieving files from. Our first public release, geoBoundaries 2.0, is available online through the [Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/PGAIQY).


## Programmatic / API Access
Full details on our API are available [here](https://www.geoboundaries.org/api.html).  

To find information on the most up-to-date boundaries available:

```
https://www.geoboundaries.org/api/current/gbOpen/[3-LETTER-ISO-CODE]/[ADM-LEVEL]/
```

Users can also enter the special phrase "ALL" for either "ADM" or "ISO" to get a multi-boundary return. Each requested boundary returns all metadata available for that boundary in the gBOpen release, including a link to both the full-resolution, large-file size and the simplified small-file size versions. Users can additionally replace "gbOpen" with either "gbAuthoritative" or "gbHumanitarian" to filter results to only include boundaries from those two respective releases.


To find information on any geoBoundary, past or present, based on the geoBoundary ID:
```
https://www.geoboundaries.org/api/gbID/[geoBoundaryID]/
```

Starting with the geoBoundaries 4.0 release, all geoBoundaries can be referenced by ID using the above API. The returned elements are identical to those in the /current/ API endpoint.

Of note, to facilitate speed of queries against the API, all JSONs are pre-cached and can be exported in bulk by cloning the [geoBoundaries Website repository](https://github.com/wmgeolab/gbWeb) for local use.


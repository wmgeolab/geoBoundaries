# geoBoundaries
![image](https://user-images.githubusercontent.com/7882645/216724015-071055db-e635-418b-83a6-acbdde726c6c.png)
Built by the [community](https://github.com/wmgeolab/geoBoundaries/) and [William & Mary geoLab](https://geolab.wm.edu/), the geoBoundaries Global Database of Political Administrative Boundaries Database is an online, open license (CC BY 4.0) resource of information on administrative boundaries (i.e., state, county) for every country in the world. Since 2016, we have tracked approximately 1 million boundaries within over 200 entities, including all UN member states. All boundaries are available to view or download in common file formats; the only requirement for use is acknowledgement.

# Getting Involved
We welcome contributions to the geoBoundaries dataset.  Involvement can take many forms: assistance identifying errors in the database, contributing boundary files, or even contributing code for our build or website scripts.  To get started, you could:
- [Report Boundary Errors](https://github.com/wmgeolab/geoBoundaries/issues/new?assignees=&labels=&template=boundary-errata.md&title=%5BBOUNDARY+ERRATA%5D): While we try to ensure geoBoundaries is as error-free as possible, we are currently tracking around 300 million vertices across hundreds-of-thousands of geometries - there are bound to be issues!  We very much welcome any reports of errors across the database.
- [Contribute Boundaries](https://github.com/wmgeolab/geoBoundaries/blob/main/CONTRIBUTING.md): We carefully curate all boundaries that are submitted to the database, and have a very active community.  Join us in the fun!  We try to keep things simple for everyone, requiring only a zipfile upload. 
- [Fix Known Issues](https://github.com/wmgeolab/geoBoundaries/issues): We have a number of known issues with the database, and always welcome contributions that might fix any of these.  
- [Help with the Python Code](https://github.com/wmgeolab/geoBoundaryBot): We always welcome contributions to our codebase that improve the efficiency of our processing, or introduce new types of checks to automatically prevent errors.  Our code includes a number of different pieces, such as the www.geoboundaries.org website, API, the geoBoundaryBot (responds to PRs), and our formal build scripts.


# File Access

We provide three different mechanisms to download geoBoundaries data: a web-based GUI, HTML file access on GitHub (for archival versions), and an API. Releases come in both unsimplified and simplified types, and include a global composite of ADM0, ADM1, and ADM2 with gaps filled between borders ("CGAZ").  Acronyms describing these datasets you may encounter include:

_HPSCU_  - High Precision Single Country Unstandardized. The premier geoBoundaries release, representing the highest precision files available for every country in the world. Every country is represented as that country represents itself, so (for example) two countries may overlap in the case of contested boundaries.

_SSCU_  - Simplified Single Country Unstandardized. A simplified version of every file available for every country in the world, using the HPSCU product as a base. 

_CGAZ_  - Comprehensive Global Administrative Zones. A global composite of the SSCU ADM0, ADM1 and ADM2, clipped to international boundaries (US Department of State), with gaps filled between borders.  Also available at higher levels of simplification.

## Versioned Releases for Research Replication

While geoBoundaries is always updating, we provide annual releases to facilitate future research replication. To download a file from any release, you can navigate to our [releases page](https://github.com/wmgeolab/geoBoundaries/releases/), and choose the release you are interested in retrieving files from, or you can navigate to the appropriate location using this table:
Release | Date | Link
-- | -- | --
geoBoundaries 4.0.0 | August 31, 2021 | [299e006](https://github.com/wmgeolab/geoBoundariesArchive_4_0_0/tree/299e00623ece6c03bcb9a751eda6094b1eac85a6)
geoBoundaries 3.0.0 | June 5, 2020 | [7c8dbc5](https://github.com/wmgeolab/geoBoundariesArchive_3_0_0/tree/7c8dbc599e312d9204e450aecfa66c204b8cf9b8)
geoBoundaries 2.0.1 | December 7, 2019 | [375ea48](https://github.com/wmgeolab/geoBoundariesArchive_2_0_1/commit/375ea48193eda78f74b964f1c898a04bd4cb465d)
geoBoundaries 1.3.4 | November 11, 2018 | [d3f7490](https://github.com/wmgeolab/geoBoundariesArchive_1_3_3/tree/d3f7490211be2971214f355055629b0c2dedeef6)


## Programmatic / API Access
Full details on our API are available [here](https://www.geoboundaries.org/api.html).  

To find information on the most up-to-date boundaries available:

```
https://www.geoboundaries.org/api/current/gbOpen/[3-LETTER-ISO-CODE]/[ADM-LEVEL]/
```

Users can also enter the special phrase "ALL" for either "ADM" or "ISO" to get a multi-boundary return. Each requested boundary returns all metadata available for that boundary in the gBOpen release, including a link to both the full-resolution, large-file size and the simplified small-file size versions. Users can additionally replace "gbOpen" with either "gbAuthoritative" or "gbHumanitarian" to filter results to only include boundaries from those two respective releases.

Of note, to facilitate speed of queries against the API, all JSONs are pre-cached and can be exported in bulk by cloning the [geoBoundaries Website repository](https://github.com/wmgeolab/gbWeb) for local use.


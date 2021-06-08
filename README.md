# geoBoundaries

![](https://www.geoboundaries.org/images/pic11.jpg)
Produced and maintained by the William & Mary [geoLab](http://geolab.wm.edu/) since 2017, the geoBoundaries Global Database of Political Administrative Boundaries Database is an online, open license resource of boundaries (i.e., state, county) for every country in the world. We currently track 199 total entities, including all 195 UN member states, Greenland, Taiwan, Niue, and Kosovo. All boundaries are available to view or download in common file formats, including shapefiles; the only requirement for use is [acknowledgement](https://www.geoboundaries.org/index.html#citation). The most up-to-date information about geoBoundaries can be found at www.geoboundaries.org.

# Getting Involved
We welcome contributions to the geoBoundaries dataset.  Involvement can take many forms: assistance identifying errata in the database, contributing boundary files, or even contributing code for our build or website scripts.  To get started, you could:
- [Report Boundary Errors](https://github.com/wmgeolab/geoBoundaries/issues/new?assignees=&labels=&template=boundary-errata.md&title=%5BBOUNDARY+ERRATA%5D): While we try to ensure geoBoundaries is as error-free as possible, we are currently tracking trillions of vertices across hundreds-of-thousands of geometries - there are bound to be issues!  We very much welcome any reports of errors across the database.
- [Contribute Boundaries](https://github.com/wmgeolab/geoBoundaries/blob/main/CONTRIBUTING.md): We carefully curate all boundaries that are submitted to the database, and have a very active community.  Join us in the fun!  We try to keep things simple for everyone, requiring only a zipfile upload.  Learn more [here](https://github.com/wmgeolab/geoBoundaries/blob/main/CONTRIBUTING.md).
- [Fix Known Issues](https://github.com/wmgeolab/geoBoundaries/issues): We have a number of known issues with the database, and always welcome contributions that might fix any of these.  
- [Help with the Python Code](https://github.com/wmgeolab/geoBoundaryBot): We always welcome contributions to our codebase that improve the effeciency of our processing, or introduce new types of checks to automatically prevent errors.  Our code includes a number of different pieces, such as the www.geoboundaries.org website, API, the geoBoundaryBot (responds to PRs), and our formal build scripts.


# File Access

We provide three different mechanisms to download geoBoundaries data: a web-based GUI, HTML file access (for archival versions), and an API. Releases come in five different flavors:

_HPSCU_  - High Precision Single Country Unstadardized. The premier geoBoundaries release, representing the highest precision files available for every country in the world. No standardization is performed on these files, so (for example) two countries may overlap in the case of contested boundaries.

_HPSCGS_  - High Precision Single Country Globally Standardized. A version of geoBoundaries high percision data that has been clipped to the U.S. Department of State boundary file, ensuring no contested boundaries or overlap in the dataset. This globally standardized product may have gaps between countries. If you need a product with no gaps, we recommend our simplified global product.

_SSCU_  - Simplified Single Country Unstandardized. A simplified version of every file available for every country in the world. No standardization is performed on these files, so (for example) two countries may overlap in the case of contested boundaries.

_SSCGS_  - Simplified Single Country Globally Standardized. A version of geoBoundaries simplified data that has been clipped to the U.S. Department of State boundary file, ensuring no contested boundaries or overlap in the dataset. This globally standardized product may have gaps between countries.

_CGAZ_  - Comprehensive Global Administrative Zones. A global composite of the SSCGS ADM0, ADM1 and ADM2, with gaps filled between borders.  Also available at higher levels of simplification.

## Manual Data Retrieval

There are two ways to manually download geoBoundaries.  Option 1 is to use the GUI available on our website, located [here (simplified)](https://www.geoboundaries.org/downloadSimple.html) and [here (full precision)](https://www.geoboundaries.org/downloadFull.html).  This provides access to all of our current data, and provides visualizations for quick assessment.  

Additionally, you can access all geoBoundary files through the online HTML-based file browser, located at http://www.geoboundaries.org/data/ .  

## Programmatic / API Access
Full details on our API are available [here](https://www.geoboundaries.org/api.html).  

Information on every geoBoundary - current and past - can be retrieved through a simple query; a JSON object is returned:

```
https://www.geoboundaries.org/gbRequest.html?ISO=[3-LETTER-ISO-CODE]&ADM=[ADM-LEVEL]
```

Users can also enter special phrases "ALL" for either "ADM" or "ISO" to get a multi-boundary return (within the element 'geoBoundaries'). A full list of parameters users can include are:

-   **ISO**  - Optional; defaults to 'ALL'. The three-letter ISO code representing the country of interest. The special phrase 'ALL' can be entered to return all ISO codes in the database.
-   **ADM**  - Optional; defaults to 'ALL'. One of ADM0, ADM1, ADM2, ADM3, ADM4 or ADM5, representing each level of administrative hierarchy. The special phrase 'ALL' can be entered to return all levels available.
-   **VER**  - Optional; defaults to the most recent version of geoBoundaries available. The geoboundaries version requested, with underscores. For example, 3_0_0 would return data from version 3.0.0 of geoBoundaries.
-   **TYP**  - Optional; defaults to HPSCU. One of HPSCU, HPSCGS, SSCGS, or SSCU. Determines the type of boundary link you receive.



# geoBoundaries

![](https://www.geoboundaries.org/images/pic11.jpg)
Produced and maintained by the William & Mary [geoLab](http://geolab.wm.edu/) since 2017, the geoBoundaries Global Database of Political Administrative Boundaries Database is an online, open license resource of boundaries (i.e., state, county) for every country in the world. We currently track 199 total entities, including all 195 UN member states, Greenland, Taiwan, Niue, and Kosovo. All boundaries are available to view or download in common file formats, including shapefiles; the only requirement for use is [acknowledgement](https://www.geoboundaries.org/index.html#citation). The most up-to-date information about geoBoundaries can be found at www.geoboundaries.org.


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



## Contributing
We welcome new submissions to geoBoundaries, and will openly assess any submissions you might want to make that would improve our data. Right now, we accept submissions that are:

-   Compatible with the Open Data Commons Open Database License.
-   Of higher quality (either spatial or temporal) than our existing data.
-   Provisioned with clear and full metadata about the source of the file.

If you have a boundary (or set of boundaries) that you believe meets the above qualifications and you would like us to include, please either send us an email (team@geoboundaries.org) with the boundary data, or submit a new issue on our Github repository (https://github.com/wmgeolab/gbRelease/issues/new) that contains the country, source, and license of the boundary (all information must be verifiable). Once we receive your request, we will publish it on GitHub as an Issue (unless you created it already), and accept comments on the boundary until the next major point release of geoBoundaries.

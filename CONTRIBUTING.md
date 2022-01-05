# Contributor Guidelines

## Quick Start
Expert and just want to get started?  
**If you haven't used github in the past:**
You can use our [submission tool](https://www.geoboundaries.org/gbContribute.html) (**NEW!**). This tool will walk you through all of the data we need, and automatically generate the github pull request on your behalf.  Someone from our team will then review your submission.

**If you have used gitHub in the past:**
Take a look at [this example PR containing a boundary](https://github.com/wmgeolab/geoBoundaries/pull/1447) - the submission zip file has the exact formats you will need, including the meta.txt and license.png files. A more detailed explanation of the requirements are listed below.


## We welcome new submissions to geoBoundaries, and will openly assess any submissions that would improve our data. Right now, we accept submissions that are:

1. Compatible with the Open Data Commons Open Database License (or better). 
2. Of higher quality (spatially more accurate, representing more accurate divisions, or more recent) than our existing data. 
3. Provisioned with clear and full metadata about the source of the file.

If you have a boundary (or set of boundaries) that you believe meets the above qualifications and you would like us to include, please either send us an email (team@geoboundaries.org) with the boundary data, or submit a new issue on our Github repository (https://github.com/wmgeolab/geoBoundaries/issues/) that contains the country, source, and license of the boundary (all information must be verifiable). We are also happy to accept Pull Requests with the same information. Once we receive your request a multiple-stage review will commence in which: A) Automated checks are conducted on the validity of the data, and recommended changes are commented on the pull request; B) A human review team will assess the data to ensure its validity and improvement over our existing capabilities; C) We will open the boundary for comment; and D) If A-C look good, we'll accept it!



If you intend to submit a file for review, please follow our **standard conventions**. Three major components for each submission are needed (shapefile, meta.txt, license.png) stored in a zip file:

1. **Map Projection**
	1. Only files submitted in EPSG: 4326 (WGS84) will be accepted.
2. **Attribute Conventions**
	1. All files are to contain a capitalized ‘Name’ field, i.e. name of each administrative subunit (e.g. USA_ADM1 would include Alabama, Arkansas, etc.).  In some cases, this field may be left blank if names are not known.
	2. All files are to contain a capitalized ‘Level’ field, i.e. level of administrative division (ADM0, ADM1, etc.).  
	3. Special Standards for Submitting ADM0 or ADM1 shapes - ISO_Code - Files representing ADM0-1 are also to include ‘ISO_Code’ field (spelled as shown here), containing each subunit’s ISO 3166 code (ISO 3166-1 Alpha-3 or ISO 3166-2 Alpha-3).

3. **Metadata Conventions**
    1. Metadata should be saved as “meta.txt”, and should include the following information for each boundary submission in a plaintext file, spelled as is -
    2. Boundary Representative of Year: The year the geometry represents (NOT the year the data was produced!)
    3. ISO-3166-1 (Alpha-3):  3 digit ISO-3166 of Country
    4. Boundary Type: ADM0, ADM1, ADM2, ADM3, ADM4 or ADM5.
    5. Canonical Boundary Name: Name given to administrative level (district, arrondissement, province, etc.)
    6. Source 1: Primary source, i.e. where did you get this data? If you modified the polygons in this data, please list your organization in this field.
    7. Source 2: Secondary source if applicable, i.e. where did source 1 get this data?
    8. Release Type: One of gBOpen, gBHumanitarian, or gbAuthoritative.  We recommend most individuals submit to gbOpen and we can help sort into the appropriate class; if you are a power-user, the explicit licenses accepted by each release are noted [here](https://github.com/wmgeolab/geoBoundaryBot/blob/main/dta/gbLicenses.csv).
    9. License: Exact license type- list of acceptable licenses can be found [here](https://github.com/wmgeolab/geoBoundaryBot/blob/main/dta/gbLicenses.csv).  If you do not see your license on this list, and believe it should be, please do not hesitate to submit and start a conversation.
    10. License Notes: Any additional notes about the license that may be helpful.
    11. License Source: URL Link to License
    12. Link to Source Data: URL Link to Source Data
    13. Other Notes: Any other notes that may be useful in assessing the data.

4. **License Screenshot** - Each submission should include a license.png file, which is a screencapture of the source which provided the license for a given file.

**What’s a release type?**
	
Currently, geoBoundaries offers three datasets; gB OPEN, gB Authoritative, and gB Humanitarian. These datasets differ in licensure and usage, but follow the same attributional and metadata conventions listed above. gB OPEN contains data which is suitable for open use; CC-BY, ODbL, Public Domain, etc. gB Authoritative offers data sourced directly from the state it represents, e.g. the Mexican government offering MEX_ADM0-2. gB Humanitarian covers data which is licensed ‘for humanitarian use only’. A full list of acceptable license types for gB OPEN can be found at https://github.com/wmgeolab/geoBoundaryBot/blob/main/dta/gbLicenses.csv . 

**Contiguity**

We anticipate that most submitted boundaries will be contiguous, however, if the file you are submitting is genuinely non contiguous by nature (e.g. each canton (ADM2) of CHE has adminstrative agency to subdivide into districts (ADM3); some do not subdivide into districts, leading to a non contiguous CHE_ADM3 layer), we ask that you include relevant documentation for use in our wiki. Non contiguous files submitted without documentation will not be considered.

**Treatment of Water Boundaries**

geoBoundaries offers _terrestrial_ boundaries. Submissions of coastal or island state boundaries should contain only terrestrial boundaries and not extend into state-claimed waters.
	
**Bias and Representation of Disputed Territory**

geoBoundaries is committed to offering accurate, properly licensed and clearly documented administrative boundary data. A primary goal of geoBoundaries is to represent each state _as they represent themselves_ for individual state boundaries. As such, territories disputed between two states are given to both states (e.g. both IND and PAK files contain the Kashmir region with respective canonical naming conventions). Submissions which do not contain disputed territory claimed by a state will not be accepted.


Thank you!
The geoBoundaries Team

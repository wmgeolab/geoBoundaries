Current Contributor Guidelines

We welcome new submissions to geoBoundaries, and will openly assess any submissions that would improve our data. Right now, we accept submissions that are:



1. Compatible with the Open Data Commons Open Database License (or better). 
2. Of higher quality (either spatial or temporal) than our existing data. 
3. Provisioned with clear and full metadata about the source of the file.

If you have a boundary (or set of boundaries) that you believe meets the above qualifications and you would like us to include, please either send us an email (team@geoboundaries.org) with the boundary data, or submit a new issue on our Github repository (https://github.com/wmgeolab/geoBoundaries/issues/) that contains the country, source, and license of the boundary (all information must be verifiable). We are also happy to accept Pull Requests with the same information. Once we receive your request a multiple-stage review will commence in which: A) Automated checks are conducted on the validity of the data, and recommended changes are commented on the pull request; B) A human review team will assess the data to ensure its validity and improvement over our existing capabilities; C) We will open the boundary for comment; and D) If A-C look good, we'll accept it!

If you intend to submit a file for review, please follow our **standard conventions**. Three major components for each submission are needed (shapefile, meta.txt, license.png) stored in a zip file:



1. Map Projection
	1. Only files submitted in EPSG: 4326 (WGS84) will be accepted.
2. Attribute Conventions
	1. All files are to contain a capitalized ‘Name’ field, i.e. name of each administrative subunit (e.g. USA_ADM1 would include Alabama, Arkansas, etc.).  In some cases, this field may be left blank if names are not known.
        2. All files are to contain a capitalized ‘Level’ field, i.e. level of administrative division (ADM0, ADM1, etc.).  
    	3. Special Standards for Submitting ADM0 or ADM1 shapes - ISO_Code - Files representing ADM0-1 are also to include ‘ISO_Code’ field (spelled as shown here), containing each subunit’s ISO 3166 code (ISO 3166-1 Alpha-3 or ISO 3166-2 Alpha-3).
3. Metadata Conventions
    1. Metadata should be saved as “meta.txt”
    2. Metadata is to include the following information for each boundary submission in a plaintext file, spelled as is, separated by line:
        1. Boundary Representative of Year: 
            Year of last update to data
        2. ISO-3166-1 (Alpha-3):
            3 digit ISO-3166 of Country
        3. Boundary Type:
            ADM0-5
        4. Canonical Boundary Name:
            Name given to administrative level (district, arrondissement, province, etc.)
        5. Source 1: 
            A. Primary source, i.e. where did you get this data? 
            B. If you modified the polygons in this data, please list your organization in this field.
        6. Source 2:
            Secondary source if applicable, i.e. where did source 1 get this data?
        7. Release Type: 
            gB OPEN, gBHumanitarian, gBAuthoritative
                1. gB OPEN includes all licenses which are ‘open’
                2. gBHumanitarian includes ‘for humanitarian use only’ licenses, often HUMDATA/OCHA
                3. gBAuthoritative includes boundaries sourced from the governments themselves, i.e. Swiss Federal Office of Topology offering CHE_ADM0-2.
                    A. These may overlap with gB OPEN
        8. License: 
            Exact license type- list of acceptable licenses found &lt;here>
        9. License Notes: 
            Oddities in license
        10. License Source: 
            Link to license
        11. Link to Source Data: 
        12. Other Notes: 
            Any oddities or notes on data 

4. License Screenshot - Each submission should include a license.png file, which is a screencapture of the source which provided the license for a given file.

			

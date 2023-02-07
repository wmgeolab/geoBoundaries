# geoBoundaries
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-46-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
![image](https://user-images.githubusercontent.com/7882645/216724015-071055db-e635-418b-83a6-acbdde726c6c.png)
Built by the [community](https://github.com/wmgeolab/geoBoundaries/) and [William & Mary geoLab](https://geolab.wm.edu/), the geoBoundaries Global Database of Political Administrative Boundaries Database is an online, open license (CC BY 4.0) resource of information on administrative boundaries (i.e., state, county) for every country in the world. Since 2016, we have tracked approximately 1 million boundaries within over 200 entities, including all UN member states. All boundaries are available to view or download in common file formats; the only requirement for use is acknowledgement.

# Related Repositories
The geoBoundaries project is made up of a number of different repositories; you are currently on the core repo which stores all input datasets and builds.  If you are interested in understanding other components of geoBoundaries, you can visit:
- [geoBoundaryBot](https://github.com/wmgeolab/geoBoundaryBot): where our build scripts live, as well as the various QA/QC algorithms applied to pull requests in this repository.  If you're interested in the specifics of our topology checks or simplification strategies, this is where to look.
- [gbWeb](https://github.com/wmgeolab/gbWeb): where the website itself lives, as well as the API.  Various scripts that aid in building the API and other things related to the website can be found here as well.
- [rgeoboundaries](https://github.com/wmgeolab/rgeoboundaries): built by community member @dickoa, this library allows you to retrieve and manipulate geoBoundaries data within the R programming environment.
- [pygeoboundaries](https://github.com/ibhalin/pygeoboundaries) built by community member @ibhalin, this package allows you to retrieve and manipulate geoBoundires data within the python programming environmennt.

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
geoBoundaries 5.0.0 | December 19, 2022 | [997c6a8](https://github.com/wmgeolab/geoBoundaries/tree/b7dd6a55701c76a330500ad9d9240f2b9997c6a8)
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

## Note on Cloning

As of geoBoundaries 5.0.0, all files in geoBoundaries are stored using Git's Large File Storage (LFS).  Because this entails such a large volume of files, a bug in the current GitHub API results in a rate limiting error if you attempt to clone using https methods (i.e., ``git clone https://github.com/wmgeolab/geoBoundaries.git`` will fail with a rate limiting error).  Cloning with SSH (``git clone git@github.com:wmgeolab/geoBoundaries.git``) and the GitHub CLI (``gh repo clone wmgeolab/geoBoundaries``) work without issue. 

## Contributors

geoBoundaries wouldn't be possible without our community ❤️❤️. \
Key to contributions: \
:computer: - Contributed code to the project.\
:cd: - Contributed data to the project.\
:blue_book: - Helped with documentation or other training materials.\
:technologist: - Helped with QA/QC and accepting data into the repository.\
:gear: - Flagged/Identified an issue in the database, or came up with a great idea.

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://geolab.wm.edu"><img src="https://avatars.githubusercontent.com/u/7882645?v=4?s=100" width="100px;" alt="Dan Runfola"/><br /><sub><b>Dan Runfola</b></sub></a><br /><a href="[:computer:](https://github.com/wmgeolab/geoBoundaries/ "Code")," title="Code">:computer:</a> <a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a> <a href="[:blue_book:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:blue_book:</a> <a href="[:gear:](https://github.com/wmgeolab/geoBoundaries/ "Issues & Ideas")," title="Issues & Ideas">:gear:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kovaca"><img src="https://avatars.githubusercontent.com/u/5686693?v=4?s=100" width="100px;" alt="Alex Kovac"/><br /><sub><b>Alex Kovac</b></sub></a><br /><a href="[:computer:](https://github.com/wmgeolab/geoBoundaries/ "Code")," title="Code">:computer:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/slfuhrig"><img src="https://avatars.githubusercontent.com/u/49990394?v=4?s=100" width="100px;" alt="slfuhrig"/><br /><sub><b>slfuhrig</b></sub></a><br /><a href="[:computer:](https://github.com/wmgeolab/geoBoundaries/ "Code")," title="Code">:computer:</a> <a href="[:blue_book:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:blue_book:</a> <a href="[:technologist:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:technologist:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/sylviashea1"><img src="https://avatars.githubusercontent.com/u/55154868?v=4?s=100" width="100px;" alt="Sylvia Shea"/><br /><sub><b>Sylvia Shea</b></sub></a><br /><a href="[:blue_book:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:blue_book:</a> <a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a> <a href="[:technologist:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:technologist:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/helenabuckman"><img src="https://avatars.githubusercontent.com/u/70856803?v=4?s=100" width="100px;" alt="helenabuckman"/><br /><sub><b>helenabuckman</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/larogersWM"><img src="https://avatars.githubusercontent.com/u/70722024?v=4?s=100" width="100px;" alt="Lindsey Rogers"/><br /><sub><b>Lindsey Rogers</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kpupkiewicz"><img src="https://avatars.githubusercontent.com/u/70856698?v=4?s=100" width="100px;" alt="kpupkiewicz"/><br /><sub><b>kpupkiewicz</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/memulder"><img src="https://avatars.githubusercontent.com/u/67922294?v=4?s=100" width="100px;" alt="Maddy Mulder"/><br /><sub><b>Maddy Mulder</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/carolinamonrivera"><img src="https://avatars.githubusercontent.com/u/70854437?v=4?s=100" width="100px;" alt="carolinamonrivera"/><br /><sub><b>carolinamonrivera</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.researchgate.net/profile/karim-bahgat"><img src="https://avatars.githubusercontent.com/u/6413369?v=4?s=100" width="100px;" alt="Karim Bahgat"/><br /><sub><b>Karim Bahgat</b></sub></a><br /><a href="[:computer:](https://github.com/wmgeolab/geoBoundaries/ "Code")," title="Code">:computer:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/SamUpdike"><img src="https://avatars.githubusercontent.com/u/70855947?v=4?s=100" width="100px;" alt="SamUpdike"/><br /><sub><b>SamUpdike</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jrhabib"><img src="https://avatars.githubusercontent.com/u/70856754?v=4?s=100" width="100px;" alt="Josh"/><br /><sub><b>Josh</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jdturner303"><img src="https://avatars.githubusercontent.com/u/70858775?v=4?s=100" width="100px;" alt="jdturner303"/><br /><sub><b>jdturner303</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dorianvmiller"><img src="https://avatars.githubusercontent.com/u/70725306?v=4?s=100" width="100px;" alt="dorianvmiller"/><br /><sub><b>dorianvmiller</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://www.linkedin.com/in/hannah-slevin/"><img src="https://avatars.githubusercontent.com/u/54992420?v=4?s=100" width="100px;" alt="Hannah Slevin"/><br /><sub><b>Hannah Slevin</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/oforiaddaejnr"><img src="https://avatars.githubusercontent.com/u/25621519?v=4?s=100" width="100px;" alt="oforiaddaejnr"/><br /><sub><b>oforiaddaejnr</b></sub></a><br /><a href="[:computer:](https://github.com/wmgeolab/geoBoundaries/ "Code")," title="Code">:computer:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/neelsimpson"><img src="https://avatars.githubusercontent.com/u/70907487?v=4?s=100" width="100px;" alt="Neel Simpson"/><br /><sub><b>Neel Simpson</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/SidonieH"><img src="https://avatars.githubusercontent.com/u/70904764?v=4?s=100" width="100px;" alt="Sidonie"/><br /><sub><b>Sidonie</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nmspage"><img src="https://avatars.githubusercontent.com/u/68017504?v=4?s=100" width="100px;" alt="nmspage"/><br /><sub><b>nmspage</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MichaelR-geoLab"><img src="https://avatars.githubusercontent.com/u/70650770?v=4?s=100" width="100px;" alt="Michael Roth"/><br /><sub><b>Michael Roth</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/rsritchey"><img src="https://avatars.githubusercontent.com/u/77251857?v=4?s=100" width="100px;" alt="rsritchey"/><br /><sub><b>rsritchey</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/charliealtman"><img src="https://avatars.githubusercontent.com/u/77692298?v=4?s=100" width="100px;" alt="charliealtman"/><br /><sub><b>charliealtman</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/taraamcl"><img src="https://avatars.githubusercontent.com/u/77515858?v=4?s=100" width="100px;" alt="taraamcl"/><br /><sub><b>taraamcl</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/iaschreur"><img src="https://avatars.githubusercontent.com/u/70705524?v=4?s=100" width="100px;" alt="iaschreur"/><br /><sub><b>iaschreur</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/lydiatroup"><img src="https://avatars.githubusercontent.com/u/60264585?v=4?s=100" width="100px;" alt="Lydia Troup"/><br /><sub><b>Lydia Troup</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a> <a href="[:blue_book:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:blue_book:</a> <a href="[:technologist:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:technologist:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/rmbiddle"><img src="https://avatars.githubusercontent.com/u/78105842?v=4?s=100" width="100px;" alt="rmbiddle"/><br /><sub><b>rmbiddle</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dfornatora"><img src="https://avatars.githubusercontent.com/u/70817875?v=4?s=100" width="100px;" alt="Dominic Fornatora"/><br /><sub><b>Dominic Fornatora</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hadleyday"><img src="https://avatars.githubusercontent.com/u/70859534?v=4?s=100" width="100px;" alt="Hadley Day"/><br /><sub><b>Hadley Day</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ceedwards1"><img src="https://avatars.githubusercontent.com/u/74315012?v=4?s=100" width="100px;" alt="Caroline Edwards"/><br /><sub><b>Caroline Edwards</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nirajpatel10122"><img src="https://avatars.githubusercontent.com/u/59022421?v=4?s=100" width="100px;" alt="nirajpatel10122"/><br /><sub><b>nirajpatel10122</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jcsiwek"><img src="https://avatars.githubusercontent.com/u/74273985?v=4?s=100" width="100px;" alt="Jane Siwek"/><br /><sub><b>Jane Siwek</b></sub></a><br /><a href="[:technologist:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:technologist:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/owachob"><img src="https://avatars.githubusercontent.com/u/75225935?v=4?s=100" width="100px;" alt="Olivia Wachob"/><br /><sub><b>Olivia Wachob</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/fpate"><img src="https://avatars.githubusercontent.com/u/60228490?v=4?s=100" width="100px;" alt="fpate"/><br /><sub><b>fpate</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.pathwaysdata.com"><img src="https://avatars.githubusercontent.com/u/23552439?v=4?s=100" width="100px;" alt="Lee Berryman"/><br /><sub><b>Lee Berryman</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/sgmurphy216"><img src="https://avatars.githubusercontent.com/u/68017245?v=4?s=100" width="100px;" alt="Sean Murphy"/><br /><sub><b>Sean Murphy</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a> <a href="[:technologist:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:technologist:</a> <a href="[:blue_book:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:blue_book:</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mlwilliams01"><img src="https://avatars.githubusercontent.com/u/67924018?v=4?s=100" width="100px;" alt="mlwilliams01"/><br /><sub><b>mlwilliams01</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ssheminway"><img src="https://avatars.githubusercontent.com/u/90479751?v=4?s=100" width="100px;" alt="Selwyn Heminway"/><br /><sub><b>Selwyn Heminway</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/shauntmathew"><img src="https://avatars.githubusercontent.com/u/90479830?v=4?s=100" width="100px;" alt="shauntmathew"/><br /><sub><b>shauntmathew</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/heatherbaier"><img src="https://avatars.githubusercontent.com/u/44214106?v=4?s=100" width="100px;" alt="Heather Baier"/><br /><sub><b>Heather Baier</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a> <a href="[:blue_book:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:blue_book:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/VictorGedeck"><img src="https://avatars.githubusercontent.com/u/69996575?v=4?s=100" width="100px;" alt="Victor Gedeck"/><br /><sub><b>Victor Gedeck</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jingjli1"><img src="https://avatars.githubusercontent.com/u/98781786?v=4?s=100" width="100px;" alt="Jing Li"/><br /><sub><b>Jing Li</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/maxmalynowsky"><img src="https://avatars.githubusercontent.com/u/4202166?v=4?s=100" width="100px;" alt="Max Malynowsky"/><br /><sub><b>Max Malynowsky</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a> <a href="[:computer:](https://github.com/wmgeolab/geoBoundaries/ "Code")," title="Code">:computer:</a> <a href="[:technologist:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:technologist:</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jcourson"><img src="https://avatars.githubusercontent.com/u/13521890?v=4?s=100" width="100px;" alt="Jim Courson"/><br /><sub><b>Jim Courson</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Sarangaban"><img src="https://avatars.githubusercontent.com/u/113078405?v=4?s=100" width="100px;" alt="Sarangaban"/><br /><sub><b>Sarangaban</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/JialuT"><img src="https://avatars.githubusercontent.com/u/78135581?v=4?s=100" width="100px;" alt="JialuT"/><br /><sub><b>JialuT</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jshobart"><img src="https://avatars.githubusercontent.com/u/113035902?v=4?s=100" width="100px;" alt="jshobart"/><br /><sub><b>jshobart</b></sub></a><br /><a href="[:cd:](https://github.com/wmgeolab/geoBoundaries/ "Data")," title="Data">:cd:</a></td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td align="center" size="13px" colspan="7">
        <img src="https://raw.githubusercontent.com/all-contributors/all-contributors-cli/1b8533af435da9854653492b1327a23a4dbd0a10/assets/logo-small.svg">
          <a href="https://all-contributors.js.org/docs/en/bot/usage">Add your contributions</a>
        </img>
      </td>
    </tr>
  </tfoot>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

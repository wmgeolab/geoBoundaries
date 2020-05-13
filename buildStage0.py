#######
#Build stage 0 for the geoBoundaries Release.
#This stage checks all metadata fields exist and are valid before proceeding.
#######

import os
import urllib.request
import importlib
import zipfile
import pandas as pd
import pathlib
import sys
import datetime
import requests
from urllib3.exceptions import InsecureRequestWarning

#Note:To ensure that the exact files desired are included in a build,
#it is required the user manually upload a single zipFile.  
#The zip file should be a *copy* of everything in "current".
#Note the metadata file must be in excel format.

def retrieveZip(buildID):
  if(os.path.isfile("./releaseCandidateZips/" + buildID + ".zip")):
    print("++ Zipfile is already available, proceeding without downloading.")
  else:
    try:
      auto_url = "http://www.geoboundaries.org/rcs/" + buildID + ".zip"
      print("++ Attempting to download from URL " + auto_url + ".")
      urllib.request.urlretrieve(auto_url, "./releaseCandidateZips/" + buildID + ".zip")
    except:
      print("CRITICAL: File download failed.")
      sys.exit("Error: No zip file existed, and the file download failed.")

  if(os.path.isdir("./releaseCandidateRaw/" + buildID + "/")):
    print("++ Release has already been unzipped.  Skipping.")
  else:
    print("++ Unzipping the contents of the retrieved zip file.")
    with zipfile.ZipFile("./releaseCandidateZips/" + buildID + ".zip", "r") as zipObj:
      zipObj.extractall("./releaseCandidateRaw/")
  

def metaDataChecks(buildID, exceptions):
  try:
    metaData_folder = "./releaseCandidateRaw/" + buildID + "/metadata/"
    metaFiles = [f for f in os.listdir(metaData_folder) if os.path.isfile(os.path.join(metaData_folder, f))]
    metaData = pd.read_excel(metaData_folder + metaFiles[0])
  except:
    print("CRITICAL: The provided release zip is invalid." +
          "It must have a single metadata excel file in the metadata folder.")
    sys.exit("Error: No metadata file existed.")
  
  if(os.path.isfile("./build_logs/success/" + buildID + "_metaData.csv")):
    print("++ Metadata checks have already succesfully passed for this release. Skipping.")
  else:
    #Conduct metadata checks
    iso_name_Dta = pd.read_csv("./ISO_3166_1_Alpha_3.csv", encoding="ISO-8859-1")  
    
    files_exist_pass = 1
    name_pass = 1
    iso_pass = 1
    source_pass = 1
    license_pass = 1
    link_pass = 1
    pass_flag = 1

    total_count = len(metaData.index)

    #Load in a list of all existant zipfiles in the version
    posix_existing_paths = list(pathlib.Path("./releaseCandidateRaw/" + buildID + "/").rglob("*"))
    existing_paths = [os.fspath(item) for item in posix_existing_paths]

    for index, row in metaData.iterrows():
      print("Processing Metadata (" +  str(index) +" | " + str(total_count) + ") " + str(row["Processed File Name"]))
      #Check the file name is valid and exists in the zipfile
      length = len(str(row["Processed File Name"]))

      if(length != 12):
        metaData.loc[index, "Process File Name QA Check"] = "The processed file name has too many characters.  It needs to be of the format 'XXX_YYY.ZIP'."
        pass_flag = 0
        name_pass = 0 
      else:
        metaData.loc[index, "Process File Name QA Check"] = ""

      ADM_code = str(row["Processed File Name"])[:3]
      
      if(not ADM_code in iso_name_Dta["Alpha-3code"].values):
        pass_flag = 0
        iso_pass = 0
        metaData.loc[index, "File Name ISO Code"] = ("The first three characters of the file"+
                                                     "are not a valid ISO code: " + (ADM_code))

      else:
        metaData.loc[index, "File Name ISO Code"] = ""


      #Check file reference exists
      expected_path = ("releaseCandidateRaw/" + str(buildID) + "/" + 
                       str(row["Boundary Level"]).replace(" ", "") + "/" + 
                      str(row["Processed File Name"]))
      if(not expected_path in existing_paths):
        print("No exist.")
        pass_flag = 0
        files_exist_pass = 0
        metaData.loc[index, "Process File Name Existance Check"] = "This file does not exist, or either the 'Processed File Name' or 'Boundary' are incorrect in the metadata.  File should be at /ADM0/'Processed File Name'_'Boundary'.zip." 
      else:
        metaData.loc[index, "Process File Name Existance Check"] = ""

      if(pd.isnull(metaData.loc[index]["Source 1"]) and pd.isnull(metaData.loc[index]["Source 2"])):
        pass_flag = 0
        source_pass = 0
        metaData.loc[index, "Source Check"] = "You must have at least one source."
      else:
        metaData.loc[index, "Source Check"] = ""


      acceptable_licenses = ["Attribuzione 3.0 Italia (CC BY 3.0 IT)",
                            "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
                            "Creative Commons Attribution - NonCommercial 4.0 International (CC BY-NC 4.0)",
                            "Creative Commons Attribution 2.5 India (CC BY 2.5 IN)",
                            "Creative Commons Attribution 3.0 License",
                            "Creative Commons Attribution 4.0 International (CC BY 4.0)",
                            "Creative Commons Attribution for Intergovernmental Organisations (CC BY-IGO)",
                            "Creative Commons Attribution-EqualShare 3.0 Unported (CC BY-SA 3.0)",
                            "Creative Commons Attribution-ShareAlike 2.0",
                            "Creative Commons Attribution-ShareAlike 3.0 Unported",
                            "Creative Commons Attribution-ShareAlike 4.0 International License",
                            "Data license Germany - Attribution - Version 2.0",
                            "MIMU Data License (MIMU)",
                            "Non-Commercial Use Only",
                            "Open Data Commons Attribution License 1.0",
                            "Open Data Commons Open Database License 1.0",
                            "Open Government Licence v3.0",
                            "Open Government License v1.0",
                            "Other - Direct Permission",
                            "Other - Humanitarian",
                            "Other - Organization Specific",
                            "Public Domain",
                            "Singapore Open Data License Version 1.0",
                            "Creative Commons Attribution-ShareAlike 3.0 Germany"]

      

      #Check the license field matches one of the acceptable licenses.
      if(not (row["License"] in acceptable_licenses)):
        metaData.loc[index, "License Check"] = ("The license is not on the list of " +
                                                "acceptable licenses.  Check the " + 
                                                "geolab.wm.edu/data geoBoundaries " + 
                                                "page for the most recent list of " + 
                                                "acceptable license types.  You may " + 
                                                "also use 'Other' and place the license " + 
                                                "details in the license details column.")
        license_pass = 0
        pass_flag = 0

      else:
        metaData.loc[index, "License Check"] = ""


      #Check if the license type is "Other" that ther eis a license detail.
      if(row["License"] == "Other"):
        if(pd.isnull(row["License Detail"])):
          license_pass = 0
          pass_flag = 0
          metaData.loc[index, "License Detail Check"] = ("If license type is other, " +
                                                         "you must enter the license " +
                                                         "detail.")
        elif(len(row["License Detail"]) < 1):
          license_pass = 0
          pass_flag = 0
          metaData.loc[index, "License Detail Check"] = ("If license type is other, " +
                                                         "you must enter the license " +
                                                         "detail.")

      
      #Cache web URLs so we aren't bouncing against them more than we need to.
      webCache = []
      
      #Suppress errors originating from SSL verification ignore option
      requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
      
      #Check the license source exists *and can load*.  Must be a resolvable URL.
      #Students should create a tweet with relevant license data to cite if
      #an informal source / screenshot etc.
      try:
        if(pd.isnull(row["License Source"])):
          license_pass = 0
          pass_flag = 0
          metaData.loc[index, "License Source Check"] = ("You must enter a license source. " +
                                                         "Further, the source must be a URL "+
                                                         "and that URL must work today. " +
                                                         "If there is no URL, for example "+
                                                         "if the website is down or it " +
                                                         "was personal communications, " +
                                                         "use the geoLab twitter via Slack " +
                                                         "to create a tweet with the appropriate " +
                                                         "screenshot, along with the message " +
                                                         "Thanks to _____ for making their data public!" +
                                                         "and use the URL to that tweet as the License Source."
                                                        )
        elif(len(row["License Source"]) < 1):
          license_pass = 0
          pass_flag = 0
          metaData.loc[index, "License Source Check"] = ("You must enter a license source. " +
                                                         "Further, the source must be a URL "+
                                                         "and that URL must work today. " +
                                                         "If there is no URL, for example "+
                                                         "if the website is down or it " +
                                                         "was personal communications, " +
                                                         "use the geoLab twitter via Slack " +
                                                         "to create a tweet with the appropriate " +
                                                         "screenshot, along with the message " +
                                                         "Thanks to _____ for making their data public!" +
                                                         "and use the URL to that tweet as the License Source."
                                                        )


        elif(row["License Source"] in exceptions[buildID]["URL"]):
          metaData.loc[index, "License Source Check"] = ""
      
      
        #Check if the website has already been verified this run.  If so, skip.
        elif(row["License Source"] in webCache):
          metaData.loc[index, "License Source Check"] = ""
          
      #Check source license URL exists.
        elif(not str(requests.get(row["License Source"], verify=False)) == '<Response [200]>'):
          license_pass = 0
          pass_flag = 0
          metaData.loc[index, "License Source Check"] = ("You must enter a license source. " +
                                                         "Further, the source must be a URL "+
                                                         "and that URL must work today. " +
                                                         "If there is no URL, for example "+
                                                         "if the website is down or it " +
                                                         "was personal communications, " +
                                                         "use the geoLab twitter via Slack " +
                                                         "to create a tweet with the appropriate " +
                                                         "screenshot, along with the message " +
                                                         "Thanks to _____ for making their data public!" +
                                                         "and use the URL to that tweet as the License Source."
                                                        )

        else:
          metaData.loc[index, "License Source Check"] = ""
          webCache.append(row["License Source"])

      except:
        metaData.loc[index, "License Source Check"] = ("Something went wrong when we were checking the license source URL." +
                                                      "This can be indicative of many things, but frequently means the license source "+
                                                      "URL is invalid.  Double check what's going on!")

      try: 
        if(pd.isnull(row["Link to Source Data"])):
          link_pass = 0
          pass_flag = 0
          metaData.loc[index, "Link to Source Data Check"] = ("You must enter a data source. " +
                                                         "Further, the source must be a URL "+
                                                         "and that URL must work today. " +
                                                         "If there is no URL, for example "+
                                                         "if the website is down or it " +
                                                         "was personal communications, " +
                                                         "use the geoLab twitter via Slack " +
                                                         "to create a tweet with the appropriate " +
                                                         "screenshot, along with the message " +
                                                         "Thanks to _____ for making their data public!" +
                                                         "and use the URL to that tweet as the data source."
                                                        )
        elif(len(row["Link to Source Data"]) < 1):
          link_pass = 0
          pass_flag = 0
          metaData.loc[index, "Link to Source Data Check"] = ("You must enter a data source. " +
                                                         "Further, the source must be a URL "+
                                                         "and that URL must work today. " +
                                                         "If there is no URL, for example "+
                                                         "if the website is down or it " +
                                                         "was personal communications, " +
                                                         "use the geoLab twitter via Slack " +
                                                         "to create a tweet with the appropriate " +
                                                         "screenshot, along with the message " +
                                                         "Thanks to _____ for making their data public!" +
                                                         "and use the URL to that tweet as the data source."
                                                        )


        elif(row["Link to Source Data"] in exceptions[buildID]["URL"]):
          metaData.loc[index, "Link to Source Data Check"] = ""
        
        #Check if the website has already been verified this run.  If so, skip.
        elif(row["Link to Source Data"] in webCache):
          metaData.loc[index, "Link to Source Data Check"] = ""
        
      #Check source license URL exists.
        elif(not str(requests.get(row["Link to Source Data"], verify=False)) == '<Response [200]>'):
          link_pass = 0
          pass_flag = 0
          metaData.loc[index, "Link to Source Data Check"] = ("You must enter a data source. " +
                                                         "Further, the source must be a URL "+
                                                         "and that URL must work today. " +
                                                         "If there is no URL, for example "+
                                                         "if the website is down or it " +
                                                         "was personal communications, " +
                                                         "use the geoLab twitter via Slack " +
                                                         "to create a tweet with the appropriate " +
                                                         "screenshot, along with the message " +
                                                         "Thanks to _____ for making their data public!" +
                                                         "and use the URL to that tweet as the License Source."
                                                        )

        else:
          metaData.loc[index, "Link to Source Data Check"] = ""
          webCache.append(row["Link to Source Data"])
      except:
        metaData.loc[index, "Link to Source Data Check"] = ("Something went wrong with our check of the data source URL. This error can indicate many things, " +
                                                           "but frequently means the URL is invalid (i.e., it's not actually a URL).")


        
    #Output to terminal.
    print("")
    if(name_pass == 0):
        print("All processed file names correct length................... FAILED") 
    else:
        print("All processed file names correct length................... PASSED") 

    if(iso_pass == 0):
        print("All processed file names correct ISO...................... FAILED") 
    else:
        print("All processed file names correct ISO...................... PASSED") 

    if(files_exist_pass == 0):
        print("All processed file names exist............................ FAILED") 
    else:
        print("All processed file names exist............................ PASSED") 

    if(source_pass == 0):
        print("All processed files have a source......................... FAILED") 
    else:
        print("All processed files have a source......................... PASSED")


    if(license_pass == 0):
        print("All processed files have a valid license with link........ FAILED") 
    else:
        print("All processed files have a valid license with link........ PASSED")


    if(link_pass == 0):
        print("All processed files have a source link.................... FAILED") 
    else:
        print("All processed files have a source link.................... PASSED")


    if(pass_flag != 1):
      print("CRITICAL ERROR: At least one metadata check failed, and the build will halt.")

      error_csv_path = ("./build_logs/" + buildID + "_metaCheckFailure_" + str(datetime.datetime.timestamp(datetime.datetime.now())) + ".csv") 
      metaData.to_csv(error_csv_path)
      print("A debug file has been output to:" + error_csv_path)
      sys.exit("Metadata check failed.")
    else:
      print("All Metadata Checks Passed.")
      metaData.to_csv("./build_logs/success/" + buildID + "_metaData.csv")
  

    

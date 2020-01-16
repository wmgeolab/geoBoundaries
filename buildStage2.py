import pandas as pd
import os

def metaStandardization(buildID):
  metaData_folder = "./releaseCandidateRaw/" + buildID + "/metadata/"
  metaFiles = [f for f in os.listdir(metaData_folder) if os.path.isfile(os.path.join(metaData_folder, f))]
  metaData = pd.read_excel(metaData_folder + metaFiles[0])
  
  

  metaData["boundaryID"] = "ERROR"
  metaData["boundaryISO"] = "ERROR"
  metaData["boundaryYear"] = "ERROR"
  metaData["boundaryType"] = "ERROR"
  metaData["boundarySource-1"] = "ERROR"
  metaData["boundarySource-2"] = "ERROR"
  metaData["boundaryLicense"] = "ERROR"
  metaData["licenseDetail"] = "ERROR"
  metaData["licenseSource"] = "ERROR"
  metaData["boundarySourceURL"] = "ERROR"
  metaData["boundaryUpdate"] = "ERROR"
  metaData["downloadURL"] = "ERROR"
  
  bndCnt = 0
  for i, row in metaData.iterrows():
    bndCnt = bndCnt + 1
    rowISO = row["Processed File Name"][:3]
    rowADM = row["Boundary Level"].replace(" ","")
    rowGroup = ["boundaryGroup"]
    
    #Create unique ID for each row
    metaData.at[i,'boundaryID'] = rowISO + "-" + rowADM + "-" + buildID.split('_', 1)[1] + "-G" + str(bndCnt)
    
    #Save ISO for each row
    metaData.at[i, 'boundaryISO'] = rowISO
    
    #Save Year
    metaData.at[i, "boundaryYear"] = row["Year"]
    
    #Save Type
    metaData.at[i, "boundaryType"] = rowADM
    
    #Save sources
    metaData.at[i, "boundarySource-1"] = row["Source 1"]
    metaData.at[i, "boundarySource-2"] = row["Source 2"]
    
    #License
    metaData.at[i, "boundaryLicense"] = row["License"]
    
    #License Detail
    metaData.at[i, "licenseDetail"] = row["License Detail"]
    
    #License Source
    metaData.at[i, "licenseSource"] = row["License Source"]
    
    #Boundary Source URL
    metaData.at[i, "boundarySourceURL"] = row["Link to Source Data"]
    

    if(not str(row["Last Updated Date"]).find("-") == -1):
      metaData.at[i, "boundaryUpdate"] = str(pd.to_datetime(row["Last Updated Date"], format='%Y-%m-%d', errors="coerce").date())
    else:
      metaData.at[i, "boundaryUpdate"] = str(pd.to_datetime('today', format='%Y-%m-%d', errors='ignore').date())
    
    #Download URL
    fullURL = "https://geoboundaries.org/data/geoBoundaries-" + buildID.split('_', 1)[1] + "/" + rowISO + "/" + rowADM + "/"
    fullFile = "geoBoundaries-" + buildID.split('_', 1)[1] + "-" + rowISO + "-" + rowADM + "-all.zip"
    metaData.at[i, "downloadURL"] = fullURL + fullFile
    
    #Confirm there are no remaining errors.  There should not be at this stage, so this exits the build.  
    if(not all(metaData.iloc[i].str.contains('ERROR', na=False) == False)):
      lFile = logID = ("./build_logs/" + buildID + "_metaBuildStep_" + str(datetime.datetime.timestamp(datetime.datetime.now())) + ".csv")
      metaData.to_csv(lFile)
      print("At least one error remains in the metaData, which must be corrected.")
      print("Check the log at: " + lFile)
      sys.exit("Build failed.")
    
  
  cleanMeta = metaData[["boundaryID", "boundaryISO", "boundaryYear", "boundaryType",
                         "boundarySource-1", "boundarySource-2", "boundaryLicense", "licenseDetail",
                         "licenseSource", "boundarySourceURL", "boundaryUpdate", "downloadURL"]]

  
  
  
  
  #Generate the final CSV for the package.
  cleanMeta.to_csv("./releaseCandidateInit/" + buildID + "/" + buildID + ".csv", index=False)
    
  
  
  
if __name__ == "__main__": 
  import buildMain
  importlib.reload(buildMain)
  buildMain.geoBoundaries_build("gbReleaseCandidate_2_0_0_0")
  
  

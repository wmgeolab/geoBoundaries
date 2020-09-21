#Script to move metadata from unified CSVs to individual zip files.
#Should allow for easier push/pulls for distributed workflows.

import zipfile
import pandas as pd
import shutil
import os

baseDir = "/home/dan/git/gbRelease/"

gbA = pd.read_csv(baseDir + "sourceData/gbAuthoritativeMetaData.csv", encoding='latin1')


for index, row in gbA.iterrows():
    iso = row["Processed File Name"][:3]
    adm = row["Processed File Name"][:-4][4:]
    authPath = baseDir + "sourceData/gbAuthoritative/" + iso + "_" + adm + ".zip"



#Create *.txt in a temporary directory
    with open('metaExample.txt', 'w+') as txtWrite:
        txtWrite.write("Boundary Representative of Year: "+ str(row["Year"]) +"\n")
        txtWrite.write("ISO-3166-1 (Alpha-3): "+str(iso)+"\n")
        txtWrite.write("Boundary Type: "+str(adm)+"\n")
        txtWrite.write("Canonical Boundary Type Name: \n")
        txtWrite.write("Source 1: "+str(row["Source 1"])+"\n")
        txtWrite.write("Source 2: "+str(row["Source 2"])+"\n")
        txtWrite.write("Release Type: gbAuthoritative\n")
        txtWrite.write("License: "+str(row["License"])+"\n")
        txtWrite.write("License Notes: "+str(row["License Detail"]) +"\n")
        txtWrite.write("License Source: "+str(row["License Source"])+"\n")
        txtWrite.write("Link to Source Data: "+str(row["Link to Source Data"])+"\n")
        txtWrite.write("Other Notes: ")

    if(os.path.exists(authPath)):
        bWrite = zipfile.ZipFile(authPath, 'a')
        if("meta.txt" not in bWrite.namelist()):
            bWrite.write('metaExample.txt', 'meta.txt')
        bWrite.close()

    else:
        print("Something Authoritative is missing!" + str(iso) + "_" + str(adm))

    
##gbOpen
gbA = pd.read_csv(baseDir + "sourceData/gbOpenMetaData.csv", encoding='latin1')


for index, row in gbA.iterrows():
    iso = row["Processed File Name"][:3]
    adm = row["Processed File Name"][:-4][4:]
    openPath = baseDir + "sourceData/gbOpen/" + iso + "_" + adm + ".zip"

#Create *.txt in a temporary directory
    with open('metaExample.txt', 'w+') as txtWrite:
        txtWrite.write("Boundary Representative of Year: "+ str(row["Year"]) +"\n")
        txtWrite.write("ISO-3166-1 (Alpha-3): "+str(iso)+"\n")
        txtWrite.write("Boundary Type: "+str(adm)+"\n")
        txtWrite.write("Canonical Boundary Type Name: \n")
        txtWrite.write("Source 1: "+str(row["Source 1"])+"\n")
        txtWrite.write("Source 2: "+str(row["Source 2"])+"\n")
        txtWrite.write("Release Type: gbOpen\n")
        txtWrite.write("License: "+str(row["License"])+"\n")
        txtWrite.write("License Notes: "+str(row["License Detail"]) +"\n")
        txtWrite.write("License Source: "+str(row["License Source"])+"\n")
        txtWrite.write("Link to Source Data: "+str(row["Link to Source Data"])+"\n")
        txtWrite.write("Other Notes: ")

    if(os.path.exists(openPath)):
        bWrite = zipfile.ZipFile(openPath, 'a')
        if("meta.txt" not in bWrite.namelist()):
            bWrite.write('metaExample.txt', 'meta.txt')
        bWrite.close()

    else:
        print("Something Open is missing!" + str(iso) + "_" + str(adm))

##gbHum
gbA = pd.read_csv(baseDir + "sourceData/gbHumanitarianMetaData.csv", encoding='latin1')


for index, row in gbA.iterrows():
    iso = row["Processed File Name"][:3]
    adm = row["Processed File Name"][:-4][4:]

    humPath = baseDir + "sourceData/gbHumanitarian/" + iso + "_" + adm + ".zip"

#Create *.txt in a temporary directory
    with open('metaExample.txt', 'w+') as txtWrite:
        txtWrite.write("Boundary Representative of Year: "+ str(row["Year"]) +"\n")
        txtWrite.write("ISO-3166-1 (Alpha-3): "+str(iso)+"\n")
        txtWrite.write("Boundary Type: "+str(adm)+"\n")
        txtWrite.write("Canonical Boundary Type Name: \n")
        txtWrite.write("Source 1: "+str(row["Source 1"])+"\n")
        txtWrite.write("Source 2: "+str(row["Source 2"])+"\n")
        txtWrite.write("Release Type: gbOpen\n")
        txtWrite.write("License: "+str(row["License"])+"\n")
        txtWrite.write("License Notes: "+str(row["License Detail"]) +"\n")
        txtWrite.write("License Source: "+str(row["License Source"])+"\n")
        txtWrite.write("Link to Source Data: "+str(row["Link to Source Data"])+"\n")
        txtWrite.write("Other Notes: ")

    if(os.path.exists(humPath)):
        bWrite = zipfile.ZipFile(humPath, 'a')
        if("meta.txt" not in bWrite.namelist()):
            bWrite.write('metaExample.txt', 'meta.txt')
        bWrite.close()

    else:
        print("Something Humanitarian is missing!" + str(iso) + "_" + str(adm))   




print("Done.")
import requests
import pandas as pd

df = pd.read_csv("/home/dan/git/gbRelease/ancillaryData/ingestScripts/ADM0.csv", index_col=0, header=[0,1], skiprows=[0,3,4], dtype=str)

lookup = pd.read_csv("/home/dan/git/gbRelease/ancillaryData/ingestScripts/ADM0.csv", index_col=0, header=[0,1], skiprows=[0], nrows=2)

valid = []
for i in range(0, len(df.columns)):
    #First element of data in each case
    if(df.columns[i][1] == "Value"):
        validSet = {}
        validSet["Name"] = df.columns[i][0]
        print("======================================================\n")
        print("Conducting metadata check for " + str(df.columns[i][0]) + "\n")

        try:
            if((int(lookup[df.columns[i][0]]["Year Represented"][0]) > 1500) and (int(lookup[df.columns[i][0]]["Year Represented"][0]) < 2500)):
                validSet["startYear"] = lookup[df.columns[i][0]]["Year Represented"][0]
                validSet["endYear"] = lookup[df.columns[i][0]]["Year Represented"][0]
                print("YEAR(S) REPRESENTED: PASS")
            else:
                print("Year field for " + str (df.columns[i][0]) + " is invalid!\n")
                validSet["startYear"] = False
                validSet["endYear"] = False
        except:
            #Range of Years
            try:
                yearSplit = str(lookup[df.columns[i][0]]["Year Represented"][0]).split("-")
                if(int(yearSplit[0]) > 1500 and int(yearSplit[0]) < 2500):
                    if(int(yearSplit[1]) > 1500 and int(yearSplit[1]) < 2500):
                        validSet["startYear"] = yearSplit[0]
                        validSet["endYear"] = yearSplit[1]
                    
                    else:
                        print("It looks like you're trying to specify a range of years.  This must be in YYYY-YYYY format.")
                        print("Raw Format Detected: " + str(lookup[df.columns[i][0]]["Year Represented"][0]))
                        print("Parsed Format: " + str(yearSplit))
                        validSet["startYear"] = False
                        validSet["endYear"] = False
                else:
                    print("It looks like you're trying to specify a range of years.  This must be in YYYY-YYYY format.")
                    validSet["startYear"] = False
                    validSet["endYear"] = False
            except:
                print("Invalid year specified for this ingest script.")
                validSet["startYear"] = False
                validSet["endYear"] = False

        try:
            if(len(lookup[df.columns[i][0]]["Source"][0]) > 1):
                validSet["source"] = lookup[df.columns[i][0]]["Source"][0]
                print("SOURCE:              PASS")
        
            else:
                print("Source field for " + str(df.columns[i][0]) + " is invalid!\n")
                validSet["source"] = False
        except:
            print("Source field could not be parsed for " + str(df.columns[i][0])+ ".\n")
        

        #Try to find URL
        try:
            if('http' in lookup[df.columns[i][0]]["Other Notes"][1]):
                validSet["url"] = lookup[df.columns[i][0]]["Other Notes"][1]
            else:
                print("No valid URL detected.")
                validSet["url"] = False
        except:
            print("No valid URL detected.")
            validSet["url"] = False

        #Detect Tags
        validSet["tags"] = []
        try:
            validSet["tags"].append(lookup[df.columns[i][0]]["Value"][1])
        except:
            print("No tag 1 found.")
        try:
            validSet["tags"].append(lookup[df.columns[i][0]]["Year Represented"][1])
        except:
            print("No tag 2 found.")


        valid.append(validSet)


keys = valid[0].keys()
import os
import csv
with open(os.path.expanduser("~") + "/tmp/ancillaryData/gdTranslate_metaDataChecks.csv", "w") as f:
    writer = csv.DictWriter(f, keys)
    writer.writeheader()
    writer.writerows(valid)


#Create folders and data structures.
#Only doing this for a subset that we have 10-char names for, for now.
metaCrosswalk = {}
metaCrosswalk["Maternal Mortality Rate"] = "MATMORRATE"
metaCrosswalk["Proportion of Population with Access to Electricity"] = "PERPOPELEC"
metaCrosswalk['Maternal Mortality Rate'] = 'MATHMORRATE'
metaCrosswalk['Proportion of Population with Access to Electricity'] = 'PERPOPELEC'
metaCrosswalk['Prevalence of Undernourishment'] = 'PREVUNDNOR'
metaCrosswalk['Proportion of births attended by skilled health care personnel'] = 'PRBRTSKHEL'
metaCrosswalk['Neonatal Mortality Rate'] = 'NEONATMORT'
metaCrosswalk['Prevalence of Stunting among children under 5 years of age'] = 'PREVSTUNFV'
metaCrosswalk[' Renewable energy share in the total final energy consumption'] = 'RENEWENGCON'
metaCrosswalk['Forest area as a proportion of total land area'] = 'PROFORAREA'
metaCrosswalk['Mortality rate attributed to unintentional poisoning'] = 'POISONMORT'
metaCrosswalk['Proportion of Individuals Using the Internet'] = 'PROINTUSER'
metaCrosswalk['Mountain Green Cover Index'] = 'MTGREENIDX'
metaCrosswalk['Prevalence of malnutrition'] = 'PREMALNUTR'
metaCrosswalk['Mortality Rate due to Unsafe Water'] = 'MORTBADWTR'
metaCrosswalk['Victims of intentional homicide'] = 'INTHOMVCTM'
metaCrosswalk['Unsentenced Detainees as a Proportion of Total Prison Population'] = 'UNSENDETAIN'
metaCrosswalk[' Proportion of population using safely managed drinking water'] = 'PROSAFEWTR'
metaCrosswalk['Deaths due to air pollution'] = 'AIRPOLDTHS'
metaCrosswalk['Coverage of protected marine areas'] = 'MARINEPROT'
metaCrosswalk['Proportion of youth not employed or in formal education training'] = 'UNEMPYOUTH'
metaCrosswalk['Number of ATMS per 100,000 adults'] = 'ATMSPERPOP'
metaCrosswalk['Number of banks per 100,000 adults'] = 'BANKPERPOP'
metaCrosswalk['CO2 emissions per unit of value added'] = 'EMISSVALADD'
metaCrosswalk['Proportion of urban population living in slums, informal settlements or inadequate housing'] = 'URBPOPSLUM'
metaCrosswalk['Change in water-use efficiency over time'] = 'WTREFFCHNG'
metaCrosswalk['Level of water stress: freshwater withdrawal as a proportion of available freshwater resources'] = 'FRWTRWDRAW'
metaCrosswalk['Research (in full-time equivalent) per million inhabitants'] = 'RESERCHERS'
metaCrosswalk['Proportion of population with primary reliance on clean fuels and technology'] = 'POPCLNENGY'
metaCrosswalk['Energy intensity measured in terms of primary energy and GDP'] = 'ENGYINTGDP'
metaCrosswalk['Population Using Safely Managed Drinking Services'] = 'POPSAFEWTR'
metaCrosswalk['Research and development expenditure as a proportion of GDP'] = 'PRNDEXPGDP'
metaCrosswalk['Account Ownership at a Financial Institution or with a Mobile-money-service Provider'] = 'ACCNTOWNER'
metaCrosswalk['Direct Economic Loss Attributed to Disasters Relative to GDP (%)'] = 'DISLOSSGDP'
metaCrosswalk['Proportion of population that has undergone female genital mutilitation'] = 'POPEXPRFGM'
metaCrosswalk['Proportion of women ages 20-24 who were married before age 15'] = 'MARPREFITN'
metaCrosswalk['Proportion of women ages 20-24 who were married before age 18']  = 'MARPREEGTN'
metaCrosswalk['Total freight volume transported by aviation measured in tonne kilometers'] = 'FVOLAIRTKM'
metaCrosswalk['Passenger volume transported through aviation measured in passenger kilometers'] = 'PVOLAIRPKM'
metaCrosswalk['Total freight volume transported by rail measured in tonne kilometers'] = 'FVOLRTKM'
metaCrosswalk['Passenger volume transported using rail measured in passenger kilometers'] = 'PVOLRPKM'
metaCrosswalk['Indicator of food price anomalies for corn'] = 'CORNPRANOM'
metaCrosswalk['Indicator of food price anomalies in rice'] = 'RICEPRANOM'
metaCrosswalk['Indicator of food price anomalies in wheat'] = 'WHTPRIANOM'
metaCrosswalk['Indicator of food price anomalies in sorghum'] ='SORGPRANOM'
metaCrosswalk['Indicator of food price anomalies in millet'] = 'MILLPRANOM'
metaCrosswalk['Number of plant and animal genetic resources for food and agriculture secured in either medium- or long-term conservation facilities'] = 'STORGENELR'
metaCrosswalk['Annual Growth Rate of GDP per employed person'] = 'GRTGDPEMPL'
metaCrosswalk['The proportion of small-scale industries in total industry value added'] = 'PROSSINDVA'
metaCrosswalk['The proportion of small-scale industries with a loan or line of credit'] = 'PROSSCRDIT'
metaCrosswalk['Proportion of transboundary aquifers with an operational arrangement for water cooperation (%)'] = 'TBAQUFMNGD'
metaCrosswalk['Proportion of total research budget allocated to research in the field of marine technology'] = 'MARTECHBGT'
metaCrosswalk['Number of local plant species with sufficient genetic information secured in either medium- or long-term conservation facilities to reconstitute the breed in the case of an extinction'] = 'LRPLTRECON'
metaCrosswalk['Proportion of local breeds that are classifed as not being at risk of extinction'] = 'LBRDNORISK'
metaCrosswalk['Number of directly affected persons attributed to disasters per 100,000 population'] = 'POPDISTDAP'
metaCrosswalk['Number of countries with a national statistical plan that is fully funded and under implementation, by source of funding'] = 'NFUNSTPLAN'
metaCrosswalk['Proportion of local breeds that are classified as being at risk of extinction'] = 'LBREEDRISK'
metaCrosswalk['Proportion of local breeds with an unknown risk of extinction classification'] = 'LBRDUKRISK'
metaCrosswalk['The proportion of medium-high and high-tech industry value added in total value added of manufacturing'] = 'HTECHVAMAN'
metaCrosswalk['Has the country adopted and implemented investment promotion regimes for least developed countries'] = 'ADPTINVLDC'
metaCrosswalk['Countries with national statistics plans with funding from others'] = 'STPLNEXFUN'
metaCrosswalk['Does the country have a national statistics plan that is fully funded and under implementation'] = 'FFUNSTPLAN'
metaCrosswalk['Gross disbursements of total official development assistance and other official flows from all donors in support of infrastructure'] = 'ODAGROSSDSP'
metaCrosswalk['Proportion of local governments that adopt and implement local disaster risk reduction strategies in line with national disaster risk reduction strategies'] = 'DISRISKPLN'
metaCrosswalk['Dollar value of all resources made available to strengthen statistical capacity in developing countries (current United States dollars'] = 'VALSTATCAP'
metaCrosswalk['Total net official development assistance to medical research and basic health sectors'] = 'TODAHEALTH'
metaCrosswalk['Developing countries’ and least developed countries’ share of global exports'] = 'SHREXPORTS'
metaCrosswalk['National recycling rate, tons of material recycled'] = 'RECYCLETON'
metaCrosswalk['Agriculture orientation index for government expenditures)'] = 'AGORGINDEX'
metaCrosswalk['Material footprint per capita'] = 'MATFPPERCAP'
metaCrosswalk['Has the country reported progress in multi-stakeholder development effectiveness monitoring frameworks that support the achievement of the sustainable development goals'] = 'STKHOLDPLN'
metaCrosswalk['Total official development assistance for biodiversity, by donor countries (millions of constant 2016 United States dollars)'] = 'ODABIODIVR'
metaCrosswalk['Proportion of the population with household expenditures on health representing greater than 25% of total household expenditure or income'] = 'HLTHEXPTFP'
metaCrosswalk['National recycling rate'] = 'RECYCLRATE'
metaCrosswalk['Tariff rate for primary and manufactured products'] = 'TARRIFMANU'
metaCrosswalk['Volume of official development assistance flows for scholarships'] = 'ODASCHOLAR'
metaCrosswalk['Gross disbursements of total ODA and other official flows from all donors to the agriculture sector'] = 'ODAAGRICUL'
metaCrosswalk['The gross disbursements and commitments of total Official Development Assistance (ODA) from all donors for aid for trade'] = 'ODAAIDTRAD'
metaCrosswalk['Has the country achieved birth registration data that are at least 90 percent complete'] = 'BIRTHREGIS'
metaCrosswalk['Has the country achieved death registration data that are at least 75 percent complete'] = 'DEATHREGIS'
metaCrosswalk['Proportion of children and young people (a) in grades 2/3; (b) at the end of primary; and (c) at the end of lower secondary achieving at least a minimum proficiency level in mathematics'] = 'MATHPROFIC'
metaCrosswalk['Proportion of individuals who own a mobile telephone'] = 'CELLOWNERS'
metaCrosswalk['Fixed Internet broadband subscriptions per 100 inhabitants'] = 'INTNETSUBS'
metaCrosswalk['Proportion of children aged 1–17 years who experienced any physical punishment and/or psychological aggression by caregivers in the past month'] = 'PCHLDABUSE'
metaCrosswalk['Does the country have national statistical legislation that compiles with the Fundamental Principle of Official Statistics'] = 'FUNPOSTATS'
metaCrosswalk['Does the country have indepdendent national human rights institutions in compliance with the Paris Principles'] = 'PARISHRINT'
metaCrosswalk['Has the country conducted at least one population and housing census in the last 10 years'] = 'CENSUSDONE'
metaCrosswalk['Compliance with the Rotterdam Convention on hazardous waste and other chemicals'] = 'ROTTERDAMC'
metaCrosswalk['Compliance with the Basel Convention on hazardous waste and other chemicals'] = 'BASELCONVN'
metaCrosswalk['Compliance with the Montreal Convention on hazardous waste and other chemicals'] = 'MONTREALC'
metaCrosswalk['Homicide rate (per 100,000 people)'] = 'RTHOMOCIDE'
metaCrosswalk['The material footprint, the attribution of global material extraction to domestic final demand of a country, for biomass per capita'] = 'MFPBMASSPC'
metaCrosswalk['The material footprint, the attribution of global material extraction to domestic final demand of a country, per capita for non-metal ore'] = 'NMETALFPPC'
metaCrosswalk['The material footprint, the attribution of global material extraction to domestic final demand of a country, for biomass, fossil fuels, metal ores, and non-metal ores per capita'] = 'MFPTOTALPC'
metaCrosswalk['The material footprint, the attribution of global material extraction to domestic final demand of a country, per capita for metal ore'] = 'OREMFPPERC'
metaCrosswalk['Countries with National Human Rights Institutions and no status with the Paris Principles'] = 'NOPARISPRI'
metaCrosswalk['Proportion of young women and men aged 18–29 years who experienced sexual violence by age 18'] = 'SEXVIOLENC'
metaCrosswalk['Proportion of medium and high-tech industry value added in total value added'] = 'HTECHVALUE'
metaCrosswalk['Progress in multi-stakeholder development effectiveness monitoring frameworks that support the achievement of the sustainable development goals'] = 'STKHLDPROG'
metaCrosswalk['The material footprint, the attribution of global material extraction to domestic final demand of a country, for fossil fuel per capita'] = 'FFUELMFPPC'
metaCrosswalk['Proportion of young men aged 18-29 years who experienced sexual violence by age 18'] = 'SEXVIOLENM'
metaCrosswalk['Proportion of young women aged 18-29 years who experienced sexual violence by age 18'] = 'SEXVIOLENF'
metaCrosswalk['Does the country have independent national human rights institutions in compliance with the Paris Principles'] = 'INDPHRINST'
metaCrosswalk['The proportion of males in grades 2/3 achieving at least a minimum proficiency level in mathematics'] = 'TWOMINMTHM'
metaCrosswalk['The proportion of female students in grades 2/3 achieving at least a minimum proficiency level in mathematics'] = 'TWOMINMTHF'
metaCrosswalk['Material footprint of raw material (tonnes)'] = 'RAWMTFPTON'
metaCrosswalk['Material footprint of non-metallic materials (tonnes)'] = 'NONMETALTON'
metaCrosswalk['Material footprint of biomass (tonnes)'] = 'BIOMASSTON'
metaCrosswalk['Material footprint of metal ores (tonnes)'] = 'OREMTFPTON'
metaCrosswalk['Material footprint of fossil fuels (tonnes)'] = 'FFUELFPTON'
metaCrosswalk['The proportion of students in grades 2/3 achieving at least a minimum proficiency level in reading'] = 'TWOMINREAD'
metaCrosswalk['Domestic material consumption of metal ores per capita'] = 'ORECONPERC'
metaCrosswalk['Domestic material consumption of non-metallic minerals per capita'] = 'NMETALCPRC'
metaCrosswalk['Domestic material consumption of crops per capita'] = 'CROPCONSPC'
metaCrosswalk['Primary government expenditures as a proportion of original approved budget'] = 'GOVEXPBDGT'
metaCrosswalk['Growth rates of household expenditure or income per capita among the total population'] = 'GRHHEXPDPC'
metaCrosswalk['Proportion of children under 5 years of age whose births have been registered with a civil authority'] = 'REGISBIRTH'
metaCrosswalk['Total government revenue as a proportion of GDP'] = 'GOVTREVGDP'
metaCrosswalk['Proportion of domestic budget funded by domestic taxes'] = 'PRPBDGTTAX'
metaCrosswalk['Worldwide weighted tariff-average'] = 'WWTARIFAVG'
metaCrosswalk['Progress towards sustainable forest management'] = 'SUSFORMGMT'
metaCrosswalk['The proportion of land that is degraded over total land area'] = 'DEGRADLAND'
metaCrosswalk['Proportion of forest area located within legally established protected areas'] = 'PROTECTFOR'
metaCrosswalk['Proportion of forest area under a long-term forest management plan'] = 'LTMGMTFORP'
metaCrosswalk['Forest area under an independently verified forest management certification scheme'] = 'INDPMGMTFR'
metaCrosswalk['The mean percentage of each important site for biodiversity that is covered by protected area designations'] = 'PROBIODIVR'
metaCrosswalk['Number of disruptions to basic services attributed to disasters'] = 'DISTDISRUP'
metaCrosswalk['Participation rate in organized learning (one year before the official primary entry age)'] = 'RORGPREEDU'
metaCrosswalk['Male participation rate in organized learning (one year before the official primary entry age)'] = 'RORGPREDUM'
metaCrosswalk['Female participation rate in organized learning (one year before the official primary entry age)'] = 'RORGPREEDUF'
metaCrosswalk['Progress by countries in the degree of implementation of international instruments aiming to combat illegal, unreported and unregulated fishing'] = 'ILLFISHLAW'
metaCrosswalk['Does country have sustainable consumption and production (SCP) national action plan?'] = 'SCPNACTPLN'
metaCrosswalk['Researchers (in full-time equivalent) per million inhabitants'] = 'RESEARCHER'
metaCrosswalk['The annual growth rate of GDP per capita measured in constant US dollars'] = 'GWRREALGDP'
metaCrosswalk['International financial flows to developing countries in support of clean energy research and development and renewable energy production, including in hybrid systems'] = 'CLNENGYFIN'
metaCrosswalk['Proportion of wastewater safely treated'] = 'SAFEWSTWTR'

metaCrosswalk = {k.strip().upper(): v for (k, v) in metaCrosswalk.items()}

print(metaCrosswalk)
for i in range(0, len(valid)):
    try:
        l = valid[i]["Name"].strip().upper()
        varName = metaCrosswalk[l]
        crosswalk = True
    except:
        print("No crosswalk exists for this variable:" + valid[i]["Name"])
        crosswalk = False
    
    if(crosswalk == True):
        fname = "meta" + varName + ".txt"

        metaC = "geoDesc (www.geodesc.org) Ancillary Variables Metadata File \n"
        metaC = metaC +  "==============================================================\n"
        metaC = metaC +  "Metadata for: " + varName + "\n"
        metaC = metaC +  "Full Variable Name: " + valid[i]["Name"] + "\n"
        metaC = metaC +  "==============================================================\n"
        metaC = metaC +  "\n"
        metaC = metaC +  "Data Definition: \n"
        metaC = metaC +  "Units: \n"
        metaC = metaC +  "Data Representative Of Year(s): " + str(valid[i]["startYear"])[:-2] + "-" + str(valid[i]["endYear"])[:-2] + "\n"
        metaC = metaC +  "Each row in the dataset is representative of: " + "ADM0\n" 
        metaC = metaC +  "Each row ID is defined by: " + "ISO 3166-1 alpha-3\n"
        metaC = metaC +  "Data Processing Methodology: \n"
        
        metaC = metaC +  "Data Collection Methodology (or link to documentation): \n"
        try:            
            metaC = metaC +  "Source 1: " + str(valid[i]["source"]) + "\n"
        except:
            metaC = metaC + "Source 1: " + "INVALID.\n"
        metaC = metaC +  "Source 2: " + "\n"

        metaC = metaC +  "License: \n" 
        metaC = metaC +  "License Source: \n"
        metaC = metaC +  "Link to Source Data: " + str(valid[i]["url"]) + "\n"

        metaC = metaC + "Tag(s): "
        for j in range(0, len(valid[i]["tags"])-1):
            metaC = metaC +  str(valid[i]["tags"][j]) + ","
        metaC = metaC[:-1] + "\n"

        metaC = metaC +  "Other Notes: \n" 

        with open(os.path.expanduser("~") + "/git/gbRelease/ancillaryData/gdOpen/ADM0/" + fname, "w+") as f:
            f.write(metaC)

        #Write out the data for this variable.
        csvName = os.path.expanduser("~") + "/git/gbRelease/ancillaryData/gdOpen/ADM0/" + varName + ".csv"
        df[valid[i]["Name"]]["Value"].to_csv(csvName, index_label="ID", header=["Value"])
        
        


    
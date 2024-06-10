import js
import micropip
import sys
await micropip.install("pandas")
import pandas as pd
import os

# Import csvs to dataframes using pandas
dir_path = '/home/pyodide/calculator_utils' # calculator_utils is a zip unpacked by pyodide into its file system
zipdf = pd.read_csv(dir_path + '/tn_zips_rvals.csv') # zip codes and corresponding counties and lat/long coords
# tree csv
treedf = pd.read_csv(dir_path + '/treeinfo.csv')
# native plant csv
plantsdf = pd.read_csv(dir_path + '/nativeplants.csv')


# get county name (without county at the end) from zipcode
county = zipdf.loc[zipdf['zip']==zipcode,'county'].values[0].split()[0] # "Davidson County" -> "Davidson"

# utils for printing out the results
def print_species_list(species_list):
    if len(species_list) == 0:
        return "There are no species planted."
    elif len(species_list) == 1:
        return "The most common species planted was " + species_list[0] + "."
    elif len(species_list) == 2:
        return "The most common species planted were " + species_list[0] + " and " + species_list[1] + "."
    else:
        species_str = ", ".join(species_list[:-1])
        return "The most common species planted were " + species_str + ", and " + species_list[-1] + "."




# if county is not in database
if not county in treedf['County'].unique():
    tree_response = "There are currently no trees that have been reported and surveyed in your county, " + \
        "however, that does not mean that there are none associated with TNSY. " +\
        "Be one of the first in your area to sequester and store carbon, " + \
        "avoid runoff, remove pollution, and produce oxygen by planting native trees in your yard and getting certified with TNSY."
else: # else county is in database
    countytrees = treedf.loc[treedf['County']==county,]

    # Sentence about number of trees
    ntrees = f"There are a total of {len(countytrees)} reported trees planted in TNSY certified yards in {county} county." 
    # Sentence about most common species
    topthreespecies = print_species_list(list(countytrees['SpeciesName'].value_counts().nlargest(3).index))
    
    estbenefits = "Estimated Benefits: \n" +\
    f"{countytrees['GrossCarbonSequestrationLBYR'].sum():.1f} lbs of carbon sequestered per year \n" +\
    f"{countytrees['CarbonStoragelb'].sum():.1f} lbs of carbon stored* \n" +\
    f"{countytrees['AvoidedRunoffGYR'].sum():.1f} gallons of runoff avoided per year \n" +\
    f"{countytrees['PollutionRemovalOZYR'].sum():.1f} ounces of pollution removed per year \n" +\
    f"{countytrees['OxygenProductionLBYR'].sum():.1f} pounds of oxygen produced per year \n" +\
    f"Total annual benefits of carbon sequestration, avoided runoff, and pollution removal amounts to ${countytrees['TotalAnnualBenefitsDYR'].sum():.2f} per year! \n" +\
    "*Note: pounds of carbon prevented from being released into the atmosphere"

    tree_response = ntrees + " \n\n" + topthreespecies  + " \n\n" +  estbenefits
#  *pounds of carbon prevented from being released into the atmosphere


# Native Plant Runoff
# Data: Native Plant Improvement.csv


# If zip code is not is database:
if not zipcode in plantsdf['Zip_Code'].unique():
    nativeplant_response = "There is currently no reported and surveyed TNSY land that has been improved with native plants in your zip code, " + \
    "however, that does not mean land improvement with native plants has not occurred. " + \
    "Be one of the first in your area to decrease runoff, prevent erosion, and increase biodiversity by planting native plants and getting certified with TNSY."
else:
    zipplants = plantsdf.loc[plantsdf['Zip_Code']==zipcode]

    # sum(df$Zip_Code == “userzipcode”) reported TNSY certified yards in your zip code have been improved with native plants. 
    nyards = f"{len(zipplants)} reported TNSY certified yards in your zip code ({zipcode}) have been improved with native plants." 
    # In total, sum(df$Zip_Code == “userzipcode” [Sq_Ft]) square feet have been improved with native plants. 
    sqft = f"In total, {zipplants['Sq_Ft'].sum():.1f} square feet have been improved with native plants."
    # This has decreased runoff, prevented erosion, and increased biodiversity. 
    nativeplant_response = nyards + " \n\n" + sqft + " \n\n" + "This has decreased runoff, prevented erosion, and increased biodiversity. "

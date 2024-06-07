# import rasterio # rasterio not in pyodide yet
# import rasterio.warp
import pandas as pd
import os
import js

# to make sure we import the files from the correct directory
dir_path  = os.path.dirname(os.path.realpath(__file__))

tnzips = pd.read_csv(dir_path + '/tn_zipcodes.csv') # zip codes and corresponding counties and lat/long coords
lsdf = pd.read_csv(dir_path + '/ls_values.csv') # ls values given slope percent and length

result = js.forminfo.zipcode.value + 5000
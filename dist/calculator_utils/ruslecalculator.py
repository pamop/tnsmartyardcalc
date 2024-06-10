import js
import micropip
import sys
await micropip.install("pandas")
import pandas as pd
import os

# for debugging
# print(os.listdir('/home/pyodide/calculator_utils'))
# print(js_var) # if js_var is set to pyodide in App.vue it will be here!

# Import csvs to dataframes using pandas
dir_path = '/home/pyodide/calculator_utils' # calculator_utils is a zip unpacked by pyodide into its file system
zipdf = pd.read_csv(dir_path + '/tn_zips_rvals.csv') # zip codes and corresponding counties and lat/long coords
lsdf = pd.read_csv(dir_path + '/ls_values.csv') # ls values given slope percent and length

def find_nearest_value(input_value, available_values):
  return min(available_values, key=lambda x: abs(x - input_value))

def find_intersecting_length(slope_percentage, slope_length):
  # Find the nearest slope percentage in the table
  nearest_slope_percentage = find_nearest_value(slope_percentage, lsdf['slope_percents'].unique())
  # Find the nearest slope length in the table
  nearest_slope_length = find_nearest_value(slope_length, lsdf['slope_lengths'].unique())
  # Find the intersecting length (LS) from the table
  intersecting_length = lsdf.loc[(lsdf['slope_lengths']==nearest_slope_length) & (lsdf['slope_percents']==nearest_slope_percentage), 'ls'].values[0]
  return intersecting_length

percentNormal = 1 - percentNative

if slope_percentage/100 <= 0.16:
  P = 0.1
elif slope_percentage/100 <= 0.25:
  P = 0.12
else:
  P = 0.14

LS = find_intersecting_length(slope_percentage, slope_length)
K = 0.295
R = zipdf.loc[zipdf['zip']==zipcode,'rfactor'].values[0] # e.g. 200
cFactorNative = 0.05
cFactorGrass = 0.1


def erosion(after):
  if after:
     return (((R * K * LS * cFactorNative * P)*percentNative) +\
     ((((R * K * LS * cFactorGrass * P)*percentNormal))))/43560*area
  else:
       return ((R * K * LS * cFactorGrass * P)/43560) * area
       
afterVol = (erosion(True)*2204)/90
beforeVol = (erosion(False)*2204)/90
afterLB = erosion(True)*2204
beforeLB = erosion(False)*2204
erosion_response = f'Your erosion is {afterLB:.2f} pounds per year or {afterVol:.2f} cubic feet per year, but if you did not have native plants, ' + \
      f'your erosion would be {beforeLB:.2f} pounds per year or {beforeVol:.2f} cubic feet per year.'
print(f'Your erosion is {afterLB:.2f} pounds per year or {afterVol:.2f} cubic feet per year, but if you did not have native plants, '\
      f'your erosion would be {beforeLB:.2f} pounds per year or {beforeVol:.2f} cubic feet per year.')

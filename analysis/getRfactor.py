import rasterio
import rasterio.warp
import pandas as pd
import os

# to make sure we import the files from the correct directory
dir_path  = os.path.dirname(os.path.realpath(__file__))

# zipcode dataframe
tnzips = pd.read_csv(dir_path + '/tn_zipcodes.csv')

def getRfac(zipcode):
    lat = tnzips.loc[tnzips['zip']==zipcode,'latitude'].values[0]
    long = tnzips.loc[tnzips['zip']==zipcode,'longitude'].values[0]
    # Open your raster file
    # dataset = rasterio.open('./tn_rfactors.tif')
    with rasterio.open(dir_path + '/Rfactors.tif') as dataset:
        # convert decimal degrees (global coordinates) into dataset's CRS
        # Define the target CRS. the CRS of the raster dataset
        target_crs = dataset.crs

        # Transform the global coordinates to the dataset's CRS
        x, y = rasterio.warp.transform(src_crs="EPSG:4326", dst_crs=target_crs, xs=[long], ys=[lat])

        # Sample the pixel value at the transformed coordinates
        for val in dataset.sample([(x[0], y[0])], indexes=1):
            rval = val[0]
    return rval

# this line takes about 5 seconds to run 
tnzips['rfactor'] = tnzips.apply(lambda row: getRfac(row['zip']), axis=1)

# write dataframe with rfactor column to file
tnzips.to_csv(dir_path + '/tn_zips_rvals.csv')
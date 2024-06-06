import rasterio
import rasterio.warp
import pandas as pd
import os

# to make sure we import the files from the correct directory
dir_path  = os.path.dirname(os.path.realpath(__file__))


# get zipcode from user
zipcode = 37212

tnzips = pd.read_csv(dir_path + '/tn_zipcodes.csv')

# check if zipcode is valid
if not (zipcode in tnzips['zip'].unique()):
    print("Error: this zipcode is not found in our database! Is it a Tennessee zip code?")
else:
    print("Calculating...")
    # Get coordinates from zipcode from file (coords in decimal degrees)
    def get_coordinates(zipcode):
        lat = tnzips.loc[tnzips['zip']==zipcode,'latitude'].values[0]
        long = tnzips.loc[tnzips['zip']==zipcode,'longitude'].values[0]
        return lat,long

    # Example usage
    # address = input(f'your address')
    lat,long = get_coordinates(zipcode)

    # Open your raster file
    # dataset = rasterio.open('./tn_rfactors.tif')
    with rasterio.open(dir_path + '/tn_rfactors.tif') as dataset:
        # convert decimal degrees (global coordinates) into dataset's CRS
        # Define the target CRS. the CRS of the raster dataset
        target_crs = dataset.crs

        # Transform the global coordinates to the dataset's CRS
        x, y = rasterio.warp.transform(src_crs="EPSG:4326", dst_crs=target_crs, xs=[long], ys=[lat])

        # Sample the pixel value at the transformed coordinates
        for val in dataset.sample([(x[0], y[0])], indexes=1):
            rval = val[0]


    # Print the value
    print("The R Factor at the given zipcode is:", rval)


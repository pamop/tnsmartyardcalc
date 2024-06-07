from osgeo import gdal, osr
import pandas as pd
import os

# Ensure correct directory for files
dir_path = os.path.dirname(os.path.realpath(__file__))

# Get zipcode from user
zipcode = 37212

tnzips = pd.read_csv(dir_path + '/tn_zipcodes.csv')

# Check if zipcode is valid
if not (zipcode in tnzips['zip'].unique()):
    print("Error: this zipcode is not found in our database! Is it a Tennessee zip code?")
else:
    print("Calculating...")

    # Get coordinates from zipcode from file (coords in decimal degrees)
    def get_coordinates(zipcode):
        lat = tnzips.loc[tnzips['zip'] == zipcode, 'latitude'].values[0]
        long = tnzips.loc[tnzips['zip'] == zipcode, 'longitude'].values[0]
        return lat, long

    # Example usage
    lat, long = get_coordinates(zipcode)
    print(f"Coordinates (lat, long): {lat}, {long}")

    # Open your raster file
    dataset = gdal.Open(dir_path + '/tn_rfactors.tif')

    if not dataset:
        raise FileNotFoundError(f"Unable to open the raster file: {dir_path + '/tn_rfactors.tif'}")

    # Get the dataset's CRS
    target_wkt = dataset.GetProjection()
    target_srs = osr.SpatialReference()
    target_srs.ImportFromWkt(target_wkt)

    # Print the target CRS to verify
    print(f"Target CRS: {target_srs.ExportToPrettyWkt()}")

    # Define the source CRS (EPSG:4326 for latitude/longitude)
    source_srs = osr.SpatialReference()
    source_srs.ImportFromEPSG(4326)

    # Print the source CRS to verify
    print(f"Source CRS: {source_srs.ExportToPrettyWkt()}")

    # Create a transform object to convert from source to target CRS
    transform = osr.CoordinateTransformation(source_srs, target_srs)

    # Transform the global coordinates to the dataset's CRS
    x, y, _ = transform.TransformPoint(long, lat)
    print(f"Transformed coordinates (x, y): {x}, {y}")

    # Get GeoTransform parameters
    gt = dataset.GetGeoTransform()
    print(f"GeoTransform: {gt}")

    # Calculate the pixel offset
    px = int((x - gt[0]) / gt[1])
    py = int((y - gt[3]) / gt[5])
    print(f"Pixel coordinates (px, py): {px}, {py}")

    # Ensure the pixel coordinates are within the raster dimensions
    if not (0 <= px < dataset.RasterXSize and 0 <= py < dataset.RasterYSize):
        print(f"Raster dimensions (XSize, YSize): ({dataset.RasterXSize}, {dataset.RasterYSize})")
        raise ValueError("Pixel coordinates are outside the raster dimensions")

    # Get the raster band
    band = dataset.GetRasterBand(1)

    # Read the pixel value
    rval = band.ReadAsArray(px, py, 1, 1)[0][0]

    # Print the value
    print("The R Factor at the given zipcode is:", rval)

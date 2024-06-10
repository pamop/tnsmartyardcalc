from osgeo import gdal
from geopy.geocoders import Nominatim

# Initialize the geocoder
geolocator = Nominatim(user_agent="geoapiExercises")

# Function to geocode an address
def get_coordinates(address):
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# Example usage
address = input(f'your address')
coordinates = get_coordinates(address)

# Open your raster file
raster_file = gdal.Open('./Rfactors.tif')

# Get the raster band (1 in this case)
band = raster_file.GetRasterBand(1)

# Define your coordinate (longitude, latitude)

x, y = coordinates

# Convert the coordinate to the raster's georeferenced space
transform = raster_file.GetGeoTransform()
xOrigin = transform[0]
yOrigin = transform[3]
pixelWidth = transform[1]
pixelHeight = -transform[5]

# Compute the pixel offset
xOffset = int((x - xOrigin) / pixelWidth)
yOffset = int((y - yOrigin) / pixelHeight)

# Read the value at the computed offset
value = band.ReadAsArray(xOffset, yOffset, 1, 1)

# Close the raster file
raster_file = None

# Print the value
print("The value at the given coordinate is:", value[0][0])


from function import random_points as rp
from function import range

## Get coordinate x and y
def get_coordinates():
    location = rp.polygon_random_points(range.poly, 1)
    # The way it was done is by returning both coordinates.
    for coordinates in location:
        return coordinates.x, coordinates.y
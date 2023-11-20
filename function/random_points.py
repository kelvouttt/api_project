from shapely.geometry import Polygon, Point
import random


## Define the randomizer function using NumPy
def polygon_random_points(poly, num_points):
    min_x, min_y, max_x, max_y = poly.bounds

    points = []
    while len(points) < num_points:
        random_point = Point([random.uniform(min_x, max_x),
                            random.uniform(min_y, max_y)])
        if (random_point.within(poly)):
            points.append(random_point)
    # This function will return a list with only 1 length, the next function will split this up into coordinate x and coordinate y.
    return points
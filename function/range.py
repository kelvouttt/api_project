from shapely.geometry import Polygon, Point

## Define desired Polygon
# https://medium.com/the-data-journal/a-quick-trick-to-create-random-lat-long-coordinates-in-python-within-a-defined-polygon-e8997f05123a
poly = Polygon([(-33.822218,151.084762), 
                (-33.919981,151.099747),
                (-33.917772,151.240542),
                (-33.872596, 151.262135)])
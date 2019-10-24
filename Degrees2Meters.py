# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 15:44:18 2014

@author: guidolo
"""

As alfaciano says in shapely, the distance is the Euclidean Distance or Linear distance between two points on a plane and not the Great-circle distance between two points on a sphere.

from shapely.geometry import Point
point1 = Point(50.67,4.62)
point2 = Point(51.67, 4.64)
import math
# Euclidean Dustance
def Euclidean_distance(point1,point2):
     return math.sqrt((point2.x()-point1.x())**2 + (point2.y()-point1.y())**2)

print Euclidean_distance(point1,point2)
1.00019998 # distance in degrees (coordinates of the points in degrees)

# with Shapely
print point1.distance(point2)
1.0001999800039989 #distance in degrees (coordinates of the points in degrees)

For the great-circle distance, you need to use algorithms as the law of cosines or the Haversine formula (look at Why is law of cosines more preferable than haversine when calculating distance between two latitude-longitude points?) or use the module pyproj that performs geodetic calculations.

# law of cosines
distance = math.acos(math.sin(math.radians(point1.y))*math.sin(math.radians(point2.y))+math.cos(math.radians(point1.y))*math.cos(math.radians(point2.y))*math.cos(math.radians(point2.x)-math.radians(point1.x)))*6371
print "{0:8.4f}".format(distance)
110.8544 # in km
# Haversine formula
dLat = math.radians(point2.y) - math.radians(point1.y)
dLon = math.radians(point2.x) - math.radians(point1.x)
a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(point1.y)) * math.cos(math.radians(point2.y)) * math.sin(dLon/2) * math.sin(dLon/2)
distance = 6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
print "{0:8.4f}".format(distance)distance
110.8544 #in km

# with pyproj
import pyproj
geod = pyproj.Geod(ellps='WGS84')
angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
print "{0:8.4f}".format(distance/1000)
110.9807 #in km
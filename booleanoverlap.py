# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 16:26:57 2017

Boolean Overlap Tool

@author: Eliza Wallace, ewallace@mapc.org
"""
import arcpy
import sys

points = arcpy.GetParameterAsText(0)
polygons = arcpy.GetParameterAsText(1)
newfield = arcpy.GetParameterAsText(2)

# function that adds a suffix to a field name if it already exists
def AutoName(raster):
    raster = raster.replace(' ','') # removes spaces from layer name for ESRI GRID format
    checkraster = arcpy.Exists(raster) # checks to see if the raster already exists
    count = 2
    newname = raster

    while checkraster == True: # if the raster already exists, adds a suffix to the end and checks again
        newname = raster + str(count)
        count += 1
        checkraster = arcpy.Exists(newname)

    return newname
    
# function that adds a short integer to a point feature class, then shows whether or not
    #it overlaps a polygon in another feature class.
def booleanoverlap(points, polygons, newfield):
    #copy polygons to new feature class
    #polycopy = "polygonscopy"
    polycopy = AutoName("polygonscopy")
    arcpy.CopyFeatures_management(polygons,polycopy)  
    
    arcpy.AddField_management(polycopy,newfield,"SHORT")
    arcpy.CalculateField_management(polycopy,newfield,"1","PYTHON")
    joindata = AutoName("joindata")
    
    arcpy.SpatialJoin_analysis(points, polycopy, joindata)
    
    arcpy.JoinField_management(points, "OBJECTID", joindata, "OBJECTID", newfield)
    
    arcpy.Delete_management(joindata, polycopy)    

try:
    booleanoverlap(points, polygons, newfield)
    
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
    arcpy.AddError(e.args[0])
    
    
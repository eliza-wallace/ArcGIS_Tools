# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 13:53:07 2017

@author: Eliza Wallace

Count Overlap tool
Tool that counts the features that overlap each polygon in a feature class.

"""
import arcpy
import sys

catchments = arcpy.GetParameterAsText(0)
features = arcpy.GetParameterAsText(1)
fieldname = arcpy.GetParameterAsText(2)
idfield = arcpy.GetParameterAsText(3)

#fcdescr = arcpy.Describe(features)
#shape = str(fcdescr.shapeType)

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

try: 
    # spatial joins features to catchments 
    sjoutput = AutoName("spatialjoin")
    arcpy.SpatialJoin_analysis(catchments,features,sjoutput,"JOIN_ONE_TO_MANY","KEEP_COMMON")

    # counts features joined to each catchment
    statsoutput = AutoName("statsoutput")
    arcpy.Statistics_analysis(sjoutput, statsoutput,[["Join_Count","SUM"]], idfield)

    # adds the specified field name to the feature class
    arcpy.AddField_management(statsoutput, fieldname, "SHORT") 
    
    # copies the count of features to the new field
    arcpy.CalculateField_management(statsoutput, fieldname,"!SUM_Join_Count!", "PYTHON")
    
    # joins the new field to the catchment feature class
    arcpy.JoinField_management(catchments,idfield,statsoutput,idfield,[fieldname])
    
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
    arcpy.AddError(e.args[0])
    
    
    
    
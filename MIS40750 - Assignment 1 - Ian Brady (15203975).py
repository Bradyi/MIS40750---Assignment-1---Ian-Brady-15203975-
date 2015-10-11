# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 22:17:16 2015

@author: Ian
MIS40750 - Assignment 1
"""

#import relevant libraries
import sqlite3
import pandas as pd
import math

#create connection to database through the variable conn
conn = sqlite3.connect("C:\\Users\\Ian\\Documents\\Business Analytics\\Analytics Research & Implementation\\Assignment 1\\renewable.db") 
#use sql querys to read the tables from the database and store each in a pandas dataframe
df_locations = pd.read_sql_query("SELECT * FROM location;",conn)
df_ports = pd.read_sql_query("SELECT * FROM ports;",conn)

#distance between two points function
def distance (x1, y1, x2, y2):
    dist = math.sqrt((x2-x1)**2+(y2-y1)**2)
    return dist

#function to calculate the distance between two locations, takes in two dataframes of locations 
def route_distances (locations_a, locations_b):
    #iterrate through each row of first dataframe
    for i, row in locations_a.iterrows():
        #store values from row i, column 'lat' and row i, column 'long'
        a_lat = (locations_a.loc[[i],'lat']).values
        a_long = (locations_a.loc[[i],'long']).values
        #At each row of dataframe 1, iterrate through each row of dataframe 2
        for j, row in locations_b.iterrows():
            #store values
            b_lat = (locations_b.loc[[j],'lat']).values
            b_long = (locations_b.loc[[j],'long']).values
            #call distance method to calculate distance between two points
            x = distance(a_lat,a_long,b_lat,b_long)
            #assign x value to new column. Column depends on the name of the port/row number
            #In this case 3 extra columns will be created for each port. 3 x values for each row i
            locations_a.set_value(i,'to port (%d)'% j, x)
    print(locations_a)
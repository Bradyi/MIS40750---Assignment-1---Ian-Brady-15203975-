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
    
#function that checks 2 values, returns true if second is less than the first
def shorter_route(distance1, distance2):
    if distance2 < distance1:
        return True
    else:
        return False

#function that calculates and returns profit amount per route
def profit_per_route(distance, production, cost_per_dist, price_per_piece, limit):
    #limit = demand limit or transport capability limit - used if all of production will not/can not be transported 
    if production > limit:
        cost = distance * cost_per_dist * limit
        sales_value = limit * price_per_piece
    else:
        cost = distance * cost_per_dist * production
        sales_value = production * price_per_piece
    profit = sales_value - cost
    return profit
    
#funtion to calculate the shortest and most profitable route
def route_analysis(locations, cost_per_dist, price_per_piece, limit):
    min_dist = 9999999
    max_profit = -99999999
    port1 = 0
    location1 = 0
    port2 = 0
    location2 = 0
    #iterrate through each row of locations table
    for i, row in locations.iterrows():
        #quantity of ports = number of columns minus the first 3 columns
        ports_qty = len(locations.columns)-3
        #assign this locations production to variable
        loc_production = (locations.loc[[i],'production'% i]).values
        #for each location iterrate through last 3 columns/ports
        for j in range(0, ports_qty):
            #assign distance to port j to variable
            dist_to_port = (locations.loc[[i],'to port (%d)'% j]).values
            #call function to check if this distance is shorter than previously assigned
            if shorter_route(min_dist, dist_to_port):
                #if it is store the distance, port & location
                min_dist = dist_to_port
                port1 = j
                #I realise that 'i' will be updated more times than is necessary but I felt this was cleaner than checking if it needs to be updated
                location1 = i
            #call function to calculate the profit of route
            route_profit = profit_per_route(dist_to_port, loc_production, cost_per_dist, price_per_piece, limit )
            if route_profit > max_profit:
               #only update if value is greater than previosuly assigned
               max_profit = route_profit
               port2 = j
               location2 = i
    print('Shortest possible route: Location (%d) to Port (%d).Distance = (%f)' % (location1, port1, min_dist))
    print('Most profitable route: Location (%d) to Port (%d).Profit = € (%f)' % (location2, port2, max_profit))
    
    
route_distances(df_locations, df_ports)
#run analysis to calculate shortest and most profitable route. Assume limit of 200000
route_analysis(df_locations, 10, 20, 200000)
#Recommend to build plant at location 4

#Most profitable route (or least loss making) will only differ in extreme and unrealistic circumstances
route_analysis(df_locations, 60, -20, 300000)

#Send updated dataframe to excel to communicate to team
df_locations.to_excel("C:\\Users\\Ian\\Documents\\Business Analytics\\Analytics Research & Implementation\\Assignment 1\\Location To Port Distances.xlsx")
    
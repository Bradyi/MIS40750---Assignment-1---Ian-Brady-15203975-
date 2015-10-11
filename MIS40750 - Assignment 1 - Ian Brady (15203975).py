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
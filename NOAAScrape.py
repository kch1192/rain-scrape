# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 11:53:08 2018

@author: Kevin
"""

import requests as req
import pandas as pd

#json parameters, changes based on API
param = {"limit" : 299}

#query API; status code should return as "200"
weather = req.get("https://api.weather.gov/stations/KBOS/observations", param)
print(weather.status_code)

weather = weather.json()

#initialize list of dicts for conversion to a dataframe
weather_list = []

#each element in the weather[] dictionary is a list of dictionaries of dictionaries
for features in range(len(weather["features"])):

    #each weather["features"] dictionary is an observation at a particular time
    #each further element (weather["features"][feature]) in the dictionary is an observed attribute: time, rainfall, etc
    #"properties" are the properties of any given attribute: scalar value, units of measurement, etc.
    
    prop_key = list(weather["features"][features]["properties"].keys())
    properties = weather["features"][features]["properties"]

    #create dictionary of dictionaries
    weather_dict = {}

    #only select observations with scalar attributes
    for i in prop_key:
        if ("value" in properties[i]):
            weather_dict[i] = properties[i]

    dict_key = list(weather_dict.keys())

    x_value = {}

    for z in dict_key:
        #collapse collected observation dictionary of dictionaries into single dictionary for each observation
        x_value[z] = weather_dict[z]["value"]
        #assign timestamp to each observation
        x_value["time"] = properties["timestamp"]

    #fill list of dicts
    weather_list.append(x_value)
    
bframe = pd.DataFrame(weather_list)
bframe.to_csv('boston_weather.csv')

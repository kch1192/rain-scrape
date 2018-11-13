# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 11:53:08 2018

@author: Kevin
"""

import requests as req
import pandas as pd

boston_params = {"start":"2010-01-01T00:00:00+00:00", "end":"2018-11-09T00:00:00+00:00", "limit": 2}
weather = req.get("https://api.weather.gov/stations/KBOS/observations", boston_params)

print(weather.status_code)
print(weather.text)
weather = weather.json()


prop_key = list(weather["features"][0]["properties"].keys())
properties = weather["features"][0]["properties"]

weather_dict = {}

for i in prop_key:
    if ("value" in properties[i]):
        weather_dict[i] = properties[i]

dict_key = list(weather_dict.keys())

x_value = {}

for z in dict_key:
    x_value[z] = weather_dict[z]["value"]
    x_value["time"] = properties["timestamp"]


print(x_value)

weather_list = []
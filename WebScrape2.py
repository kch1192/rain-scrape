# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 16:47:23 2018

@author: Kevin
"""
from selenium import webdriver
import pandas as pd

#open the browser to Boston Water and Sewage Comission's daily rainfall webpage
browser = webdriver.Chrome('C://Users//Kevin//Desktop//chromedriver.exe')
browser.get('http://www.bwsc.org/COMMUNITY/rainfall/telog_rainfall/rf_daily.asp')

#Initialize page elements to enable page changes and interactions
#Month/Year Dropdowns, Submit button to request changes, Area Radio Buttons
year_select = browser.find_element_by_name("reqyear")
month_select = browser.find_element_by_name("reqmonth")

submit = browser.find_element_by_id("SubBtn")

roslindale = browser.find_element_by_id("RadioGroup1_1")
union_park = browser.find_element_by_id("RadioGroup1_0")
dotadams = browser.find_element_by_id("RadioGroup1_2")
allston = browser.find_element_by_id("RadioGroup1_3")
charlestown = browser.find_element_by_id("RadioGroup1_4")
longwood = browser.find_element_by_id("RadioGroup1_5")
hyde_park =browser.find_element_by_id("RadioGroup1_6")
dottalbot = browser.find_element_by_id("RadioGroup1_7")
eboston = browser.find_element_by_id("RadioGroup1_8")
roxbury = browser.find_element_by_id("RadioGroup1_9")

#Initialize for-loop iterator values. These values are also part of the end CSV
months = ["January", "February", "March", "April", "May", "June", "July", "August", 
          "September", "October", "November", "December"]

areas = [roslindale, union_park,dotadams, allston, charlestown, longwood, hyde_park,
         dottalbot, eboston, roxbury]

areanames = ["roslindale", "union_park", "dotadams", "allston", "charlestown", "longwood",
             "hyde_park", "dottalbot", "eboston", "roxbury"]

#Actually scrape data
for place in areas:
    
    #Start year is 2013, first name is roslindale
    year = 2013
    name = 0
    
    #reinitialize every time the web page changes (every time "submit" is clicked)
    year_select = browser.find_element_by_name("reqyear")
    month_select = browser.find_element_by_name("reqmonth")
    
    submit = browser.find_element_by_id("SubBtn")
    
    download = browser.find_element_by_css_selector("#FormSelectItems > tbody > tr > td:nth-child(4) > a")
    roslindale = browser.find_element_by_id("RadioGroup1_1")
    union_park = browser.find_element_by_id("RadioGroup1_0")
    dotadams = browser.find_element_by_id("RadioGroup1_2")
    allston = browser.find_element_by_id("RadioGroup1_3")
    charlestown = browser.find_element_by_id("RadioGroup1_4")
    longwood = browser.find_element_by_id("RadioGroup1_5")
    hyde_park =browser.find_element_by_id("RadioGroup1_6")
    dottalbot = browser.find_element_by_id("RadioGroup1_7")
    eboston = browser.find_element_by_id("RadioGroup1_8")
    roxbury = browser.find_element_by_id("RadioGroup1_9")
    
    #area change
    place.click()
    
    #initialize list part of list-of-dicts for dataframe conversion
    raindata = []
    
    #this is where data is actually scraped 
    for i in range(6):
        
        #year change
        year_select.send_keys(str(year))
        for m in months:
            
            #month change
            month_select.send_keys(m)
            
            #submit after year, area, and month are first changed
            submit.click()
            
            #find the table with the relevant data
            table = browser.find_element_by_id("tblRainfallData")
            
            #reinitialize after submit; area does not change until the next loop
            year_select = browser.find_element_by_name("reqyear")
            month_select = browser.find_element_by_name("reqmonth")
            submit = browser.find_element_by_id("SubBtn")
            
            #find data; table rows have class "</tr>", are read as lists
            #[2:-3] indexing chops off headers, footers, and whitespace
            for row in table.find_elements_by_xpath(".//tr")[2:-3]:
                entry = {}
                entry['year'] = year
                entry['month'] = m
                #row elements have class "</td>", read as "td" objects with text attribute
                #rows have 2 td objects in each; day and rainfall in inches
                entry['day'] = row.find_elements_by_xpath(".//td[text()]")[0].text
                entry['rainfall'] = row.find_elements_by_xpath(".//td[text()]")[1].text
                raindata.append(entry)
    
        year += 1
    
    #convert list of dicts to dataframe and convert to csv    
    daily_rain = pd.DataFrame(raindata)
    daily_rain.to_csv(areanames[name])
    
    #change area name
    name += 1
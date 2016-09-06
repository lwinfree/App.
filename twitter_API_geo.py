# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 12:24:02 2016

@author: lillywinfree
"""
#! usr/bin/env python3
from twitter import *
import sys
import csv
#set geo location, radius 5 km
latitude = 45.5
longitude = -122.67
max_range = 5
num_results = 700
outfile = "geoTweets9.csv"

#API creds
config= {}
exec(open("config.py").read(), config)

#create Twitter API object
twitter = Twitter(
        auth=OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
    
#create CSV
csvfile=open(outfile, "w")
csvwriter=csv.writer(csvfile)
#add headers
row = ["user", "text", "latitude", "longitude"]
csvwriter.writerow(row)

#break up search into 10 pages of 100 tweets
result_count=0
last_id=None
while result_count < num_results:
    #perform our geo search
    query = twitter.search.tweets(q = "beer", geocode = "%f,%f,%dkm" % (latitude, longitude, max_range), count = 100, max_id = last_id)
    for result in query["statuses"]:
        if result["geo"]:    #only use results that have geolocation
            user = result["user"]["screen_name"]
            text = result["text"]
            text = text.encode('ascii', 'replace')
            latitude = result["geo"]["coordinates"][0]
            longitude = result["geo"]["coordinates"][1]
            #write to CSV file
            row = [ user, text, latitude, longitude ]
            csvwriter.writerow(row)
            result_count += 1
        last_id = result["id"]
    print("got %d results" % result_count) 
    #keep me posted about count
    
#close csv file
csvfile.close()

print("writen to %s" % outfile) 